---
type: paper-analysis
title: 'UGPhysics: A Comprehensive Benchmark for Undergraduate Physics Reasoning with
  Large Language Models'
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
id: paper--xu2025-ugphysics-analysis
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
# UGPhysics — 论文分析

^[sources/papers/xu2025-ugphysics.md]

UGPhysics 将本科物理题组织成大规模、双语、按学科与推理技能标注的评测集，并配套 Model-Assistant Rule-based Judgment（MARJ）答案判定流水线。方法细节见 [[xu2025-ugphysics-method]]，数值证据见 [[xu2025-ugphysics-results]]，边界分析见 [[xu2025-ugphysics-critical]]；两个新增实体分别是 [[entities/ugphysics]] 与 [[entities/marj]]。

论文版本为 arXiv:2502.00334v4（2025-06-03），发表信息为 Proceedings of the 42nd International Conference on Machine Learning, PMLR 267。代码与数据在论文摘要给出的同一仓库公开：<https://github.com/YangLabHKUST/UGPhysics>。

## 证据口径速览

- 数字优先取预提取文本中的摘要、正文、Table、Figure 和 Appendix，并在段落中标出位置。
- “5,520 道题”和“11,040 个语言实例”是源题数与双语文本实例数，不能混写成同一个计数。
- 论文叙述的 49.78% 与 Table 5 新增 DeepSeek-R1 的 56.34% 并存；本页保留冲突而不替作者修正。
- MARJ 的 98% 来自 100 个样本，错误类型的百分比来自 100 个 OpenAI-o1-mini 错误答案。
- 对提取乱码造成的阈值、表头和具体实现缺口，统一使用“无法从提供文本确认”。
- 评测结果是题库、翻译、提示、模型快照、答案抽取和判定器共同作用的结果。
- 论文作者为 Xin Xu、Qiyun Xu、Tong Xiao、Tianhao Chen、Yuchen Yan、Jiaxin Zhang、Shizhe Diao、Can Yang、Yang Wang。
- 年份为 2025，venue 为 Proceedings of ICML 2025 / PMLR 267；提供文本未给出 DOI。
- 原始 arXiv 标识为 2502.00334v4，代码与数据 URL 均为 YangLabHKUST/UGPhysics 仓库。
- 本页的“贡献”与“研究机会”区分论文已报告结果和基于边界提出的后续建议。

## 1. 工程背景

> **⚙️ 非线性类型：** 本文不涉及物理非线性。它是面向大语言模型物理推理能力的文本基准与答案评测器研究，不建立 PDE、材料/本构或动力学模型；题目中可能出现的非线性物理现象只是被测问题内容，不是本文的建模对象。

物理问题求解同时要求物理知识、定律适用条件、数学推导和实际情境建模。论文指出，已有物理基准多集中于中学/高中或选择题，大学层级基准在题目规模、学科广度和答案类型上仍有限（引言与 Table 1，PDF pp. 2–3）。因此，对 AI/科学语言代理而言，需要一个能区分“记住公式”和“在物理语境中正确推导”的本科物理评测接口。

本文的工程对象是评测基础模型，而不是生产级物理仿真软件。其价值在于把题目来源、学科、主题、答案表示和推理技能放在同一数据结构中，并让答案判定处理单位换算、物理常数和等价表达式。

## 2. Research Gap

- 既有基准常以中学/高中题和多项选择题为主，难以覆盖本科物理的广度与多步推理。
- 一些大学或竞赛级基准规模较小、学科范围有限，或把物理与其他科学领域混合，不能提供细粒度本科物理诊断（Table 1）。
- 纯规则判定对复杂表达式不灵活，纯模型判定又可能在精确数值、单位和常数上出错；论文引用 OlympiadBench 物理题约 12% 的判定错误率来说明这一问题（Section 2，PDF p. 3）。
- 评测集还面临训练数据污染风险，因此题目收集与 n-gram 泄漏检测需要被纳入基准构建流程。

## 3. 科学问题

论文考察的核心问题是：当前 LLM 在数学能力很强的情况下，能否可靠处理需要物理知识、物理定律和实用含义的本科题？进一步的问题包括：

1. LLM 在 Knowledge Recall、Laws Application、Math Derivation 和 Practical Application 四类技能上的差异是什么？
2. 不同学科、英文/中文、答案类型和模型家族会否暴露稳定的能力缺口？
3. 一个结合规则精确计算与模型灵活判断的 MARJ 流水线，能否比单一判定方式更可靠？
4. 数据泄漏在多大程度上影响 UGPhysics 的测量结果？

