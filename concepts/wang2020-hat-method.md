---
title: "HAT 方法机制：SuperTransformer + 延迟预测器 + 进化搜索"
created: 2026-06-13
updated: 2026-06-13
type: concept
tags: [hardware-aware-nas, latency-prediction, evolutionary-search, weight-sharing-supernet, heterogeneous-transformer, encoder-decoder-attention, latency-constraint]
sources: [raw/papers/wang2020_hat.md]
confidence: high
---

# HAT 方法机制

> 父页面：[[wang2020-hat-analysis]]

## 核心框架

```
                    ① 设计空间
                    ├─ Arbitrary Encoder-Decoder Attention
                    └─ Heterogeneous Transformer Layers
                            │
                            ▼
                    ② SuperTransformer 训练
                    ├─ 权重共享：子网继承最大模型参数
                    ├─ 均匀采样训练：每次迭代随机采 SubTransformer
                    └─ 输出：一次训练 → 所有子网的性能代理
                            │
                            ▼
                    ③ 延迟预测器训练（每种硬件独立）
                    ├─ 采集 2000 (架构向量, 实测延迟) 样本
                    └─ 训练三层 MLP → RMSE ~0.1s
                            │
                            ▼
                    ④ 进化搜索（latency-constrained）
                    ├─ 查询延迟预测器 → 过滤超限架构
                    ├─ 查询 SuperTransformer → validation loss
                    └─ 30 轮进化 → 最优 SubTransformer
                            │
                            ▼
                    ⑤ 从头训练最终模型
```

---

## ① 设计空间 (Design Space)

HAT 破坏了 Transformer 的两条传统设计惯例，构建了 ~10^15 量级的搜索空间：

### 1.1 Arbitrary Encoder-Decoder Attention

```
传统 Transformer:                     HAT:
Decoder Layer 1 ──→ Enc Layer N      Decoder Layer 1 ──→ Enc Layer i, j
Decoder Layer 2 ──→ Enc Layer N      Decoder Layer 2 ──→ Enc Layer k
Decoder Layer 3 ──→ Enc Layer N      Decoder Layer 3 ──→ Enc Layer m, n
（信息瓶颈：只有最后一层）              （多编码器层：打破瓶颈）
```

**机制**：每个 decoder 层可选择关注 1~3 个 encoder 层。KV 向量沿句子长度维度拼接（如图 4），再输入 encoder-decoder cross attention。

**效率**：无额外参数。关注 2 层时，GPU 延迟仅增 0.4%。

**动机**：不同 encoder 层提取不同抽象级别的特征——低层编码词法/句法，高层编码语义。传统设计强制所有 decoder 层只关注高层，丢失低层信息。

### 1.2 Heterogeneous Transformer Layers

传统 Transformer 所有层共享相同架构。HAT 让每层独立选择：

| 弹性维度 | 取值范围 | 说明 |
|----------|---------|------|
| **Head 数量** (self-attn) | {4, 8} | Voita et al. (2019) 发现多头冗余；每层按需选择 |
| **Head 数量** (enc-dec attn) | {4, 8} | decoder 侧 cross-attention 的 head 数 |
| **FFN Hidden Dim** | {1024, 2048, 3072} | 传统 2×/4× 固定——不同层特征提取难度不同，容量应不同 |
| **Embedding Dim** | {512, 640} | encoder/decoder 各自统一，但两者可不同 |
| **Decoder 层数** | {1, 2, 3, 4, 5, 6} | Encoder 固定 6 层（仅占 5% 延迟，影响小） |

---

## ② SuperTransformer：权重共享性能代理

### 2.1 为何需要？

搜索空间有 ~10^15 个候选架构，逐一训练评估完全不可能。需要一种**只需训练一次就能评估所有架构**的方法。

### 2.2 权重共享机制

SuperTransformer = 搜索空间中最大的模型（embed dim 640, hidden dim 3072, head 8, decoder 6 层）。所有 SubTransformer 从 SuperTransformer 继承对应部分的权重：

```
弹性 Embedding Dim 权重共享:
  Max Embed Dim = 640
  SubTransformer (embed=512) ─→ 取前 512 维的 embedding + FC 权重
  
弹性 FFN Hidden Dim 权重共享:
  Max Hidden Dim = 3072
  SubTransformer (hidden=1024) ─→ 取前 1024 维的 FC 权重

弹性 Head 数量权重共享:
  Q/K/V 向量维度固定为 512（搜索空间内不变）
  8 heads → 每 head 64 dim → 4 heads → 每 head 128 dim
  通过划分而不是截断实现

弹性层数权重共享:
  共享前 N 层（decoder 6 层 → 选 4 层 → 共享前 4 层）
```

