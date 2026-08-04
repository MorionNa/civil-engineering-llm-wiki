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
id: paper--wu2022-llm-autoformalization-method
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
# Autoformalization with Large Language Models — 方法

^[sources/papers/wu2022-llm-autoformalization.md]

本页只展开论文的方法机制；总体论点见 [[wu2022-llm-autoformalization-analysis]]，实验数字见 [[wu2022-llm-autoformalization-results]]，算法实体见 [[entities/wu-llm-autoformalization]]。

## 1. 任务定义与输出对象

论文把 autoformalization 定义为把自然语言数学翻译为形式规格与证明的过程，但本研究的主要实验对象是 theorem statements。输入是英文数学题，输出是 Isabelle/HOL 中可由 theorem prover 处理的形式命题；模型需要同时给出变量类型、assumes 和 shows，而不是只翻译数学名词（PDF pp. 1, 3–4）。

竞赛题经常以“求答案”的问句出现，而形式语言需要 proposition。论文的预处理做法是把最终答案拼接到题目末尾，形成 “The final answer is $Answer.”，再要求模型把完整自然语言版本翻成 Isabelle 版本（PDF p. 4）。

这种处理把问题分成两个隐含子任务：把叙述压缩成可验证命题，以及把自然语言概念映射到 Isabelle 现有库中的类型、函数和谓词。论文没有把完整证明作为 LLM 直接输出目标。

## 2. Few-shot 提示机制

case study 使用固定格式：

Natural language version: $Natural_Language_Statement.

Translate the natural language version to an Isabelle version:

随后给出两个 Isabelle theorem 示例。两个示例都来自 MiniF2F，作为跨语言格式示范；论文明确说明构造 prompt 时没有额外 prompt engineering 或 prompt tuning，并随机选择这两个示例（PDF p. 4）。

两个示例覆盖复数求和/乘积和对数方程，主要展示从 LaTeX/英文叙述到 Isabelle 变量、假设和结论的表面及结构对应。它们不是完整自然语言证明，因此模型主要需要补足表述和形式库对齐，而非生成一条人类证明过程。

在 BLEU 对比中，论文按 subject 改用更多相关示例：algebra 与 number_theory 各随机采样 10 道题构造 few-shot prompt，剩余 algebra 130 题、number_theory 110 题作为评估集（PDF p. 6）。

## 3. 模型、解码与尺度

使用的模型包括 PaLM 8B、64B、540B，以及 Codex。所有实验采用标准 greedy decoding，即 temperature=0、p=1；论文没有报告随机采样、多次候选或后处理投票（PDF p. 4）。

case study 2 用同一自然语言题比较 PaLM 不同规模：8B 与 64B 无法给出正确形式化，540B 可以；这被作者用来说明 scale 对该任务的重要性（PDF pp. 5, 21）。

case study 3 展示了 few-shot 的机制边界。Codex 看见 “linear function” 时假定 Isabelle 已存在名为 linear 的概念并输出 linear f，导致错误；当 prompt 额外加入一个解释如何形式化直线的示例后，Codex 能把线性函数写成 f x = a * x + b 的形式（PDF pp. 5, 22）。

## 4. 自动形式化的评估协议

论文使用三种互补信号：

1. **案例研究：** 观察输出是否为正确 Isabelle theorem，并对失败给出具体解释。
2. **BLEU：** 对 140 道 algebra 和 120 道 number_theory 题，将模型输出与人工 Isabelle formalization 比较。它衡量字符串/片段相似度，不能独立保证语义等价。
3. **人工失败分析：** 从 MATH 随机抽取 algebra、number_theory、intermediate_algebra 各 50 题，共 150 题，由人工按 incomplete prompt、定义/概念不对齐、假设缺失、语法/类型错误等类别检查（PDF pp. 6–7）。

论文把“perfect translation”作为人工判断的严格结果，而不是把语法可解析当作完美。相应的失败类别详见 [[wu2022-llm-autoformalization-results]]。

## 5. Expert iteration 闭环

论文将自动形式化作为 neural theorem proving 的数据启动器。设基础神经定理证明器为 M₀，自动形式化命题集合为 A。第 i 轮使用 Mᵢ₋₁ 对 A 做 best-first proof search，收集被证明器找到的成功证明 Sᵢ。

成功命题与 PISA/已有形式数学问题合并，且把历轮成功证明的命题按 problem statement 去重；得到的训练集合用于把基础模型 M₀ 微调恰好一个 epoch，生成下一轮模型 Mᵢ。论文采用过去所有轮次成功证明的并集，而不是只保留最近一轮（PDF p. 7）。

这一设计把 LLM 输出分成两个层次：

- LLM 负责从自然语言生成候选形式命题；
- Isabelle proof checker 与 best-first search 负责筛选能产生成功 proof trajectory 的命题。

