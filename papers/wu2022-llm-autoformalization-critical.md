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
id: paper--wu2022-llm-autoformalization-critical
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
# Autoformalization with Large Language Models — 批判性分析

^[sources/papers/wu2022-llm-autoformalization.md]

本页把论文的贡献、核心知识、失败边界、可迁移知识和研究机会分开讨论；方法细节见 [[wu2022-llm-autoformalization-method]]，原始数字见 [[wu2022-llm-autoformalization-results]]，总体 12 维概览见 [[wu2022-llm-autoformalization-analysis]]。

## 1. 贡献

### 1.1 把低对齐数据问题变成可测量的 LLM 任务

论文在自然语言数学与 Isabelle/HOL 几乎没有对齐语料的前提下，使用 PaLM/Codex 的 in-context learning 直接生成形式 theorem statements。150 道随机 MATH 题中 38 道被人工判为 perfect，给出了 25.3% 这一可复查的起点，而不是只展示单个成功案例（PDF pp. 1, 6–7）。

### 1.2 把规模与示例敏感性具体化

BLEU 表显示 PaLM 从 8B、64B 到 540B 在 algebra 和 number_theory 上逐级上升；linear function 案例则显示，一个解释线性函数表示方式的额外示例足以改变 Codex 的形式化行为（Table 1, Figure 3, Appendix B.3）。

这两类证据分别说明容量和表示示例都重要，但不等价于“只要扩大模型就能解决定义对齐”。失败分类仍显示 Greatest/Max、factorial、函数调用和缺失假设是主要障碍。

### 1.3 形成生成—验证—学习闭环

论文最有工程价值的结构是把 LLM 作为候选命题生成器，把 Isabelle proof search 作为可验证过滤器，再把成功证明用于 expert iteration。两轮循环后，Thor 在 MiniF2F test 上达到 35.2%，高于基础模型 M₀ 的 29.9%（Table 3, PDF p. 8）。

这把自动形式化从“翻译演示”推进到“为证明器制造训练数据”的系统作用，但提升来自整个闭环，不应只归因于自然语言转写的 BLEU。

### 1.4 提出反方向数据扩展

38 个高等数学形式语句的 informalization 中，29 个按宽松人工标准被判为 more-or-less correct（76%）。论文据此提出 back-translation 可能比严格 formalization 更容易产出对齐文本，并能为后续循环提供数据（PDF pp. 8–10）。

## 2. 核心知识

### 2.1 正确性是分层的

该工作至少包含四个不同层级：

1. 文本能否被模型生成；
2. Isabelle 语法和类型能否接受；
3. 自然语言含义是否完整映射为 assumptions/conclusion；
4. 定理证明器能否找到成功 proof。

论文的 3,363 条语法正确候选、150 题人工 perfect 分类和 proof search 成功数分别对应不同层级。把它们合并成一个“准确率”会掩盖定义对齐和假设遗漏问题。

### 2.2 表示示例比表面相似更重要

linear function 案例没有直接给出 “linear function” 的形式库定义；只增加一个“如何形式化直线”的切题示例，Codex 就能输出 f x = a * x + b 的结构。由此可迁移的原则是：few-shot 示例应显式展示目标库的概念展开方式，而不只展示格式。

### 2.3 Checker 让生成数据具有可控 provenance

自动形式化的全体输出不能直接作为标签。本文先生成候选，再用 Isabelle proof search 取得成功证明，最后把成功命题与 PISA 数据合并、按 problem statement 去重。这种 provenance 链条是闭环可靠性的关键。

### 2.4 反向任务不能复用同一评价标准

formalization 要求隐含上下文、类型、量词和库定义精确闭合；informalization 则允许人类补足显然上下文。76% informalization 结果有启发性，但不能和 25.3% strict perfect formalization 直接比较为同一种 accuracy。

## 3. 失败边界

### 3.1 概念和库定义对齐

人工分析中，Fail to align definitions or concepts 是高频类别。论文举例说明模型不能稳定把 greatest possible value 对齐到 Isabelle 的 Greatest/Max，把 factorial 对齐到 fact；进入专业数学后，同一对象可能有不同上下文和形式表示，风险会增加。

### 3.2 隐含假设和量词范围

先进数学 Brouwer fixed-point 案例缺少 f(S) ⊆ S 的映射假设。MATH 失败案例还漏掉速度问题中的 (x+6) 分母、把结论写成不正确的变量等。这表明模型可能捕捉题面局部结构，却没有把全部自然语言约束闭合地放入 theorem。

### 3.3 Isabelle 类型、前缀和运算优先级

附录展示了 real/nat 区间、函数前缀应用、变量类型转换和 −(3²) 的括号等问题。它们不是简单拼写错误，而是自然语言数学约定与 Isabelle 具体语法/类型系统之间的接口失败。

### 3.4 缺失定义与长上下文

