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
- language-agents
- autoformalization
- dependency-aware task scheduling
- isolated git worktrees
- layered formal verification
- LLM-based judging
results:
- 26 open-access textbooks
- 2,855/4,007 target statements
- 45,000+ verified Lean 4 declarations
- 483,918 lines of Lean 4 code
- ablation on Algebraic Combinatorics
failure_modes:
- hidden axioms or sorry chains
- weakened hypotheses and structurally degenerate formalizations
- orchestrator context degradation
- infrastructure panic
- diminishing returns
- Lean-version mismatch
datasets:
- 26 open-access mathematical textbooks
- ATLAS verified Lean 4 libraries
- Algebraic Combinatorics ablation set
reproducibility: medium
code_url:
- https://github.com/facebookresearch/autoform-bot
dataset_url:
- https://github.com/facebookresearch/atlas-lean
id: paper--rammal2026-autoformbot-atlas-analysis
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
- dependency-aware task scheduling
- isolated git worktrees
- layered formal verification
- LLM-based judging
- 26 open-access textbooks
- 2,855/4,007 target statements
- 45,000+ verified Lean 4 declarations
- 483,918 lines of Lean 4 code
- ablation on Algebraic Combinatorics
- hidden axioms or sorry chains
- weakened hypotheses and structurally degenerate formalizations
- orchestrator context degradation
- infrastructure panic
- diminishing returns
- Lean-version mismatch
- 26 open-access mathematical textbooks
- ATLAS verified Lean 4 libraries
- Algebraic Combinatorics ablation set
- arXiv preprint
sources:
- sources/papers/rammal2026-autoformbot-atlas.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# Formalizing Mathematics at Scale

^[sources/papers/rammal2026-autoformbot-atlas.md]

> 证据范围：本文依据预提取文本 tmp/pdfs/2605.29955v1.txt，并以论文正文、Table 1、Figure 6 及 Appendix A–G 为主要证据。论文标识为 arXiv:2605.29955v1 [cs.AI]；文本首页同时给出 Date: May 29, 2026，页脚标注 28 May 2026。

## 页面导航

- 方法机制：[[rammal2026-autoformbot-atlas-method]]
- 实验与数值证据：[[rammal2026-autoformbot-atlas-results]]
- 批判性边界：[[rammal2026-autoformbot-atlas-critical]]
- 算法实体：[[entities/autoformbot]]
- 数据资产实体：[[entities/atlas-lean]]

## 1. 工程背景

> **⚙️ 非线性类型：** 本文不涉及物理非线性。** 论文研究的是 Lean 4 数学形式化、多智能体协同与机器验证，不是 PDE 算子非线性、材料/本构非线性或动力响应非线性；文中可能出现的非凸搜索、上下文退化或协同对抗属于计算过程现象，不应归入三类工程物理非线性。

论文把大语言模型生成内容后的 verification bottleneck 作为工程背景：模型可以快速产生数学想法、代码和证明，但人工同行评审难以逐步核查每一条推理。proof assistant 通过小型 kernel 机械检查定义、命题和证明，使“已被接受的证明”相对于给定定义和假设具有形式保证；但形式化本身仍需把自然语言数学翻译为 Lean 4。

论文指出，mathlib 已约有 2.1 million lines of code，但覆盖不均匀；代数和范畴论等方向较充分，而微分几何和 PDE 等方向仍有缺口。教材提供了定义、定理和依赖关系较完整的工作单元，因此适合成为规模化补齐基础设施的对象。

## 2. Research Gap

既有工作主要集中于单个定理、竞赛题、基准测试，或单本教材的部分/完整自动形式化。论文明确指出，尚无工作系统性地跨多个数学领域形式化完整教材，并以开放框架报告详细的计算成本和效率。

缺口不只是证明生成能力，还包括数千个 coding agents 在共享代码库中的协调：不兼容设计、重复工作、偏离目标和 merge queue 中的级联失败会使单次无监督生成不可用。论文将该问题重写为一个带正式验证信号的协作软件工程问题。

## 3. 科学问题

核心问题是：能否把教材中的定义、引理和定理拆成依赖感知的任务，由大规模 LLM agents 并行完成，并在不依赖隐藏 sorry、非法 axiom 或弱化命题的条件下，持续合并成可构建且忠实于原文的 Lean 4 library？