因此，expert iteration 不是对所有自动形式化输出做无条件监督，而是用可验证成功证明作为训练数据过滤器。

## 6. Thor 证明器与 Sledgehammer 接口

基础模型是 Thor，一个针对 Isabelle 的神经定理证明器。Thor 在 PISA 数据集上微调；PISA 包含 Isabelle/HOL 库与 Archive of Formal Proofs 中共 2.49 million proof steps。给定 proof state 和上一个 proof step，语言模型预测下一个 proof token（PDF p. 7）。

当 ground-truth proof step 含有 metis、meson 或 smt 关键词时，训练目标使用特殊 token <hammer>。评估时若生成该 token，Thor 调用 Isabelle 的 Sledgehammer，并设置 30 秒 timeout。这使语言模型可以把部分搜索交给自动化证明方法。

## 7. Thor 的公开实验配置

论文报告的 Thor 语言模型是 GPT-2 风格 decoder-only Transformer：

| 配置 | 论文报告值 |
|---|---|
| 非 embedding 参数 | 700M |
| 层数/attention heads | 24 / 24 |
| hidden dimension | 1536 |
| vocabulary size | 50,400 |
| optimizer | AdamW |
| 预训练数据 | The Pile 的 GitHub + arXiv 子集 |
| 预训练步数/上下文 | 200,000 steps / 2,048 tokens |

预训练学习率先在 3,000 steps 内从 0 线性升到 2×10⁻⁴，再使用 cosine scheduler，最终学习率为 1.2×10⁻⁵；global batch size 为 32 sequences，即 65,536 tokens。微调使用 10,000 warmup steps、90,000 annealing steps、最高学习率 3×10⁻⁴、最终学习率 3×10⁻⁵，global batch size 为 144 sequences，即 294,912 tokens；evaluation loss 在 13,000 steps 后达到最小，使用该 checkpoint（PDF pp. 7–8）。

## 8. 自动形式化数据的生成

应用实验中，Codex 用与 failure study 相同的 few-shot prompts，对 MATH training set 中 algebra、intermediate algebra、number theory 三类共 3,908 道题进行 greedy formalization。论文报告其中 3,363 条语法正确，随后才把它们送入 expert iteration 的 proof search（PDF p. 8）。

论文文本没有给出自动生成结果文件、逐题 prompt/output 清单或可下载的成功 proof 集合。因此，方法流程可以据文中配置重建，但 exact candidate pool 与每一轮搜索轨迹无法从提供文本直接取得。

## 9. Informalization 方法

反向任务把 Isabelle formal statement 翻译为自然语言。作者从 Isabelle expert 选取 38 个 theorem、lemma 和 definition，使用 Codex 自动生成 informal mathematics，结果放在 Appendix A.3 与 D.2。

该方向的评价标准有意更宽松：如果人类读者能够从上下文补足显然背景或纠正小错误，就可以视为 acceptable；但遗漏 identical-distribution 等关键假设会被视为 major error。这个标准与形式化要求的精确类型和假设闭合不同（PDF p. 9）。

## 10. 设计理由与依赖链

- **few-shot：** 解决自然语言—形式数学平行数据几乎为空的问题。
- **Isabelle library：** 让竞赛题尽量复用已有背景定义，避免每题先引入新理论。
- **greedy decoding：** 固定候选生成协议，便于比较规模与模型；同时没有探索采样策略的潜在收益。
- **checker-filtered expert iteration：** 将形式命题生成和 proof search 连接起来，把可验证成功轨迹转成训练数据。
- **back-translation：** 从形式库反向产生自然语言，探索扩大对齐语料的可能性。

整个实现依赖 Isabelle/HOL、Sledgehammer、Thor/PISA、MATH、MiniF2F 以及 PaLM/Codex 访问条件；论文未给出本论文代码 URL，相关可复现边界见 [[wu2022-llm-autoformalization-analysis]] 的第 12 维。

## 11. 方法边界

该方法最适合已有形式库覆盖背景定义、输出主要是 theorem statement 的小规模问题。进入大型理论时，模型不仅要翻译命题，还要维护新增定义、依赖、隐含上下文和长序列；作者明确指出当前上下文窗口难以容纳整个大型理论（PDF pp. 8, 10）。

另一个边界是，proof search 只会验证搜索到的成功证明；它不能自动证明所有语法正确的候选命题语义正确。定义缺失、类型转换、函数前缀调用和量词范围错误仍需库级反馈或人工检查。

对应的贡献、失败边界和可迁移知识见 [[wu2022-llm-autoformalization-critical]]；论文提出的具体算法实体见 [[entities/wu-llm-autoformalization]]。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[wu2022-llm-autoformalization-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | 无公开代码 |
| **数据集** | 无外部数据集 URL（或使用论文内/合成数据） |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
