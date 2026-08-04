---
type: paper-analysis
title: 'LeanMarathon: Toward Reliable AI Co-Mathematicians through Long-Horizon Lean
  Autoformalization'
authors:
- Yuanhe Zhang
- Yuekai Sun
- Taiji Suzuki
- Jason D. Lee
- Fanghui Liu
year: 2026
venue: arXiv preprint
tags:
- domain/ai4s
- domain/llm
- evidence/paper
methods:
- blueprint-system-of-record
- dynamic-proof-DAG
- contract-scoped-agents
- two-stage-orchestration
- deterministic-CI-gate
- source-aware-refinement
results:
- seven-target-theorems
- 258-proof-nodes
- no-sorry
- incremental-development
- parallel-PRs
failure_modes:
- goal-drift
- lost-in-the-middle
- coherence-loss
- self-evaluation-bias
- irreversibility
- source-gap
- library-gap
datasets:
- paper-sources
- canonical-target-statements
reproducibility: medium
code_url:
- https://github.com/YuanheZ/LeanMarathon
dataset_url: []
id: paper--zhang2026-leanmarathon-analysis
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
- long-horizon
- co-mathematician
- benchmark
- evaluation
- mathematics-at-scale
- human-in-the-loop
- reproducibility
- blueprint-system-of-record
- dynamic-proof-DAG
- contract-scoped-agents
- two-stage-orchestration
- deterministic-CI-gate
- source-aware-refinement
- seven-target-theorems
- 258-proof-nodes
- no-sorry
- incremental-development
- parallel-PRs
- goal-drift
- lost-in-the-middle
- coherence-loss
- self-evaluation-bias
- irreversibility
- source-gap
- library-gap
- paper-sources
- canonical-target-statements
- arXiv preprint
sources:
- sources/papers/zhang2026-leanmarathon.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# LeanMarathon：面向长时程 Lean 自动形式化的可靠 AI 数学合作者

^[sources/papers/zhang2026-leanmarathon.md]

> 证据范围：原始标题为 *LeanMarathon: Toward Reliable AI Co-Mathematicians through Long-Horizon Lean Autoformalization*；作者为 Yuanhe Zhang、Yuekai Sun、Taiji Suzuki、Jason D. Lee、Fanghui Liu；arXiv:2606.05400v1，2026。正文证据主要来自论文 §1–§5、Tables 1–6、Figures 1–5 和 Appendix A。
>
> 相关页面：方法机制见 [[zhang2026-leanmarathon-method]]；结果证据见 [[zhang2026-leanmarathon-results]]；批判性边界见 [[zhang2026-leanmarathon-critical]]；算法实体见 [[entities/leanmarathon]]。

## 1. 工程背景

> **⚙️ 非线性类型：** 该论文不涉及物理非线性。它研究的是 Lean 4 研究数学自动形式化、多智能体编排和证明依赖管理，不是 PDE 算子非线性、材料/本构非线性或动力响应非线性（线性弹性）问题。因此，论文中的 “long-horizon”“drift” 和代理交互复杂性不能归类为物理非线性。

研究级数学形式化需要把论文中的定义、引理和定理全部变成 Lean 4 中可编译、无 `sorry` 的机器检查对象。论文指出，单个目标的证明能力并不能直接解决整个研究论文：一个发展可能包含数百个相互依赖的声明，局部改动会让远端证明失效，错误的中间形式化还可能得到“形式上正确但与目标无关”的推理图。

从工程可靠性看，长时运行具有类似软件工程的故障：上下文陈旧、依赖纠缠、目标漂移、局部修复污染远端状态，以及代理在错误方向上无法恢复。论文将瓶颈表述为 agent durability，即代理能否在多小时运行中保持目标一致、识别失败状态并限制错误传播。

## 2. Research Gap

既有神经定理证明器多聚焦于一个或少量 Lean 目标；教材形式化通常已有细粒度证明蓝图，代理主要执行从既定计划到 Lean 代码的翻译。研究级自动形式化缺少可信的细粒度计划，代理必须同时发现、维护和修复证明结构。

论文将缺口归纳为两个长期故障：goal drift，即中间推理逐渐偏离终端目标；lost-in-the-middle，即代理在不断膨胀的无效子问题空间中迷失。单一代理同时负责读论文、搭骨架、证明、诊断和修复，缺少独立的目标保真度审查和故障隔离机制。

LeanMarathon 的研究问题不是简单提升单个 prover 的能力，而是设计一个使长时程形式化可读、可恢复且抗漂移的 harness。论文把可演化 proof DAG、契约化代理、外部/确定性验证和并行 CI 门控组合为系统性回答。

## 3. 科学问题

论文实际考察的核心问题包括：

