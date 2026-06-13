---
title: "AutoFormer 方法机制：Weight Entanglement + 弹性搜索空间"
created: 2026-06-13
updated: 2026-06-13
type: concept
tags: [neural-architecture-search, one-shot-nas, weight-entanglement, weight-sharing-nas, vision-transformer, transformer, evolutionary-search]
sources: [raw/papers/chen2021_autoformer.md]
confidence: high
---

# AutoFormer 方法机制

> 父页面：[[chen2021-autoformer-analysis]]

## 核心架构

```
Search Space (embed dim, Q-K-V dim, head num, MLP ratio, depth)
        │
        ├── Phase 1: Supernet Training with Weight Entanglement
        │       Uniformly sample subnet α per iteration
        │       Update weights of subnet's blocks in WA
        │       Largest block stores full weights; smaller ones extract subset
        │       → Single block update benefits ALL sharing blocks
        │
        └── Phase 2: Evolution Search under Resource Constraints
                Population=50, generations=20
                Top-10 parents → crossover + mutation
                Fitness = max accuracy s.t. param budget
```

## Weight Entanglement 机制

### 问题：经典权重共享在 Transformer 上为何失败？

经典 one-shot NAS（如 SPOS [Guo et al. 2020]）中，同层不同候选 block 的权重**相互独立**（w_j ∩ w_k = ∅）。这在 CNN 空间有效，但在 Transformer 空间：

1. **收敛慢**：每个 block 仅在采样到时更新一次，训练效率低
2. **子网性能差**：继承权重评估的子网精度远低于 from-scratch（69.7% vs 80.1% at ~23M）

### 解决方案：Weight Entanglement

**核心思想**：强制同层候选 block 共享公共权重部分。

```
Classical Weight Sharing:
  Block 1 [W1], Block 2 [W2], Block 3 [W3]
  W1 ∩ W2 ∩ W3 = ∅  (independent)

Weight Entanglement:
  Block_large [W_full]          ← stores full weights
  Block_medium ⊂ Block_large    ← extracts subset
  Block_small  ⊂ Block_medium   ← extracts subset
  All share intersected weights (W_small ⊂ W_medium ⊂ W_large)
```

**实现方式**：每层仅存储最大 block 的权重，小 block 的权重是大 block 权重的子矩阵提取。

### 为何适用于 Transformer？

Transformer 由 homogeneous 的全连接层组成（MSA + MLP），不同大小的 block 在结构上天然兼容：

- Q-K-V 投影矩阵：大 embedding dim 的矩阵包含小 embedding dim 的矩阵（取左上角子矩阵）
- MLP 隐藏层：大 MLP ratio 的权重包含小 MLP ratio 的权重
- Attention heads：多头注意力的 Q/K/V 可按 head 维度切片

### Weight Entanglement 的三重优势

| 优势 | 机制 | 证据 |
|------|------|------|
| **更快收敛** | 每个 block 被更多子网采样时更新（共享权重被反复更新） | Fig.4 左：train loss 下降更快 |
| **更低显存** | 每层只存最大 block 参数，非所有候选 | 显存 ≈ 最大子网而非所有候选之和 |
| **子网质量高** | 继承权重性能 ≈ from-scratch | Fig.4 右：entanglement 子网追平 from-scratch |

### 为什么 Weight Entanglement 有效？（两个 conjecture）

1. **正则化效应**：采样小子网时，其 hidden unit 不能依赖其他 unit → 类似 Dropout，减少 co-adaptation
2. **优化深窄网络**：宽子网的梯度回传帮助更新窄子网的权重（overparameterization helps optimization），弹性 depth 类似 stochastic depth 的 deep supervision 效果

## 搜索空间

AutoFormer 设计了覆盖 Vision Transformer 五个核心维度的搜索空间：

| 维度 | Supernet-Tiny | Supernet-Small | Supernet-Base |
|------|:---:|:---:|:---:|
| Embed Dim | 192–240 (step 24) | 320–448 (step 64) | 528–624 (step 48) |
| Q-K-V Dim | 192–256 (step 64) | 320–448 (step 64) | 512–640 (step 64) |
| MLP Ratio | 3.5–4 (step 0.5) | 3–4 (step 0.5) | 3–4 (step 0.5) |
| Head Num | 3–4 (step 1) | 5–7 (step 1) | 8–10 (step 1) |
| Depth | 12–14 (step 1) | 12–14 (step 1) | 14–16 (step 1) |
| **Params Range** | **4–9M** | **14–34M** | **42–75M** |

**重要设计决策**：

- **Q-K-V dim 与 head num 解耦**：固定 Q-K-V dim / head num 的比值，使 attention scaling factor 1/√dh 对 head 数不变，稳定梯度
- **MLP ratio 弹性化**：与 embedding dim 一起决定隐藏层维度 = embedding_dim × MLP_ratio
- **三层 supernet 分区**：按参数量目标分区，使搜索聚焦在特定资源约束区间
- **总搜索空间 > 1.7×10^16 候选架构**

### 与 ViT/DeiT 的架构关系

AutoFormer 的 supernet 基于标准 ViT encoder：patch embedding → [class] token + position embedding → L 层 Transformer encoder → classification head。每层 Transformer block = MSA + MLP，均含 LayerNorm + residual。**不同层可使用不同配置**（打破传统所有层相同结构的惯例）。

## 搜索 Pipeline

### Phase 1: Supernet 训练

| 超参 | 值 |
|------|-----|
| Epochs | 500 |
| Optimizer | AdamW |
| Batch Size | 1024 |
| LR | 1e-3, cosine decay |
| Weight Decay | 5e-2 |
| Warmup | 20 epochs |
| Label Smoothing | 0.1 |
| Drop Path | 0.1 |
| Data Aug | RandAugment + CutMix + Mixup + Random Erasing |
| GPU | Nvidia Tesla V100 (multi-GPU) |

每 iteration 均匀采样一个子网，冻结 supernet 其他权重，仅更新子网对应部分。

### Phase 2: 进化搜索

```
初始化: N=50 随机架构作为种子
重复 20 代:
  评估所有个体 (继承 supernet 权重 → ImageNet val subset 精度)
  选 Top-10 为 parent
  产生下一代:
    Crossover: 随机选两个 parent，交叉产生新个体
    Mutation:
      以 Pd=0.2 概率突变 depth
      以 Pm=0.4 概率突变每个 block 的配置
目标: max accuracy s.t. param ≤ budget
```

验证集：ImageNet 训练集中随机抽取 10,000 张（每类 100 张），保留完整验证集做最终测试。

## 关联页面

- [[chen2021-autoformer-analysis]] — 全维度总览
- [[chen2021-autoformer-results]] — 实验结果
- [[chen2021-autoformer-critical]] — 贡献·局限·可迁移·机会
