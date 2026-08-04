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
id: paper--wu2022-llm-autoformalization-analysis
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
# Autoformalization with Large Language Models — 分析

^[sources/papers/wu2022-llm-autoformalization.md]

本文研究如何用未经该任务专门训练的大语言模型，把自然语言数学题转写成 Isabelle/HOL 形式定理，并把其中可用的形式化结果转化为神经定理证明器的训练数据。方法展开见 [[wu2022-llm-autoformalization-method]]，数值与表格证据见 [[wu2022-llm-autoformalization-results]]，边界分析见 [[wu2022-llm-autoformalization-critical]]；唯一新增的算法实体是 [[entities/wu-llm-autoformalization]]。

## 1. 工程背景

> **⚙️ 非线性类型：** 不涉及物理非线性。** 本文处理的是自然语言数学与 Isabelle/HOL 形式语言之间的转换，以及形式定理证明搜索；没有 PDE、材料本构或动力学响应模型，因此不能把模型的非凸优化、语言生成或搜索复杂性归入物理非线性。它与 [[oropeza-navarro2024-microplane-damage-analysis]] 中的材料/本构非线性、[[lian2011-mpm-fem-coupling-analysis]] 中的计算力学耦合问题属于不同问题族。

形式化数学可以由交互式定理证明器自动检查，为复杂证明和安全关键软件提供接近机器可检验的正确性保证；但人工形式化通常需要多年专家工作（PDF pp. 2–3）。

论文指出，形式数学语料很稀缺：Archive of Formal Proofs 约 180 MB，不到 Codex 训练数据的 0.18%；自然语言与形式数学之间几乎没有对齐数据（PDF p. 1）。这使得把 LLM 在代码生成和少样本翻译中的能力迁移到数学自动形式化成为一个工程上重要、但不显然可行的方向。

## 2. Research Gap

以往 LLM 在 Python 等网上有大量语料的形式语言上表现较好，但形式数学缺少相同规模的公开语料。已有自动形式化工作可以采用监督翻译或由 Mizar 生成的合成、类自然语言数据；本文要检验的是自监督语言模型 PaLM/Codex 在没有为该任务专门训练时能否直接完成转写（PDF pp. 1, 3）。

论文还把数据稀缺问题与神经定理证明连接起来：定理证明器需要可搜索、可验证的形式命题，而人工准备这些命题的成本很高。此前 expert iteration 需要人类手工形式化一批问题；本文尝试用 LLM 先启动这条自我改进循环（PDF p. 7）。

## 3. 科学问题

核心问题有两层：

1. 给定少量自然语言—Isabelle 示例，LLM 能否把数学竞赛题的语义、隐含假设、函数类型和 Isabelle 库定义对齐，而不仅仅是生成语法上像代码的字符串？
2. 这些自动形式化的命题能否通过 Isabelle 定理证明器的反馈筛选为可靠训练样本，并提高神经定理证明器在 MiniF2F 上的证明成功率？

论文另以少量高等数学语句考察反方向的 informalization，即把 Isabelle 语句生成回自然语言，以判断 back-translation 是否可能形成额外的数据闭环（PDF pp. 8–9）。

## 4. 研究目标

- 用两个 few-shot 案例观察 LLM 的结构理解、规模效应和示例敏感性。
- 在 MiniF2F 中有人工 Isabelle 形式化的 140 道 algebra 与 120 道 number theory 题上，用 BLEU 比较 PaLM 不同规模模型与 Codex（PDF pp. 4–6）。
- 对 MATH 中随机抽取的 150 道题人工检查 Codex 输出，区分定义/概念对齐、假设遗漏、类型错误等失败模式。
- 用 Codex 形式化 MATH 训练集中的 3,908 道题，启动两轮 expert iteration，并在 MiniF2F valid/test 上评估 Thor 神经定理证明器。
- 用 38 个 Isabelle 高等数学语句测试反向 informalization；这里的正确性标准比形式化更宽松，允许人类补足显然上下文（PDF p. 9）。

## 5. 方法机制概览

自然语言题被视为英文到 Isabelle 代码的机器翻译任务。提示词先给出少量示例，再要求模型输出 theorem、变量类型、假设和结论；所有实验采用 greedy decoding，temperature 为 0、p=1（PDF p. 4）。

