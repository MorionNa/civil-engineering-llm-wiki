---
id: papers--fedus2021-switch-transformer-method
title: Fedus et al. (2021) — 方法机制展开
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/llm
- evidence/paper
- method/transformer
sources:
- sources/papers/fedus2021-switch-transformer.md
created: '2026-06-13'
updated: '2026-07-31'
confidence: high
methods:
- mixture-of-experts
- switch-routing
- top-1-routing
- load-balancing-loss
- selective-precision
- expert-dropout
- expert-parallelism
- model-parallelism
- data-parallelism
- capacity-factor
---

# Fedus et al. (2021) — 方法机制展开

> 返回概述 → [[fedus2021-switch-transformer-analysis]]

---

## 核心思路

将 Transformer 的密集 FFN 层替换为 **Switch FFN 层**：每个 token 通过一个轻量 router 被路由到 **恰好一个** expert FFN（k=1），而非 MoE 的 top-k（k≥2）。由此在保持 FLOPs/token 不变的前提下，通过增加 expert 数量大幅扩展总参数量。

---

## Switch Routing (k=1)

### 与 MoE Routing 的对比

| 维度 | MoE (Shazeer 2017) | Switch Transformer |
|------|---------------------|---------------------|
| 路由策略 | top-k (k ≥ 2) | **top-1 (k = 1)** |
| Router 输出 | k 个 expert 的加权组合 | 1 个 expert 乘以 gate value |
| Expert capacity | 较大（token 被多次分配） | **至少减半** |
| 通信成本 | 高（k 路 all-to-all） | **降低** |
| 梯度流假设 | 需要 k≥2 比较不同 expert | **k=1 即可（gate value 保证可微性）** |

### 数学表达

给定 token 表示 x 和 N 个 expert {E_i}：

```
Router logits:  h(x) = W_r · x
Gate value:     p_i(x) = softmax(h(x))_i
Expert 选择:     i* = argmax p_i(x)
层输出:          y = p_i*(x) · E_i*(x)
```

其中 gate value `p_i*(x)` 被乘回到 expert 输出上（dotted-line in Figure 2），保证 router 可微。

---

## 负载均衡损失 (Load Balancing Loss)

为确保 token 在 experts 间均匀分布，添加辅助损失：

```
loss_aux = α · N · Σ_{i=1}^{N} (f_i · P_i)
```

| 符号 | 含义 | 可微？ |
|------|------|--------|
| f_i | 实际路由到 expert i 的 token 比例 | ❌ 不可微 |
| P_i | router 分配给 expert i 的概率比例（平均 softmax） | ✅ 可微 |
| α | 损失系数，论文使用 **10⁻²** | — |
| N | Expert 总数（用于归一化，保持损失与 expert 数量无关） | — |

- α ∈ [10⁻¹, 10⁻⁵] swept，10⁻² 在"快速均衡"和"不干扰主任务"间取得最佳平衡
- 目标：使 f 和 P 都接近均匀分布 1/N

---

## Expert Capacity 与 Token Dropping

### 容量机制

```
expert_capacity = (tokens_per_batch / num_experts) × capacity_factor
```

| Capacity Factor | 效果 |
|-----------------|------|
| 1.0 | 理论最小值，内存最优，但可能溢出 |
| 1.25 | 论文最佳平衡点 |
| 1.5 | 更多 buffer，但浪费计算和内存 |
| 2.0 | MoE baseline 值，Switch 不需要 |

- 如果路由到某 expert 的 token 数超过 capacity，超出部分被 **跳过**（通过残差连接直接传递到下一层）
- 实验表明 token 丢弃率通常 <1%
- 附录 B 尝试了 No-Token-Left-Behind（迭代重路由到第二选择），但未带来经验收益

---

## 训练稳定化技术

### 1. 选择性精度 (Selective Precision)

| 方案 | 质量 (Neg. Log Perp.) | 速度 (ex/sec) |
|------|----------------------|---------------|
| float32 全精度 | -1.718 | 1160 |
| bfloat16 全精度 | **-3.780 [diverged]** | 1390 |
| **选择性精度** | **-1.716** | **1390** |

