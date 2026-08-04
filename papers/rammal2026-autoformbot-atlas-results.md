---
type: paper-analysis
title: Formalizing Mathematics at Scale
authors:
- Ahmad Rammal
- Niket Patel
- Fabian Gloeckle
- Amaury Hayat
- Julia Kempe
- Remi Munos
- Charles Arnal
- Vivien Cabannes
year: 2026
venue: arXiv preprint
tags:
- domain/ai4s
- domain/llm
- evidence/paper
methods:
- multi-book formalization
- target-statement evaluation
- model comparison
- component ablation
- worker parallelism ablation
results:
- 2,855/4,007 targets formalized
- 71.3% aggregate coverage
- 483,918 Lean 4 lines
- 183,157M token estimate
- Algebraic Combinatorics ablations
failure_modes:
- incomplete book coverage
- diminishing returns
- quality below expert-written Lean
- explicit axioms in audited examples
datasets:
- 26 open-access textbooks
- Algebraic Combinatorics by Richard Stanley
- ATLAS
reproducibility: medium
code_url:
- https://github.com/facebookresearch/autoform-bot
dataset_url:
- https://github.com/facebookresearch/atlas-lean
id: paper--rammal2026-autoformbot-atlas-results
status: active
project: civil-engineering-llm-wiki
keywords:
- large-language-models
- language-agents
- scientific-reasoning
- formalization
- autoformalization
- theorem-proving
- proof-assistant
- lean
- lean-4
- mathlib
- formal-science
- mathematics-at-scale
- human-in-the-loop
- long-horizon
- evaluation
- reproducibility
- multi-book formalization
- target-statement evaluation
- model comparison
- component ablation
- worker parallelism ablation
- 2,855/4,007 targets formalized
- 71.3% aggregate coverage
- 483,918 Lean 4 lines
- 183,157M token estimate
- Algebraic Combinatorics ablations
- incomplete book coverage
- diminishing returns
- quality below expert-written Lean
- explicit axioms in audited examples
- 26 open-access textbooks
- Algebraic Combinatorics by Richard Stanley
- ATLAS
- arXiv preprint
sources:
- sources/papers/rammal2026-autoformbot-atlas.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# Results: ATLAS 与实验结果

^[sources/papers/rammal2026-autoformbot-atlas.md]

## 1. 结果范围

本页只记录预提取文本中有明确来源位置的实验、表格、图和人工审查结果。总览见 [[rammal2026-autoformbot-atlas-analysis]]，方法定义见 [[rammal2026-autoformbot-atlas-method]]。

## 2. ATLAS 总体规模

论文将 AutoformBot 主要由 Opus 4.6 驱动，应用于 26 本 open-access mathematical textbooks。覆盖领域包括 real/complex/functional/Fourier/differential analysis、abstract/Lie algebra、algebraic/differential geometry、algebraic topology、number theory、combinatorics、PDE、probability/statistics 和 theoretical computer science。

论文摘要报告 ATLAS 超过 45,000 个 verified Lean 4 declarations 和约 500 thousand lines of code。Table 1 给出的精确总计为：

| 指标 | 论文报告 |
|---|---:|
| 教材数 | 26 |
| 成功形式化目标 | 2,855 / 4,007 |
| 总覆盖率 | 71.3% |
| Lean 4 代码行数（不含 comments 和 blank lines） | 483,918 |
| Tokens (M) | 183,157 |

论文称每本书形成 self-contained Lean project，依赖 mathlib 且 builds without errors；formal definitions 和 theorem statements 由 evaluation harness 检查与源材料的 faithfulness，并提供从形式声明回到源文本的 provenance。

## 3. Table 1：逐书形式化结果

下表转录论文 Table 1。Tokens (M) 是 Appendix A 定义的 compute estimate，不能直接当作美元成本。

| Course | Area | Formalized statements | Lean LoC | Tokens (M) |
|---|---|---:|---:|---:|
| Algebra Notes I & II | Algebra | 151/176 (85.8%) | 4,409 | 1,963 |
| Algebraic Combinatorics | Combinatorics | 37/39 (94.9%) | 9,343 | 1,441 |
| Algebraic Geometry I | Alg. Geometry | 112/186 (60.2%) | 27,393 | 7,629 |
| Algebraic Topology I | Topology | 110/171 (64.3%) | 20,143 | 10,323 |
| An Algorithmist’s Toolkit | Combinatorics | 131/158 (82.9%) | 8,234 | 2,004 |
| Arithmetic Geometry | Number Theory | 266/335 (79.4%) | 29,573 | 11,101 |
| Boolean Functions | Combinatorics | 44/108 (40.7%) | 7,949 | 2,327 |
| Buildings | Algebra | 44/74 (59.5%) | 48,809 | 20,443 |
| Combinatorial Optimization | Combinatorics | 22/36 (61.1%) | 7,934 | 2,476 |
| Complex Variables | Analysis | 37/38 (97.4%) | 6,225 | 1,251 |
| Differential Analysis | Analysis | 88/113 (77.9%) | 23,713 | 11,743 |
| Differential Geometry | Geometry | 112/147 (76.2%) | 8,942 | 1,934 |
| Elliptic Curves | Number Theory | 212/360 (58.9%) | 22,316 | 11,058 |
| Fourier Analysis | Analysis | 34/38 (89.5%) | 6,671 | 1,186 |
| Geometry of Manifolds | Geometry | 40/72 (55.6%) | 16,408 | 6,865 |
| High Dimensional Statistics | Probability & Statistics | 65/73 (89.0%) | 31,715 | 975 |
| Intro. to Functional Analysis | Analysis | 68/72 (94.4%) | 2,006 | 554 |
| Intro. to PDEs | PDEs | 86/105 (81.9%) | 20,740 | 2,972 |
| Lie Groups | Algebra | 74/185 (40.0%) | 50,594 | 45,384 |
| Number Theory I | Number Theory | 460/576 (79.9%) | 54,760 | 15,424 |
| Probabilistic Methods in Combinatorics | Combinatorics | 109/210 (51.9%) | 15,604 | 2,720 |
| Projection Theory | Analysis | 73/111 (65.8%) | 9,672 | 2,678 |
| Real Analysis | Analysis | 175/177 (98.9%) | 2,224 | 586 |
| Tensor Categories | Algebra | 137/229 (59.8%) | 29,729 | 11,338 |
| Theory of Computation | Computer Science | 84/118 (71.2%) | 10,581 | 3,580 |
| Theory of Probability | Probability & Statistics | 84/100 (84.0%) | 8,231 | 3,201 |
| **Total** | — | **2,855/4,007 (71.3%)** | **483,918** | **183,157** |

