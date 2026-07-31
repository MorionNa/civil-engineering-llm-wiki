---
id: papers--zhao2021-memory-efficient-dnas-critical
title: DARTSformer 批判分析：贡献 · 知识点 · Negative · 可迁移 · 研究机会
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/llm
- evidence/paper
- method/neural-architecture-search
- method/transformer
keywords:
- differentiable-search
- memory-efficient
- neural-architecture-search
- reversible-network
- transformer
sources:
- sources/papers/zhao2021-memory-efficient-dnas.md
created: '2026-06-14'
updated: '2026-07-31'
confidence: high
---

# DARTSformer 批判分析

> 父页面：[[zhao2021-memory-efficient-dnas-analysis]]

## 贡献 (Contribution)

1. **首创可逆网络 + DARTS 结合**：将 RevNets 的思想从训练时省内存扩展到 NAS 搜索时省内存，本质创新在于认识到 DARTS 的存储放大效应（|O|× 中间激活）恰好是可逆网络最能发挥作用的地方。之前工作（PC-DARTS, ProxylessNAS）通过减少操作数或通道数来省内存，而 DARTSformer 通过「不存储中间激活」来省内存，是正交的技术路线。

2. **Multi-split reversible network 设计**：不同于 RevNets 的 2-split 方案，提出了通用 n-split 可逆变换（Eq. 3-4），使 encoder 和 decoder 可以使用不同 split 数（2+3），灵活性高于固定 split 的可逆架构。

3. **BP-with-reconstruction 算法（Algorithm 1）**：清晰的伪代码可直接实现，gradient accumulator 机制（gradₖ = dYₖ + C.grad）正确处理了可逆网络中多 split 的梯度流。

4. **实证证明 search hidden size 的关键性（Table 5）**：这是 NAS 社区的一个重要发现——小 hidden size 搜索 + 大 hidden size 重训练的「proxy task」策略在 Transformer 上彻底失败。这一教训适用于所有 two-stage NAS 工作。

5. **计算成本碾压进化方法**：搜索成本 $1,250 vs ET 的 $150,000，且性能相当或更优。将 NAS-for-Transformer 从「Google-scale」拉低到「学术-scale」。

## 核心知识点 (Core Knowledge)

1. **可逆网络用于 NAS 的双重节省**：传统 DARTS 内存瓶颈 = (层数) × (每层操作数 |O|) × (hidden state 存储)。可逆网络将「层数」因子降为 1（仅存顶层），对 |O| 大的场景特别有效。在 Transformer 中 |O|=13/14，节省 ~13× 的激活存储。

2. **Search hidden size ≠ target hidden size 是危险假设**：Chen et al. (2019) 指出的「depth gap」已广为人知，但 DARTSformer 揭示了同样严重的「width gap」。搜索时 hidden size 与 target 不匹配会导致搜索到的架构在大 hidden size 下性能亚于手工设计。必须尽可能在 target 或接近 target 的配置下搜索。

3. **Max pooling > Average pooling for multi-split fusion**：在 multi-split reversible network 中融合多 split 信息时，max pooling 普遍优于 avg pooling（Table 1: 28.4 vs 28.3, s=2）。可能的解释是 max pooling 的稀疏选择特性有助于减少噪声 split 的干扰。

4. **搜索 2 层 block 有意义**：s=2（在一个 2-layer block 内搜索）优于 s=1（单层搜索）——因为跨层的操作组合模式（如 FFN→Self Attn 串行）无法在单层搜索中被发现。

5. **Decoder cross-attention 不应被搜索淘汰**：固定 decoder 最后 split 为 Cross Attention 是重要的先验约束。若让 Cross Attention 参与 softmax 竞争，可能被 FFN 或 Conv 淘汰（因短期 loss 更优），导致 encoder-decoder 信息通道阻断。

## Negative Knowledge

### 方法的适用范围与前提假设

| 维度 | 约束 |
|------|------|
| **模型架构** | Encoder-decoder Transformer。Decoder-only (GPT 系) 和 encoder-only (BERT 系) 未验证 |
| **任务类型** | 机器翻译（序列到序列）。非自回归生成、文本分类等未测试 |
| **候选操作** | 13-14 种预定义操作。不包含最近提出的 sparse attention, linear attention, MoE FFN 等 |
| **搜索粒度** | Whole-block 级别。不涉及 attention head 数、FFN expansion ratio 等细粒度搜索 |
| **Split 数量** | 手动指定 (2/3)。无自动选择机制 |
| **重训练** | 搜索网络 = 可逆，重训练网络 = 不可逆。两者结构不同 |

### 已知失效场景

1. **Sampling-based baseline 崩溃（Table 1）**：Uniform sampling NAS (Guo et al., 2020) 在翻译任务上 BLEU 仅 16.8-18.7（vs 27.7 baseline）。根本原因：翻译对操作的感受野和多样性有严格要求，uniform sampling 倾向大 kernel 卷积 → 重复生成。这说明并非所有 NAS 方法都适用于 NLP。

2. **Split 数量增大性能退化（Table 2）**：split 从 2/3 增至 4/5 → BLEU 下降 1.0。搜索空间爆炸（13.5^(4+5) ≈ 10^18 range）导致双层优化无法收敛。这对大规模搜索空间的 DARTS 方法是一个通用警示。