### 2.3 训练策略

- 每次迭代**均匀随机采样**一个 SubTransformer
- 只更新该 SubTransformer 对应的权重（被采的样子网越多，训练越充分）
- 训练步数 = baseline Transformer 训练步数（WMT: 40K steps）
- 训练后，任何 SubTransformer 直接继承权重跑 validation → 得到性能代理

### 2.4 代理质量验证

关键结论：**继承权重 BLEU 与从头训练 BLEU 的排名一致**（Table 5）：

| WMT'14 En-De | 继承 Val Loss | 继承 BLEU | 从头训练 BLEU |
|-------------|--------------|-----------|--------------|
| 模型 A | 4.71 | 24.9 | 25.8 |
| 模型 B | 4.07 | 26.3 | 28.1 |
| 模型 C | 4.02 | 26.7 | 28.2 |
| 模型 D | 4.01 | 26.9 | 28.4 |

排名完全一致。此外，**继承后微调 10K 步（1/4 正常训练）可达甚至超过从头训练 40K 步的 BLEU**（Table 6）。

---

## ③ 延迟预测器

### 3.1 为何需要？

进化搜索中评估每个候选架构的延迟有两种方式：(1) 在目标硬件上实测——单次需数百次推理，耗时数分钟；(2) 用预测器——即时预测。HAT 选后者。

### 3.2 数据采集

对每种目标硬件（Raspberry Pi ARM CPU, Intel Xeon CPU, Nvidia TITAN Xp GPU）：

- 随机采样 2000 个 SubTransformer 架构
- 在硬件上实测翻译 30-token 句子的延迟（300 次取中间 80% 平均）
- Split: train:valid:test = 8:1:1

### 3.3 模型架构

```
输入特征向量（10 维）:
  - Encoder: layers, embed dim, avg hidden dim, avg self-attn heads
  - Decoder: layers, embed dim, avg hidden dim, avg self-attn heads
  - Enc-Dec: avg attention heads, avg attended encoder layers

模型: 3 层 MLP (400 hidden dim, ReLU)
  特征归一化 → FC(10→400)→ReLU → FC(400→400)→ReLU → FC(400→1)
  
精度: RMSE ~0.1s（图 6，预测值与实测值接近 y=x）
```

**设计选择**：三层优于单层（精度更高），超过三层不再提升。

---

## ④ 进化搜索

### 4.1 搜索流程

```
初始化: 随机生成 125 个 SubTransformer 架构
  │
循环 30 轮:
  │
  ├─→ 延迟预测器 ← 过滤：只保留延迟 ≤ 约束的架构
  │
  ├─→ SuperTransformer ← 适应度评估：validation loss
  │
  ├─→ 选择: Top 25 作为 parents
  ├─→ 变异: 25 → 50 (0.3 概率变异) 
  ├─→ 交叉: 25 → 50 (crossover)
  │
  └─→ 新一代 125 子代 → 下一轮
```

### 4.2 关键参数

| 参数 | 值 |
|------|----|
| 种群大小 | 125 |
| 父代数量 | 25 |
| 变异种群 | 50（0.3 概率） |
| 交叉种群 | 50 |
| 迭代次数 | 30 |
| 适应度 | validation loss (越低越好) |
| 硬约束 | 延迟 ≤ target latency |

### 4.3 进化 vs 随机搜索

进化搜索能比随机搜索找到更低 validation loss 的模型（图 9），证明搜索策略有效。

---

## ⑤ 最终训练

搜索完成后，最优 SubTransformer 架构被提取出来，**从头训练**（而非使用继承权重），保证与 baseline 的公平对比。可选方案：直接微调继承权重 → 节省 4× 训练步数（Table 6）。

---

## 关联页面

- [[wang2020-hat-analysis]] — 全维度总览
- [[wang2020-hat-results]] — 实验结果
- [[wang2020-hat-critical]] — 贡献·局限·可迁移·机会
- [[chen2021-tenas-method]] — TE-NAS 的 training-free 评估 vs HAT 的权重共享评估
