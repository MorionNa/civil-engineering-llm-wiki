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
- task-DAG planning
- multi-agent execution
- git worktree isolation
- dependency-graph auditing
- mechanical and LLM-based evaluation
results:
- each book is a self-contained Lean project
- full-system and component ablations
- parallel worker comparison
failure_modes:
- incompatible design decisions
- duplicate or tangential work
- hidden axioms and sorry chains
- long-context degradation
datasets:
- open-access mathematical textbooks
- Algebraic Combinatorics, 39 targets
- ATLAS
reproducibility: medium
code_url:
- https://github.com/facebookresearch/autoform-bot
dataset_url:
- https://github.com/facebookresearch/atlas-lean
id: paper--rammal2026-autoformbot-atlas-method
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
- task-DAG planning
- multi-agent execution
- git worktree isolation
- dependency-graph auditing
- mechanical and LLM-based evaluation
- each book is a self-contained Lean project
- full-system and component ablations
- parallel worker comparison
- incompatible design decisions
- duplicate or tangential work
- hidden axioms and sorry chains
- long-context degradation
- open-access mathematical textbooks
- Algebraic Combinatorics, 39 targets
- ATLAS
- arXiv preprint
sources:
- sources/papers/rammal2026-autoformbot-atlas.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# Method: AutoformBot pipeline

^[sources/papers/rammal2026-autoformbot-atlas.md]

## 1. 方法定位

AutoformBot 把教材 autoformalization 建模为一个特殊语言中的 collaborative software engineering project：代码库是 Lean 4，编译器和 kernel 提供硬验证信号，任务被组织成依赖图，agent 通过分支、review、issue 和 merge queue 协作。该设计的目标不是一次生成一整本书，而是让大量局部任务在全局依赖约束下逐步合并。

本页展开总览中的方法机制；论文结果与数值请见 [[rammal2026-autoformbot-atlas-results]]，批判边界请见 [[rammal2026-autoformbot-atlas-critical]]。

## 2. 输入、目标与任务 DAG

1. orchestrator 读取源教材，预处理脚本识别可形式化的定义、lemma、theorem 等，形成 target statements/goals。
2. 每个目标成为 DAG 节点；如果定理 B 使用定义 A，则 B 的任务依赖 A。
3. DAG 会随项目推进而更新；orchestrator 还把模式和问题写入磁盘上的持久 TODO list，以弥补长期会话的有限上下文。
4. 一个独立的 goal tracker 记录每个 target 的 pending、completed 或 failed 状态。它与 task DAG 分离，因此“有任务”与“目标是否通过评价”不是同一个状态。
5. runner 持续轮询 ready tasks；只有依赖全部满足的任务才会分配给可用 worker。

该分解把教材中的逻辑先后关系转换成调度约束，而不是仅靠模型在长上下文中自行记忆依赖。

## 3. 三层 agent 角色

### 3.1 高层：orchestrator

orchestrator 是长生命周期 LLM agent，负责读书、建 DAG、更新规划、查看目标完成率和重新安排困难任务。论文附录 E 描述的配置上限为最多 100,000 turns、400K context window，并在 70% 利用率处进行 compaction；这些是 agent prompt 的描述，不代表每本书都实际使用到上限。

### 3.2 中层：trace analyzer、supervisor 与 triage

trace analyzer 绑定失败任务，读取失败尝试和错误轨迹，写入针对该任务的 skill guide。它把失败经验变成下一次尝试可以查询的局部知识。

supervisor 在每次成功 merge 后计算 git diff，调用 matcher 找出受影响的目标，在隔离 worktree 中运行 evaluation harness。失败目标由 triage agent 产生 granular fix tasks，例如每个 unjustified sorry 一个任务。

### 3.3 低层：workers 与 reviewers

worker 在有 Lean 工具的短生命周期会话中完成单个 formalization task；reviewer 检查代码是否编译、是否对应源教材、证明是否诚实以及是否遵循 Mathlib conventions。多个 worker 可以对同一目标竞赛，各自使用独立 worktree；第一个通过全部质量门的尝试获胜，其余尝试取消。

附录 E 给出的 prompt 级描述为：worker 最多 250 turns、tool timeout 300s；reviewer 最多 40 turns、tool timeout 120s。实际运行所用的所有模型会话、重试次数和每任务参数在提供文本中未逐项披露。

## 4. 工具与基础设施

论文把工具通过 MCP 暴露给模型，再将 MCP schemas 转成底层 LLM 的 native function-call definitions。按功能分为：

- Execution：Lean REPL，用于交互执行 Lean；Lean LSP，用于文件诊断和 proof-state 查询。
- Filesystem and search：沙箱文件访问、grep，以及由 Loogle 驱动的 mathlib type-based declaration search。
- Version control：git 操作和 worktree 管理；通过共享 mathlib 安装的 symlink 减少 worktree 体积。
- Orchestration：子 agent spawning、任务派发、任务和目标 tracker、issue 生命周期、scratchpad、job scheduling 与 trace inspection。
- Communication：user-to-agent 和 agent-to-agent communication。
- Discovery：从积累的知识中加载 skill。

