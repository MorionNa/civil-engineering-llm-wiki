---
title: "Lepikhin et al. (2020) — 方法机制展开"
created: 2026-06-13
updated: 2026-06-13
type: concept
tags: [neural-network, deep-learning, transformer, mixture-of-experts, sparse-moe, gating-network, top-k-routing, load-balancing, conditional-computation, automatic-sharding, spmd, model-parallelism, distributed-training, sublinear-scaling, einsum, compiler-optimization, xla-compiler]
sources: [raw/papers/lepikhin2021_gshard.md]
methods: [top-2-gating, expert-capacity, auxiliary-loss, random-routing, local-group-dispatching, einsum-partitioning, spmd-partitioning, alltoall-resharding, tensor-sharding-annotations, split-api, replicate-api, halo-exchange]
confidence: high
---

# Lepikhin et al. (2020) — 方法机制展开

> 返回概述 → [[lepikhin2021-gshard-analysis]]

## 核心思路

GShard 是一个三层系统：**模型层**用 MoE 实现条件计算使计算量亚线性于模型容量；**标注层**用轻量 API 将分片策略从模型代码中解耦；**编译层**用 SPMD 自动分区器生成 O(1) 编译时间的并行程序。三者组合实现了 600B 参数模型在 2048 TPU 上 4 天训练。

---

## Layer 1: MoE Transformer 模型

### 架构

标准 Transformer encoder/decoder 每隔一个 FFN 层替换为 Position-wise MoE 层：

```
Encoder: [Self-Attn → FFN] × N  →  [Self-Attn → MoE] × N  (交替)
Decoder: [Self-Attn → Cross-Attn → FFN]  →  [Self-Attn → Cross-Attn → MoE]
```

MoE 层包含 E 个专家 FFN₁...FFNᴇ，每个专家是标准 2 层 ReLU FFN。

### 前向传播

```
Gs,E = GATE(xs)                    # 门控：每个 token 选择专家
FFNe(xs) = wₒᵉ · ReLU(wᵢᵉ · xs)    # 选中的专家计算
ys = Σₑ Gs,e · FFNe(xs)            # 加权平均输出
```

每个 token 最多被 dispatch 到 **2 个专家**，其余专家对该 token 贡献为 0。未获任何专家处理的 overflow token 通过残差连接直接传递到下一层。

### Top-2 Gating 机制（Algorithm 1 核心）

| 组件 | 机制 | 目的 |
|------|------|------|
| **Expert Capacity** | C = O(N/E)，每个专家最多处理 C 个 token | 强制负载均衡 |
| **Local Group Dispatching** | token 分 G 组独立并行处理，每组容量 2N/(G·E) | 门控并行化 |
| **Auxiliary Loss** | ℓaux = (1/E) Σₑ (cₑ/S) · mₑ，其中 mₑ 是 softmax 均值的可微近似 | 防止门控坍缩到少数专家 |
| **Random Routing** | 以概率 ∝ 2·g₂ 决定是否 dispatch 到第二专家 | 节省容量，g₂ 很小时跳过 |

总损失：**L = ℓnll + k · ℓaux**（k 是常数乘子）

### 前向传播的线性代数表达（Algorithm 2）

```
gates = softmax(einsum("GSM, ME → GSE", inputs, wg))
combine_weights, dispatch_mask = Top2Gating(gates)
dispatched_inputs = einsum("GSEC, GSM → EGCM", dispatch_mask, reshaped_inputs)
h = relu(einsum("EGCM, EMH → EGCH", dispatched_inputs, wi))
expert_outputs = einsum("EGCH, EHM → GECM", h, wo)
outputs = einsum("GSEC, GECM → GSM", combine_weights, expert_outputs)
```

维度：G=组数, S=每组 token 数, E=专家数, C=容量, M=模型维度, H=隐藏维度。加下划线字母（G, E）标注了需要分片的维度。

### 计算复杂度分析

假设 G=O(D), E=O(D), S=O(1), M=O(1), H=O(1), C=O(1/D)：
- Softmax: O(D²) → 每设备 O(D)
- Top2Gating/Dispatch/Combine/FFN: 每设备均 O(1)
- **每设备总 FLOPS ≈ O(1)**，满足亚线性缩放

---

## Layer 2: GShard 标注 API

### API 设计

| API | 语义 | 用法 |
|-----|------|------|
| `replicate(tensor)` | 张量复制到所有设备 | 非 MoE 层权重（attention, FFN） |
| `split(tensor, dim, num)` | 沿 dim 维度均匀分片 | 输入 batch、MoE 专家权重 |
| `shard(tensor, device_assignment)` | 多维自定义分片布局 | 高级用例（空间分区图像、优化通信拓扑） |

