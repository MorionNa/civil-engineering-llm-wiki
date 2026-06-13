---
title: "NAS-BERT 批判分析：贡献 · 知识点 · Negative · 可迁移 · 研究机会"
created: 2026-06-13
updated: 2026-06-13
type: concept
tags: [bert-compression, neural-architecture-search, knowledge-distillation, supernet, block-wise-training, progressive-shrinking]
sources: [raw/papers/xu2021_nas_bert.md]
confidence: high
---

# NAS-BERT 批判分析

> 父页面：[[xu2021-nas-bert-analysis]]

## 贡献 (Contribution)

1. **首次将 NAS 引入 BERT 预训练级压缩**：不同于 prior work 仅在 fine-tune 阶段做 task-specific NAS（如 AdaBERT）或在 CV 领域做 efficient model NAS（Once-for-All, BigNAS），NAS-BERT 是第一个在 NLP 预训练任务上做 chain-structured NAS 搜索的工作
2. **任务无关 + 多尺寸输出**：单一 supernet 训练一次，输出 5M–60M 覆盖 12 种不同尺寸的架构族——这是 BERT 压缩领域前所未有的能力
3. **Bin-based progressive shrinking**：解决"大会早期被淘汰、小会后期限于容量"的 diversity collapse 问题，是最核心的方法贡献
4. **Block-wise 蒸馏 + 弹性 hidden size**：证明可以通过可学习线性变换在 teacher/student hidden size 不匹配时进行有效的 block-wise 知识迁移
5. **SepConv 在小模型 NLP 中的价值发现**：NAS 自动发现 SepConv 在 5-30M 参数区间比标准 Transformer 层更有竞争力——为 NLP 轻量架构设计提供了实证依据

## 核心知识点 (Core Knowledge)

1. **NAS 可以做 BERT 级预训练压缩**，前提是必须用 block-wise 分治 + progressive shrinking 控制成本。直接训练完整 supernet 在 preliminary experiments 中甚至无法收敛——这是重要的"don't even try"经验
2. **Bin-based shrinking = 多样性保证机制**：任何需要保持输出多样性的 pruning 搜索（不仅 NAS）都可以借鉴。分 bin 本质是在约束空间内做局部竞争，避免全局 winner-takes-all
3. **Block-wise 训练中 teacher/student hidden size 不匹配的解决方案**：可学习线性投影层是简单有效的最小干预方案。这不限于 NAS，任何 teacher-student 异构蒸馏场景都适用
4. **Performance approximation 的 trade-off**：block-wise loss 加法 + 逐层 latency 累加在 layer 间交互可忽略时近似良好，但引入了系统性的低估（无法捕捉 block 间的 cascade error / 层间 latency 开销）
5. **Search 空间的 composition vs novelty**：NAS-BERT 的核心价值不在"发现新操作"，而在自动组合已有操作（MHA/FFN/SepConv/Identity）到最优架构——这种"组合创新"是 NAS 区别于手工设计的本质优势

## Negative Knowledge

### 方法的适用范围与前提假设

| 维度 | 约束 |
|------|------|
| **模型类型** | Encoder-only Transformer（BERT 系）。Decoder-only（GPT 系）的 cross-attention 和自回归结构不适用当前搜索空间 |
| **模型尺寸** | 5M-60M 参数。更大模型（>100M）的 supernet 训练能否收敛未验证 |
| **蒸馏范式** | 仅 prediction layer distillation。未覆盖 attention/embedding/hidden distillation |
| **硬件** | 延迟在 Intel Xeon CPU 上测量。不同硬件平台的架构排名可能不同 |
| **搜索空间** | 链式结构，不支持跨层连接（如 DenseNet 式的 skip）或 attention 操作前的归一化层搜索 |

### 已知失效场景

1. **完整 supernet 直接训练不收敛**：作者 preliminary experiments 证实，不用 block-wise+progressive shrinking，直接训练 24 层 supernet 的 loss 无法下降。这是方法的核心前提——分治是必需的而非可选的
2. **Block-wise 引入的 isolation bias**：每个 block 独立用教师 block 输出训练，忽略了 block 间交互。最优 block 子架构的组合不一定是全局最优——这类似于"局部贪心"的基本局限
3. **Progressive shrinking 可能过度剪枝**：每 epoch 剪 50%，最后只剩 10 个/block。如果早期阶段 noise 导致好架构被误杀，无法恢复
4. **SepConv 主导小模型可能过度**：5M-10M 架构中 SepConv 占比极高，但文中未提供纯 MHA/FFN 小模型的对比——可能是搜索空间 bias（SepConv 恰好在该参数量级上参数利用更高效）
5. **CoLA 偏差问题**：作者承认 teacher 在 CoLA 和 RTE 上因小数据集波动大。先 work 与 NAS-BERT 在 CoLA 上的差距部分源于 teacher 质量差异

