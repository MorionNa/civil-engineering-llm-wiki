---
id: papers--zhao2021-memory-efficient-dnas-analysis
title: Zhao et al. (2021) — Memory-Efficient Differentiable Transformer Architecture Search 论文分析
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- evidence/paper
- method/neural-architecture-search
- method/transformer
keywords:
- differentiable-search
- efficient-inference
- machine-translation
- neural-architecture-search
- transformer
sources:
- sources/papers/zhao2021-memory-efficient-dnas.md
created: '2026-06-14'
updated: '2026-07-31'
confidence: high
methods:
- differentiable-nas
- memory-efficient-nas
- gradient-checkpointing
- reversible-layer
results:
- wmt14-en-de
- wmt14-en-fr
- wmt18-en-cs
- bleu
failure_modes:
- search-evaluation-gap
- split-number-sensitivity
- sampling-baseline-failure
- convergence-difficulty-large-search-space
datasets:
- wmt14
- wmt18
reproducibility: high
code_url:
- https://github.com/microsoft/DARTSformer
---

# Memory-Efficient Differentiable Transformer Architecture Search

> Yuekai Zhao, Li Dong, Yelong Shen, Zhihua Zhang, Furu Wei, Weizhu Chen — Peking University & Microsoft — ACL-IJCNLP 2021 Findings
> **核心贡献**：将多分割可逆网络 (multi-split reversible network) 与 DARTS 结合，提出 DARTSformer，使 Transformer 架构搜索的内存消耗减半，首次实现大 hidden size 下的可微分搜索。

## 1. 工程背景 (Engineering Background)

Transformer (Vaswani et al., 2017) 在机器翻译、语言建模等序列任务上取得了统治性表现，但标准 Transformer 架构（6 层 encoder + 6 层 decoder，每层 Self-Attn → FFN）是人工设计的固定模式。随着神经架构搜索 (NAS) 在 CV 领域成功超越人工设计，将 NAS 应用于 Transformer 以自动发现更优架构成为自然需求。然而 DARTS (Liu et al., 2018) 在 Transformer 上的直接应用面临严重的内存瓶颈——每个 search node 的混合操作（softmax 加权和）需要存储所有候选操作的中间输出用于反向传播。当 hidden size d > 400 时，即使在 NVIDIA P100 (16GB) 上也会 OOM，这迫使搜索只能使用小 hidden size，导致搜索与最终训练的 hidden size 不一致，产生性能缺口 (Chen et al., 2019)。^[raw/papers/memory_efficient_dnas2021.pdf]

## 2. Research Gap

已有 NAS 方法用于序列任务主要是 RL-based (Pham et al., 2018) 和进化-based (So et al., 2019; Wang et al., 2020)，但它们计算成本极高——Evolved Transformer 搜索成本约 $150k（200 TPU 芯片）。DARTS 类方法计算高效，但内存瓶颈使其无法在 Transformer 上以足够大的 hidden size 进行搜索，也无法使用丰富的候选操作集。**核心空白是：如何在保持 DARTS 计算效率的同时，突破内存瓶颈，使 Transformer 架构搜索可以在大 hidden size 和丰富候选操作的条件下进行？** ^[raw/papers/memory_efficient_dnas2021.pdf]

## 3. 科学问题 (Scientific Question)

**如何设计一种内存高效的可微分架构搜索方法，使得在 Transformer backbone 上可以使用大 hidden size (d=960) 和丰富候选操作集 (|O|=13/14) 进行搜索，同时保持搜索到的架构在重训练后优于人工设计的 Transformer 基线？** ^[raw/papers/memory_efficient_dnas2021.pdf]

## 4. 研究目标 (Research Objective)

提出 DARTSformer：(1) 设计 multi-split reversible network 作为 backbone，使每层的输入可以从输出重构；(2) 设计 backpropagation-with-reconstruction 算法，仅存储最后一层输出即可完成梯度计算；(3) 将可逆网络与 DARTS 混合操作搜索节点结合；(4) 在 WMT'14 En-De 上搜索架构，重训练验证泛化能力。^[raw/papers/memory_efficient_dnas2021.pdf]

## 5. 方法机制 (Method & Mechanism)

→ [[zhao2021-memory-efficient-dnas-method]]

