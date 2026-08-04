---
type: paper-analysis
title: 'UGPhysics: A Comprehensive Benchmark for Undergraduate Physics Reasoning with
  Large Language Models — Results'
authors:
- Xin Xu
- Qiyun Xu
- Tong Xiao
- Tianhao Chen
- Yuchen Yan
- Jiaxin Zhang
- Shizhe Diao
- Can Yang
- Yang Wang
year: 2025
venue: Proceedings of the 42nd International Conference on Machine Learning (PMLR
  267)
tags:
- domain/ai4s
- evidence/paper
methods:
- benchmark
- evaluation
- MARJ
- rule-based-judgment
- model-based-judgment
- zero-shot-evaluation
results:
- benchmark
- evaluation
- human-evaluation
- data-contamination
- error-analysis
failure_modes:
- physics-reasoning
- scientific-reasoning
- evaluation
- data-contamination
- large-language-models
datasets:
- UGPhysics
- undergraduate-physics-problems
reproducibility: high
code_url:
- https://github.com/YangLabHKUST/UGPhysics
dataset_url:
- https://github.com/YangLabHKUST/UGPhysics
id: paper--xu2025-ugphysics-results
status: active
project: civil-engineering-llm-wiki
keywords:
- large-language-models
- physics-reasoning
- benchmark
- evaluation
- scientific-reasoning
- data-contamination
- reproducibility
- MARJ
- rule-based-judgment
- model-based-judgment
- zero-shot-evaluation
- human-evaluation
- error-analysis
- UGPhysics
- undergraduate-physics-problems
- Proceedings of the 42nd International Conference on Machine Learning (PMLR 267)
sources:
- sources/papers/xu2025-ugphysics.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# UGPhysics — 结果证据

^[sources/papers/xu2025-ugphysics.md]

本页只保留预提取文本中可定位到摘要、正文、表格或图的实验/数值结果。方法流程见 [[xu2025-ugphysics-method]]，总体解释见 [[xu2025-ugphysics-analysis]]，对统计口径和限制的批判见 [[xu2025-ugphysics-critical]]。

## 1. 基准统计

Table 2 报告的 UGPhysics 结构统计如下：

| 指标 | 论文报告值 | 来源 |
|---|---:|---|
| 源问题数 | 5,520 | Table 2 |
| 语言数 | 2 | Table 2 |
| 物理域 | 3 | Table 2 |
| 核心学科 | 13 | Table 2 |
| 主题 | 59 | Table 2 |
| 答案类型 | 7 | Table 2 |
| 难度等级 | 4 | Table 2 |
| 平均题目长度 | 82.4 tokens | Table 2 |
| 平均解答长度 | 318.5 tokens | Table 2 |
| 平均答案数 | 1.34 | Table 2 |

引言和 Table 1 说明，5,520 道原始中文题翻译成英文后，双语文本测试实例为 11,040。三个域为 Mechanics & Thermodynamics、Electromagnetism 和 Modern Physics。

Table 14 给出的 11,040 个语言实例技能分布为：Knowledge Recall 1,168，Laws Application 3,914，Math Derivation 4,440，Practical Application 1,106，Others 412。

## 2. MARJ 人工可靠性

Section 5.2 从测试例中随机选择 100 个样本，以人工标注作为 gold standard，比较 MARJ 与人工判断。论文报告 MARJ accuracy 为 **98%**。作者同时指出，Sympy 对容易直接验证的答案评测效率较高，MARJ 对不适合纯规则判定的复杂答案也具有韧性。

该 98% 是 100 个随机样本上的报告值；文本没有给出按答案类型、学科或置信区间拆分的结果。

## 3. 主模型结果

Table 5 的主体模型行给出以下总体准确率（百分比）：

| 模型 | EN | ZH | Overall Average | 来源 |
|---|---:|---:|---:|---|
| OpenAI-o1-mini-2024-09-12 | 49.96 | 49.60 | **49.78** | Table 5 |
| DeepSeek-R1-Distill-Llama-70B | 45.96 | 34.38 | **40.17** | Table 5 |
| QwQ-32B-Preview | 37.37 | 37.30 | 37.34 | Table 5 |
| Qwen2.5-Math-72B-Instruct | 39.60 | 39.44 | 39.52 | Table 5 |
| GPT-4o-2024-08-06 | 39.29 | 38.01 | 38.66 | Table 5 |

Section 4.2 进一步写明：31 个被评估 LLM 中有 15 个总体分数低于 20%，只有两个模型超过 40%；作者据此把 UGPhysics 描述为对当前 LLM 具有挑战性的基准。

### 3.1 表格与摘要的版本口径

Table 5 在主体四组模型之后另列 “Newly-added Results”：Phi-4 的 EN 37.16、ZH 33.44、总体 35.30；DeepSeek-R1 的 EN 57.16、ZH 55.53、总体 **56.34**。摘要、Section 4.2 和 Conclusion 仍把 OpenAI-o1-mini 的约 49.8% 写成最高结果。

因此，本页同时保留两类证据：叙述主实验中的 49.78% 与表格新增行的 56.34%。提供文本未说明新增行是否应从“31 个模型”统计中排除，也未解释排名冲突；不能替作者把它们合并成一个无歧义排行榜。

## 4. 学科与推理技能结果

Figure 2a 将八个强 LLM 的结果按学科平均：

