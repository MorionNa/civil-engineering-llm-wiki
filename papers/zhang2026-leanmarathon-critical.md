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
id: paper--zhang2026-leanmarathon-critical
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
# LeanMarathon 批判性页面：贡献、边界与可迁移研究机会

^[sources/papers/zhang2026-leanmarathon.md]

> 本页合并论文第 7–11 维。可核对的统计见 [[zhang2026-leanmarathon-results]]，方法合同见 [[zhang2026-leanmarathon-method]]，总览与复现等级见 [[zhang2026-leanmarathon-analysis]]；算法实体见 [[entities/leanmarathon]]。

## 1. 贡献判断

### 1.1 论文明确展示的贡献

1. **问题重心的转移**：把研究级自动形式化的主要困难从“单个 lemma 是否足够难”转向“长时运行能否保持目标和状态一致”。
2. **动态 proof DAG**：不把初始 decomposition 当成可信真理，而让图在拆分、修复和底向上证明中演化。
3. **可恢复的故障隔离**：四类 contract-scoped agent、局部编辑区域、确定性 CI gate 和 PR/issue 流把错误限制为可拒绝的 patch 或局部 issue。
4. **双重记录与 parity**：同一个 blueprint 同时保存 Lean 声明、LaTeX proof prose 和依赖图，结构检查要求两种依赖边一致。
5. **源感知维修**：Refiner 必须读取 source proof，并把 illness area 区分为 blueprint drift 或 source gap。
6. **研究级示范**：论文报告两篇研究论文、四个 Erdős 问题、七个目标定理在三次运行中无 `sorry` 完成，共 258 个 proof nodes。

### 1.2 贡献的证据边界

这些贡献主要由系统设计、三次运行、消融、案例分析和 Aristotle 对照支持。文本没有提供跨模型、跨数学领域、跨 Lean/Mathlib 版本的系统性统计，也没有公开可核对的独立数据集 URL。因此，“harness 设计有效”比“LeanMarathon 普遍优于其他自动形式化系统”更接近论文证据所能支持的表述。

## 2. 核心知识

- **共享状态要可检查**：把 blueprint 作为唯一 system of record，减少代理之间隐性上下文和 compaction 后状态不一致。
- **目标审查必须早于大规模证明**：错误 root theorem 会使所有下游计算失去价值，Target-Reviewer 的只读角色是成本控制而不是形式装饰。
- **局部事务比单体长会话更易恢复**：Worker 只证明一个 dynamic leaf，Refiner 只修复最小 connected sub-DAG，CI 负责机械合并。
- **失败证据可以反过来改进数学**：论文报告 `1 ≤ 0`、`4/3 ≤ 2/3` 等编译/实例化冲突，以及 `Summable` 缺失、real/`ENNReal` 语义错误等问题被转化为具体修复。
- **论文压缩语句是形式化成本热点**：“routine calculation”和“an induction gives”在 #1217 中扩展成许多显式分析、概率和测度论引理。

## 3. 失败边界

### 3.1 目标语义仍不是自动保证

CI 能检查 elaboration、命名、依赖 parity 和 lemma closeness，但它不独立证明 Lean type 与源论文的自然语言意图相同。Target-Reviewer 和源证明访问权承担了额外的语义保真职责；若 canonical target 本身有误，形式系统可以忠实地证明错误目标。

### 3.2 数学库覆盖是硬边界

unit-distance disproof 的失败运行用 dummy number-field record 获得了可类型检查的局部对象，却无法提供真实几何证明所需的代数数论。这个反例说明 harness 不会自动创造缺失的库定理；类型检查通过也可能只是错误抽象下的空壳成功。

### 3.3 源盲 Refiner 会导致漂移

消融中，Refiner 看不到 source proof 时会把 issue 当作开放式建构问题，生成源论文没有的 machinery，约十二天后仍有 26 个 `sorry`。论文因此把 source access 作为修复契约的一部分，而不是可有可无的上下文增强。

### 3.4 长度预算不是合理停止规则

早期 Worker 以固定 physical-line budget 为“无法形式化”的理由，14 个 issue 引用该预算；当前版本要求 issue 给出具体的错误声明、反例、Lean contradiction 或 invalid input，并允许在局部区域长出 refinement DAG。由此可见，规模大不等于失败，缺少可证伪的 stopping rule 才是问题。

### 3.5 实验外推有限

评估集中在分析数论的 Erdős 问题，运行代理是 Codex/GPT-5.5-xhigh，baseline 是论文可访问的 Aristotle。提供文本无法确认公平的模型预算、精确版本和所有原始 artifact，因此不应将表 6 的胜负直接外推为一般 prover 排名。

## 4. 可迁移知识

### 4.1 对长时程科学代理的迁移

可以把“共享事实—局部编辑—外部验证—可合并事务”迁移到科学代码、实验工作流和结构化文献推理。关键不是照搬四个 agent 名称，而是明确每个 agent 的输入、输出、不可编辑区域和失败交付格式。

### 4.2 对知识图与执行图的迁移

自然语言说明和可执行依赖图并置，能让“解释中的依赖”与“系统实际依赖”接受一致性检查。对其他系统，可对应为文档边与数据/代码调用边的双向 parity，并用 orphan-node 检查发现漂移。

### 4.3 对验证闭环的迁移

低成本反驳、编译器/静态检查、独立审查和图级维修应承担不同角色：反驳用于尽早否定，编译器用于确定性筛选，审查用于语义保真，维修用于最小范围重构。任何单一信号都不应代替全部四者。

## 5. 研究机会

以下是基于论文边界提出的后续问题，不是本文已完成的实验结果：

1. **Durability benchmark**：收集跨领域论文、canonical targets、blueprint、PR/issue trace，公开目标漂移率、reopen 次数、故障恢复时间、CI 通过率和成本。
2. **Alignment verifier**：把源论文段落、LaTeX statement、Lean type 和 downstream use 组成可审计 provenance，减少“有效但无关”的定理。
3. **Library-gap triage**：自动区分 source gap、Mathlib 缺口、模型检索失败与目标错误，并为每类缺陷安排不同的恢复路径。
4. **预算与并行度研究**：在固定数学任务上改变 Worker 并行度、`maxHeartbeats`、Refiner 频率和上下文预算，测量成本—可靠性曲线。
5. **人机协作审查**：研究人类只审查根目标/高风险 illness area 是否足以替代逐节点人工检查，同时保留可停止、可回滚的安全边界。
6. **跨库和跨模型复核**：锁定 Lean/Mathlib commit，比较不同模型与 prover，并发布完整输入和输出 artifact，使“系统设计贡献”与“特定模型收益”可分离。

## 6. 复现与证据风险

代码 URL 已由论文披露为 [https://github.com/YuanheZ/LeanMarathon](https://github.com/YuanheZ/LeanMarathon)。论文给出代理契约、CI 检查、三次运行的统计和若干 issue 机制，但未在提供文本中给出独立数据集地址、完整 canonical target 文件、精确环境 commit 或全量 PR/issue 归档。

因此 frontmatter 使用 `reproducibility: medium`：方法足够具体，可以理解并尝试重建 harness；但无法仅凭提供文本声称一次无歧义的端到端复现。结果数字应以 [[zhang2026-leanmarathon-results]] 的表格位置为锚，不能脱离运行和表内口径使用。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[zhang2026-leanmarathon-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | https://github.com/YuanheZ/LeanMarathon |
| **数据集** | 无外部数据集 URL（或使用论文内/合成数据） |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