标注不改逻辑 shape——用户仍在"全尺寸"张量上编程。

### MoE 层标注示例

```python
inputs = split(inputs, 0, D)          # 沿 G 维度分片
wg = replicate(wg)                     # 门控权重复制
gates = softmax(einsum("GSM,ME→GSE", inputs, wg))
# ... Top2Gating + dispatch einsum ...
dispatched_inputs = split(dispatched_inputs, 0, D)  # 从 G 切换到 E 维度分片
h = einsum("EGCM,EMH→EGCH", dispatched_inputs, wi)
# ...
```

关键：einsum 的分片策略由编译器根据输入标注自动推导。模式在 MoE 层（专家维度 E 分片）和非 MoE 层（batch 维度 G 分片）之间自动切换。

### 混合手动/自动分片

允许对特定算子（如 Gather）手动分区，通过 `auto_to_manual_spmd_partition` / `manual_to_auto_spmd_partition` 在两种模式间切换——适用于编译器无法从算子语义推断分片边界的情况。

---

## Layer 3: XLA SPMD Partitioner

### SPMD vs MPMD

- **MPMD（传统）**：为每个设备生成单独程序 → 图节点数 O(D)、边数 O(D²)，编译时间爆炸
- **SPMD（GShard）**：生成一个在所有设备上运行的通用程序 → 编译时间 O(1)

### 通信原语

| 原语 | 功能 | MoE 中的用途 | 复杂度 |
|------|------|-------------|--------|
| **AllToAll** | 每设备沿一维分片数据，各自发往不同目的地 | MoE dispatch/combine 的分片维度切换（G↔E） | O(√D) |
| **AllReduce** | 所有设备 element-wise 求和 | 收缩维度分片的偏结果累加 | O(1)（TPU 上） |
| **AllGather** | 拼接所有设备数据 | 分片→复制转换 | O(D) |
| **CollectivePermute** | 指定源-目标对的数据传输 | 分片间设备顺序重排、halo exchange | O(1) |

### Einsum 分区的三种通信模式

```
(a) Resharding (AllToAll):    G-partitioned einsum → AllToAll → E-partitioned
    用途：MoE dispatch einsum "GSEC,GSM→EGCM"

(b) AllReduce:                contracting dimension partitioned → 局部结果 → AllReduce
    用途：常规 Matmul 的收缩维分片

(c) Slicing in a loop:        non-contracting 维度均分片但不同 → CollectivePermute 循环
    用途：操作数过大无法复制时，分片循环切片计算
```

### 关键技术挑战

- **非均匀分片：** 维度不能被设备数整除时，填充 padding → Iota + 比较 + Select 掩码
- **静态算子配置：** 各分片的 padding/stride 需求不同 → 统一配置 + DynamicSlice 裁剪多余输出
- **Halo Exchange：** 窗口算子（Convolution）的边界数据交换 → 最大 halo 交换 + 按需 DynamicSlice + 掩码

---

## 训练配置

| 参数 | 值 |
|------|-----|
| Transformer 维度 | 1024 |
| FFN/MoE 隐藏维度 | 8192 |
| Attention heads | 16 |
| Key/Value 维度 | 128 |
| Dropout | 0.1 |
| 优化器 | Adafactor（β₁=0, β₂=0.99, 1−t⁻⁰·⁸ schedule） |
| 学习率 | 1.0, sqrt decay after 10k steps |
| 精度 | float32 权重+激活（bfloat16 在 1T 模型上数值不稳定） |
| 词表 | SentencePiece 64k（源 102语言）+ 32k（英语目标） |

---

## 关键设计决策

1. **Every-other-layer MoE：** 非每层都是 MoE——保留一半普通 FFN 层（参数共享），平衡专家专业化与正向迁移
2. **Top-2 而非 Top-1 或 Top-k>2：** Top-2 提供容错（某专家 overflow 时可回退第二专家）和梯度路径多样性
3. **专家数 = 设备数：** 简化分片策略（每设备恰好一专家），但非必须
4. **float32 精度：** bfloat16 在 1T 模型出现数值不稳定，论文因此未包含该结果

---

## 关联

- [[lepikhin2021-gshard-analysis]] — 论文概述
- [[lepikhin2021-gshard-results]] — 结果证据展开
- [[lepikhin2021-gshard-critical]] — 贡献 / 知识点 / Negative / 可迁移 / 研究机会