**三组件协同**：Multi-split reversible network（backbone）+ Backpropagation-with-reconstruction（内存优化）+ DARTS search nodes（可微分搜索）。

- **Multi-split reversible**：将输入沿 embedding 维度分为 n 等分 {X₁,...,Xₙ}，每分通过 Gₖ 变换后逐分量相加得到 Yₖ，输出可逆重构输入（Eq. 3-4）
- **Gₖ 设计**：Pooling（融合其他 splits 的信息）→ Mixed operation search node（softmax 加权候选操作）
- **BP-with-reconstruction**：反向传播时从顶层 Y 逐层重构 X，仅需存储最后一层激活值。计算开销增加约 33%（仅搜索阶段），重训练使用普通 BP
- **搜索空间**：encoder 2-split + decoder 3-split，候选操作包括 Conv, Dynamic Conv, Self/Cross Attention, GLU, FFN, Zero, Identity 共 13(encoder)/14(decoder) 种

## 6. 结果证据 (Result & Evidence)

→ [[zhao2021-memory-efficient-dnas-results]]

- **WMT'14 En-De base (Table 1)**：DARTSformer 28.4 BLEU，超越标准 Transformer (27.7, +0.7) 和 Evolved Transformer (28.2, +0.2)
- **WMT'14 En-Fr base (Table 4a)**：40.1 BLEU vs Transformer 40.0, ET 40.6
- **WMT'18 En-Cs base (Table 4a)**：27.9 BLEU vs Transformer 27.0 (+0.9)，**En-Cs 不是搜索数据集但增益最大**，证明架构迁移能力
- **Big model (Table 4b)**：En-De 29.8 BLEU，超过 Transformer (29.1) 和 ET (29.3)
- **搜索成本 (Table 3)**：$1.25k / 8×V100 / 40h vs ET 的 $150k / 200 TPU — **计算成本降低两个数量级**
- **多尺寸验证 (Fig. 5)**：从 10M 到 200M 参数全线优于 Transformer，小模型优势更显著 (+1.3 BLEU @ small)

## 7. 贡献 (Contribution)

→ [[zhao2021-memory-efficient-dnas-critical]]

1. **首次将可逆网络引入 DARTS**：通过 multi-split reversible network 实现 Transformer 架构搜索的内存减半，使 d=960 的大 hidden size 搜索成为可能
2. **BP-with-reconstruction 算法**：仅需存储最后一层输出，重构 + 反向传播一气呵成。通用性强，可应用于任意网络结构
3. **搜索成本碾压进化方法**：$1.25k vs $150k，参数更新步数少 874 倍，使 NAS-for-Transformer 从「大公司专属」变为「学术可用」
4. **跨数据集泛化**：En-De 搜出的架构在 En-Fr/En-Cs 上持续有效，En-Cs 上甚至增益最大 (+0.9 BLEU)

## 8. 核心知识点 (Core Knowledge)

1. **可逆网络的本质 = 用计算换内存**：BP 时重新算中间激活，增加 ~33% 计算但省去 O(n) 的中间激活存储。对 DARTS 的 O(|O|×n) 存储放大效应特别有效
2. **Search hidden size 很重要 (Table 5)**：小 hidden size 搜索 → 大 hidden size 重训练的迁移路径不可靠。d=120 搜索结果甚至不如标准 Transformer。只有接近 target 的 hidden size 搜索才能保证性能增益
3. **Sampling-based NAS 不适合翻译任务 (Table 1)**：均匀采样的 NAS 在翻译任务上严重退化 (BLEU 16.8-18.7 vs 27.7)，倾向选大 kernel 卷积，导致重复生成
4. **Split 数量不宜过多 (Table 2)**：2/3 split 最优，3/4 和 4/5 性能递减——搜索空间过大 + 递归计算增加导致训练和推理变慢
5. **Decoder 的最后 split 固定为 Cross Attention**：实验发现这种约束能搜索出更好的架构

## 9. Negative Knowledge

→ [[zhao2021-memory-efficient-dnas-critical]]