- 如何在没有预先可信细粒度证明计划时，逐步发现并保持一个与论文目标一致的证明图。
- 如何让形式上正确的中间声明仍然对应源论文的数学意图，而不是把错误的目标一路证明到底。
- 如何将局部证明失败变成可定位、可修复的 issue，而不是让一个代理污染共享状态。
- 如何在多个代理并行工作时保证编辑区域不冲突，并让 CI 成为唯一合并权威。
- Lean 编译器和 Mathlib 缺失的定理能否反过来暴露论文中被压缩、遗漏或不成立的数学步骤。

## 4. 研究目标

本文提出并评估 LeanMarathon，一个面向研究数学的长时程 Lean 自动形式化多智能体 harness。目标不是声称代理本身不会犯错，而是让错误被限制在局部、能够通过外部证据恢复，并使系统最终产出完整的无 `sorry` Lean blueprint。

具体目标是：

1. 用一个同时承载 Lean 骨架、自然语言证明图和持久状态的 blueprint 作为系统记录。
2. 用 Blueprinter、Target-Reviewer、Worker 和 Refiner 四类狭域代理分离构造、审查、证明与维修。
3. 先做终端目标保真度审查，再按动态 proof DAG 的叶节点向上并行消解证明义务。
4. 通过七项确定性 CI 检查和受限编辑区域，把失败变成拒绝的 patch 或 issue。
5. 在两篇 2026 研究论文、四个 Erdős 问题上检验完整性、增量扩展、并行合并、成本和失败边界。

## 5. 方法机制

blueprint 是一个 Lean 文件，也是自然语言 proof graph 和代理共享的 system of record。每个引理/定理节点包含 Lean 声明、LaTeX statement、proof prose、title 和 `latexEnv` 元数据；Lean elaborator 提供实际依赖，验证器要求 prose 中的 `\cref` 边与类型检查得到的依赖双向一致。定义作为全局上下文，不进入 proof DAG。

四个代理拥有明确输入、输出和编辑边界：Blueprinter 生成带占位证明的初始骨架；Target-Reviewer 只读并审计 canonical target、LaTeX 和 Lean 类型；Worker 一次负责一个动态叶节点；Refiner 处理一个连通 illness sub-DAG，区分 blueprint drift 与 source gap 并提交修复。

两阶段编排先在 Stage 1 中循环执行 Blueprinter、CI、Target-Reviewer 和 Refiner，直到目标审查通过；Stage 2 每轮从当前 `main` 提取 proof DAG，找到依赖已证明的动态叶节点，为每个叶节点分配独立 Worker，所有 PR 经过 CI 后才可合并。方法细节见 [[zhang2026-leanmarathon-method]]。

该机制的关键不变量是：目标类型在 Worker formalization 阶段冻结；自然语言依赖与 elaborator 依赖保持双向 parity；完整证明在父节点变化后整体降级；CI 是唯一 merge authority。四项约束共同把全局耦合的数学任务转化为可回滚的局部事务。

## 方法—证据对应

- **Blueprint + parity** 对应论文 §2.1 和 CI 的 proof-dependency parity 检查。
- **四类代理** 对应 Table 1，并分别绑定分解、目标审查、局部证明和图级维修。
- **动态叶节点并行化** 对应 Figures 1、4、5 及 Stage 2 描述。
- **源感知维修和固定 heartbeat** 在 §4.7 消融与 §4.4–§4.6 案例中得到运行轨迹支持。

## 6. 结果证据

三次自主运行覆盖两篇研究论文、四个 Erdős 问题和七个目标定理；论文报告全部目标以无 `sorry` 完成，共证明 258 个引理和定理。Table 2 给出三种 blueprint 的行数、定义/引理/定理节点和 proof node 数；Table 3 给出轮次、Worker、Refiner、PR、并行关键路径、token 和成本。

更细的表格和案例证据见 [[zhang2026-leanmarathon-results]]。其中，Prim 运行复用 #1196 的 59 个节点并增加 145 个节点；跨三次运行有 135 个 Worker PR 合并，单轮最多 16 个，并且论文称没有发生合并冲突。

阅读这些结果时应区分三种证据：

- **完整性证据**：目标定理无 `sorry`、无 `sorry_using`，并通过七项 CI 检查。
- **工程性证据**：运行轮次、PR、冲突、重开节点和成本反映 harness 的长时程行为。
- **数学反馈证据**：issue 中的反例、totalization 暴露和 Mathlib 缺口说明形式化改变了对源证明的审查粒度。

论文没有把这三类证据合并成单一质量分数，因此本页也不把“完成率”解释为数学或工程可靠性的充分统计量。

## 7. 贡献

