---
type: paper-analysis
title: 'FormalScience: Scalable Human-in-the-Loop Autoformalisation of Science with
  Agentic Code Generation in Lean'
authors:
- Jordan Meadows
- Lan Zhang
- André Freitas
year: 2026
venue: arXiv preprint
tags:
- domain/ai4s
- evidence/paper
methods:
- human-in-the-loop
- autoformalization
- theorem-proving
- lean-4
- mathlib
- language-agents
results:
- benchmark
- evaluation
- formalization
- physics-formalization
failure_modes:
- large-language-models
- physics-formalization
- theorem-proving
- evaluation
datasets:
- physics
- benchmark
- formalization
- lean-4
reproducibility: medium
code_url:
- https://github.com/jmeadows17/formal-science
dataset_url: []
id: paper--meadows2026-formalscience-results
status: active
project: civil-engineering-llm-wiki
keywords:
- formal-science
- autoformalization
- formalization
- theorem-proving
- proof-assistant
- lean
- lean-4
- mathlib
- physics-formalization
- physics-reasoning
- scientific-reasoning
- large-language-models
- language-agents
- human-in-the-loop
- benchmark
- evaluation
- physics
- arXiv preprint
sources:
- sources/papers/meadows2026-formalscience.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# FormalScience：实验与数值结果

^[sources/papers/meadows2026-formalscience.md]

本页只记录论文正文、表格或图示文字中有证据支持的结果；机制解释见 [[meadows2026-formalscience-method]]，综合边界见 [[meadows2026-formalscience-critical]]，数据集实体见 [[entities/formalphysics]]。

## 1. FormalPhysics 的构成

论文使用 FormalScience 生成 FormalPhysics，共 200 个 physics examples，每个包含 natural-language/LaTeX statement、非形式 solution 和完整 Lean4 formal proof。样本主要来自 quantum mechanics（QM）和 electromagnetism（EM），另含 Other physics 子域。作者将其定位为 evaluation benchmark，而不是 fine-tuning corpus。

附录 A 说明：5 个 gold-standard statement-proof pairs 用于 few-shot；从 Meadows et al. (2024) 的 derivations 中随机选 200 个样本，打乱后按每批 5 个分组，形成 40 个 few-shot prompts。数据构造由一名 physics expert 在约一个月内完成，论文报告总成本约 50 USD。

## 2. 与 Lean4 benchmark 的比较

下表抄录 Table 2 的主要数值。FV 由 Lean4 判定；FQ、LP、MC 由 GPT-4.1-mini LLM judge 判定。Objects 和 Formulae 是自然语言 statement 中直接提到的数学/物理对象和公式平均数。

| Dataset | Objects | Formulae | FV (%) | FQ (%) | LP (%) | MC (%) |
|---|---:|---:|---:|---:|---:|---:|
| miniF2F | 3.14 ± 1.55 | 3.21 ± 1.53 | 88.00 | 63.00 | 92.00 | 92.00 |
| ProofNet | 3.67 ± 1.48 | 3.62 ± 1.52 | 95.50 | 61.50 | 77.50 | 77.50 |
| Lean Workbook | 3.67 ± 1.99 | 3.62 ± 2.26 | 89.00 | 46.00 | 78.00 | 85.00 |
| FormalMATH | 4.47 ± 2.45 | 4.53 ± 2.62 | 97.50 | 80.00 | 98.00 | 96.50 |
| Herald-Statement | 4.92 ± 2.43 | 4.80 ± 2.30 | 80.50 | 63.50 | 87.00 | 87.00 |
| Herald-Proof | 6.57 ± 2.32 | 6.42 ± 2.37 | 2.00 | 73.00 | 94.50 | 94.00 |
| FormalPhysics | 6.41 ± 2.34 | 6.22 ± 2.13 | 100.00 | 73.50 | 72.00 | 72.50 |

论文据此报告：FormalPhysics 的每例对象/公式数量大约是 miniF2F、ProofNet 和 Lean Workbook 的两倍，并与 Herald-Proof 的复杂度相近；FormalPhysics 的 FV 为 100%，FQ 为第二高，但 LP 和 MC 在表中最低。作者把后两项与 vector calculus、Dirac notation 和基础 calculus 在 Lean4/Mathlib 中的表达困难联系起来。

## 3. Statement autoformalisation 结果

Table 3 使用 GPT-4.1-mini 作为 judge。百分比依次为 FV、FQ、LP、MC。

| Pipeline | Model | FV | FQ | LP | MC |
|---|---|---:|---:|---:|---:|
| Zero-shot | Qwen2.5-Coder-7B | 1.0 | 15.0 | 24.0 | 20.5 |
| Zero-shot | DeepSeek-Prover-7B | 13.0 | 23.0 | 27.5 | 24.0 |
| Zero-shot | Kimina-7B | 51.5 | 6.5 | 10.5 | 9.5 |
| Zero-shot | GPT-OSS-20B | 4.5 | 68.5 | 73.0 | 72.5 |
| Zero-shot | GPT-5.1 | 14.5 | 79.5 | 76.5 | 77.0 |
| Self-refinement | Qwen2.5-Coder-7B | 1.0 | 16.5 | 23.0 | 19.5 |
| Self-refinement | DeepSeek-Prover-7B | 4.5 | 17.0 | 23.0 | 23.0 |
| Self-refinement | Kimina-7B | 23.0 | 6.5 | 9.5 | 8.0 |
| Self-refinement | GPT-OSS-20B | 7.5 | 70.5 | 77.0 | 79.0 |
| Self-refinement | GPT-5.1 | 17.0 | 82.5 | 82.0 | 82.0 |
| Agentic | Qwen3-Sonnet-14B | 52.0 | 1.0 | 10.5 | 6.5 |
| Agentic | GPT-OSS-20B | 31.0 | 73.0 | 72.5 | 73.0 |
| Agentic | Qwen3-Coder-30B | 5.5 | 49.5 | 59.0 | 48.0 |
| FormalScience | GPT-5.1 / Claude-4.5 | 100.0 | 73.5 | 72.0 | 72.5 |