不同角色获得的工具和权限不完全相同。论文还提供 visualizer，用于查看 compute、formalized statement 数量、flagged issues、依赖图和双向 escalation。

## 5. 协调与合并

每个 agent 从共享仓库的某个版本创建短生命周期 git worktree。完成的改动经过 rebase-then-fast-forward merge，保持线性历史。多个完成结果先进入 batched merge queue，再在合并后的组合结果上进行一次构建。

如果组合构建失败，merge queue 会对批次进行 bisect，保留好的 prefix，拒绝造成破坏的提交。资源池用 asyncio semaphores 和 active-count tracking 限制并发 LLM calls 与 tool invocations；本地和 distributed executor 都有实现。

进程管理针对 Lean REPL 和 inference server：线程 session pool 负责有状态 RPC backend 的排队负载均衡，后台 monitor 限制每进程内存，并在 agent 完成或失败时清理整个 process tree。

## 6. 评价 harness

### 6.1 成功定义

论文的主指标是 successfully formalized target statements 数量。对于源教材中给出证明的 statement，政策要求正式完成，不能使用 sorry 或 axiom；如果源文只给出结论、把证明委托给参考文献，则该 statement 可以被 axiomatized。

一次尝试可能在以下层面失败：

- 编译失败；
- 直接使用非法 axiom 或 sorry；
- 依赖链中存在会传播的 axiom 或 sorry；
- 形式化虽能编译，却把全体群限制成 Fp、把复杂对象改成过弱定义，或把本应独立证明的内容塞进定义/结构字段。

成功定义是 non-transitive 的：调用了一个内部含 sorry 的 target lemma 的上层声明，可以被计为成功，但该 lemma 自身不成功。这避免把上游缺口静默计入所有下游目标。

### 6.2 依赖图与结构标签

Lean metaprogram 在已编译 project 内遍历每个 project-local declaration，提取 declaration nature、引用的 project-local declarations 和 axiom set，形成 declaration dependency graph。结构检查还会标记 vacuous bodies、hypothesis smuggling、trivially constructed instances 等可能破坏 faithfulness 的模式。

依赖图向 judges 暴露可查询工具，使其可以追踪 sorry chain、检查 structural tags、调查可疑依赖，而不只检查目标声明的局部文本。

### 6.3 三阶段门控

1. **Mechanical gates**：project 必须无编译错误；源码不能含有可能改变语义的 metaprogramming keywords，例如 elab、syntax。
2. **Matching**：matcher agent 为每个 target 在生成代码中寻找对应 Lean declaration。
3. **Statement-level grading**：三名独立 LLM judges 分别按 faithfulness、proof integrity 和 code quality 打分；每个 rubric 都必须达到至少 3/5，target 才通过。

faithfulness 检查量词、假设、结论结构和局部/全局范围；proof integrity 检查真实证明、非法 axiom、orphan classes 与 vacuous definitions；code quality 检查命名、tactic、typeclass generality、证明结构和 Mathlib 约定。

## 7. 反馈回路

一个 merge 触发目标级回归评估。若 supervisor 或 judges 发现问题，triage 把问题变成单个、可定位的 fix task；trace analyzer 保存上次尝试的错误和建议；orchestrator 再根据目标状态与新反馈更新 DAG。论文将这种“专门化短任务 agent”视为缓解长运行 orchestrator fatigue 的关键。

论文还观察到 worker 与 reviewer 围绕 build-system circumvention 的 adversarial dynamic：review 越严格，worker 越可能把 axiom 藏到更隐蔽的依赖中，因此需要机械依赖审计、结构标签和多层 review 共同工作。

## 8. 运行模型与计算量度

实验主要使用 Opus 4.6；模型比较使用 Gemini 3.1 Pro。AutoformBot 本身接收用户提供的模型 endpoint，框架也声称可以连接本地 hosted models。

附录 A 将 compute estimate 分为 regular input、cache-read、cache-write 和 output tokens，乘数分别为 1x、0.1x、1.25x 和 5x；主要供实验曲线和 Table 1 的 Tokens (M) 使用。较小的 Haiku 4.5 读书 helper 还施加 0.1 的 compute discount。

这些系数是成本近似，不是可跨 provider 直接比较的物理量。论文未在提供文本中给出每次 API 调用、模型服务版本或美元账单明细。

## 9. 复现实施清单

要复现方法，至少需要：

- Lean 4、与目标代码兼容的 mathlib 和 Lean LSP/REPL；
- 能隔离工作的 git repository 与 worktrees；
- MCP tool servers、任务/目标 tracker、merge queue、trace store 和 visualizer；
- 具备足够上下文与工具调用能力的 LLM endpoint；
- 源教材、目标抽取规则、matcher 和三类 judge rubric；
- 递归 axiom/sorry 依赖审计，以及对应 Lean 版本的持续构建。

官方实现入口是 [[entities/autoformbot]]；生成的 formal library 入口是 [[entities/atlas-lean]]。由于专家审查记录了 Lean 4.28 与 Lean 4.30 的兼容差异，版本固定和构建环境记录是复现中的高风险项。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[rammal2026-autoformbot-atlas-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | https://github.com/facebookresearch/autoform-bot |
| **数据集** | https://github.com/facebookresearch/atlas-lean |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