**做法**：router 函数内部将输入 cast 到 float32（计算 softmax + dispatch/combine tensors），结果立即 cast 回 bfloat16。float32 仅在 **本地设备** 内使用，不产生跨设备 float32 通信开销。

### 2. 缩小参数初始化

```
σ = √(s/n)  其中 s 从 1.0 → 0.1（缩小 10 倍）
```

| 初始化方案 | Avg Neg. Log Perp. | Std. Dev. |
|-----------|---------------------|-----------|
| 1.0× init | -3.60 | 0.68 |
| **0.1× init** | **-2.72** | **0.01** |

- 方法适用于从 223M 到 1.6T 参数的全尺度模型

### 3. Expert Dropout（仅用于 Fine-tuning）

| Dropout 方案 | GLUE | CNNDM | SQuAD | SuperGLUE |
|-------------|------|-------|-------|-----------|
| d=0.1 (标准) | 84.7 | 19.1 | 83.7 | 73.0 |
| d=0.2 | 84.4 | 19.2 | 83.9 | 73.2 |
| d=0.3 | 83.9 | 19.6 | 83.4 | 70.7 |
| **d=0.1 (非expert) + ed=0.4 (expert)** | **85.2** | **19.6** | **83.7** | **73.0** |

- 仅对 expert FFN 层增加 dropout rate 到 0.4
- 非 expert 层保持常规 dropout 0.1
- 有效缓解稀疏模型在少量 fine-tuning 数据上的过拟合

---

## 并行策略

### 三维并行架构

论文提出在 Mesh TensorFlow 中组合三种并行：

```
总核心数 N = n × m
n: data-parallel sharding ways
m: model-parallel sharding ways
E: number of experts (typically = n in expert-parallelism)
```

| 策略 | n | m | 通信模式 | 适用场景 |
|------|---|---|---------|---------|
| Data Parallelism (DP) | N | 1 | 仅梯度聚合时 all-reduce | 小模型 |
| Model Parallelism (MP) | 1 | N | 每层 forward/backward 均 all-reduce | d_ff 超过单设备内存 |
| Model + Data (MP+DP) | >1 | >1 | 混合 | 大密集模型 (T5, GPT-3) |
| Expert + Data (EP+DP) | E | 1 | 每次路由 all-to-all | **Switch 默认策略** |
| Expert + Model + Data | >1 | >1 | all-to-all + all-reduce | 万亿参数模型 |

### Expert Parallelism 详细流程

```
1. 每个 core 持有 B/n 个 tokens + 1 个 expert
2. Router 本地计算 expert 分配 → binary matrix [n, B/n, E, C]
3. einsum gather token 到对应 expert
4. all-to-all 通信交换 experts 间的 tokens
5. 每个 expert 本地计算 FFN
6. all-to-all 通信返回结果到原 core
7. 通过 combine tensor 还原 token 顺序
```

---

## 模型规格对比

| Model | Parameters | FLOPs/seq | d_model | d_ff | Layers | Experts | Expert Freq. |
|-------|-----------|-----------|---------|------|--------|---------|-------------|
| T5-Base | 0.2B | 124B | 768 | 2048 | 12 | — | — |
| Switch-Base | 7B | 124B | 768 | 2048 | 12 | 128 | 1/2 |
| T5-Large | 0.7B | 425B | 1024 | 2816 | 24 | — | — |
| Switch-Large | 26B | 425B | 1024 | 2816 | 24 | 128 | 1/2 |
| T5-XXL | 11B | 6.3T | 4096 | 10240 | 24 | — | — |
| Switch-XXL | 395B | 6.3T | 4096 | 10240 | 24 | 64 | 1/2 |
| Switch-C | 1571B | 890B | 2080 | 6144 | 15 | 2048 | 1 |

- Expert 放置频率：Switch-Base/Large/XXL 每隔一个 FFN 层放置（1/2），Switch-C 每层放置（1）

---

## 关联

- [[fedus2021-switch-transformer-analysis]] — 论文概述
- [[fedus2021-switch-transformer-results]] — 结果证据展开
- [[fedus2021-switch-transformer-critical]] — 贡献/知识点/Negative/可迁移/研究机会

## Evidence By Source

### `sources/papers/fedus2021-switch-transformer.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/fedus2021_switch_transformer.md`

^[sources/papers/fedus2021-switch-transformer.md]
