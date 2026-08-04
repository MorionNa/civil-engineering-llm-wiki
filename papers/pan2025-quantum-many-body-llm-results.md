---
type: paper-analysis
title: Quantum many-body physics calculations with large language models — results
authors:
- Haining Pan
- Nayantara Mudur
- William Taranto
- Maria Tikhanovskaya
- Subhashini Venugopalan
- Yasaman Bahri
- Michael P. Brenner
- Eun-Ah Kim
year: 2025
venue: Communications Physics
tags:
- domain/ai4s
- domain/llm
- evidence/paper
methods:
- benchmark
- human-in-the-loop
- quantum-many-body
results:
- evaluation
- physics-reasoning
failure_modes:
- data-contamination
- human-in-the-loop
datasets:
- benchmark
- quantum-many-body
reproducibility: medium
code_url:
- https://github.com/KimGroup/HartreeFock_GPT
dataset_url:
- https://github.com/KimGroup/HartreeFock_GPT
id: paper--pan2025-quantum-many-body-llm-results
status: active
project: civil-engineering-llm-wiki
keywords:
- large-language-models
- quantum-many-body
- physics
- evaluation
- reproducibility
- benchmark
- human-in-the-loop
- physics-reasoning
- data-contamination
- Communications Physics
sources:
- sources/papers/pan2025-quantum-many-body-llm.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# 结果：GPT-4 执行研究级 HF 推导

^[sources/papers/pan2025-quantum-many-body-llm.md]

## 1. 数据与实验范围

评测集包含 15 篇来自过去十年的量子多体研究论文；候选池来自 2010 年 1 月至 2023 年 8 月发表在 APS 期刊的 807 篇预印本。每篇论文先被填入 HF 模板，再让 GPT-4 执行同一套五步解析任务。

实验使用论文所称的 `gpt-4` 与 `gpt-4-0613` 近期 checkpoint；研究论文摘要的模板填充/执行示例使用 GPT-4 网页界面。结果不是开放权重模型的对比排行榜，因此不能解释为当前所有 LLM 的普遍性能。

## 2. 主要执行结果

| 指标 | 论文报告 |
|---|---|
| 最终 HF Hamiltonian | 对 15 篇论文，在中间步骤校正后 13 篇正确 |
| 全部步骤平均分 | 87.5/100，跨论文和任务汇总 |
| Rigor 评分 | 高且稳定，论文正文称高于 95 |
| 执行范围 | 五个概念步骤，覆盖 Hamiltonian、Fourier 变换、Wick 分解、二次项整理、对称性化简 |

作者指出，模型在给定正确占位符时能可靠执行每一部分。图 4 的分解显示，五个步骤的平均表现总体均匀；这支持“结构化的小任务有助于执行长推导”的判断。

## 3. 模板填充结果

模板填充任务需要为每篇论文替换 76 个以上占位符，难度高于在已给定符号下执行代数。在 5 篇论文、40 个 T4 占位符的初始实验中，GPT-4 得到 44 ± 8 的平均分。

作者按占位符信息类型分组：体系特有信息、摘录中明确出现的记号、需要根据上下文推断的记号。论文报告 GPT-4 对显式记号和一些系统信息表现较好，但对需要推断约定的内容不稳定；例子包括 Fourier 变换定义和磁场下动量偏移。

## 4. 自动评分结果

作者让 LLM 对自己的执行输出进行 Correct/Incorrect 判断，并与专家按 Correctness 层的标签比较：

| 设置 | class-balanced accuracy |
|---|---:|
| zero-shot | 69% |
| few-shot + rationale | 74% |

在要求返回 rationale 的设置中，LLM-Scorer 能识别 72.5% 的专家评分为 0 或 50 的问题为错误。该结果显示自动评分有助于扩大评测规模，但仍有明显漏检，不能替代专家复核。

## 5. 诊断性发现

- 中间步骤的结果有时不在目标论文中，评分者需要自行推导正确答案；因此最终分数同时反映模型和评测者的工作。
- 论文记录了模型或复核过程中发现原研究论文存在的排版/公式错误，说明逐步核对可反过来充当文献审计工具。
- 模型在执行固定任务时的平均表现明显高于其从摘录制定具体占位符计划的表现；阅读—规划是主要瓶颈之一。
- 作者使用训练截止日期和“步骤结果是否显式出现在论文中”两种间接分析，认为模型并非只是在复述训练语料，但这不是严格的新问题留出实验。

## 6. 结果解释边界

13/15 只在“正确模板 + 逐步纠错”的条件下成立；不能写成 GPT-4 在 15 篇论文上无辅助自动完成了 13 篇。87.5 的平均分也聚合了 Adherence、Rigor、Knowledge 和 Correctness 四层，不能直接等同于物理结论准确率。

原始结果与方法链见 [[pan2025-quantum-many-body-llm-method]]，失败边界见 [[pan2025-quantum-many-body-llm-critical]]。评测设计可与 [[xu2025-ugphysics-results]] 和 [[qiu2025-phybench-results]] 对照。

## 7. 可复现性结果

论文在 Data availability 中提供按 arXiv 编号组织的论文/数据，Code availability 中提供 GitHub 仓库和 `utils.py`。但是 GPT-4 是 API/网页服务，论文使用的历史 checkpoint、提示时的服务行为和训练数据并不能由仓库单独复现。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[pan2025-quantum-many-body-llm-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | https://github.com/KimGroup/HartreeFock_GPT |
| **数据集** | https://github.com/KimGroup/HartreeFock_GPT |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
