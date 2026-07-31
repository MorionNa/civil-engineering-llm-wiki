---
id: papers--xu2021-nas-bert-method
title: NAS-BERT 方法机制：Block-Wise Supernet 训练 + Progressive Shrinking + Model Selection
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- evidence/paper
- method/neural-architecture-search
- method/transformer
keywords:
- bert-compression
- block-wise-training
- knowledge-distillation
- neural-architecture-search
- progressive-shrinking
- supernet
- weight-sharing-nas
sources:
- sources/papers/xu2021-nas-bert.md
created: '2026-06-13'
updated: '2026-07-31'
confidence: high
---

# NAS-BERT 方法机制

> 父页面：[[xu2021-nas-bert-analysis]]

## 整体流程

```
阶段 1: 搜索空间设计
    定义 candidate operations O (26个) + 划分 N=4 blocks

阶段 2: Supernet 训练 (Block-wise + Progressive Shrinking)
    每个 block 独立训练 → 每 epoch 在 bin 内剪枝弱架构

阶段 3: 模型选择 (Lookup Table + Performance Approximation)
    组合多 block 最佳子架构 → 选满足延迟/内存约束的 top 候选
```

## 搜索空间设计

### Candidate Operations

| 类型 | Hidden Size 选项 | 参数细节 |
|------|-----------------|---------|
| **MHA** (Multi-Head Attention) | 128/192/256/384/512 | Heads: 2/3/4/6/8 |
| **FFN** (Feed-Forward Network) | 128/192/256/384/512 | Intermediate: 512/768/1024/1536/2048 |
| **SepConv** (Separable Convolution) | 128/192/256/384/512 | Kernel: {3, 5, 7}, Depthwise→Pointwise→GeLU→LayerNorm |
| **Identity** | — | Placeholder，位于尾部时可删除使网络变浅 |

共 (3 类型 × 5 hidden sizes) + 1 Identity = **26 operations**，其中 SepConv 三种 kernel size × 5 hidden sizes = 15 个。

### 选择 SepConv 的理由

- LSTM 训练和推理太慢，排除
- MHA 变体（product-key memory, lightweight conv）在小模型上没有优势
- SepConv 参数量 H² + K·H（vs Conv 的 K·H²），可以用大 kernel 获得大感受野而不显著增加参数

### Chain-Structured Supernet

- 总 L=24 层（对应 BERT-base 12 Transformer 层 × 2 sub-layer）
- 划分为 **N=4 blocks**，每 block 6 层
- **Block 内 hidden size 一致**，block 间可以不同 → 弹性宽度
- Identity 操作使层数可变 → 弹性深度
- 去冗余：只保留 Identity 在尾部的架构（{FFN, FFN, Identity, Identity} 保留，{FFN, Identity, FFN, Identity} 删除）

搜索空间复杂度（去冗余后）：每 block 97650 个子架构，4 blocks → ~10²⁰ 种组合（vs 不做 block-wise 的 26²⁴ ≈ 10³⁴）

## Supernet 训练

### Block-Wise Training with Knowledge Distillation

```
教师 BERT-base (12 layers)
    │
    ├─ Embedding → [Block 0] → [Block 1] → [Block 2] → [Block 3] → ... → output
                       │           │           │           │
                       │ MSE loss  │ MSE loss  │ MSE loss  │ MSE loss
                       │           │           │           │
    学生 Supernet →  [Block 0] → [Block 1] → [Block 2] → [Block 3]
                        ↑ 每 step 随机采样一个子架构  ↑
```

关键设计：

1. **教师 block 输出 = 学生 block 目标**：第 n 个学生 block 的输入是第 (n-1) 个教师 block 的输出，目标是预测第 n 个教师 block 的输出
2. **损失函数**：Lₙ = || f(Yₙ₋₁; Aₙ) − Yₙ ||²₂ （MSE）
3. **Hidden size 对齐**：当学生 hidden size ≠ 教师 768 时，学生 block 的输入/输出端各插入一个可学习线性变换层
4. **单路径优化**（Single-Path Optimization）：每训练步只采样一个子架构前传+反传，内存高效

### Progressive Shrinking

**动机**：即使 block-wise 后每 block 仍有 97650 个候选子架构。固定训练时间下，每个子架构得到的"摊还训练时间"不足，导致评估不准。集中资源给有潜力的架构 → progressive shrinking。

**Bin 设计**（核心创新）：
- 将每 block 的 97650 架构按模型大小分为 **B=10 个 bin**
- bin b 的参数上限 p_b = (b/B) × p(a_t)，其中 a_t 是最大架构
- 每个 bin 同时施加 latency 约束（l_b 为上限）
- **为什么需要 bin？** 大会早期优化难被淘汰，小会后期容量不足被淘汰 → 不分 bin 直接剪枝会导致尺寸多样性崩塌

**Shrinking 算法**（每 epoch 结束时执行）：
1. 在每个 bin 内采样 E=2000 个架构
2. 在 dev set（仅 5 batch，加速评估）上计算 validation loss
3. 按 loss 降序排列，删除尾部 R = E/2 = 1000 个最差架构
4. 重复直到每个 bin 只剩 m=10 个架构

**训练流程**：
- 前 3 epoch 不剪枝（warm start）
- Epoch 4 起每 epoch 剪枝一次
- 终止条件：每 bin 每 block 只剩 10 架构，训练也同步结束

### 训练配置

| 参数 | 值 |
|------|-----|
| 预训练语料 | English Wikipedia + BookCorpus (~16GB) |
| 预训练任务 | Masked Language Modeling (MLM) |
| 每句 token 数 | 512 |
| Batch size | 1024 句 |
| 教师模型 | BERT-base (L=12, H=768, A=12) |
| 计算资源 | 32 NVIDIA P40 GPUs × 3 天 |
| 对比：教师训练 | 16 V100 GPUs × 5 天 |

## Model Selection

### Lookup Table 构建

1. **Latency lookup table LT_lat**：提前在目标设备上测量 26 个单独操作的延迟，存入表
2. **架构延迟近似**：l(a) = Σᵢ₌₁ᴸ l(aᵢ)，逐层累加（忽略层间交互开销）
3. **Loss 近似**：完整架构的 loss = 各 block 子架构在 dev set 上的 block-wise distillation loss 之和
   - 只需评估 m×B×N = 10×10×4 = 400 个子架构（而非 10²⁰ 个完整架构）

### 选择流程

1. 构建包含 (m×B)ᴺ ≈ 10⁸ 条目的 lookup table LT_arch
2. 给定约束（参数量上限 P，延迟上限 L）→ 筛选满足条件的架构
3. 按近似 loss 排序，取 top T=100 候选
4. 对 T=100 候选架构在完整 dev set 上精确评估 validation loss
5. 选 loss 最低的架构作为最终压缩模型，进行完整的 pre-training + fine-tuning

### Why Performance Approximation?

- 直接评估 10⁸ 个完整架构的 dev loss → 不可行
- Block-wise loss 加法近似假设 block 间独立（与 block-wise 训练一致）
- Latency 逐层累加近似：忽略层间 kernel launch overhead，但在 CPU 上误差可接受

## 关联页面

- [[xu2021-nas-bert-analysis]] — 全维度总览
- [[xu2021-nas-bert-results]] — 实验数据
- [[xu2021-nas-bert-critical]] — 贡献·局限·可迁移·机会
- [[chen2021-tenas-method]] — TE-NAS 的 training-free NAS 方法论对比

## Evidence By Source

### `sources/papers/xu2021-nas-bert.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/xu2021_nas_bert.md`

^[sources/papers/xu2021-nas-bert.md]
