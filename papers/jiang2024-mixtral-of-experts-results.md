---
id: papers--jiang2024-mixtral-of-experts-results
title: Mixtral 8x7B 实验结果展开
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/llm
- evidence/paper
keywords:
- bias-evaluation
- code-generation-benchmark
- commonsense-reasoning
- llm-benchmark
- long-context-modeling
- math-benchmark
- multilingual-data
- router-analysis
sources:
- sources/papers/jiang2024-mixtral-of-experts.md
created: '2026-06-13'
updated: '2026-07-31'
confidence: high
---

# Mixtral 8x7B 实验结果

## 实验 1：通用 Benchmark vs Llama 家族 (Table 2)

所有模型使用统一评测管线重新评估。

| Model | Active Params | MMLU | HellaS | WinoG | PIQA | Arc-e | Arc-c | NQ | TriQA | HumanE | MBPP | Math | GSM8K |
|-------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| LLaMA 2 7B | 7B | 44.4% | 77.1% | 69.5% | 77.9% | 68.7% | 43.2% | 17.5% | 56.6% | 11.6% | 26.1% | 3.9% | 16.0% |
| LLaMA 2 13B | 13B | 55.6% | 80.7% | 72.9% | 80.8% | 75.2% | 48.8% | 16.7% | 64.0% | 18.9% | 35.4% | 6.0% | 34.3% |
| LLaMA 1 33B | 33B | 56.8% | 83.7% | 76.2% | 82.2% | 79.6% | 54.4% | 24.1% | 68.5% | 25.0% | 40.9% | 8.4% | 44.1% |
| LLaMA 2 70B | 70B | 69.9% | 85.4% | 80.4% | 82.6% | 79.9% | 56.5% | 25.4% | 73.0% | 29.3% | 49.8% | 13.8% | 69.6% |
| Mistral 7B | 7B | 62.5% | 81.0% | 74.2% | 82.2% | 80.5% | 54.9% | 23.2% | 62.5% | 26.2% | 50.2% | 12.7% | 50.0% |
| **Mixtral 8x7B** | **13B** | **70.6%** | 84.4% | 77.2% | **83.6%** | **83.1%** | **59.7%** | **30.6%** | **71.5%** | **40.2%** | **60.7%** | **28.4%** | **74.4%** |

**关键发现**：
- **数学提升最显著**：GSM8K 74.4% vs Llama 2 70B 69.6%（+4.8pp）；MATH 28.4% vs 13.8%（**+14.6pp，翻倍**）。
- **代码大幅领先**：HumanEval 40.2% vs 29.3%（+10.9pp）；MBPP 60.7% vs 49.8%（+10.9pp）。
- MMLU 70.6% 首次超越 GPT-3.5 的 70.0%。
- 仅 13B 激活参数 → 推理 FLOPs ≈ Llama 2 13B 级别。

## 实验 2：Mixtral vs Llama 2 70B vs GPT-3.5 (Table 3)

| Benchmark | Llama 2 70B | GPT-3.5 | **Mixtral 8x7B** |
|-----------|:---:|:---:|:---:|
| MMLU (MCQ 57 subjects) | 69.9% | 70.0% | **70.6%** |
| HellaSwag (10-shot) | **87.1%** | 85.5% | 86.7% |
| ARC Challenge (25-shot) | 85.1% | 85.2% | **85.8%** |
| WinoGrande (5-shot) | **83.2%** | 81.6% | 81.2% |
| MBPP (pass@1) | 49.8% | 52.2% | **60.7%** |
| GSM-8K (5-shot) | 53.6% | 57.1% | **58.4%** |
| MT Bench (Instruct) | 6.86 | 8.32 | **8.30** |

- Mixtral 在 6/7 项上超越或持平 Llama 2 70B 和 GPT-3.5。
- MT Bench 8.30 ≈ GPT-3.5-Turbo (8.32)，显著超越 Llama 2 70B chat (6.86)。

## 实验 3：多语言 Benchmark (Table 4)

对法语、德语、西班牙语、意大利语评估 Arc-c、HellaS、MMLU。

| Model | Active Params | 法语 Avg | 德语 Avg | 西班牙语 Avg | 意大利语 Avg |
|-------|:---:|:---:|:---:|:---:|:---:|
| LLaMA 1 33B | 33B | 52.4% | 51.0% | 55.9% | 52.4% |
| LLaMA 2 70B | 70B | 62.2% | 60.1% | 63.7% | 61.8% |
| **Mixtral 8x7B** | **13B** | **68.8%** | **66.3%** | **68.5%** | **66.3%** |