## 4. 研究目标

论文要完成四件相互连接的事情：

- 构建 5,520 道本科物理源题，覆盖 Mechanics & Thermodynamics、Electromagnetism、Modern Physics 三个域、13 个核心学科和 59 个主题；将中文题翻译成英文，形成 11,040 个语言实例（Introduction、Table 1–2）。
- 用六种原子答案类型加一种 compound 类型表达可判定答案，并用四类物理推理技能标注题目。
- 设计 MARJ，对不同答案表示做类型化规则匹配，再把规则标记为 False 的复杂案例交给 GPT-4o 判断。
- 用零样本提示评估 31 个 LLM，并辅以人工判定、错误分析和数据泄漏检测。

## 5. 方法机制

整体流程为“教材题收集/清洗 → LaTeX 与 Problem–Solution–Answer 结构化 → 去重与筛选 → 英译 → 答案/技能标注 → MARJ 判定 → LLM 评测”。完整机制见 [[xu2025-ugphysics-method]]。

数据来自中国科学技术大学七本本科物理习题书；团队使用 Mathpix 将 PDF 转为 LaTeX，再人工复核和修正。含图题被排除以聚焦文本推理；渐进题被拆成独立题并补全依赖信息；估计、证明和解释类等缺乏确定答案的题被排除（Section 3.2、Appendix A.1）。

MARJ 先按答案类型处理 True/False、Multiple Choice、Numerical Value、Expression、Equation 和 Interval；未被规则接受的答案进入 GPT-4o 的第二阶段，模型提示要求关注物理常数与题目定义的等价量（Section 3.3、Algorithm 1）。

实验统一采用按答案类型定制的零样本 prompt，并使用 vLLM 加速；主体设置为 greedy decoding、temperature 0、最大输出 4,096 tokens，附录对 OpenAI-o1-mini 与 o1-like 模型说明使用 8,192 tokens（Section 4.1、Appendix B.3）。

## 6. 结果证据

论文叙述中的主结果是 OpenAI-o1-mini 总体准确率 49.78%，DeepSeek-R1-Distill-Llama-70B 为 40.17%；15/31 个被评估模型低于 20%，只有两个模型超过 40%（Table 5、Section 4.2）。但 Table 5 还单列了 “Newly-added Results”，其中 DeepSeek-R1 为 56.34%；摘要和正文没有解释这两行是否纳入“31 个模型”的统计，因此不能把 49.78% 无条件表述为整张表的最高值。

八个强模型的跨学科平均准确率在 Semiconductor Physics 为 31.0%、Atomic Physics 为 26.7%，在 Theoretical Mechanics 为 16.5%；技能维度上 Knowledge Recall 相对容易，Math Derivation 更困难（Figure 2）。MARJ 在随机抽取的 100 个测试例上与人工金标准达到 98% 一致率（Section 5.2）。

OpenAI-o1-mini 的 100 个错误样本中，flawed reasoning 占 31%、knowledge deficiency 占 25%、wrong application 占 18%，其后为 computation error 8%、misunderstanding 7%、exceeding max output 5%、instruction following 4% 和 others 2%（Figure 4）。

完整模型表、学科/技能表、泄漏比例、token budget 和 clip ratio 见 [[xu2025-ugphysics-results]]；对上述“主叙述—新增行”差异的边界解释见 [[xu2025-ugphysics-critical]]。

## 7. 贡献

1. 提供覆盖三大域、13 学科、59 主题、双语和七种答案类型的本科物理基准；题目按四类物理推理技能组织。
2. 提出 MARJ，把数值/符号规则的精确性与模型判定处理复杂等价表达的能力组合起来。
3. 给出 31 个模型的总体、语言、学科和技能维度比较，并报告数据泄漏与生成长度约束。
4. 通过人工错误标注显示，物理推理中的主要错误并不只是计算失误，还包括推理缺陷、知识不足和定律误用。

这些贡献分别沉淀为数据集实体 [[entities/ugphysics]] 和评测算法实体 [[entities/marj]]。

## 8. 核心知识点

- **物理推理不等同于数学推理。** 数学专门模型在 UGPhysics 上只带来有限增益；论文将其解释为物理题需要定律、条件和实际含义，而不仅是形式计算。
- **答案表示是评测器设计的一部分。** 单位换算、精度累积、物理常数和等价量会让“字符串相等”失效，因此需要按答案类型归一化。
- **规模不能替代诊断维度。** 11,040 个语言实例只有在域、学科、主题、技能和语言切片同时保留时，才可定位模型到底在哪种物理能力上失败。
- **长推理预算有代价。** 表 8–9 显示 o1-like 模型存在较高的截断比例，而提高 token 上限只带来边际准确率提升。
- **污染检测应与基准发布同时设计。** 文中使用 5-gram 预测检查污染，并同时统计污染且回答正确的样本。

