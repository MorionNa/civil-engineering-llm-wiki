---
type: paper-analysis
title: Quantum many-body physics calculations with large language models
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
- physics-reasoning
- reproducibility
failure_modes:
- data-contamination
- scientific-reasoning
- human-in-the-loop
datasets:
- benchmark
- quantum-many-body
reproducibility: medium
code_url:
- https://github.com/KimGroup/HartreeFock_GPT
dataset_url:
- https://github.com/KimGroup/HartreeFock_GPT
id: paper--pan2025-quantum-many-body-llm-analysis
status: active
project: civil-engineering-llm-wiki
keywords:
- large-language-models
- quantum-many-body
- physics
- scientific-reasoning
- evaluation
- human-in-the-loop
- reproducibility
- language-agents
- benchmark
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
# Quantum many-body physics calculations with large language models

^[sources/papers/pan2025-quantum-many-body-llm.md]

## 1. 工程背景

> **⚙️ 非线性类型：** **其他：自洽场计算非线性**。本文评估 LLM 执行 Hartree–Fock 平均场推导；非线性主要体现在序参量与自洽方程的闭环，而不是 PDE 算子、材料本构或线性弹性动力响应。跨论文比较时，应与 [[lv2025-phase-field-gimp-fracture-analysis]] 的 PDE/断裂建模和 [[oropeza-navarro2024-microplane-damage-analysis]] 的材料损伤非线性区分。

理论物理研究同时需要自然语言理解、专门符号操作、物理约束判断和数值计算。论文选择量子多体物理中广泛使用的 Hartree–Fock（HF）平均场方法作为可拆解的研究级计算任务，而不是测试一个孤立的数学题。

HF 推导通常要从问题的物理设定构造近似 Hamiltonian，再整理 Hartree/Fock 项、对称性和自洽方程。对研究者而言，难点不只是“知道公式”，还包括辨认论文中的符号、约定、粒子自由度和对称性，并把它们一致地代入长链条推导。

## 2. Research Gap

已有 LLM 评测多集中在知识问答、数学竞赛或代码生成，尚不能说明模型能否执行真实论文中反复出现的、具有物理语境的多步解析计算。论文将这一空白具体化为：给定研究论文和一个结构化的 HF 计算模板，LLM 能否逐步得到正确的 HF Hamiltonian 和自洽关系。

另一个缺口是可扩展评估。研究级推导中间步骤往往没有直接写在目标论文里，人工填充模板和逐步评分成本高；若只看最后答案，又会掩盖错误从哪一步开始传播。

## 3. 科学问题

核心问题是：GPT-4 能否在研究级量子多体问题上，按照物理学家组织好的步骤执行 HF 推导，并保持符号、数学推理、物理知识和最终正确性的一致？

论文还考察两个辅助问题：LLM 能否从论文摘录中补齐模板占位符；LLM 能否作为评分器，减轻专家对每个中间步骤逐项检查的负担。

## 4. 研究目标

1. 把 HF 推导拆成可复用的五步提示模板。
2. 在来自近十年 APS 期刊预印本的 15 篇研究论文上评估 GPT-4。
3. 用四层评分区分遵循指令、数学严谨性、物理知识一致性和最终正确性。
4. 测试 LLM 在模板填充和自动评分两个瓶颈上的可行性。

## 5. 方法机制

论文建立一个“模板—占位符—多轮提示—逐步校正”的计算管线。每一步提示都接收上一阶段经过检查的输出，避免把未核验的错误直接传播到后续推导。

HF 模板包含五个概念步骤：建立自由度和单粒子 Hilbert 空间；做 Fourier 变换；用 Wick 定理进行平均场分解；整理二次 Hamiltonian 中的 Hartree/Fock 项；利用体系对称性化简序参量结构。详细机制见 [[pan2025-quantum-many-body-llm-method]]。

## 6. 结果证据

在正确填充模板并对中间步骤进行必要校正的条件下，GPT-4 在 15 篇论文中有 13 篇得到正确的最终 HF Hamiltonian；所有步骤、论文和评分的平均分为 87.5/100。论文还报告 Rigor 层得分稳定高于 95。