### 未解决的问题

- Block 间 hidden size 的全局最优组合策略（现有：各 block 独立选最优）
- Progressive shrinking 超参（B/m/E/R）的自动化选择
- 如何在搜索阶段考虑 downstream task 的差异（而非完全 task-agnostic）
- 搜索到的架构如何迁移到不同预训练目标（如 ELECTRA 的判别式预训练）
- 更大 teacher（BERT-large）的压缩效果未验证

## 可迁移知识 (Transferable Knowledge)

| 知识 | → 可迁移到 | 如何迁移 |
|------|-----------|---------|
| Block-wise + 教师蒸馏降搜索成本 | ViT/GPT 等大模型 NAS 压缩 | 对任何超大模型（无法直接 train supernet），按层/block 分组 + teacher 输出做蒸馏训练 |
| Bin-based progressive shrinking | 任何 prune-based 搜索需要保持输出多样性 | 将被 prune 的对象按目标属性（size/latency/type）分组，组内局部竞争替代全局竞争 |
| 可学习投影解决 teacher-student 维度不匹配 | 任何异构蒸馏（不同 arch/hidden size 的 teacher-student 对） | 输入端和输出端各一个线性层 + 主网络不变 |
| Performance approximation lookup table | 任何 latency-constrained model selection | 预测所有单操作延迟 → 逐层加法近似完整模型延迟 |
| SepConv 在 NLP 小模型中的竞争力 | 手工设计轻量 NLP 架构 | 在 5-30M 参数范围内，用 SepConv 替代部分 FFN 层可提升效率 |
| Single-path optimization 采样训练 | 任何 supernet-based NAS | 每步只前传反向传一个子网，内存高效 |

## 研究机会 (Research Opportunity)

### 方向 1：Decoder-only 模型压缩 (GPT/Llama 系)

NAS-BERT 完全围绕 encoder-only 架构设计。Decoder-only 模型的 causal attention、自回归生成、KV-cache 等特性需要全新的搜索空间和评估指标（perplexity + throughput，而非 GLUE score）。搜索空间的候选操作可能包括 GQA/MQA、sliding window attention、MoE FFN 等。

### 方向 2：Cross-block 联合搜索

当前 block 间独立搜索 + 独立蒸馏，忽略了 block 间组合效应。可以加入 light-weight cross-block coordinator（如 small MLP predictor）在 model selection 阶段考虑 block 间交互，或者用 evolutionary algorithm 做完整架构的微调搜索。

### 方向 3：Training-free 指标替代 validation loss

当前 progressive shrinking 依赖 dev set validation loss。如果引入 training-free NAS 指标（如 NTK 条件数、线性区域数，见 [[chen2021-tenas-analysis]]），可以进一步降低搜索成本，且避免 validation loss 采样不均导致的评估噪声。

### 方向 4：Searched Architecture as Initialization

NAS-BERT 搜出的架构是"架构模板"，仍需从头 pre-train。能否利用 supernet 中已训练的子网权重作为初始化，加速压缩模型的 pre-training？这需要解决 weight-sharing sub-net 权重与独立训练权重的 gap。

### 方向 5：Hardware-aware NAS + 多目标优化

当前模型选择是简单的 constraint-satisfaction（满足参数/延迟上限，选 loss 最低）。可以引入多目标优化（Pareto frontier），同时将能量消耗、吞吐量、内存带宽等纳入搜索目标。

### 方向 6：Task-aware 但无需逐任务搜索

完全 task-agnostic 可能限制了极致性能。能否在预训练阶段搜索时，加入少量 proxy tasks 的反馈（如部分 GLUE 子集），实现"one search → moderate adaptation to each task"？

## 关联页面

- [[xu2021-nas-bert-analysis]] — 全维度总览
- [[xu2021-nas-bert-method]] — 方法机制
- [[xu2021-nas-bert-results]] — 实验数据
- [[chen2021-tenas-critical]] — TE-NAS training-free NAS 的局限与机会对比
- [[jiang2024-mixtral-of-experts-critical]] — MoE 可视为 NAS-BERT 搜索空间的未来扩展操作
