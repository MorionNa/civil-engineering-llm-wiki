---
title: "So et al. (2021) — Primer: Searching for Efficient Transformers for Language Modeling 论文分析"
created: 2026-06-14
updated: 2026-06-14
type: paper-analysis
tags: [neural-architecture-search, transformer, efficient-inference, evolutionary-search, weight-sharing-supernet, search-space-design]
sources: [raw/papers/primer2021_efficient_transformers.pdf]
methods: [sq-tc-search, evolutionary-search, conceptual-initialization, halving-hurdles, low-level-primitive-search]
results: [c4-perplexity, lm1b-speedup, glue, squad, superglue, downstream-transfer, scaling-laws]
failure_modes: [redundant-search-cost, encoder-decoder-gap, negative-knowledge-extraneous-mutations, fixed-budget-proxy-noise, open-ended-space-degeneracy]
datasets: [lm1b, c4, pg19, glue, squad, superglue]
reproducibility: high
code_url:
  - https://github.com/google-research/google-research/tree/master/primer
confidence: high
---

# So et al. (2021) — Primer: Efficient Transformers for Language Modeling

> David R. So, Wojciech Mańke, Hanxiao Liu, Zihang Dai, Noam Shazeer, Quoc V. Le — Google Research, Brain Team — NeurIPS 2021
> **底层原语进化搜索**：在 TF 计算图级别搜索 Transformer 变体 → 发现两个核心改进：Squared ReLU + MDHA → 训练成本降至 1/3~1/4

## 1. 工程背景 (Engineering Background)

GPT-3 之后，大语言模型训练成本指数级增长——训练一次 GPT-3 级别模型需数百万美元级别算力。Transformer 架构自 2017 年提出后，尽管有大量变体（BERT, XLNet, T5, Evolved Transformer），但**核心 decoder-only 自回归语言模型的底层架构改进始终有限**。

已有改进路线包括：
- **激活函数**：GELU（BERT）、Swish/SwiGLU（T5++）、GLU 家族
- **归一化**：Pre-LN → 成为标准 vs. 原始 Post-LN
- **稀疏和 MoE**：Switch Transformer, GShard
- **卷积增强**：Conformer（语音），但用于文本 LM 未系统验证

工程痛点：训练成本 = 每步时间 × 步数。大多数研究只优化"步数效率"（sample efficiency），但忽略"每步耗时"——Evolved Transformer 就是典型反例：样本效率提升但推理/训练更慢，总体性价比反而不如 Vanilla Transformer。

## 2. Research Gap

已有的 Transformer NAS（如 Evolved Transformer）存在三个核心缺陷：

1. **搜索空间偏置过强**：搜索空间由高层模块（self-attention, GLU, Conv）组成，搜索只能从有限集合中挑选模块，不能修改模块内部结构
2. **优化目标偏差**：Evolved Transformer 固定训练步数比较 perplexity——优化了 sample efficiency 但忽略了 step time，导致搜索到的架构反而更慢
3. **随机搜索即可表现良好**（Li & Talwalkar 2019）：这表明搜索空间设计本身已经"预设"了答案

更根本的 gap：**没有人尝试在 TensorFlow 计算图的原语级别（ADD, MULTIPLY, CONV 1X1, DCONV 3X1, MAX, SIN...）搜索 Transformer**。这样的空间是"开放式的"——78% 的随机程序连 5 分钟训练都无法完成——但也因此可能发现高层搜索空间永远找不到的改进。

## 3. 科学问题 (Scientific Question)

**能否通过底层 TF 原语级别的进化搜索，找到一种比原版 Transformer 训练成本更低的自回归语言模型架构？该架构的改进能否在跨 codebase、跨硬件、跨规模、跨数据集的条件下稳定传输？**

这个问题的两个子问题：
- （搜索方法论）如何在极度开放、存在大量退化程序的空间中高效搜索？
- （知识发现）搜索到的改进中，哪些是最核心、最容易迁移的？

## 4. 研究目标 (Research Objective)

1. 设计基于 TF 原语的搜索空间，用进化算法搜索 decoder-only 自回归 LM 的架构
2. 提出"概念初始化 + Halving Hurdles + 固定预算隐式效率目标"的搜索策略
3. 发现 Primer 架构并在 LM1B 验证；提取核心改进形成 Primer-EZ
4. 在三个 codebase（T2T, T5, Lingvo）、三种硬件（TPUv2/v3/v4, V100）、多规模（20M~1.9B）下验证改进的可迁移性
5. 证明改进不仅体现在训练减少（1/3~1/4 compute），还能传导到 one-shot downstream task