模板填充比执行固定推导更不稳定：在 5 篇论文、40 个占位符的 T4 任务上，一次提示的初始平均分为 44 ± 8。自动评分器与专家标签的 class-balanced accuracy 在 zero-shot 和带 rationale 的 few-shot 设置下分别为 69% 和 74%；带 rationale 时能识别 72.5% 的专家评分为 0 或 50 的错误/部分正确结果。

## 7. 贡献

- 将研究级 HF 计算定义成具有物理语境的 LLM 评测任务，而不是通用知识问答。
- 提出把长推导拆成五步、并在每一步进行检查和校正的提示模板。
- 同时评估执行、论文信息抽取和自动评分三个环节，保留中间证据。
- 发布研究论文数据库、模板、完整输出及代码/数据仓库，形成可复用的评测基线。

## 8. 核心知识点

最重要的区分是“执行动作”和“制定动作计划”：GPT-4 在给定结构和约定后可以较好地执行 HF 代数，但从论文摘录中判断哪些信息应填入 76 个以上占位符更困难。结构化模板把物理推导变成可审计的状态机，逐步校正则相当于在链式推理中插入验证门。

这套设计不等于让 LLM 独立完成一个新理论。最终研究价值仍取决于输入信息是否正确、物理约定是否一致以及专家是否检查了中间结果。

## 9. Negative Knowledge

- 15 篇论文规模小，不能据此推出 GPT-4 对所有量子多体模型或其他物理理论都可靠。
- 13/15 的“正确最终 Hamiltonian”依赖中间步骤被检查和必要时纠正，并非无监督端到端成功率。
- 模板占位符需要研究者先理解论文；论文没有证明完全自动的论文阅读—建模—计算闭环。
- GPT-4 的完整训练数据未知，论文只能通过时间截断和“中间结果是否显式出现在论文中”等间接方式讨论数据污染与泛化。
- 自动评分器的准确性低于完美，不能替代专家对物理正确性和符号约定的审核。
- 本文没有展示 LLM 直接数值求解所有自洽方程，也没有证明其输出可以直接驱动可靠数值模拟。

## 10. 可迁移知识

模板化、状态化和逐步校正可迁移到需要符号、自然语言与领域知识协同的科学计算任务，例如 [[lu2026-language-agents-physics-analysis]] 讨论的物理研究代理、[[qiu2025-phybench-analysis]] 的物理推理评测和 [[meadows2026-formalscience-analysis]] 的科学形式化。

可复用的最小单元不是 HF 公式本身，而是：定义中间状态、为每一步规定输入/输出、记录约定、在状态转移前验证、同时保留专家标签和模型解释。

## 11. 研究机会

1. 将模板与符号代数、数值线性代数和自洽求解器连接起来，使模型负责提出结构、工具负责计算与检查。
2. 用更多体系、更晚发表的论文和严格留出的新问题评估真正的跨分布泛化。
3. 将评分器从二分类扩展到带物理约束的可验证评分，并校准其不确定性。
4. 对模板填充、推导执行和最终物理结论分别建模，定位错误传播的临界节点。
5. 将四层评分映射为可追踪的审计记录，支持研究者快速定位需人工重算的步骤。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 代码、论文数据库、模板和输出仓库公开，但核心模型是依赖历史 GPT-4 API/网页界面的专有系统，无法由公开权重完全替代。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 medium；方法和评测流程较清楚，但 GPT-4 checkpoint 与 API 行为不可完全复刻 |
| **官方代码** | https://github.com/KimGroup/HartreeFock_GPT，包含 `utils.py` 等代码 |
| **数据集** | 同一仓库中按 arXiv 编号组织的论文、模板和研究输出；目标论文来自 APS 预印本筛选集 |
| **协议** | 论文说明为开放获取；仓库具体许可证需以仓库当前文件为准 |
| **复现要点** | 需要固定 GPT-4/`gpt-4-0613` 等历史 checkpoint、提示模板、占位符填充、逐步校正规则以及四层人工评分；仅运行当前模型 API 不能保证得到原始分数 |

相关页面：[[pan2025-quantum-many-body-llm-method]]、[[pan2025-quantum-many-body-llm-results]]、[[entities/hartree-fock-llm-prompting]]。

## 关联页面

- [[pan2025-quantum-many-body-llm-critical]]