**跨 4 种语言全面超越 Llama 2 70B**。得益于预训练中多语言数据比例上调 + MoE 额外容量。

## 实验 4：长上下文能力 (Figure 4)

### Passkey Retrieval
- 100% 检索准确率，**与序列长度无关**（测试 0-32k tokens）
- **与 passkey 插入位置无关**（开头/中间/末尾均 100%）
- 证明 MoE 架构不损害长上下文信息提取

### Proof-Pile Perplexity
- 随上下文增加，perplexity **单调递减**
- 无长上下文退化迹象

## 实验 5：偏见评估 (Table 5 / Figure 5)

| 指标 | Llama 2 70B | Mixtral 8x7B |
|------|:---:|:---:|
| BBQ accuracy | 51.5% | **56.0%** |
| BOLD avg sentiment (全领域) | ~0.22 | ~0.23 |
| BOLD std (全领域) | ~0.09 | **~0.08** |

- **BBQ 准确率更高**（56.0% vs 51.5%）→ 更少偏见
- **BOLD 标准差更低** → 各领域内偏差更均衡
- 情感倾向更积极（higher average sentiment）

## 实验 6：指令微调效果 (Section 4)

| 模型 | MT-Bench | LMSys Elo |
|------|:---:|:---:|
| GPT-4 | — | 1212 |
| **Mixtral 8x7B Instruct** | **8.30** | **1121** |
| Claude-2.1 | — | 1117 |
| GPT-3.5-Turbo | 8.32 | 1117 |
| Gemini Pro | — | 1111 |
| Llama-2-70b-chat | 6.86 | 1077 |

- **最佳开源模型**（截至 2023.12）
- 微调方案：SFT on instruction dataset → DPO on paired feedback
- **未使用 RLHF**，仅 SFT + DPO 即超越 GPT-3.5-Turbo

## 实验 7：路由行为分析 (Section 5, Figures 7-8)

### 专家分配分布 (Figure 7)
- 在 The Pile 的 8 个子集（ArXiv、DM Mathematics、GitHub、Gutenberg、PhilPapers、PubMed、StackExchange、Wikipedia）上测量第 0/15/31 层的专家分配。
- **核心发现：无明显的领域级专家特化。** 各领域的专家分配分布高度相似。
- 唯一例外：DM Mathematics（合成数据），在第 0 层和第 31 层分布略有偏离 — 归因于合成数据有限的自然语言覆盖。

### 连续 token 专家重复 (Table 5)

| | First choice | First or second choice |
|---|---|---|
| Layer 0 (random) | ~14% (≈12.5% baseline) | ~48% (≈46% baseline) |
| Layer 15 | 23-28% | 61-67% |
| Layer 31 | 20-26% | 44-53% |

- Layer 0 **接近随机分配**
- Layer 15/31 **显著高于随机**：连续 token 常分配到相同专家
- 同一 token 的 first + second choice 组合也有 50-67% 连续重复

### 语法路由模式 (Figure 8)
- Python 中的 `self`、英文中的 `Question` 等 token → 总是分配到同一专家
- 缩进 token → 固定专家（尤其首末层）
- **结论：路由器更多基于句法/语法模式，而非领域语义**

## 关键结论

1. **MoE 以 1/5 激活参数超越密集模型** — 效率收益明确
2. **数学和代码是最大优势领域** — MATH +14.6pp, HumanEval +10.9pp
3. **多语言能力来自数据配比 + MoE 容量** — 非英语语言全面领先
4. **长上下文无退化** — MoE 与 32k context 完全兼容
5. **路由器学句法而非语义** — 对 MoE 设计的预期管理有重要启示
6. **SFT + DPO 无 RLHF 达到 SOTA** — 简化对齐 pipeline

## 关联页面
- [[jiang2024-mixtral-of-experts-analysis]] — 全维度概述
- [[jiang2024-mixtral-of-experts-method]] — 方法机制
- [[jiang2024-mixtral-of-experts-critical]] — 贡献 + Negative + 可迁移

## Evidence By Source

### `sources/papers/jiang2024-mixtral-of-experts.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/jiang2024_mixtral_of_experts.md`

^[sources/papers/jiang2024-mixtral-of-experts.md]
