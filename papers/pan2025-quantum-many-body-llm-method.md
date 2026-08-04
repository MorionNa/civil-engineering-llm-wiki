---
type: paper-analysis
title: Quantum many-body physics calculations with large language models — method
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
- language-agents
- quantum-many-body
- benchmark
- human-in-the-loop
results:
- evaluation
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
id: paper--pan2025-quantum-many-body-llm-method
status: active
project: civil-engineering-llm-wiki
keywords:
- large-language-models
- quantum-many-body
- physics
- scientific-reasoning
- human-in-the-loop
- language-agents
- benchmark
- evaluation
- data-contamination
- Communications Physics
sources:
- sources/papers/pan2025-quantum-many-body-llm.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# 方法：模板化的 Hartree–Fock 计算执行

^[sources/papers/pan2025-quantum-many-body-llm.md]

## 1. 任务定义

论文不是让 GPT-4 自由回答“什么是 Hartree–Fock”，而是把研究论文中的 HF 平均场推导定义成一串有状态的解析任务。输入包括论文摘录、体系的物理设定、符号约定和模板占位符；输出是逐步生成的 Hamiltonian、Hartree/Fock 项、序参量结构和自洽关系。

HF 方法将相互作用替换为与序参量相关的平均场，并忽略其涨落。目标计算分为解析阶段和数值阶段；本文主要评估解析阶段构造 `H_HF` 及其自洽方程，没有把完整数值迭代求解作为主要实验对象。

## 2. 五步 HF 模板

### Step 1：建立自由度与 Hamiltonian

模型先确定单粒子 Hilbert 空间、粒子 flavor、spin/orbital/valley/layer 等自由度、色散和势。随后分别写出非相互作用 Hamiltonian `H0` 与相互作用 Hamiltonian `H_int`，并显式约定算符和指标。

### Step 2：Fourier 变换

将实空间相互作用和场算符变换到动量空间，确定最终 `H_HF` 的动量依赖。论文特别指出，变换约定、动量偏移和 Fourier 定义是容易出错的占位符。

### Step 3：Wick 定理与平均场分解

用 Wick 定理把四费米子项分解为平均场期望与二次项。此步需要识别 Hartree、Fock 和可能的异常/配对结构，保持费米子交换符号与指标顺序一致。

### Step 4：整理二次 Hamiltonian

将二次项整理为 Hartree 项和 Fock 项；论文描述为 Hartree 项在 spin 空间中对角、Fock 项在 spin 空间中非对角，同时保持体系原本的 block structure。

### Step 5：利用对称性化简序参量

根据体系对称性揭示 `Δ_symm` 的结构，决定可研究的对称性破缺通道。得到 `H_HF` 后，研究者选择感兴趣的通道，再数值求解自洽方程。

## 3. 提示的状态传递

对每个概念步骤，作者进一步划分自然的原子任务，并为每个任务建立提示 `P_i`。`P_i` 同时接收模板中当前步骤的输入、论文特定的占位符，以及上一任务经过验证/校正的输出 `O_{i-1}`。

错误控制点位于每个状态转移之前：模型输出先由作者/专家检查，必要时修正，再作为下一步的上下文。这种机制牺牲了完全自主性，但减少了单个符号错误沿五步推导传播的风险。

## 4. 论文信息抽取

HF 模板每篇论文有 76 个以上的占位符。作者用另一组提示，将论文摘要或摘录与模板一起输入，让 GPT-4 识别系统信息、符号和约定，并把占位符替换为具体内容。

示例中，模型被要求回答 10 个关于体系色散、粒子类型和模型设定的问题；需要根据先验知识推断的题目可能要 2–3 次尝试。论文还对系统信息、摘录中明确出现的记号、需要推断的记号分别统计填充质量。

## 5. 评测与评分

作者从 2010 年 1 月至 2023 年 8 月的 APS 期刊预印本中筛选 807 篇候选论文，再选出 15 篇包含 HF 研究计算的论文。执行实验使用 2023 年中期的 GPT-4 checkpoint，包括 `gpt-4` 与 `gpt-4-0613`；摘要执行示例还使用了网页界面。

每个中间输出由具有 HF 经验的作者评分。评分分为四层：

| 评分层 | 检查内容 |
|---|---|
| Adherence | 是否遵循当前提示和指定约定 |
| Rigor | 数学推导、指标和符号是否严谨 |
| Knowledge | 推理是否符合物理定律和体系知识 |
| Correctness | 最终答案是否正确 |

评分使用 0、50、100 的离散标准；中间结果未在原论文显式给出时，由评分者计算或补齐目标值。为探索自动评分，作者让 LLM 对自己的输出判定 Correct/Incorrect，并与专家标签比较，另测试要求模型给出 rationale 的 few-shot 设置。

## 6. 方法边界

该流程把三类能力分开：从论文读出信息、在固定模板内执行代数、判断结果的物理正确性。它不是通用的“把任意论文变成新理论”的 agent，也不是对每个自洽方程都运行高效数值求解器。

方法页面与结果证据见 [[pan2025-quantum-many-body-llm-results]]；批判与失败边界见 [[pan2025-quantum-many-body-llm-critical]]。对于更强调物理工具链的方向，可对照 [[lu2026-language-agents-physics-analysis]] 和 [[entities/hartree-fock-llm-prompting]]。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[pan2025-quantum-many-body-llm-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | https://github.com/KimGroup/HartreeFock_GPT |
| **数据集** | https://github.com/KimGroup/HartreeFock_GPT |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