## 5. 方法机制 (Method & Mechanism)

→ [[so2021-primer-method]]

核心三部分：

1. **搜索空间**：TF 原语词汇表（~30+ 操作），DNA = 子程序集合，每条指令引用 primitive 或子程序。子程序调用有向无环（只可调用更高 index），消除环。每个指令的 argument set 包含 Input1, Input2, Constant, Dim Size，不同操作取自己需要的子集。

2. **搜索算法**：Regularized Evolution (pop=100, tournament=10) + 5 种 mutation（Delete/Insert/Delete&Insert/Mutate Field/Swap/Mutate Bank Value）。**概念初始化**（conceptual initialization）：将原始 Transformer 按概念（self-attention, ReLU, LayerNorm）拆分为子程序作为搜索起点。**Halving Hurdles**：50% 通过率 + 等计算量带，降低平均评估成本约 6.2×。**隐式效率目标**：固定训练预算（24h TPUv2），以最终 perplexity 为 fitness——步时和样本效率的权衡被隐式纳入。

3. **训练策略**：24h 训练预算，LM1B，T2T codebase，序列长度 64，batch 4096 tokens，~35M 参数。用 7h 训练 proxy（Vanilla Transformer 7h 达到 24h 的 ~90% 质量），再省 3.43×。

## 6. 结果证据 (Result & Evidence)

→ [[so2021-primer-results]]

关键数字：

| 实验 | 规模 | Primer 加速比 | 备注 |
|------|------|-------------|------|
| 搜索任务 LM1B | 35M | 1.7~2.3× | T2T T5 TPUv2 V100 |
| C4 LM 110M | 110M | 1.68~1.91× | T5 codebase, 1M steps |
| PG19 LM 110M | 110M | 1.68~1.98× | 跨数据集泛化 |
| T5 大尺度 C4 | 537M | **4.2×** | 全 T5 训练配置 |
| One-shot GPT-3 XL | 1.9B | **3×** | 27 downstream tasks |
| Switch Transformer | 550M | 1.45~1.56× | MoE 兼容性 |
| Synthesizer | 145M | 1.74~1.96× | 高效 Transformer 兼容性 |

Scaling Law：Primer 和 Transformer 的 l vs c 在双对数空间中平行，表明计算节省也服从幂律。

## 7. 贡献 (Contribution)

→ [[so2021-primer-critical]]

1. **方法论创新**：首次在 TF 底层原语级别对 Transformer 进行进化搜索，证明了"开放空间 + 概念初始化"策略的有效性
2. **核心发现**：Squared ReLU 激活（比 ReLU/GELU/Swish/SwiGLU 都好且无额外参数）和 MDHA（Q/K/V 投影后加 3×1 depthwise convolution）是两个最核心、最易迁移的改进
3. **工程价值**：Primer-EZ 可"即插即用"，无需重新调参，4.2× 训练加速在标准 T5 设置下验证
4. **可迁移性验证**：跨 codebase (3 个)、跨硬件 (4 种)、跨规模 (3 个数量级)、跨模型家族 (Switch, Synthesizer)、跨数据集
5. 引入 Halving Hurdles 和隐式效率目标等搜索策略优化

## 8. 核心知识点 (Core Knowledge)

1. **Squared ReLU = 无参 GLU 替代**：y = (max(0, x))²。当 GLU 变体（如 ReGLU）的 U=V 且前面有线性变换时等价。其 x→∞ 渐近行为与其他激活函数截然不同

2. **MDHA (Multi-DConv-Head Attention)**：点卷积 → 空间 depthwise 卷积（反常见 separable conv 的顺序）。对每个 attention head 独立做 D-Conv

3. **隐式效率目标**：固定训练预算评估最终质量，比显式多目标优化更好地捕捉 step time ↔ sample efficiency 权衡

4. **概念初始化**：在开放空间中，用"概念化"的已知好架构作为种子——自我拆解成 subprogram bank（attention, FFN, ReLU, LayerNorm）——引入 bias 但保留搜索自由度

5. **Halving Hurdles**：等计算量分带 + 50% 通过率的早期淘汰策略，本质是进化版本的 Successive Halving

6. **幂律计算节省**：当架构的 l-c 线平行时，使用更优架构的 compute savings 也遵循幂律：l = a₁(1-1/b)^k s^(-k)