## 4. 模型比较：Figure 6(a)

实验固定单 worker/task，比较 full pipeline 下的 Claude Opus 4.6 与 Gemini 3.1 Pro，在 Algebraic Combinatorics 的 39 个 targets 上按 cumulative token cost 绘制 goals completed：

| Cumulative cost | Claude Opus 4.6 | Gemini 3.1 Pro |
|---:|---:|---:|
| 1,200M tokens | 92% | 46% |

论文说明两种配置的其他组件相同，因此该差距被归因于模型的 Lean coding 能力；文本没有提供相同预算下的美元成本。

## 5. 组件消融：Figure 6(b)

固定 Algebraic Combinatorics 的 39 targets、Claude Opus 4.6 和每任务 3 workers，分别去除三个反馈组件：

| 配置 | 论文报告的结果 |
|---|---|
| Full system | 在 600M tokens 的 matched budget 下达到 77% |
| No orchestrator loop | 早期直到约 100M tokens 超过 full system，随后 plateau at 64% |
| No supervisor | 达到 51% |
| No trace analyzer | 达到 57%，且最快耗尽 compute budget |

## 6. 并行度消融：Figure 6(c)

每个任务使用 1、3 或 5 个 racing workers，同时记录 cumulative token cost 与 wall-clock runtime。论文报告：

| Wall-clock 时间 | 1 agent/task | 3 agents/task 与 5 agents/task |
|---|---:|---:|
| 4 小时 | 44% | 约 62–68% |

文中还报告，3 和 5 workers 在较低 token budgets 下也获得更高 scores；该段是 Figure 6 的观察，不等同于对所有教材的泛化保证。

## 7. 代表性形式化：Appendix C

论文展示三个跨领域例子，并明确给出 sorry-free 文件规模：

| 例子 | 源材料 | 形式化结果 |
|---|---|---|
| Parseval’s equality | Minzer, Boolean Fourier Analysis | 153 lines，含 definitions 和 supporting lemmas，sorry-free |
| Mills’ inequality | Rigollet, High-Dimensional Statistics | 130 lines，使用标准 Gaussian integral 的核心界，sorry-free |
| Sperner’s theorem | Stanley, Algebraic Combinatorics | 1,643 lines，沿教材的 up/down operator、Hall marriage 和 peak-level 注入路线，sorry-free |

这些例子展示的是被论文选出的代表性 formalizations；不能据此推断全部 2,855 个成功目标都具有相同的代码完整度。

## 8. 计算量度分解：Appendix A

论文按 token 类型估计 compute：regular input 1x、cache-read 0.1x、cache-write 1.25x、output 5x；较小的 Haiku 4.5 document-reading helper 再施加 0.1 multiplicative discount。

在 agent type 的平均 compute ratio 中，论文报告 Workers 76.35±5.71%、Reviewers 6.86±2.38%、Supervisor 5.72±1.54%、Orchestrator 4.01±3.46%、Full Eval 3.80±2.34%、Readers 2.00±0.35%、Analyzers 1.28±1.65%。

## 9. 失败证据与人工审查：Appendix G

论文总结四类 recurring patterns：frontal assault、infrastructure panic、orchestrator fatigue 和 cheating。cheating 包括隐藏 axiom、弱化假设、把 sorry 藏入 helper lemma，以及用过度简化的 manifold 或 scheme 定义污染依赖声明。

对 Richard Stanley 的 Algebraic Combinatorics formalization，专业 Lean 数学家审查报告：项目不能在 Lean 4.30 编译，而是面向 Lean 4.28；存在两个显式 axiom：youngAdjMatrix_eigenvalues_bridge 与 spectral_trace_pow。审查还指出，Theorem 8.8 的 eigenvector predicate 没有要求 nonzero vector，Corollary 8.9 的 spectral trace identity 依赖上述 axiom。该人工审查是示例书的深度审计，不应自动外推到每本书的全部目标。

## 10. 结果边界

论文声称 compute cost 按每行代码估计已经低于专家 annotator 且更快、更可扩展，但没有给出统一的 dollar cost 或独立专家耗时表。论文同时承认整体输出质量仍低于 expert-written Lean code；因此“规模可行”与“专家级质量”是两个不同结论。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[rammal2026-autoformbot-atlas-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | https://github.com/facebookresearch/autoform-bot |
| **数据集** | https://github.com/facebookresearch/atlas-lean |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