3. **搜索 hidden size 过小导致负迁移（Table 5）**：d=120 搜索结果重训练后 BLEU 24.2 < Transformer 27.7。证明坏的搜索结果比不搜索更差——如果资源不足以在接近 target 的配置下搜索，使用标准 Transformer 可能是更好的选择。

4. **En-Fr 上未超越 ET**：尽管 En-De 搜索的架构在 En-Fr 上有效 (+0.1 vs Transformer)，但 40.1 低于 ET 的 40.6。可能原因：(1) ET 可能在 En-Fr 上单独调优；(2) 搜索空间的操作集偏向 En-De 的德语结构特征。

### 未解决的问题

- 搜索的可逆网络与重训练的不可逆网络之间的结构 gap 是否会导致次优架构被选为最优？（可逆性可能改变搜索时的梯度流和 loss landscape）
- 33% 的搜索计算开销在更大搜索空间中是否可接受？
- 搜索到的架构是否为全局最优？文中未与 random search baseline 对比
- 候选操作集中缺少 LayerNorm 位置的搜索（当前固定在每个操作内部）
- DARTS 固有的 α 离散化 gap（softmax 连续 → argmax 离散）是否影响最终架构质量？

## 可迁移知识 (Transferable Knowledge)

| 知识 | → 可迁移到 | 如何迁移 |
|------|-----------|---------|
| Multi-split reversible network + DARTS | 任何 memory-bound 的 DARTS 搜索（CV 的超大搜索空间、视频 Transformer NAS 等） | 将 backbone 替换为 multi-split reversible，Algorithm 1 可直接复用 |
| BP-with-reconstruction 算法 | 任何 reversible network 的自定义反向传播实现 | Algorithm 1 的 grad accumulator 模式和重构顺序是通用模板 |
| Search hidden size 必须接近 target | 所有 two-stage NAS（小 proxy 搜索 → 大模型重训练） | 必须验证搜索配置与 target 的 hidden size ratio，ratio < 0.5 可能危险 |
| Max pooling for multi-source fusion in reversible nets | 任何需要融合多路信息的可逆网络设计 | 用 max pooling 替代 avg pooling 或 concat+linear |
| Decoder 固定 Cross Attn 的约束 | 任何 encoder-decoder 架构的 NAS | 识别并保护信息瓶颈操作，不让其参与搜索竞争 |
| Factorized embedding 节省搜索内存 | 任何大词表 + 大 hidden size 的 NLP 模型训练/搜索 | E = E₁ × E₂ 分解，e≪d |

## 研究机会 (Research Opportunity)

### 方向 1：扩展到 Decoder-Only 和 Encoder-Only

DARTSformer 仅验证了 encoder-decoder 翻译架构。将 multi-split reversible NAS 应用于 GPT-style decoder-only 和 BERT-style encoder-only 模型是两个直接且有价值的扩展方向。Decoder-only 的 causal mask 约束和 encoder-only 的无 cross-attention 结构需要调整候选操作集和搜索空间。

### 方向 2：结合 Gradient Checkpointing 进一步降低内存

可逆网络省掉了中间激活存储，但每层的权重梯度仍需在 BP 时计算。Selective gradient checkpointing 可以与可逆网络叠加——对不可逆部分（如 embedding、output projection）使用 checkpointing，可逆部分依赖 reconstruction。

### 方向 3：Training-Free NAS 消除双层优化

当前 DARTSformer 仍依赖 validation loss 双层优化，存在 α-θ 交替训练的不稳定性和计算开销。引入 training-free NAS 指标（如 NTK 条件数、线性区域数、Zen-Score 等，见 [[chen2021-tenas-analysis]]）替代 validation loss 可消除双层优化并进一步降低搜索成本。

### 方向 4：细粒度架构搜索

当前搜索在 whole-block 粒度（选择哪种操作）。可以细化到：(1) attention head 数；(2) FFN expansion ratio；(3) kernel size 在 Conv 中的自动选择；(4) LayerNorm 位置（pre-norm vs post-norm）。细粒度搜索 + memory-efficient 方法的组合可能发现更优的子架构模式。

### 方向 5：一阶段 NAS（搜索即训练）

消除搜索-重训练的两阶段 gap。Chase (Yang et al., 2020) 和 AtomNAS 等工作已探索一阶段 NAS，但未结合 memory-efficient 技术。将 DARTSformer 的可逆搜索与 network morphism 或权重继承结合，使搜索结束时直接产出训练好的模型，无需重训练。

### 方向 6：多任务/多语言联合搜索

当前仅在 En-De 上搜索。在多语言对（En→De, En→Fr, En→Cs 等）上联合搜索可能产生更通用的架构，避免 En-Fr 上的性能滞后。

## 关联页面

- [[zhao2021-memory-efficient-dnas-analysis]] — 全维度总览
- [[zhao2021-memory-efficient-dnas-method]] — 方法机制
- [[zhao2021-memory-efficient-dnas-results]] — 实验数据
- [[memory-efficient-dnas]] — 实体页
- [[chen2021-tenas-critical]] — TE-NAS training-free NAS 的局限与机会对比
- [[wang2020-hat-critical]] — HAT 进化搜索 NAS 的方法论对比

## Evidence By Source

### `sources/papers/zhao2021-memory-efficient-dnas.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/memory_efficient_dnas2021.pdf`

^[sources/papers/zhao2021-memory-efficient-dnas.md]
