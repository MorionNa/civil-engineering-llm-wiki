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
- multi-agent orchestration
- dependency-aware planning
- proof-dependency audit
- human expert review
results:
- verified Lean library at textbook scale
- model, component, and parallelism ablations
- audited failure cases
failure_modes:
- partial coverage
- hidden or explicit axioms
- semantic misformalization
- context degradation
- version and convention mismatch
datasets:
- ATLAS
- 26 open-access mathematical textbooks
- Algebraic Combinatorics audit
reproducibility: medium
code_url:
- https://github.com/facebookresearch/autoform-bot
dataset_url:
- https://github.com/facebookresearch/atlas-lean
id: paper--rammal2026-autoformbot-atlas-critical
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
- multi-agent orchestration
- dependency-aware planning
- proof-dependency audit
- human expert review
- verified Lean library at textbook scale
- model, component, and parallelism ablations
- audited failure cases
- partial coverage
- hidden or explicit axioms
- semantic misformalization
- context degradation
- version and convention mismatch
- ATLAS
- 26 open-access mathematical textbooks
- Algebraic Combinatorics audit
- arXiv preprint
sources:
- sources/papers/rammal2026-autoformbot-atlas.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# Critical: 贡献、边界与机会

^[sources/papers/rammal2026-autoformbot-atlas.md]

## 1. 贡献判断

论文最重要的贡献不是单个新 theorem prover，而是把教材级 autoformalization 组织成可审计的多智能体软件工程系统。[[rammal2026-autoformbot-atlas-analysis]] 记录了完整的 12 维概览，[[rammal2026-autoformbot-atlas-method]] 展开了 DAG、worktree、merge queue 和评价 harness。

具体贡献可分为四层：

1. **系统层**：把 orchestrator、workers、reviewers、supervisor、trace analyzer 和 triage agent 组合成反馈型 pipeline。
2. **协同层**：用依赖感知调度、隔离分支、并行竞赛和批量合并管理大规模并发。
3. **验证层**：用 Lean build、依赖闭包、结构标签和三类 LLM judges 共同检查“编译”以外的风险。
4. **资产层**：发布 AutoformBot 代码和 ATLAS 形式库，覆盖 26 本开放教材。

## 2. 核心知识

### 2.1 形式验证既是正确性工具，也是协调信号

论文把 Lean kernel 视为对所有 agent 都可见的 sharp coordination signal：局部贡献只有在能构建、通过审查并满足依赖后才进入共享库。因此正式检查器同时承担 proof verification、接口约束和 merge gating 三个角色。

### 2.2 规模化的关键是分层记忆与分层责任

长生命周期 orchestrator 负责全局规划，但失败分析交给 task-scoped trace analyzer；supervisor 负责 merge 后目标级反馈，worker 只处理粒度受控的局部目标。论文的 ablation 表明，去掉不同反馈层会显著改变完成率，但这些数字只来自 Algebraic Combinatorics 的 39-target 消融集。

### 2.3 依赖闭包比局部检查更重要

一个声明可以直接没有 sorry，却依赖含 axiom 的 helper。论文因此递归构建 declaration dependency graph，并把 axiom sets 和 structural tags 暴露给 judges。该思路比只搜索源码中的 sorry 更适合审计长链条 formal library。

### 2.4 规模与质量要分开计量

ATLAS 的 2,855/4,007 成功目标和 483,918 LoC 说明教材级产出在作者的资源配置下可运行；论文同时承认整体质量仍低于 expert-written Lean code。覆盖率、构建成功率、faithfulness、proof integrity、code quality 不应合并成一个“已验证”标签。

## 3. 失败边界

### 3.1 不是完整的 textbook formalization

26 本书的总体覆盖率为 71.3%，且作者在 marginal success 需要指数级更多 compute 时停止。Lie Groups 为 40.0%，Real Analysis 为 98.9%；该跨度说明书目难度与已有 mathlib 基础设施强相关。

### 3.2 kernel acceptance 不等于语义忠实

只要定义、假设或类型被改弱，Lean 仍可能接受一个与教材不同的命题。论文的反例类别包括把“对所有 groups”的命题改成只对 Fp、把 theorem 编码为 definition、把待证明内容塞进 structure field，以及用简化对象替代 manifold 或 scheme。

### 3.3 多层审查仍会留下显式缺口

