---
title: "Fedus et al. (2021) — Switch Transformers: 论文分析"
created: 2026-06-13
updated: 2026-06-13
type: paper-analysis
tags: []
sources: [raw/papers/fedus2021_switch_transformer.md]
methods: [mixture-of-experts, switch-routing, load-balancing-loss, selective-precision, expert-dropout, expert-parallelism, model-parallelism, data-parallelism, distillation, top-1-routing]
results: [pre-training-speedup-7x, downstream-fine-tuning-sota, multilingual-101-languages, distillation-99pct-compression, trillion-parameter-scaling, perplexity, t5-baseline]
failure_modes: [training-instability-bfloat16, large-model-instability, upstream-downstream-translation-gap, expert-overflow, token-dropping]
datasets: [c4, mc4, glue, superglue, squad, cnndm, bbc-xsum, winogrande, trivia-qa, natural-questions, web-questions, arc, anli]
reproducibility: high
code_url:
  - https://github.com/google-research/t5x
  - https://github.com/tensorflow/mesh/blob/master/mesh_tensorflow/transformer/moe.py
dataset_url:
  - https://www.tensorflow.org/datasets/catalog/c4
  - https://www.tensorflow.org/datasets/catalog/glue
  - https://www.tensorflow.org/datasets/catalog/super_glue
confidence: high
---

# Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity

