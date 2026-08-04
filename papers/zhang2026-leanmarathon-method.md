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
- local-refinement-DAG
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
id: paper--zhang2026-leanmarathon-method
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
- local-refinement-DAG
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
# LeanMarathon 方法机制：用动态 blueprint 管理长时程 Lean 形式化

^[sources/papers/zhang2026-leanmarathon.md]

> 本页展开论文第 5 维“方法机制”。论文原始来源为 [arXiv:2606.05400](https://arxiv.org/abs/2606.05400)；代码 URL 为 [github.com/YuanheZ/LeanMarathon](https://github.com/YuanheZ/LeanMarathon)。总览见 [[zhang2026-leanmarathon-analysis]]，结果见 [[zhang2026-leanmarathon-results]]。

## 1. 核心抽象：blueprint 是 system of record

LeanMarathon 不把代理之间的持久状态放在隐藏内存中，而是把所有耐久的数学状态写入一个 Lean blueprint 文件。文件同时承担三种角色：

- **形式证明骨架**：保存定义、lemma/theorem 声明和当前证明体。
- **自然语言证明图**：每个节点旁保存 LaTeX statement、标题和 proof prose，并用 `\cref{...}` 表示意图依赖。
- **代理任务接口**：代理读取同一文件，按契约只对自己的区域进行审查、证明或维修。

一个 proof node 是带结构化 `@[blueprint ...]` 属性的 Lean declaration。属性字段包括 statement、proof、title 和 `latexEnv`。例如论文给出的节点形态是：

```lean
@[blueprint "lem:weighted-tail-bound"
  (statement := /-- LaTeX statement text -/)
  (proof := /-- LaTeX proof prose with \cref{...} citations -/)
  (title := /-- one-line LaTeX title -/)
  (latexEnv := "lemma")]
lemma weighted_tail_bound ... : ... := by
  sorry_using [aux_lemma_one, aux_lemma_two]
```

节点有三种证明体状态：`by sorry`；带有预期依赖列表的 `by sorry_using [...]`；以及完整 Lean proof。定义被视为全局上下文，不计入 proof DAG 的节点统计。

依赖图不是只由 prose 推测：Lean elaborator 提供实际的声明依赖，验证器要求每条 elaborator 边都在 `\cref` 中出现，且每条 lemma/theorem `\cref` 都对应实际 Lean 依赖。`sorry_using` 只能引用前面已经出现的 proof node。这种双向 parity 使自然语言图与类型图不能静默分叉。

## 2. 四类 contract-scoped agents

| Agent | 输入 | 输出 | 允许编辑 | 主要暴露/包含的故障 |
|---|---|---|---|---|
| **Blueprinter** | source proof、canonical statements、blueprint | 初始骨架 PR，证明体为 placeholder | 整个骨架的构造 | 分解过粗、repair radius 过大 |
| **Target-Reviewer** | canonical statements、blueprint | issue 或 clean review | 只读，不编辑 | 形式上有效但目标错误 |
| **Worker** | canonical statements、blueprint | proof PR 或 issue | 一个节点的 prose、proof body 和 local refinement region | 局部证明失败、静默证明错误节点 |
| **Refiner** | source proof、canonical statements、open issues、blueprint | 一个连接 illness sub-DAG 的 repair PR | 全 blueprint，但受 repair 决策规则约束 | blueprint drift、source gap |

这种分工不是按模型能力划分，而是按可检查的输入/输出和失败模式划分。尤其 Target-Reviewer 不得编辑 blueprint，因此不能在审查时偷偷把目标改成容易证明的形式。

## 3. Blueprinter：先构造可修复的骨架

Blueprinter 读取源证明和 canonical target statements，生成所有声明都能 elaborate 的初始 Lean 文件；证明体先使用 `sorry` 或 `sorry_using`。它的任务是选择足够忠实、足够局部的分解，而不是在第一步修复源论文。

论文把这一任务描述为 repair-radius optimization：如果某个声明以后被发现错误，预计需要改动的下游声明数量应尽量小。Blueprinter 提交一个骨架 PR 后退出，由 stop hook 监测 PR/CI 状态；数学修复明确交给后续 Refiner。

## 4. Target-Reviewer：在大规模证明前审计目标保真度

Reviewer 对每个目标定理比较三件事：canonical target statement、blueprint 中保存的 LaTeX statement，以及 Lean type。检查对象包括假设、量词、定义、结论和数学角色是否一致。

如果审查干净，编排器进入 Stage 2；如果发现目标错位、缺少假设、错误依赖或其他 blueprint 缺陷，Reviewer 只提交 grouped issue。Refiner 修复并通过 CI 后，Reviewer 再次审查，直到所有 target review clean。这样可以把最昂贵的错误——证明了一个非目标定理——尽量前移拦截。

## 5. Worker：一个动态叶节点的四阶段流程

每个 Worker 获得当前同一 frozen substrate commit，以及一个目标节点和其机械限定的编辑区域。它按四个有序阶段工作：

### 5.1 Misformalization audit

Worker 把 Lean type 当作可疑规格，先和 blueprint prose 对照，再检查节点存在的原因、下游使用者和所需事实。如果缺假设、结论错误、抽象不合适，或声明与 proof DAG 中的角色不符，Worker 停止证明并提交 issue。

### 5.2 Cheap falsification

如果声明允许有限、数值或边界测试，Worker 先尝试反驳。找不到反例只表示低成本 sanity check 通过，不能当作证明；一旦发现反例或可疑边界，就以证据提交 issue。

### 5.3 Statement polish

在类型通过前两阶段后，Worker 可以只编辑节点的 LaTeX statement、title 和 proof prose，使自然语言与冻结的 Lean type 精确一致，不能借机改变类型。

### 5.4 Formalization

Worker 在冻结 Lean type 的前提下替换 placeholder proof body。若需要辅助引理，只能在目标节点之前的 local refinement region 中新增；辅助节点必须依赖已经可见的声明或更早的局部辅助节点，并以目标节点作为唯一终点。

编辑约束由论文所述的 patch MCP server 机械执行：Worker 不能触碰目标类型或无关节点。不同 Worker 的区域互不相交，因此成功 patch 在构造上可交换；失败 patch 只能成为被拒绝的局部变更或诊断 issue。

## 6. Refiner：用 illness area 修复图级缺陷

Refiner 处理 Reviewer 或 Worker 提交的问题。它先用 dag-tracker 找到受影响的最小连接子图，称为 illness area，然后将缺陷分类为：

- **Blueprint drift**：blueprint 已偏离源证明，例如声明错误、依赖错误或 prose 不再描述 Lean declaration。
- **Source gap**：源证明本身不完整、含糊或在形式化所需层面为假。

修复时，Refiner 逐节点决定保留或降级证明体。新节点先保持 placeholder；已有 placeholder 按新依赖集合对齐；已有完整 tactic proof 若修复后仍能编译则保持字节级不变，否则整体替换为 placeholder。编译器而不是代理决定“仍能编译”与否，Refiner 不得对完整证明体进行部分协商式修改。

如果修改了父节点声明，相关下游完整证明会被整体降级，交由后续 Worker 重新证明。这样牺牲局部复用，换取依赖变化后不会留下未经核验的陈旧 proof body。

## 7. 两阶段编排

### Stage 1：Cold Start / Target Review

1. Blueprinter 生成初始 blueprint。
2. CI 验证 Lean build、节点格式、依赖和其他结构约束。
3. Target-Reviewer 比较 canonical target、LaTeX 和 Lean type。
4. clean review 直接进入 Stage 2；否则形成 grouped issue。
5. Refiner 提交 repair PR，PR 通过 CI 并合并后重复审查。

Stage 1 只有在目标陈述被认证为 faithful 后结束。

### Stage 2：DAG-orchestrated proof discharge

每轮以当前 `main` 为 system of record，重新提取 proof DAG，寻找“尚未证明但其依赖已证明”的 dynamic leaves。编排器给每个叶节点分配独立 Worker；Worker 并行运行并提交 proof PR 或 issue。

所有 proof PR 只能经过 CI gate 才能进入 `main`。通过且不冲突的 PR 直接 squash-merge；失败 PR 被拒绝并保留诊断。每轮 Worker 结束后，Refiner 处理累计 issue，提交同一 CI 路径的 repair PR。循环直到所有 proof nodes 都有完整 proof，且 blueprint 不再含 placeholder。

## 8. CI gate 的七项结构检查

论文 §3.3 列出以下检查：

1. Lean compilation：诊断必须为空，或只允许声明使用 `sorry` 的 warning。
2. Node well-formedness：每个 `@[blueprint]` 的 statement/title/proof 非空；placeholder 必须是多行 `sorry` 或 `sorry_using`，不允许不完整 proof body。
3. `latexEnv` consistency：Lean 关键字与 `latexEnv` 一致，例如 lemma 对 lemma、theorem 对 theorem。
4. Label-name normalization：`lem:foo-bar` 等 blueprint label 规范化后必须对应真实 Lean 名称。
5. Unique labels：每个 blueprint node 的 Lean 命名唯一。
6. Proof-dependency parity：Lean elaborator 依赖与 prose `\cref` 双向一致；`sorry_using` 只能指向前序 proof node。
7. Lemma closeness：每个非终端 lemma 必须被之后的 lemma 或 theorem 引用；终端 theorem 可无后继。

前六项保护可编译性、命名和图的一致性，第七项用结构方式拦截漂移产生的 orphan lemma。CI 的定位是接口和结构验证，不替代对数学语义的目标审查。

## 9. 长时运行的恢复机制

- **Stop hook**：代理声明完成后，stop hook 检查 `delivery.yml`；若已开 PR，则轮询成功合并或 CI 失败，失败时把 verifier comment 和原始 job log 重新注入调试上下文。
- **Bounded scope**：契约、patch server、只读 sandbox 和 path allowlist 联合限制每个代理可以编辑的路径和 span；最坏结果应是 rejected patch，而不是 poisoned PR。
- **On-disk communication**：代理之间只通过 blueprint 和 GitHub PR/issue 流传递状态，没有隐藏 scratch memory 或进程内共享通道。
- **Deterministic compute**：论文在运行中把 Lean 的 `maxHeartbeats` 从 0 改成固定 500K，减少无界 `nlinarith`、`simp`、`aesop` 搜索造成的粗粒度超时；这属于实验中根据 trace 观察做的 harness 调整。

## 10. 方法边界

该架构能组织缺陷、缩小修复半径并暴露 Mathlib 缺口，但不能凭空提供缺失的代数数论或概率分析。方法的详细实验验证见 [[zhang2026-leanmarathon-results]]，失败边界和可迁移启示见 [[zhang2026-leanmarathon-critical]]，算法实体见 [[entities/leanmarathon]]。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[zhang2026-leanmarathon-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | https://github.com/YuanheZ/LeanMarathon |
| **数据集** | 无外部数据集 URL（或使用论文内/合成数据） |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