| 学科 | 平均准确率 |
|---|---:|
| Semiconductor Physics | 31.0% |
| Atomic Physics | 26.7% |
| Thermodynamics | 23.6% |
| Quantum Mechanics | 22.7% |
| Solid-State Physics | 22.5% |
| Classical Electromagnetism | 22.2% |
| Statistical Mechanics | 21.7% |
| Classical Mechanics | 21.6% |
| Relativity | 20.7% |
| Wave Optics | 20.2% |
| Electrodynamics | 19.3% |
| Geometrical Optics | 16.9% |
| Theoretical Mechanics | 16.5% |

Figure 2b 的作者观察是八个强模型在 Knowledge Recall 上表现较好，在 Math Derivation 上更困难；OpenAI-o1-mini 在四类技能及 Others 上均高于其他所列模型。Table 20 给出 OpenAI-o1-mini 的一个具体切片：EN/ZH Knowledge Recall 为 69.18/63.87，Laws Application 为 53.60/51.46，Math Derivation 为 42.16/45.05，Practical Application 为 47.92/45.75，Others 为 50.49/50.97。

## 5. 语言差异

Table 5 的总体 EN/ZH 结果显示，不同模型的语言差异并不一致：

| 模型 | EN | ZH | EN−ZH 绝对差 |
|---|---:|---:|---:|
| LLaMA3.3-70B-Instruct | 35.87 | 26.07 | 9.80 个百分点 |
| DeepSeek-R1-Distill-Llama-70B | 45.96 | 34.38 | 11.58 个百分点 |
| Qwen2.5-72B-Instruct | 35.98 | 36.47 | 0.49 个百分点 |
| QwQ-32B-Preview | 37.37 | 37.30 | 0.07 个百分点 |

Figure 3 按 EN−ZH 差异排序展示若干模型；正文将 LLaMA 与 Qwen 的差异联系到预训练/微调中文语料量，但这属于作者的解释而非单独的因果实验。

## 6. 错误类型

Section 5.3 选择 OpenAI-o1-mini 的 100 个错误答案进行人工标注，Figure 4 报告：

| 错误类型 | 比例 |
|---|---:|
| flawed reasoning | 31.0% |
| knowledge deficiency | 25.0% |
| wrong application | 18.0% |
| computation error | 8.0% |
| misunderstanding | 7.0% |
| exceeding max output | 5.0% |
| instruction following | 4.0% |
| others | 2.0% |

这组统计的分母是“OpenAI-o1-mini 的 100 个错误答案”，不是全部测试答案；各类别合计 100%。

## 7. 数据泄漏检测

Table 6 在若干模型子集上报告污染比例和“污染且正确”比例：

| 模型 | Contaminated | Contaminated & Correct |
|---|---:|---:|
| DeepSeek-Math-7B-RL | 0.00% | 0.00% |
| LLaMA3.1-8B-Instruct | 0.53% | 0.06% |
| LLaMA3.3-70B-Instruct | 0.65% | 0.29% |
| Qwen2.5-Math-7B-Instruct | 0.65% | 0.36% |
| Qwen2.5-Math-72B-Instruct | 0.75% | 0.68% |
| QwQ-32B-Preview | 0.71% | 0.65% |
| DeepSeek-R1-Distill-Qwen-7B | 0.00% | 0.00% |
| DeepSeek-R1-Distill-Qwen-32B | 0.00% | 0.00% |

论文说这些污染样本以及污染且正确样本都很少，因此认为泄漏对 UGPhysics 的影响有限；检测仅覆盖表中子集，不能解释未测试模型的污染情况。

## 8. 与其他基准比较

Table 7 报告 GPT-4o 在不同基准上的准确率：MMLU college physics 68.60%，MMLU high school physics 72.80%，MMLU conceptual physics 92.30%，MMLU-pro 75.06%，OlympicArena 55.92%，GPQA 53.60%，MATH 76.60%，UGPhysics 38.67%。这些是不同数据集上的对照值，不是同一题集上的迁移实验。

## 9. Token 使用与截断

Section 5.5 报告，DeepSeek-R1 在不设置最大 token 限制的 API 使用方式下，解决 UGPhysics 平均需要 5,555 tokens。对最大输出 8,192 的 DeepSeek-R1-Distill-Qwen-32B，UGPhysics 平均 4,081 tokens，MATH 平均 3,079 tokens。

Table 8 的 clip ratio（百分比）显示，8,192 上限下 DeepSeek-R1-Distill-Llama-70B 为 19.16%，QwQ-32B-Preview 为 19.01%，DeepSeek-R1-Distill-Qwen-32B 为 38.55%；扩展上限后分别为 12.25%、8.54% 和 34.47%。OpenAI-o1-mini 在 8,192 下为 2.01%。正文称扩展到 16,384，表头文本显示为 “16382”，该处存在文本/表头不一致。

Table 9 的性能（8,192 → 扩展上限）为：DeepSeek-R1-Distill-Qwen-7B 24.64% → 24.86%，Qwen-32B 31.93% → 32.21%，Llama-8B 13.11% → 14.51%，Llama-70B 40.17% → 41.77%，QwQ-32B 37.34% → 38.90%。

## 10. 结果边界

以上数值均保留表格、图或正文中的原始统计口径；未把新增 DeepSeek-R1 行强行并入 31 模型主榜，也未把 100 例人工样本结果外推到全部题目。复现设置、判定级联和阈值边界见 [[xu2025-ugphysics-method]]；对结果矛盾、污染检测和评测外推限制的分析见 [[xu2025-ugphysics-critical]]。

## 12. 可复现性（Reproducibility）

**🟢 高复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[xu2025-ugphysics-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟢 高复现性 |
| **官方代码** | https://github.com/YangLabHKUST/UGPhysics |
| **数据集** | https://github.com/YangLabHKUST/UGPhysics |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
