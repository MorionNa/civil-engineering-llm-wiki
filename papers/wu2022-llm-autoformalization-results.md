---
type: paper-analysis
title: Autoformalization with Large Language Models
authors:
- Yuhuai Wu
- Albert Q. Jiang
- Wenda Li
- Markus N. Rabe
- Charles Staats
- Mateja Jamnik
- Christian Szegedy
year: 2022
venue: arXiv preprint
tags:
- domain/ai4s
- domain/llm
- evidence/paper
methods:
- in-context-learning
- machine-translation
- greedy-decoding
- expert-iteration
- best-first-search
- neural-theorem-proving
- formal-verification
- back-translation
results:
- autoformalization
- BLEU
- MiniF2F
- proof-search
- expert-iteration
- informalization
failure_modes:
- definition-alignment
- missing-assumption
- syntax-type-error
- wrong-function-application
- missing-Isabelle-definition
- context-window
- data-contamination
datasets:
- MATH
- MiniF2F
- PISA
- Archive of Formal Proofs
- The Pile
reproducibility: medium
code_url: []
dataset_url: []
id: paper--wu2022-llm-autoformalization-results
status: active
project: civil-engineering-llm-wiki
keywords:
- large-language-models
- autoformalization
- formalization
- theorem-proving
- proof-assistant
- mathematics-at-scale
- benchmark
- evaluation
- scientific-reasoning
- data-contamination
- reproducibility
- in-context-learning
- machine-translation
- greedy-decoding
- expert-iteration
- best-first-search
- neural-theorem-proving
- formal-verification
- back-translation
- BLEU
- MiniF2F
- proof-search
- informalization
- definition-alignment
- missing-assumption
- syntax-type-error
- wrong-function-application
- missing-Isabelle-definition
- context-window
- MATH
- PISA
- Archive of Formal Proofs
- The Pile
- arXiv preprint
sources:
- sources/papers/wu2022-llm-autoformalization.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# Autoformalization with Large Language Models — 结果

^[sources/papers/wu2022-llm-autoformalization.md]

本页只报告预提取论文文本中有明确案例、比例、表格或资源记录支撑的结果；方法解释见 [[wu2022-llm-autoformalization-method]]，整体判断见 [[wu2022-llm-autoformalization-analysis]]，失败边界见 [[wu2022-llm-autoformalization-critical]]。

## 1. 数据与评估范围

论文使用的 MATH 数据集共有 12,500 道中学和高中数学竞赛题，其中 7,500 道训练题、5,000 道测试题，包含 algebra、pre-algebra、intermediate algebra、number theory、precalculus、probability、geometry 七类（PDF p. 4）。

MiniF2F 包含 488 个由人工以三种形式语言形式化的数学竞赛命题。论文使用其中与 MATH 对应的 algebra 140 题和 number_theory 120 题作为有人工 Isabelle ground truth 的比较集；MiniF2F 的 Isabelle formalization 于 2022 年 3 月提交到仓库（PDF p. 4）。

应用实验另使用 MATH training set 中 algebra、intermediate algebra、number theory 三类 3,908 道题生成自动形式化候选。证明器训练背景 PISA 含 2.49 million Isabelle/HOL 与 Archive of Formal Proofs proof steps（PDF pp. 7–8）。

## 2. 案例研究

### Case study 1：IMO 1987 题

对“存在从非负整数到自身的函数 f，使 f(f(n)) = n + 1987”这一命题，Codex 输出了 Isabelle theorem：把函数类型写成 nat → nat，把存在性否定转成假设后证明 False。论文把该输出作为 perfect autoformalization 示例，并强调它捕捉了 proof-by-contradiction 与 “to itself” 的类型含义（Figure 1, PDF pp. 1–2, 5）。

PaLM 在该案例中整体结构大致正确，但产生了语法错误；论文没有在正文给出该案例的数值成功率（Appendix B.1, PDF pp. 5, 20）。

### Case study 2：行列余数题

同一题要求把“按 8 人一行余 7 人”形式化为“按 4 人一行余多少人”。论文报告：

| 模型 | 该案例结果 |
|---|---|
| PaLM 8B | 无法正确形式化 |
| PaLM 64B | 无法正确形式化 |
| PaLM 540B | 正确形式化为 n mod 8 = 7 ⇒ n mod 4 = 3 |

该对比来自 Appendix B.2；作者据此指出，在该例上模型规模从 64B 增大到 540B 改变了能否得到正确形式化的结果（PDF pp. 5, 21）。

### Case study 3：linear function

对“f 是满足 f(6) − f(2) = 12 的线性函数，求 f(12) − f(2)”的问题，Codex 初始输出使用 linear f，论文判定为错误，因为该写法没有正确展开 Isabelle 中的线性函数概念（Figure 3, PDF pp. 5–6）。

当 prompt 额外加入“通过 f x = a * x + b 表示一条直线”的示例后，Codex 输出了带 a、b 和逐点约束的正确形式化，结论为 30（Appendix B.3, PDF p. 22）。

## 3. BLEU 模型比较

论文对 algebra 的 130 个评估问题和 number_theory 的 110 个评估问题，计算自动形式化与人工 Isabelle ground truth 之间的 BLEU：