## 9. Negative Knowledge

- UGPhysics 排除了含图题，因此它不是多模态物理理解基准，也不能直接评估图表、示意图或实验装置读取。
- 估计、证明和解释类问题因缺乏确定答案被排除；结果主要衡量可自动判定的最终答案，不等于完整的教学质量或证明质量。
- MARJ 的人工验证只有随机 100 个测试例；98% 是该抽样协议下的结果，不应外推为所有学科、所有答案类型的绝对准确率。
- 泄漏检测只报告若干模型子集，且用随机位置的 5-gram 预测作为信号；“检测到的污染很少”不能证明整个训练语料没有污染。
- 规则阶段去掉物理常数、对数值使用相对误差容忍，会带来领域相关的评测假设；提供文本中该相对误差阈值的指数出现字符损坏，具体指数“无法从提供文本确认”。
- 实验主要是零样本生成与答案匹配，没有证明在物理专门语料上继续预训练或监督微调后的能力上限；闭源模型版本、系统提示和服务端变化也限制跨时间复测。
- Table 5 的新增 DeepSeek-R1 行与摘要/正文的“最高 49.8%”陈述不一致；该版本不能在不查原始实验协议的情况下把所有表行合并成单一排行榜。

## 10. 可迁移知识

- 对科学问答基准，可复用“答案类型 → 归一化规则 → 复杂案例模型复核”的分层判定模式，而不是把一个通用 judge 用于所有输出。
- 对多语言科学数据，可同时保留源语言与翻译语言，并按语言报告性能差异；但需要额外的翻译一致性审计。
- 对污染敏感的静态基准，可采用抽样 n-gram/检索式检测，并报告“污染”和“污染且正确”两个指标。
- 对物理推理诊断，可用 Knowledge Recall、Laws Application、Math Derivation、Practical Application 作为可迁移的技能切片；这是一种论文中的标注框架，不是已验证的通用认知模型。
- 评测报告应同时记录答案准确率、错误类型和 token 截断率，避免只用一个总体分数解释长链推理系统。

## 11. 研究机会

- 按论文 Impact Statement 扩展含图题、多模态输入和更多语言，并验证翻译是否保持物理量、单位和边界条件。
- 建立物理专门的继续预训练/SFT 数据，直接检验“数学训练只带来有限增益”的因果解释。
- 扩大人工判定样本并按七种答案类型、13 个学科分层抽样，审计 MARJ 的错误结构与 GPT-4o judge 偏差。
- 设计动态或新题生成机制，降低静态题库污染，并报告模型版本、提示和随机种子对结果的影响。
- 把最终答案判定扩展为逐步推理、量纲一致性、物理定律适用条件和不确定性校准的联合评测。
- 对 Table 5 的新增结果重跑统一模型集合与 token 设置，厘清版本更新导致的排名变化。

## 12. 可复现性

**🟢 high（按论文披露的代码+数据公开分级）。** 摘要给出统一仓库 <https://github.com/YangLabHKUST/UGPhysics>，并明确称 codes and data available；论文同时披露了题目来源与清洗流程、答案类型、技能标注提示、MARJ 两阶段逻辑、主要模型清单、零样本 prompt 设计方向、vLLM、解码温度和输出长度设置。因此本页按 SCHEMA 的三档规则标为 high。

仍需区分“流程可复现”和“数字完全可复现”：评测依赖 OpenAI-o1-mini、GPT-4o 等闭源模型，模型版本与服务端行为会变化；附录对普通模型 4,096 tokens、o1-like 模型 8,192 tokens 的描述与正文设置并不完全一致；提供文本没有给出每个数据源习题书的完整书目信息或所有人工标注明细。独立复现时应固定模型版本、提示、答案抽取器、MARJ 阈值和污染检测抽样位置。

原始来源：arXiv:2502.00334v4，<https://arxiv.org/abs/2502.00334>；本地源文件为 `raw/papers/2502.00334v4.pdf`。方法、证据和批判边界分别链接到 [[xu2025-ugphysics-method]]、[[xu2025-ugphysics-results]] 和 [[xu2025-ugphysics-critical]]。