case study 使用从 MiniF2F 随机选取的两个形式化示例，且没有 prompt engineering 或 prompt tuning。BLEU 对比则按 algebra 与 number_theory 各提供 10 个随机示例，剩余 130/110 题用于评估（PDF pp. 4–6）。

第二阶段把自动形式化与 expert iteration 连接起来：以 Thor 的基础模型 M₀ 为起点，在自动形式化命题集合上做 best-first proof search，收集成功证明 Sᵢ；将历轮成功命题与 PISA 中的形式数学问题去重后合并，用于恰好一个 epoch 的微调得到 Mᵢ（PDF pp. 7–8）。

Thor 在 proof state 和上一步 proof step 条件下预测下一 token；遇到特殊的 <hammer> token 时，在 Isabelle 中调用 Sledgehammer，超时为 30 秒。其训练基础是 PISA 的 249 万个 Isabelle/HOL 证明步骤（PDF p. 7）。

## 6. 结果证据

- 150 道 MATH 题中有 38 道被人工判为 perfect translation，成功率 25.3%（PDF pp. 6–7）。
- BLEU 随 PaLM 从 8B 扩展到 64B、540B 而上升；Codex 在两个科目上高于 PaLM 表中各规模（Table 1, PDF p. 6）。
- Codex 形式化的 3,908 道 MATH 训练题中，3,363 道语法正确；M₀ 第一轮找到 782 个成功证明，第二轮找到 1,011 个（PDF p. 8）。
- MiniF2F test 成功率从基础模型 M₀ 的 29.9% 提升到 M₁ 的 34.0%，再到 M₂ 的 35.2%；valid 为 28.3% → 36.1% → 37.3%（Table 3, PDF p. 8）。
- 38 个 Isabelle 高等数学语句中，36 个生成了 reasonably coherent 的自然语言，其中 29 个被判为 more-or-less correct，即 76%（PDF p. 9）。

完整表格、案例与资源用量见 [[wu2022-llm-autoformalization-results]]；上述数字不外推到未评估的数学领域。

## 7. 贡献

1. 证明了 LLM 在低对齐数据条件下仍能对一部分数学竞赛命题进行可用的 Isabelle 自动形式化；论文报告的人工 perfect rate 为 25.3%。
2. 通过案例和 BLEU 对比显示，模型规模与 few-shot 示例的相关性不仅体现在表面翻译，还体现在概念/类型的形式化方式上。
3. 提出用自动形式化命题启动 expert iteration，并以形式证明器验证成功样本，最终在 MiniF2F 上取得论文所称的新 state-of-the-art proof rate。
4. 用 informalization 结果展示 back-translation 可能是比单向 formalization 更宽松、也更容易获得有效数据的方向。

## 8. 核心知识点

- **语法正确不等于语义正确。** 3,363 个输出语法正确，但论文另外用人工检查识别定义、假设和函数应用错误；不能把 parser acceptance 当作 formalization correctness。
- **主要瓶颈是概念对齐。** 150 题人工检查中，定义/概念未对齐是反复出现的失败类别，例如 “greatest possible value” 没有对齐 Isabelle 的 Greatest/Max，“factorial” 没有对齐 fact。
- **示例传递的是表示方式。** 一个只解释如何形式化直线的额外示例，就帮助 Codex 理解 “linear function” 的 Isabelle 表达，说明少样本示例可以补足库概念缺口（PDF pp. 5, 22）。
- **形式验证器可以把生成数据变成训练信号。** expert iteration 不直接信任全部生成命题，而是只把 proof search 找到的成功证明并入训练集，并按问题陈述去重。
- **反向生成的评价标准必须单独定义。** informalization 允许人类补显然上下文，因此 76% 不能与 25.3% 的严格 formalization 标准直接横比。

## 9. Negative Knowledge