7. **负知识 - Decoder vs Encoder gap**：Primer 改进在 encoder-decoder MLM（BERT-style）上不及 Transformer++，说明 decoder LM 和 encoder MLM 需要不同的架构选择

## 9. Negative Knowledge (负面知识)

→ [[so2021-primer-critical]]

### 适用范围 / 前提假设
- **仅 decoder-only 自回归 LM 有显著优势**：encoder-decoder MLM（T5 masked LM）实验中 Primer-EZ Decoder 仅在 vanilla Transformer 上有提升，不如 Transformer++（SwiGLU + RMSNorm）
- **大模型验证仅到 1.9B**：距 GPT-3 全尺寸（175B）和现代百亿级模型还有差距
- **固定超参数搜索**：搜索在 24h/35M/LM1B 条件下进行——改进不一定在所有 settings 下最优
- **训练数据相对干净**：LM1B/C4/PG19 是标准语料，未测试在噪声/多语言/代码等数据上的表现

### 失效场景
- **Encoder-only/encoder-decoder MLM**：Primer 改进不如 SwiGLU+RMSNorm 的 T5++
- **序列长度极长**（>10K）：MDHA 的 3×1 卷积窗口固定，可能导致长程依赖不够
- **需要精细 control 的生成**（如温度采样）：Squared ReLU 的二次渐近可能影响 logit 分布

### 未解决的问题
- Squared ReLU 为什么在大规模上比 SwiGLU 更好？——理论上未完全解释
- MDHA 中 depthwise→pointwise vs. pointwise→depthwise 的反直觉顺序为什么更好？
- 搜索到的额外 modification（如 ×(-1.12)）是 noise artifact 还是隐藏了未发现的机制？
- 能不能用相同的搜索方法找到 encoder-decoder MLM 的改进？

## 10. 可迁移知识 (Transferable Knowledge)

→ [[so2021-primer-critical]]

1. **Squared ReLU**：可直接替换任何 Transformer FFN 中的激活函数——一行代码，无额外参数，stable to training
2. **MDHA pattern**：对 attention 的 Q/K/V 做 pointwise→spatial 处理可推广到其他序列模型
3. **开放空间 + 概念初始化**：对任何"想发现已有架构的底层层级改进"的场景适用——不仅是 Transformer，CNN/RNN/GNN 都可以
4. **隐式效率目标**：对任何硬件-软件协同优化场景适用（固定预算评估最终质量）
5. **Halving Hurdles**：任何计算密集型进化搜索的通用加速策略
6. **幂律 compute savings 分析框架**：可迁移到任何架构对比实验的分析中

## 11. 研究机会 (Research Opportunities)

→ [[so2021-primer-critical]]

1. **Encoder-decoder MLM 的 Primer-style 搜索**：直接以 MLM 为搜索目标，可能找到不同于 Squared ReLU 和 MDHA 的改进
2. **更大规模验证**（10B+）：Primer 的 scaling law 是否可以外推到 GPT-4 级别的规模？
3. **Squared ReLU 的理论分析**：其二次渐近行为与 training dynamics 的关系
4. **MDHA 的变体探索**：更大的 D-Conv 窗口？dilated D-Conv？跨 head 共享 D-Conv？
5. **搜索成本优化**：Primer 搜索耗费 1145.8 TPUv2-day (~2.06 MTCO2e)，能否用训练-free NAS（TE-NAS）或权重共享减少？
6. **跨模态推广**：Squared ReLU + MDHA 在视觉 Transformer（ViT, DeiT）、语音 Transformer 上是否有效？
7. **长序列优化**：MDHA 的 local conv 可能不足——能否结合 linear attention 或 state-space model？
8. **与其他高效技术的组合**：FlashAttention + Primer? 量化 + Primer?

## 12. 可复现性 (Reproducibility)

→ [[so2021-primer-critical]]

| 维度 | 评估 |
|------|------|
| 代码开源 | ✅ Tensor2Tensor 和 T5 对比代码开源 |
| 搜索 DNA 公开 | ✅ 完整 Primer DNA 在附录 (Figure 25) |
| 超参数详细 | ✅ 附录 A.8 全训练细节 + T2T/T5 默认参数 |
| 数据集 | ✅ LM1B, C4, PG19 均为公开数据 |
| 硬件 | TPUv2/v3/v4 — 大部分人无法复现硬件环境 |
| 闭源部分 | ❌ GPT-3 式 one-shot 实验使用 proprietary pretraining 数据 |
| 总体评价 | **高** — 核心开源 + 清晰附录，但 TPU 和部分数据限制了完整复现 |