> **Authors:** William Fedus, Barret Zoph, Noam Shazeer (Google Brain)
> **Published:** JMLR 23 (2022) | arXiv: 2101.03961
> **License:** CC-BY 4.0 | Code + checkpoints: [t5x](https://github.com/google-research/t5x)

---

## 1. 工程背景 (Engineering Background)

大规模语言模型的密集扩展（如 GPT-3 175B、T5-11B）虽然有效，但计算成本极高——训练一次需数百万美元级别资源。Mixture of Experts (MoE) 提供了一条替代路径：通过稀疏激活——每个输入仅激活模型参数的一个子集——在不增加每个 token 计算量（FLOPs）的前提下大幅增加模型总参数量。然而，MoE 的广泛采用受限于三大障碍：**实现复杂度高**（top-k 路由需多个 expert 协同）、**通信开销大**（跨设备 all-to-all 通信）、**训练不稳定**（路由的硬决策导致梯度方差大，bfloat16 精度下尤其严重）。解决这些问题将使"万亿参数模型高效训练"从愿景变为工程现实。

## 2. Research Gap

Shazeer et al. (2017) 的 MoE Transformer 使用 top-k（k≥2）路由——每个 token 同时发送给多个 expert，计算其输出的加权和。当时普遍认为 k≥2 是必要的，因为路由函数需要比较至少两个 expert 才能获得有意义的梯度。此外，GShard (Lepikhin et al., 2020) 用 float32 全精度训练 MoE，放弃了 bfloat16 的速度优势。**核心矛盾**：top-k 路由导致计算量和通信量翻倍，而 float32 训练进一步拖慢速度——但没人验证过 k=1 是否可行，也没人解决 bfloat16 下的 MoE 训练稳定性。

## 3. 科学问题 (Scientific Question)

**能否设计一种每个 token 仅路由到单个 expert（k=1）的稀疏模型，在保持模型质量的前提下，降低计算和通信开销，并实现低精度（bfloat16）下的稳定大规模训练？**

## 4. 研究目标 (Research Objective)

提出 **Switch Transformer**：一个简化且高效的 MoE 架构，用 top-1（Switch）路由替代 top-k 路由，配合选择性精度训练、缩小的参数初始化和 expert dropout 等训练技巧，在预训练、微调和多任务多语言三个 NLP 场景中全面超越 FLOP-matched 的密集 T5 基线，并扩展到万亿参数规模。

## 5. 方法机制 (Method & Mechanism)

→ [[fedus2021-switch-transformer-method]]

**核心简化 — Switch Routing (k=1)：** 每个 token 仅路由到 router 输出概率最高的单个 expert，乘以 gate value 后通过残差连接输出。相比 top-k MoE：(1) router 计算量减半；(2) expert capacity（每 expert 处理的 batch size）至少减半；(3) 通信开销降低。

**负载均衡：** 辅助损失函数 `loss = α·N·Σ(fi·Pi)` 鼓励 token 在 experts 间均匀分布，α=10⁻²。超标的 token 被"丢弃"（通过残差连接跳过该层）。

**选择性精度：** router 函数内部使用 float32 计算 softmax 和 dispatch/combine tensors，结果立即 cast 回 bfloat16，避免昂贵的 float32 跨设备通信。

**训练稳定性：** (1) 初始化 scale 缩小 10×（σ = √(0.1/n)）；(2) fine-tuning 时对 expert FFN 层使用高 dropout（0.4），非 expert 层保持 0.1。

**并行策略：** 提出 data / model / expert 三维并行（N = n × m），可组合使用以扩展到万亿参数。

## 6. 结果证据 (Result & Evidence)

→ [[fedus2021-switch-transformer-results]]

**预训练缩放：** Switch-Base 64e 在 1/7 时间内达到 T5-Base 同等 perplexity（**7× speedup**）。Switch-Base 比 T5-Large（3.5× FLOPs/token）仍有 **2.5× speedup**。Switch-XXL (395B) 和 Switch-C (1.6T) 分别比 T5-XXL 快 **4×**。

**下游微调：** Switch-Base 在 SuperGLUE +4.4pp、Winogrande +6.7pp、Trivia QA +6.2pp。Switch-Large 全面超越 T5-Large（SuperGLUE +2.0pp, Trivia QA +7.4pp）。

**蒸馏：** 可将稀疏模型压缩 95-99%，同时保留 ≈30% 的质量增益。

**多语言：** 101 种语言全部提升，平均 5× 步数加速，91% 语言获得 ≥4× 加速。

## 7. 贡献 (Contribution)

→ [[fedus2021-switch-transformer-critical#7-贡献-contribution]]

1. **Switch Routing (k=1)：** 证明单个 expert 路由不仅可行，且优于 top-k MoE——更简单、更快、质量相当或更好
2. **选择性精度训练：** 首次实现 bfloat16 下 MoE 的稳定训练
3. **训练稳定化技术：** 缩小初始化 + expert dropout
4. **Expert 并行 + 模型并行 + 数据并行**的三维组合策略
5. **稀疏→密集蒸馏：** 99% 压缩比下保留 30% 质量增益
6. **万亿参数模型训练：** Switch-C (1.6T) 和 Switch-XXL (395B) 的预训练与评估

## 8. 核心知识点 (Core Knowledge)

→ [[fedus2021-switch-transformer-critical#8-核心知识点-core-knowledge]]

1. **参数量是独立于 FLOPs 的缩放轴**：增加 expert 数量不增加每 token FLOPs，但持续提升模型质量
2. **k=1 路由既简单又高效**：与当时学界共识（k≥2 为梯度所必需）相悖，但实验证明 k=1 表现更好
3. **容量因子（capacity factor）是精度-效率的调节旋钮**：1.0 最省内存但 tokens 可能溢出，1.25 是最佳平衡点
4. **负载均衡损失对稀疏训练至关重要**：α=10⁻² 足以均衡负载而不干扰主任务

## 9. Negative Knowledge

→ [[fedus2021-switch-transformer-critical#9-negative-knowledge]]

- ⚠️ Switch-XXL (395B, 大 FLOPs/token) 训练不稳定，Switch-C (1.6T, 小 FLOPs/token) 反而稳定——**更大 FLOPs ≠ 更稳定**
- ⚠️ 上游 perplexity 的优势不完全转化为下游任务性能（尤其在推理任务 SuperGLUE 上）
- ⚠️ Expert overflow + token dropping 是架构固有缺陷，No-Token-Left-Behind 尝试未带来经验收益
- ⚠️ 仅在 Transformer FFN 层替代 expert，Attention expert 在 bfloat16 下发散

## 10. 可迁移知识 (Transferable Knowledge)

→ [[fedus2021-switch-transformer-critical#10-可迁移知识-transferable-knowledge]]

- Switch Routing 简化思想可迁移到任何含"多选一"路由的稀疏架构
- 选择性精度（局部 float32 + 全局 bfloat16）是训练稀疏模型的标准策略
- Expert dropout（仅对 expert 层加高 dropout）可缓解稀疏模型 fine-tuning 过拟合

## 11. 研究机会 (Research Opportunity)

→ [[fedus2021-switch-transformer-critical#11-研究机会-research-opportunity]]

- 解决大 FLOPs/token 稀疏模型的训练稳定性
- 理解上游→下游迁移的断层（尤其推理任务）
- 异构 expert 设计（不同 expert 有不同容量/计算量）
- Expert 层扩展到 Self-Attention 以外

## 12. 可复现性 (Reproducibility)

→ [[fedus2021-switch-transformer-critical#12-可复现性-reproducibility]]

| 项目 | 说明 |
|------|------|
| **等级** | 🟢 高 |
| **官方代码** | https://github.com/google-research/t5x (JAX) + https://github.com/tensorflow/mesh (TF) |
| **数据集** | C4 (公开), mC4 (公开), GLUE/SuperGLUE/SQuAD 等标准 benchmark |
| **协议** | CC-BY 4.0 |
| **复现要点** | 论文提供了完整 pseudo-code (Appendix F) + 模型检查点公开；需要 TPU 集群复现万亿参数实验 |

---

## 关联页面

- [[fedus2021-switch-transformer-method]] — 方法机制展开
- [[fedus2021-switch-transformer-results]] — 结果证据展开
- [[fedus2021-switch-transformer-critical]] — 贡献/知识点/Negative/可迁移/研究机会
