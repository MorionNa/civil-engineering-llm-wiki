---
type: entity
title: LLM autoformalization pipeline
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
- entity/model
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
id: entity--wu-llm-autoformalization
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
- data-contamination
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
# Algorithm entity: LLM autoformalization pipeline

^[sources/papers/wu2022-llm-autoformalization.md]

## 1. 定义

这是 Wu、Jiang、Li、Rabe、Staats、Jamnik 和 Szegedy 在 2022 年论文中提出并实验验证的一条 LLM autoformalization pipeline：用少量自然语言数学—Isabelle/HOL 示例提示 PaLM/Codex，把数学竞赛题转成形式 theorem statement，再用 Isabelle 定理证明搜索筛选成功轨迹，并通过 expert iteration 训练神经定理证明器。

该实体特指论文中的“自然语言 → Isabelle/HOL → proof-search feedback → neural prover”方法链，不是泛化的 LLM 占位实体，也不等同于某一个基础模型或某一个证明器。

## 2. 机制

1. 把题目最终答案附加到自然语言陈述，使求值题成为待证明 proposition。
2. 在 prompt 中提供少量 Isabelle formalization 示例；case study 使用两个随机示例，BLEU 对比按 algebra 与 number_theory 各用 10 个示例。
3. 使用 PaLM 8B/64B/540B 或 Codex，以 greedy decoding（temperature 0、p=1）生成 theorem、变量类型、assumes 和 shows。
4. 将候选命题交给 Isabelle/Thor 做 best-first proof search，收集成功 proof。
5. 将历轮成功证明与 PISA 形式数学数据合并，按 problem statement 去重，微调基础模型一个 epoch，形成下一轮 expert iteration。
6. 另可把 Isabelle 语句反向生成自然语言，探索 back-translation 数据闭环。

方法页的完整机制说明见 [[wu2022-llm-autoformalization-method]]；总体分析见 [[wu2022-llm-autoformalization-analysis]]。

## 3. 论文证据

- 150 道 MATH 题中 38 道被人工判为 perfect translation，论文给出 25.3%。
- Codex 在 3,908 道 MATH training problems 上生成 3,363 个语法正确候选。
- Thor 基础模型第一轮从这些候选中找到 782 个成功证明，第二轮找到 1,011 个。
- MiniF2F test proof success rate 从 M₀ 的 29.9% 提升至 M₁ 的 34.0%，再至 M₂ 的 35.2%。
- 38 个 advanced Isabelle statements 的 informalization 中，36 个 reasonably coherent，29 个 more-or-less correct（76%）。

逐项表格、案例和页码锚点见 [[wu2022-llm-autoformalization-results]]。

## 4. 适用范围

该方法在论文中主要用于数学竞赛 theorem statements，且依赖 Isabelle 库已有的背景定义。它可以把低对齐数据问题转成 few-shot translation 与 checker-filtered data generation，但论文没有证明它能自动形式化包含大量新定义和依赖的完整理论。

## 5. 失败边界

- 不能稳定把自然语言概念对齐到 Isabelle 库定义，例如 Greatest/Max、factorial/fact 或线性函数。
- 可能遗漏隐含假设、量词范围、函数定义域和值域，或把自然语言中的分母和结论写错。
- 可能产生 Isabelle syntax/type error、错误函数应用、变量类型推断错误和运算优先级错误。
- 形式语法正确不等于自然语言语义正确；proof search 成功也只验证被搜索到的候选，不自动验证所有生成文本。
- 大型理论受上下文窗口、私有 PaLM/Codex 访问和 3,920 TPU hours 资源开销限制。

## 6. 复现状态

论文给出了 prompt 形式、greedy decoding、Thor 架构与部分训练超参数、数据数量和硬件资源，但没有提供本论文代码仓库、逐题生成语料或成功证明下载 URL；因此实体复现等级为 medium，而非 high。

关联的结果与边界分析见 [[wu2022-llm-autoformalization-results]] 和 [[wu2022-llm-autoformalization-critical]]。