三类 150 题中出现 Missing definition in Isabelle；更大的理论还需要把新增定义、库依赖和上下文长期保存在 prompt 中。论文明确认为当前 LLM 上下文窗口限制了整个大型理论的自动形式化（PDF pp. 8, 10）。

### 3.5 结果验证和数据污染边界

论文对 3,363 个语法正确候选没有报告逐题语义正确率；proof search 找到成功证明也只说明搜索到的形式命题可证明，不说明所有生成命题都忠实于自然语言。

作者无法访问 Codex 训练集，只通过多种网页检索没有发现案例 formalization 的匹配项。该证据降低了明显记忆的疑虑，但不能严格排除预训练数据污染。

### 3.6 计算和依赖边界

端到端实验消耗 3,920 TPU hours，且使用 PaLM/Codex、Thor、Isabelle/Sledgehammer 等具体系统。论文没有提供本论文代码仓库、自动生成语料或成功 proof 集合 URL，因此 exact reproduction 受模型服务、版本、硬件和未公开中间数据限制。

## 4. 可迁移知识

### 4.1 面向符号系统的 LLM 工作流

对需要严格语义的任务，可以将 LLM 限定为候选生成器，把类型检查、解释器、定理证明器或单元测试作为外部裁判。核心不是让模型自称正确，而是让每个被学习的轨迹带有可查询的验证结果。

### 4.2 以库概念为中心设计 few-shot

示例选择应覆盖目标 formal library 中最容易错的定义、函数签名、类型转换和量词模式。对新领域，先建立“自然语言概念 → 形式库构造”的小型示例集，可能比单纯增加相似题数量更有效。

### 4.3 生成数据的去重和来源追踪

expert iteration 使用 problem statement 去重，并保留过去轮次成功证明的并集。迁移到代码、程序合成或科学公式翻译时，也应记录输入、候选、checker 版本、成功轨迹和训练轮次，避免相同样本的伪增益。

### 4.4 双向翻译的数据闭环

自然语言到形式语言和形式语言到自然语言可以互补：前者提供可验证规格，后者降低形式库的阅读门槛并可能生成弱对齐语料。但必须把“人类可读且可修正”与“形式等价”分成两套标注标准。

### 4.5 适用于科学语言代理的分阶段评估

该论文的分层正确性可以迁移到科学语言代理：分别报告语法/单位合法性、概念对齐、边界条件完整性、数值执行和最终科学结论，而不是用一项文本相似度替代整个证据链。

## 5. 研究机会

### 5.1 长理论的检索与分层上下文

将定义、定理、类型和依赖组织为可检索图，在生成当前命题时只注入相关上下文；再用 proof checker 验证检索遗漏，针对全文理论建立增量 formalization。

### 5.2 面向失败类别的训练反馈

把失败拆成 definition alignment、missing assumption、type error、function application 和 proof search failure，分别设计修复器或训练目标。单一语言损失无法区分这些错误。

### 5.3 更严格的污染与稳健性评测

公开 prompt、随机种子、逐题输出和检索审计；在不同 prompt、模型版本和证明器库版本下重复 25.3% perfect rate 与 35.2% proof rate，并报告区间而不是单一点估计。

### 5.4 跨证明器和跨库迁移

同一自然语言题可分别生成 Isabelle、Lean、HOL Light 形式；比较的是概念保持、库检索成本和 checker 成功率，而不是只比较 token-level BLEU。Lean 与 mathlib 等体系的结果不能从本论文 Isabelle 实验直接推断。

### 5.5 计算高效的 expert iteration

研究 proof search 样本选择、失败轨迹对比学习、蒸馏和小模型路由，减少 3,920 TPU hours 的成本；同时保留 checker 证据，避免速度提升以牺牲语义完整性为代价。

### 5.6 人机协同的假设补全

对模型置信度低、出现未对齐概念或缺失假设的题，向人类请求最小澄清，再将澄清后的形式化纳入可审计数据。这样可以把人工成本集中在语义瓶颈，而不是让人逐题手写全部 theorem。

## 6. 综合判断

这篇论文的核心价值不是证明 LLM 已经能普遍“理解数学”，而是展示了一个可验证的接口：少样本语言模型生成候选，形式系统筛选轨迹，筛选结果反过来改善证明器。25.3% perfect rate 说明接口已有非平凡能力；35.2% MiniF2F test 说明闭环有下游价值；定义对齐、隐含假设、长上下文、私有模型和高计算成本则限定了结论边界。

因此，后续工作最应补的是证据链的精细化与开放性：逐题语义标签、可复现生成语料、checker 版本、污染审计和跨库测试。方法、结果和可复现性细节分别见 [[wu2022-llm-autoformalization-method]]、[[wu2022-llm-autoformalization-results]]、[[wu2022-llm-autoformalization-analysis]]。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[wu2022-llm-autoformalization-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | 无公开代码 |
| **数据集** | 无外部数据集 URL（或使用论文内/合成数据） |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