- 将 agent durability 明确为研究级自动形式化的核心工程瓶颈，并用 coherence loss、self-evaluation bias 和 irreversibility 描述单代理系统的故障来源。
- 提出动态 proof DAG：分解不在初始骨架生成时冻结，而是在失败和修复中继续拆分、重排和扩展。
- 以 blueprint 同时保存形式声明、自然语言证明和依赖图，使目标保真度、证明依赖和代码状态具有同一记录源。
- 通过四类契约化代理、冻结/可编辑区域和确定性 CI，实现 fault containment，使局部错误更容易被拒绝和恢复。
- 用源感知 Refiner 区分 blueprint drift 与 source gap；案例研究显示，这一分类能把编译器反馈转化为数学修复。
- 在研究级 Erdős 问题上展示 paper-level autoformalization 的完整运行，而不是只证明孤立的竞赛级目标。

## 8. 核心知识点

1. 形式化的系统边界应当首先定义为“目标、声明、证明和依赖的可检查状态”，而不是一段不可追踪的长上下文。
2. 动态 DAG 叶节点调度把全局耦合任务拆成可恢复的局部交易，但前提是依赖和编辑范围可机械验证。
3. Target-Reviewer 必须与生成和证明代理分离；否则“证明了一个错误目标”会在系统内部被误判为成功。
4. Worker 的低成本数值/边界反驳只用于提前发现可证伪声明，不能替代 Lean 证明。
5. 论文案例表明，Lean 的 totalization 约定可能掩盖缺失的 `Summable` 假设或不恰当的实数 `limsup` 语义；形式化需要显式检查这些边界。
6. 论文中的 “routine calculation” 和 “an induction gives” 在 proof assistant 中可能展开为大量分析、概率和测度论义务。

## 9. Negative Knowledge

- 不能把“Lean 文件编译通过”直接解释为自然语言源证明已经忠实；目标陈述、LaTeX prose 和 Lean type 的一致性仍需独立审查。
- 不能把动态 DAG 当成一次性规划器。初始分解不可靠时，必须允许局部节点拆分、错误声明降级为 placeholder 并重新证明。
- 不能让 Refiner 在看不到源证明时凭空补上数学内容。消融中 source-blind Refiner 让 blueprint 向源论文不存在的 machinery 漂移，约十二天后仍有 26 个 `sorry`。
- 不能用固定物理行数作为 “cannot formalize” 的停止规则；早期 Worker 会以规模为理由退出，而当前论文要求 issue 必须有具体的反例、矛盾、错误陈述或无效输入证据。
- 该 harness 不是数学库覆盖的替代品。unit-distance disproof 试验中，Mathlib 缺少关键代数数论后，dummy number-field record 虽可类型检查，却无法支撑真实几何结论。
- 论文只评估两篇论文、三次运行和一个可访问的商业 baseline；文本不足以证明 LeanMarathon 对所有研究领域、模型或数学库版本都优于其他系统。

## 10. 可迁移知识

契约化代理和受限编辑区域可迁移到任何长时程、依赖耦合的代码/知识工程：先冻结共享事实，再允许每个 Worker 只改局部事务，最后由确定性门控合并。动态 DAG 也可用于实验工作流、数据处理图或多阶段科学推理，但这些迁移属于方法启发，不是本文直接实验结论。

将自然语言说明与可执行依赖图并置，可作为科学软件、形式化证明和 AI 代理之间的共同接口。编译器反馈、边界测试和外部审查的分工，也可迁移为“生成—反驳—验证—维修”的可靠性闭环。

## 11. 研究机会

- 建立跨论文、跨 Lean/Mathlib 版本的 long-horizon durability benchmark，分开衡量目标保真度、证明完成率、重开节点数、成本和恢复时间。
- 发布 canonical target statements、收敛后的 blueprint、issue/PR 历史和运行配置，才能更严格地复核论文的成本与并行性结论。
- 研究更强的 source-to-blueprint alignment 检查，避免“类型正确但数学上错位”的声明在 Stage 1 以后才暴露。
- 把 Mathlib 缺口检测与库检索结合起来，区分真正的 source gap、可补的 library gap 和不应形式化的错误目标。
- 评估不同模型、上下文预算、CI 预算和 Refiner 策略对 proof DAG churn 的影响，避免把 GPT-5.5-xhigh 的单一设置当作普适结论。

## 12. 可复现性

论文披露 LeanMarathon 代码仓库为 [github.com/YuanheZ/LeanMarathon](https://github.com/YuanheZ/LeanMarathon)，并给出了输入类型、三次运行的 Table 2/3 统计、CI 七项检查、代理契约和若干失败 issue。论文未披露独立 dataset URL；正文只说明每次运行接收论文 LaTeX source 和 canonical target statements，具体目标文件、提交版本、完整运行日志和环境锁定信息无法从提供文本确认。

因此本页将可复现性评为 **medium**：代码与方法机制公开，且实验条件相对具体，但缺少可由本页确认的完整输入包、数据发布地址和逐次运行 artifact。复现入口和局限也记录于 [[zhang2026-leanmarathon-method]]、[[zhang2026-leanmarathon-results]] 和 [[zhang2026-leanmarathon-critical]]。