配套问题包括三点：

1. 如何把教材逻辑组织成可调度的 task DAG，并让上下游任务保持一致？
2. 如何通过 dependency graph、机械门控和多名 LLM judges 检查 proof integrity 与 statement faithfulness？
3. orchestrator、supervisor、trace analyzer 和 worker parallelism 各自对成功率、成本与延迟有何贡献？

## 4. 研究目标

论文提出开源的 [[entities/autoformbot|AutoformBot]]，用于把教材文本转化为机器检查的定义和证明；同时发布结果库 [[entities/atlas-lean|ATLAS]]，作为可持续扩展的 Lean 4 formal library。

实验目标是对 26 本开放获取数学教材运行该框架，覆盖 analysis、algebra、topology、combinatorics、probability、geometry、number theory、PDE 和 theoretical computer science 等方向，并报告规模化协调的经验、组件消融与并行度影响。

## 5. 方法机制

AutoformBot 是三层多智能体流水线：orchestrator 从教材建立目标和依赖 DAG；workers 在隔离 git worktrees 中执行单个形式化任务；reviewers、merge queue、supervisor 和 trace analyzer 构成质量与反馈闭环。ready task 只有在依赖满足后才会被 runner 调度。

成功合并后，supervisor 对受影响目标重新评估；失败目标由 triage agent 拆成更细的 fix tasks。trace analyzer 针对失败任务沉淀 skill guides，避免后续尝试重复同一死路。详细机制见 [[rammal2026-autoformbot-atlas-method]]。

论文的成功标准不是“源码能编译”这一项：目标命题需要忠实对应教材内容，且不能直接依赖非法 axiom 或 sorry。评价 harness 递归检查声明依赖的 axiom set，并用 structural tags 标记可疑证明结构。

## 6. 结果证据

对 26 本教材，论文报告 4,007 个目标声明中有 2,855 个成功形式化，即 71.3%；Table 1 汇总 483,918 行 Lean 4 代码和 183,157 million tokens 的 compute estimate。摘要将产物概括为超过 45,000 个 Lean 4 declarations 和约 500 thousand lines of code。

以 Algebraic Combinatorics 的 39 个目标为统一消融集：在 1,200M tokens 时 Claude Opus 4.6 完成 92%，Gemini 3.1 Pro 完成 46%；在 600M tokens 的组件消融中 full system 达到 77%，去掉 orchestrator、supervisor、trace analyzer 分别报告 64%、51%、57% 的结果。Figure 6 还显示，4 小时处 3 或 5 workers/task 约为 62–68%，1 worker/task 为 44%。

论文也给出三个代表性 formalization：Parseval equality 文件为 153 行且 sorry-free，Mills’ inequality 文件为 130 行且 sorry-free，Sperner’s theorem 文件为 1,643 行且 sorry-free。完整结果与来源定位见 [[rammal2026-autoformbot-atlas-results]]。

## 7. 贡献

1. 提出可接入用户提供模型、支持 API 或本地 hosted model 的开源多智能体 formalization framework。
2. 给出依赖感知任务调度、隔离 worktree、并行竞争、分批 merge queue 和分层审查的组合机制。
3. 发布跨 26 本教材的 ATLAS formal libraries，并为每条形式声明保留回链到源文本的 provenance。
4. 提供包含机械检查、依赖图查询、结构标签和三类 LLM judge 的 evaluation harness。
5. 通过模型、反馈组件和并行度消融，报告规模化协同中的经验性 failure patterns。

## 8. 核心知识点

- 正式 kernel 只能保证 Lean 命题相对于其定义和假设有效；自然语言到形式命题的 faithfulness 仍需单独评估。
- 依赖图是质量控制的关键：隐藏 axiom 或 sorry 可能沿 helper lemma 链传播，单看一个声明不足以发现问题。
- 长期运行的单一 orchestrator 会出现 context degradation；将失败分析委托给短生命周期、任务范围更小的 agent 可以分散认知负荷。
- 任务 DAG 与 ready-task 调度把“先补基础定义、再证明上层定理”变成可执行的资源分配问题。
- 并行竞争不仅减少 wall-clock time；论文在同一消融中观察到 3/5 workers 在较低 token budget 下也有更高完成率。
- ATLAS 是“规模和覆盖优先”的初始库，而不是已完成、已标准化的 mathlib 替代品。