论文报告 zero-shot 与 alignment mean（FQ/LP/MC 的均值）的 Spearman、Pearson 相关系数均在一位小数上为 0，且 p>0.9。对主 judge 而言，self-refinement 的对齐分数按模型基本不变，但 token 使用约增加一倍，且没有清晰改善 FV 或 alignment。

在 agentic setting，GPT-OSS-20B 的 FV 从 zero-shot 的 4.5% 提升到 31.0%，而 FQ/LP/MC 没有显著下降。FormalScience 的 100.0% FV 是该表中最佳；论文将其描述为超过最佳 open-source agentic approach 的三倍。

## 4. 独立 7B judge 的结果

Table 4 用 Qwen2.5-Coder-7B-Instruct 作为 judge，仍报告 zero-shot 与 self-refinement；列顺序为 FV、FQ、LP、MC。

| Pipeline | Model | FV | FQ | LP | MC |
|---|---|---:|---:|---:|---:|
| Zero-shot | Qwen2.5-Coder-7B | 1.0 | 8.0 | 9.0 | 12.5 |
| Zero-shot | DeepSeek-Prover-7B | 13.0 | 12.5 | 13.5 | 14.0 |
| Zero-shot | Kimina-7B | 51.5 | 11.0 | 14.5 | 6.5 |
| Zero-shot | GPT-OSS-20B | 4.5 | 15.5 | 12.5 | 17.5 |
| Zero-shot | GPT-5.1 | 14.5 | 27.0 | 28.0 | 33.0 |
| Self-refinement | Qwen2.5-Coder-7B | 1.0 | 11.5 | 7.0 | 10.5 |
| Self-refinement | DeepSeek-Prover-7B | 4.5 | 26.5 | 11.5 | 17.0 |
| Self-refinement | Kimina-7B | 23.0 | 6.0 | 7.5 | 5.0 |
| Self-refinement | GPT-OSS-20B | 7.5 | 14.5 | 10.5 | 16.5 |
| Self-refinement | GPT-5.1 | 17.0 | 38.0 | 35.0 | 42.0 |

两位 judge 在约 1,000 对 paired binary judgments/condition 上的 phi coefficient 为 0.28–0.37，均 p<10^-9。两者在每个 setting 和 metric 都把 GPT-5.1 排在第一。7B judge 更保守；对 GPT-5.1 和 GPT-OSS-20B，超过 95% 的分歧是 GPT judge=True、7B judge=False。六个 metric×setting 比较的 Kendall tau 范围为 0.2–1.0，中位数 0.80，其中五项不低于 0.6。

论文同时指出，7B judge 下的 FV–alignment 相关仍接近 0（区间约为 -0.10 到 0.30，均 p>0.6）；“self-refinement 分数不变”和 GPT-5.1 相对 DeepSeek-Prover 的效果量，则会随 judge 校准而改变。

## 5. Semantic drift 证据

论文定义四类 drift：Notational Collapse、Abstraction Elevation、Proof Strategy Substitution、Implicit Premise Selection。Figure 3 按 QM（n=88）、EM（n=77）和 Other（n=35）报告 prevalence。

- Notational Collapse 在超过 75% 的 QM proofs 中出现，是 QM 中最显著的类别；其例子把 Hilbert-space quantum statevector/Dirac 结构折叠成 complex scalar，Lean 实际验证的是更简单的复数恒等式。
- Abstraction Elevation 把 vector calculus 或积分替换成抽象线性代数、代数假设或简单恒等式；正文将其描述为 FormalPhysics 中的少数类别。
- Proof Strategy Substitution 保留数学对象，但用另一种证明策略绕开 informal derivation 中的直接微分等步骤。
- Implicit Premise Selection 显式加入自然语言中未陈述的前提；正文认为这是唯一明确有益的 drift 类型。只有 2% 的例子是“纯”该类别、没有其他 drift。

预提取文本中 Abstraction Elevation、Proof Strategy Substitution 和 Implicit Premise Selection 的比较符号部分存在字符编码损坏；除明确可读的“超过 75% QM”与“2% pure”外，本页不补写严格上下界。

## 6. 资源与规模结果

每个 agentic baseline 在 RTX 5090 上需要 100+ 小时 compute，约等于每个 physics proof 30+ 分钟；FormalScience 数据构造由一名 physics expert 用约一个月完成，论文报告总成本约 50 USD。具体 GPU 型号之外的硬件、并发方式、Lean4/Mathlib commit 和完整 token 统计，提供文本未披露或无法确认。

## 7. 结果边界

上述数字来自固定的 200-example FormalPhysics corpus、指定 LLM 版本和当时的 Lean4/Mathlib 配置。论文明确提醒模型能力和库覆盖会快速变化；因此 100.0% FV、31.0% agentic FV 以及 judge 分数都是该实验配置下的结果，而不是永久能力上限。

与方法实体和数据实体的交叉引用：[[entities/formalscience]]、[[entities/formalphysics]]。批判性解释与可迁移结论见 [[meadows2026-formalscience-critical]]。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[meadows2026-formalscience-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | https://github.com/jmeadows17/formal-science |
| **数据集** | 无外部数据集 URL（或使用论文内/合成数据） |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