- **搜索的 reversible 网络在重训练时丢弃**：可逆结构仅在搜索时用于省内存，重训练使用普通 Transformer BP。这意味着搜索和重训练的网络结构不同，可能引入搜索-训练偏差
- **Split 数量是敏感超参**：最优 split 数依赖任务，增加 split 不仅不提升性能反而退化，但论文未提供自动化选择 split 数的方案
- **Sampling-based 方法作为 baseline 太弱**：使用的是最简单的 uniform sampling 而非 SPOS (Guo et al. 2020) 的完整方案
- **仅验证了 Encoder-Decoder 翻译架构**：未在 decoder-only / encoder-only 模型上验证可逆搜索的通用性
- **33% 搜索计算开销**：虽说是搜索阶段特有的，但对大搜索空间仍不可忽视
- **未探索 operation-level search**：当前在 whole-block 维度搜索，未做到 attention head 数、FFN expansion ratio 等细粒度搜索

## 10. 可迁移知识 (Transferable Knowledge)

| 知识 | → 迁移 |
|------|--------|
| Multi-split reversible network + DARTS | 任何需要节省搜索内存的 DARTS-based NAS 场景 |
| BP-with-reconstruction 算法 | 任何 reversible network 的反向传播实现参考 |
| Search hidden size 必须接近 target 的发现 | 所有 two-stage NAS（小搜索→大训练）的通用教训 |
| 候选操作集设计（Conv×4, Dynamic Conv×4, Self/Cross Attn, GLU, FFN） | 翻译及其他序列任务的 NAS 操作集参考 |
| Max pooling 优于 average pooling 在 pooling 融合中的发现 | 可逆网络中多 split 信息融合的设计选择 |
| 搜索 2 层 block 而非单层的策略 (s=2) | 允许搜索到跨层的操作模式（如 FFN→Self Attn 串联） |

## 11. 研究机会 (Research Opportunity)

→ [[zhao2021-memory-efficient-dnas-critical]]

- **将可逆搜索扩展到 decoder-only 架构**（GPT 系）和 encoder-only（BERT 系），验证通用性
- **结合 gradient checkpointing 进一步降低内存**：当前仅用可逆网络，可与 selective checkpointing 叠加
- **Training-free NAS 评估替代 validation loss**：消除搜索阶段的双层优化不稳定性（参考 TE-NAS 等 training-free 方法）
- **细粒度搜索**：在 attention head 数、FFN expansion ratio、kernel size 等维度联合搜索
- **一阶段 NAS**：将搜索与最终训练合并，消除搜索-重训练的两阶段 gap
- **多语言搜索**：在多语言数据上联合搜索，可能产生更好的通用架构

## 12. 可复现性 (Reproducibility)

**🟢 高可复现性** — 论文开源代码，配置详尽

| 项目 | 说明 |
|------|------|
| **等级** | 🟢 高 |
| **官方代码** | https://github.com/microsoft/DARTSformer（论文承诺开源） |
| **数据集** | WMT'14 En-De/En-Fr, WMT'18 En-Cs — 全部公开 |
| **计算资源** | 搜索：8×NVIDIA V100 40h (~$1.25k)；重训练：8×V100 |
| **复现要点** | Section 3.2-3.3 提供完整搜索和训练超参（learning rate, warmup, dropout, batch size, optimizer 配置等）。算法 1-2 的伪代码可直接翻译为代码。核心挑战是实现 multi-split reversible network 的自定义反向传播。 |

## 关联页面

- [[zhao2021-memory-efficient-dnas-method]] — Multi-split reversible / BP-with-reconstruction / DARTS 结合详解
- [[zhao2021-memory-efficient-dnas-results]] — WMT'14 En-De/En-Fr, WMT'18 En-Cs 完整数据
- [[zhao2021-memory-efficient-dnas-critical]] — 贡献 / 知识点 / Negative / 可迁移 / 研究机会
- [[memory-efficient-dnas]] — 实体页
- [[xu2021-nas-bert-analysis]] — 同样将 NAS 用于 NLP/Transformer 搜索，NAS-BERT 走压缩路线形成对比
- [[wang2020-hat-analysis]] — HAT 是进化-based NAS for Transformer，与本文的 gradient-based 形成方法论对比

## Evidence By Source

### `sources/papers/zhao2021-memory-efficient-dnas.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/memory_efficient_dnas2021.pdf`

^[sources/papers/zhao2021-memory-efficient-dnas.md]