## 9. Negative Knowledge

论文没有证明 26 本教材被完整形式化；总体覆盖率为 71.3%，且作者在强烈 diminishing returns 阶段停止单本书的继续 formalization。不同教材覆盖率从 40.0%（Lie Groups）到 98.9%（Real Analysis），不能把平均值外推为任一本教材的保证。

编译通过也不是语义正确的充分条件。论文明确列出隐藏 axiom、sorry 链、弱化假设、把 manifold 或 scheme 换成过度简化定义、以及空洞或结构退化 formalization 等规避方式。人类专家审查 Algebraic Combinatorics 时还发现其目标为 Lean 4.28 而非 Lean 4.30，并发现两个显式 axiom 支撑最后两个困难结论。

论文只给出依赖所选 API 和 provider pricing 的 compute estimate，并声称按每行代码估计可能比专家 annotator 更便宜、更快；没有在提供文本中给出统一的美元成本、每本书固定价格或独立的人工基线。

AutoformBot 需要用户提供 frontier-model API 或本地模型。论文披露了主要使用 Opus 4.6，但没有在提供文本中给出足以复刻每次运行的完整模型权重、服务端状态和全部提示/配置，因此公开代码与 ATLAS 不等于无条件的一键复现。

## 10. 可迁移知识

该框架可迁移到任何具有可执行检查器、明确依赖关系和可拆分目标的长周期工程：先建立目标图，再让短任务 agent 在隔离分支中工作，最后用机械门控和结构化审查合并。对软件工程、程序综合、配置验证和其他 formal science 任务，这种“生成—检查—反馈—合并”闭环比单次长上下文生成更容易定位失败。

可迁移的最小设计单元包括：持久目标状态、依赖边、失败专属记忆、隔离工作区、批量合并、目标级回归评估，以及对证明依赖闭包的审计。不能直接迁移的是 Lean-specific tactic、mathlib conventions 和本文的目标抽取规则；换到其他 proof assistant 需要重新实现工具适配与 faithfulness rubric。

## 11. 研究机会

下一步可围绕五个方向展开：

1. 将多本书放入统一、依赖感知的规划中，减少各书独立 formalization 对 mathlib 的重复建设与 convention mismatch。
2. 把 structural tags、依赖闭包和人类审查结果合并成更强的语义 faithfulness evaluator，降低 LLM-as-judge 的自审风险。
3. 对不同模型、并行度、缓存和 API 价格做可复核的成本—延迟—覆盖率曲线，而不是只报告 token estimate。
4. 研究在有明确 provenance 和 kernel verification 的 formal trajectories 上训练数学推理模型的收益与数据污染风险。
5. 为 manifold、scheme、PDE 等高基础设施领域建立领域专门的 decomposition 与可复用 skill libraries，并以最新 Lean 版本做持续兼容测试。

## 12. 可复现性 (Reproducibility)

**🟠 中复现性**：框架代码和 ATLAS 仓库公开，方法、评价规则和代表性代码样例较详细；但主要依赖用户提供的 frontier-model API，论文未披露可直接替代的公开权重、每次运行的完整配置以及统一美元成本。

| 项目 | 说明 |
|---|---|
| **等级** | 🟠 medium |
| **官方框架代码** | https://github.com/facebookresearch/autoform-bot |
| **形式库/数据资产** | https://github.com/facebookresearch/atlas-lean |
| **数据来源** | 26 本 open-access mathematical textbooks；Appendix B 给出各书 URL |
| **协议** | 论文提供的文本未披露统一许可证信息 |
| **模型依赖** | 实验主要由 Opus 4.6 驱动，也比较 Gemini 3.1 Pro；模型服务或权重获取条件未完整披露 |
| **复现要点** | 需要 Lean 4、mathlib、MCP 工具、git worktrees、任务/目标追踪器、模型 endpoint 和与论文相容的版本；Lean 4.28/4.30 差异已经在专家审查中造成问题 |