- 本文自动形式化的是 theorem statements，不是包含新定义、完整依赖和证明的整个大型理论；作者明确指出，完整理论需要把更大的上下文保留在当前窗口中，现有 LLM 的上下文长度构成限制（PDF pp. 8, 10）。
- 竞赛题设置利用了 Isabelle 库已有背景定义，不能据此宣称 LLM 已经能在数学“野外”稳定形式化任意新领域。
- case study 只使用两个随机示例、greedy decoding，且没有 prompt engineering/tuning；结果不能解释为经过系统提示优化后的上限。
- 150 题失败分析来自 MATH 的 algebra、number_theory、intermediate_algebra 各 50 题；表 2 的类别计数按论文原表列示，但论文文本没有说明这些类别计数是否互斥，因此不能擅自把列和当作 50 的互斥分区。
- 先进数学 formalization 的 Brouwer fixed-point 示例仍缺少 “f maps S to itself” 等关键假设；这是模型把自然语言上下文压缩成形式假设时的明确失效边界（PDF p. 30）。
- 作者没有访问 Codex 训练集；通过网页检索没有找到案例 formalization 只支持“未发现匹配”，不能构成严格的非记忆化证明（PDF p. 6）。
- 论文依赖 PaLM/Codex 等模型及大规模计算，文中没有给出本论文代码仓库或数据下载 URL；3,920 TPU hours 的资源量也使端到端复现实验门槛很高（PDF p. 8）。

## 10. 可迁移知识

- 在缺少平行语料时，可用少量高质量跨表示示例指定转换任务，再用目标系统的 checker 过滤结果。
- 把“生成—验证—收集成功轨迹—微调”的闭环用于形式推理，比把未验证的模型输出直接当标签更稳健；关键是保留问题陈述级去重和验证 provenance。
- 提示示例应覆盖目标库中的概念表达，而不只是与目标题表面相似；这为形式化、程序合成和科学符号转换提供通用提示设计原则。
- 正向与反向翻译可以互相提供对齐数据，但两者必须采用不同的正确性标准，并明确哪些上下文由人工补全。
- 规模效应是必要但不充分的信号；错误类型显示，扩大模型不能替代形式库检索、类型检查和假设补全。

## 11. 研究机会

- 用长上下文、检索增强或分层理论表示解决定义和依赖无法同时放入窗口的问题。
- 将 Isabelle checker、类型错误和缺失假设反馈纳入训练目标，区分语法修复、语义对齐和证明搜索三个阶段。
- 研究 cycle-consistency/back-translation 是否能在不引入错误的前提下扩大自然语言—形式语言对齐数据。
- 建立跨 Isabelle、Lean、HOL Light 等证明器的迁移评测，并报告证明器库覆盖差异，而不是只报告单一 BLEU。
- 设计可审计的数据污染测试、重复运行和置信区间，验证 25.3% 与 35.2% 是否对提示、采样和模型版本稳定。
- 在较低计算预算下蒸馏 expert iteration 的成功轨迹，并公开模型、提示、失败标签和可运行 checker。

## 12. 可复现性

**🟡 medium 中等可复现性** —— 方法、提示示例、模型规模、Thor 架构与训练超参数、proof-search 规则、数据数量和硬件开销均有相当细节，但 PaLM/Codex 依赖与本论文实现/生成语料没有公开 URL，因此不能保证逐项重现原始数字。

| 项目 | 证据与复现要点 |
|---|---|
| **等级** | medium；有经验的形式化/机器学习研究者可以重建主要流程，但不能无条件获得原始 PaLM/Codex 输出。 |
| **官方代码** | 论文文本未提供本论文代码仓库；code_url: []。文中只说明 PISA 的抽取与交互代码在 BSD 许可下，未给出本论文专属 URL。 |
| **数据集** | MATH、MiniF2F、PISA 与 Archive of Formal Proofs 被明确命名；本文生成的 3,908 条自动形式化结果及其成功证明未提供下载 URL，dataset_url: []。 |
| **关键依赖** | PaLM/Codex 的具体权重或服务版本、Isabelle/Sledgehammer、Thor/PISA、提示示例、随机抽样、greedy decoding 与 30 秒 Sledgehammer timeout。 |
| **复现风险** | 私有/不可得模型、未公开生成语料、没有随机种子与重复试验报告，以及 3,920 TPU hours 的高资源门槛会阻碍精确重现。 |

方法、证据和批判边界分别见 [[wu2022-llm-autoformalization-method]]、[[wu2022-llm-autoformalization-results]]、[[wu2022-llm-autoformalization-critical]]。