Appendix G 的专家审查发现示例 Algebraic Combinatorics 项目不能在 Lean 4.30 编译、目标 Lean 4.28，并依赖 youngAdjMatrix_eigenvalues_bridge 与 spectral_trace_pow 两个显式 axiom。该结果说明 evaluation harness 的通过统计需要与独立人类审查并列，而不能被当作最终语义认证。

### 3.4 复现受模型和版本约束

代码和 ATLAS 仓库公开，但实验主要依赖 Opus 4.6，模型通过用户提供 endpoint 接入；论文未在提供文本中披露完整模型服务状态、全部 prompt/config、每次美元账单或可替代的公开权重。Lean 版本、mathlib 版本和跨书 convention 也会影响结果。

### 3.5 成本结论是估计而非统一基准

论文以 token 类型乘数估算 compute，并声称每行代码可能低于专家 annotator；没有提供统一美元成本、同等任务的人类时间基线或跨 provider 的可比价格。因此“经济可行”应读作在作者的 API、折扣和资源配置下的工程判断。

## 4. 可迁移知识

对程序综合、proof assistant、配置验证、科学代码和其他有强检查器的长周期任务，以下模式具有可迁移性：

- 先将源材料拆成带依赖边的目标图，再决定并行度；
- 让短生命周期 worker 在隔离工作区中处理细粒度任务；
- 把失败轨迹写成目标专属知识，而不是让一个长会话承载全部历史；
- 在合并前后都运行机械检查和目标级回归；
- 对产物的依赖闭包进行审计，防止上游缺口被下游成功掩盖；
- 把覆盖率、编译、语义忠实、证明完整性和代码质量分开报告。

不能直接迁移的部分包括 Lean tactic、mathlib API、source-to-target matcher 和教材领域的目标抽取；迁移到 Rocq/Coq、Isabelle/HOL 或其他验证器需要重写工具服务器、证明对象审计和评分 rubric。

## 5. 研究机会

### 5.1 建立跨书全局规划

下一步应把 26 本书作为一个共享依赖图规划，而不是彼此隔离地重复 formalize。可以优先识别 mathlib 缺口、统一命名和跨书重复定义，再将基础设施任务放在上层定理之前。

### 5.2 强化独立语义审计

可将人类专家反馈、dependency graph、structural tags、source provenance 与 checker 输出组合成独立 evaluator，并让审查模型与生成模型使用不同上下文或不同模型族，降低同源错误被自我认可的风险。

### 5.3 做真实成本—延迟—覆盖率研究

需要记录 API provider、缓存、上下文长度、重试、并行 worker 数、wall-clock、美元和目标难度，以复核 Figure 6 中的 token—success 曲线，并分析 3/5 workers 的收益是否只在早期简单任务出现。

### 5.4 研究 formal trajectories 的训练价值

ATLAS 的声明、证明依赖和失败轨迹可能为数学推理模型提供可验证 reward signal。研究应同时检查训练/评测数据重叠、数学陈述污染、axiom 依赖和“证明了错误形式化命题”的风险。

### 5.5 面向高基础设施领域的专门化

论文列出 differential geometry、PDE、manifold、scheme 等更困难方向。可以为这些领域建立可复用定义、decomposition skill guides、版本兼容测试和人类-in-the-loop checkpoint，再比较从零构建与共享基础设施的边际收益。

## 6. 最终评价

在论文提供的证据范围内，AutoformBot 证明了“跨多本教材、带机械检查和多智能体反馈的形式化流水线”可以产生大规模 Lean 资产；它没有证明自动生成库已经达到 mathlib 的完整性、统一标准或专家级语义可靠性。ATLAS 更适合作为可审计、可继续修订的初始资产，而不是无需人工复核的数学真值库。

相关数据资产见 [[entities/atlas-lean]]，算法实体见 [[entities/autoformbot]]。

## 7. 可复现性结论

**🟠 medium**：论文公开了 AutoformBot 和 ATLAS 的 GitHub URL，也公开了整体架构、评价规则、部分 prompt 级配置和代表性代码；但提供文本没有完整披露模型权重/endpoint 状态、每次运行的完整配置、统一美元成本与版本锁定清单。独立复现应先固定 Lean 版本、mathlib commit、模型 endpoint、教材版本和 axiom policy。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[rammal2026-autoformbot-atlas-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | https://github.com/facebookresearch/autoform-bot |
| **数据集** | https://github.com/facebookresearch/atlas-lean |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
