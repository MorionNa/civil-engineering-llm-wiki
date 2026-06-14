---
title: "Primer"
created: 2026-06-14
updated: 2026-06-14
type: entity
tags: [architecture, transformer, efficient-inference, language-model, nas, primer]
sources: [raw/papers/primer2021_efficient_transformers.pdf]
confidence: high
---

# Primer (PRIMitives searched transformER)

So et al. (NeurIPS 2021) 通过底层 TF 原语进化搜索发现的 Transformer 高效变体。在 decoder-only 自回归语言建模上，以 1/3 ~ 1/4 的训练计算量达到原版 Transformer 同等质量。核心改进仅两项：**Squared ReLU** 激活函数和 **MDHA (Multi-DConv-Head Attention)**。

## 关键信息

| 属性 | 值 |
|------|-----|
| **全称** | PRIMitives searched transformER |
| **类型** | 神经网络架构（decoder-only Transformer 变体） |
| **作者** | David R. So, Wojciech Mańke, Hanxiao Liu, Zihang Dai, Noam Shazeer, Quoc V. Le |
| **机构** | Google Research, Brain Team |
| **发表** | NeurIPS 2021 (arXiv: 2109.08668) |
| **核心改进** | Squared ReLU (FFN) + MDHA (Attention) |
| **代码** | https://github.com/google-research/google-research/tree/master/primer |
| **训练加速** | 1.7× ~ 4.2× vs Vanilla Transformer（因 setting 而异） |

## 架构核心

### Primer-EZ（推荐简单版本）

仅在标准 Transformer decoder 上做两处修改：

1. **Squared ReLU**：FFN 中的 ReLU → (max(0, x))²。无参，数学上与 ReGLU (U=V) 等价但更简单
2. **MDHA**：每个 attention head 的 Q/K/V 1×1 投影后加 3×1 spatial depthwise convolution（pointwise → depthwise 顺序）

### 完整 Primer 额外修改

- Pre/post norm 重排（attention 之前 norm，FFN 之后 norm）
- 自定义归一化（x(x-μ) 代替 (x-μ)²）
- 12× bottleneck projection（小 d_model 大 d_ff，仅小模型有效）
- Post-softmax spatial gating（仅固定长度）
- Shared QK weights（通常有害）

> ⚠️ 推荐：新手从 Primer-EZ 开始。完整 Primer 仅在 T2T/Lingvo 下展示进一步增益，且包含不普适的修改。

## 性能概要

| Setting | 规模 | vs Vanilla Transformer |
|---------|------|----------------------|
| LM1B 搜索任务 | 35M | **1.7~2.3×** speedup |
| C4 LM (T5) | 110M | **1.68~1.91×** speedup |
| PG19 LM (T5) | 110M | **1.68~1.98×** speedup |
| C4 LM 大尺度 (T5) | 537M | **4.2×** speedup |
| One-shot GPT-3 style | 1.9B | **3×** speedup |

## 关联页面

- [[so2021-primer-analysis]] — 完整论文分析（12 维度）
- [[so2021-primer-method]] — 搜索空间、进化算法、训练策略
- [[so2021-primer-results]] — 关键实验数据与表格
- [[so2021-primer-critical]] — 贡献、负面知识、可迁移、研究机会
- [[chen2021-tenas-analysis]] — TE-NAS（训练-free NAS，潜在加速 Primer 搜索的方法）
- [[entities/nasbench201]] — NAS-Bench-201（NAS benchmark）