| 模型 | algebra | number_theory |
|---|---:|---:|
| PaLM 8B | 31.49 | 22.10 |
| PaLM 64B | 43.13 | 31.43 |
| PaLM 540B | 50.30 | 36.16 |
| Codex | 57.13 | 43.33 |

表中 PaLM 两个 subject 都随模型规模增加而上升；Codex 在两个列上的 BLEU 均高于 PaLM 540B。论文将 Codex 的优势可能归因于其训练中接触了更多形式数据，但这只是作者提出的可能解释，并非独立因果验证（Table 1, PDF p. 6）。

## 4. 150 题人工失败分析

论文从 MATH 随机抽取 algebra、number_theory、intermediate_algebra 各 50 题，由人工检查 Codex 的自动形式化。表 2 的原始计数如下：

| 失败/结果类别 | algebra | number_theory | intermediate_algebra |
|---|---:|---:|---:|
| Perfect translation | 13 | 17 | 8 |
| Incomplete/ill-formed/unclear prompt | 9 | 3 | 14 |
| Fail to align definitions or concepts | 10 | 18 | 18 |
| Inconsistent/missing assumption | 8 | 9 | 9 |
| Syntactical/type error | 7 | 2 | 11 |
| Missing definition in Isabelle | 0 | 12 | 3 |
| Wrong application of functions | 6 | 13 | 16 |
| Other | 6 | 2 | 1 |

三类合计 150 题中，38 题被判为 perfect translation，论文给出的成功率为 25.3%（Table 2, PDF pp. 6–7）。表中各列的类别计数并不都加总为对应的 50 题；提供文本没有说明类别是否允许多标签，因此这里只保留原表，不把它重新解释为互斥分区。

正文给出的典型错误包括：没有把 “greatest possible value” 对齐到 Isabelle 的 Greatest/Max；没有把 factorial 对齐到 fact；错误应用函数；以及缺少 Isabelle 中的定义（PDF pp. 6–7, 27–29）。

## 5. 自动形式化数据与 proof search

Codex 对 3,908 道 MATH training problems 进行形式化，其中 3,363 个自动形式化定理语法正确。以这些语法正确候选为集合，Thor 基础模型 M₀ 第一轮证明了 782 个，成功率为 23.3%；第二轮找到 1,011 个成功证明，成功率为 30.1%（PDF p. 8）。

这些成功证明被并入 PISA/形式数学训练数据，并按 problem statement 去重后微调基础模型。论文没有报告 3,908 个候选的逐题语义正确率，也没有提供生成候选或成功 proof 文件下载地址。

## 6. MiniF2F proof rate

论文在 MiniF2F valid/test 上报告如下 proof success rate：

| 模型 | valid | test |
|---|---:|---:|
| PACT | 23.9% | 24.6% |
| FMSCL | 33.6% | 29.6% |
| Base model (M₀) | 28.3% | 29.9% |
| After 1 expert iteration (M₁) | 36.1% | 34.0% |
| After 2 expert iterations (M₂) | 37.3% | 35.2% |

相对于 M₀，第一轮 expert iteration 把 valid 从 28.3% 提高到 36.1%，把 test 从 29.9% 提高到 34.0%；第二轮进一步提高到 37.3% 和 35.2%。按表中 test 数值，M₂ 的 35.2% 比此前表中 FMSCL 的 29.6% 高 5.6 个百分点；论文正文称其为比此前 state of the art 高 5.6%（Table 3, PDF p. 8）。

## 7. Advanced mathematics informalization

论文从 Isabelle standard library 选取 38 个 theorem、lemma 和 definition，使用 Codex 翻译为自然语言：

- 36/38 个输出被认为 reasonably coherent；
- 其中 29/38 个被认为 more-or-less correct，即 76%；
- 论文把这一结果与 Section 4.4 的约 25% formalization success rate 作对照。

该评价明确允许人类读者补充显然上下文并纠正小错误；例如遗漏 identical distributions 被视为 major error。因此 76% 是在较宽松的人类可读性标准下得到的 informalization 结果，不能当作严格形式等价率（PDF pp. 8–10）。

## 8. 计算资源记录

论文报告全部实验使用 Google Cloud 的 8-core TPUv3；Isabelle 进程最多可访问 32 个 CPU cores。总实验量为 3,920 TPU hours，其中 3,200 用于自动形式化定理的 proof search，240 用于成功证明训练，480 用于 MiniF2F evaluation（PDF p. 8）。

论文还报告 Thor 的基础训练/微调配置：700M non-embedding parameters、24 层、24 attention heads、hidden dimension 1536、vocabulary 50,400；这些是复现实验资源和模型配置记录，不等同于自动形式化准确率（PDF pp. 7–8）。

## 9. 结果证据边界

上述表格没有提供置信区间、跨随机种子的均值/方差或不同 prompt 重复实验；提供文本也没有给出逐题输出、代码 URL 或自动生成数据 URL。因此，本页只报告论文列出的点估计、案例和资源记录，不把它们扩展成统计稳定性结论。

更完整的失败边界和可迁移解释见 [[wu2022-llm-autoformalization-critical]]；本论文提出的流程实体见 [[entities/wu-llm-autoformalization]]。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[wu2022-llm-autoformalization-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | 无公开代码 |
| **数据集** | 无外部数据集 URL（或使用论文内/合成数据） |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
