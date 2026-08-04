---
type: paper-analysis
title: 'FormalScience: Scalable Human-in-the-Loop Autoformalisation of Science with
  Agentic Code Generation in Lean'
authors:
- Jordan Meadows
- Lan Zhang
- André Freitas
year: 2026
venue: arXiv preprint
tags:
- domain/ai4s
- evidence/paper
methods:
- human-in-the-loop
- autoformalization
- theorem-proving
- lean-4
- mathlib
- language-agents
results:
- benchmark
- evaluation
- formalization
- physics-formalization
failure_modes:
- large-language-models
- physics-formalization
- theorem-proving
- evaluation
datasets:
- physics
- benchmark
- formalization
- lean-4
reproducibility: medium
code_url:
- https://github.com/jmeadows17/formal-science
dataset_url: []
id: paper--meadows2026-formalscience-method
status: active
project: civil-engineering-llm-wiki
keywords:
- formal-science
- autoformalization
- formalization
- theorem-proving
- proof-assistant
- lean
- lean-4
- mathlib
- physics-formalization
- physics-reasoning
- scientific-reasoning
- large-language-models
- language-agents
- human-in-the-loop
- benchmark
- evaluation
- physics
- arXiv preprint
sources:
- sources/papers/meadows2026-formalscience.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# FormalScience：方法机制

^[sources/papers/meadows2026-formalscience.md]

本文展开分析页的第 5 维。总览见 [[meadows2026-formalscience-analysis]]；实验结果见 [[meadows2026-formalscience-results]]；算法实体见 [[entities/formalscience]]。

## 1. 输入、假设与目标

论文把输入写成一组 informal proofs D，以及 5 个 gold-standard statement-proof pairs 的集合 D′。在 physics 实例中，D 来自 Meadows et al. (2024) 的 derivations；作者随机选取 200 个样本、按 5 个一批分组。目标不是只生成形式语句，而是得到三元组：

$$
Z=\{(Q,A,C):L(C)=(0,\epsilon)\},
$$

其中 Q 是 informal question/statement，A 是 expanded informal answer/proof，C 是 Lean4 formal proof，L 是 Lean 编译器。论文正文用 S/P 表述，附录算法用 Q/A 表述；二者分别对应 informal statement/proof。

## 2. Stage 1：非形式问答生成与对齐

### 2.1 Few-shot 扩展

few-shot template T_fs 将 gold pairs 作为上下文，要求 LLM：

- 为 equation-only derivation 生成物理上正确、上下文丰富的 question；
- 扩展答案，加入细粒度推导步骤、物理语境和标准 LaTeX；
- 维持问题与答案的语义对应。

每个 batch 含 5 个 derivations，自动生成 40 个 few-shot prompts。论文使用 GPT-5.1 thinking mode 生成中间数据；每个 raw output 交替包含 Q1–Q5 与 A1–A5，之后由 post-processing script 拆成 5 个字典，字典保留 field、question、answer。

### 2.2 人工对齐门

领域专家检查每一批 statement-proof alignment。若不接受，继续在同一会话中要求 GPT 改进；只有在专家认可后，样本才进入 Lean 形式化阶段。这一门控把“LLM 生成了一个看似合理的问题”与“问题确实对应输入 derivation”区分开来。

## 3. Stage 2：Lean 代码生成和编译纠错

### 3.1 编译器反馈

Lean4 + Mathlib 被定义为工具 L：

$$
L(C)=
\begin{cases}
(0,\epsilon),& C\text{ compiles}\\
(1,e),& \text{otherwise}
\end{cases}
$$

第一次代码由 formalisation prompt T_g 生成：

$$
C^{(0)}=M'(T_g(x)).
$$

若编译失败，correction template T_c 将输入 x、当前代码 C^(t) 和 fatal error e 交给多轮 LLM agent：

$$
C^{(t+1)}=M'(T_c(x,C^{(t)},e)).
$$

成功时停止，得到 C=C^(t*)。论文强调会移除非 fatal warnings，以节约上下文；没有把 sorry 或 axiom 当作完整证明。

### 3.2 两种实现入口

约三分之一样本通过 ChatGPT interface 处理：人工复制代码、在 Lean 中编译、把原始错误贴回同一会话。单个初始 formalisation prompt 大约需要 1–2 小时和多轮提示，这一耗时是论文对该操作流程的报告。

其余样本通过 Claude Code（VSCode）处理。作者编写自定义 Python Lean compilation script，把使用方式和错误处理说明追加到 prompt；同时保存 exact formalisation prompt，减轻 context-window compactification 对后续 alignment 的影响。

## 4. Stage 3：形式语言 alignment

编译成功仍不表示语义正确。论文定义由 LLM 辅助的 alignment analysis，并让人类专家对其作二分类：

$$
H^{(k)}=H(M'(T_g(x),C^{(k)}))\in\{0,1\}.
$$

H=0 表示专家接受当前 alignment；H=1 表示拒绝。若拒绝，固定 prompt P_g 要求根据 alignment analysis 改进 formal code，然后重新执行编译纠错循环 R。最大 patience P=3：

$$
C^{(k+1)}=R\left(M'\left(M'(T_g(x),C^{(k)}),P_g\right)\right).
$$

这一循环的关键不是让编译器判断物理意义，而是将“formal code 是否仍表达 A1–A5 和 acceptance criteria”交给 domain expert。

## 5. Stage 4：拆分、后处理与最终复核

每个 Stage 3 输出含 C1–C5，且 5 个 proof 共用顶部 Mathlib imports。Python script 将它们拆成 5 个文件，再统一 question、informal answer、formal proof 和 physics subdomain，形成 200 条数据。

拆分可能引入新的语法或 import 错误，因此作者对每个 C 重新运行 L。若失败，就回到 Stage 3，并把 prompt 改成一次只处理一个 Q/A/C；修正后的例子再写回数据集。这一步把“原始生成能编译”和“后处理后的独立样本能编译”分开验证。

## 6. 无人工 alignment 的 agentic 对照

论文另实现一个面向 consumer-grade hardware 的 CodeAgent pipeline，基于 smolagents 和 ReAct。它不执行 FormalScience 的人工 H gate，目标是通过 test-time scaling 同时提高编译率和 alignment。

### 6.1 Initial generation 与 surface guard

初始生成最多尝试 N=25 次。LLM 输出先经 extract 去除 Markdown fences，再经 surface guard G 检查：

- forbidden tokens 或不兼容的 physics notation；
- 不完整证明标记 sorry、axiom；
- 注释分隔符是否配对；
- imports 是否按要求排序。

guard 失败时，把 rejection reason 加入 regeneration template T_r；通过后才允许进入 Lean 编译。

### 6.2 错误分类与修复策略

编译循环最多 N_max=25 步。编译错误被映射到六类：

syntax、unknown_id、missing_module、type_mismatch、unsolved_goals、other。

前三类是 structural errors，触发 base LLM 的全文件 regeneration；后三类是 semantic errors，交给 patch agent，用带行号的最小 unified diff 修改当前代码。结构错误意味着整体理解或 imports 可能不对，语义错误则更可能只需局部 tactic/expression 修复。

### 6.3 ReAct 工具循环

CodeAgent 的一次循环通常包含 planning、tool-calling action 和 observation。结构修复使用 compiler error category 与 message；语义修复使用 apply_unified_diff。若 25 步内仍失败，算法返回 best-effort 的最后代码，而不是宣称完整证明。

## 7. 评估接口

论文把 Statement Autoformalisation 定义为 sNL → sFL；formal proof 对应 pNL → pFL。Formal validity（FV）由 Lean4 theorem prover 判定。Formal quality（FQ）、logical preservation（LP）和 mathematical consistency（MC）由 LLM-as-a-judge 二分类并在样本上取百分比。

主 judge 是 GPT-4.1-mini，temperature=0.2；独立 robustness judge 是 Qwen2.5-Coder-7B-Instruct。论文还比较 zero-shot、self-refinement 和 agentic pipeline，并在 FormalScience 行使用 GPT-5.1 / Claude-4.5 构造数据。

## 8. 方法边界

FormalScience 具有可迁移的管线骨架，但它依赖少量 gold prompts、专家 alignment、可运行 Lean/Mathlib 环境和足够上下文。它没有解决 Lean4 对 vector calculus 与 Dirac notation 的原生表达缺口；因此 Stage 3 的“对齐”可能只能接受一个编译成功的 surrogate。关于这种 drift 的类别和保证，见 [[meadows2026-formalscience-critical]] 与 [[entities/formalphysics]]。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[meadows2026-formalscience-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | https://github.com/jmeadows17/formal-science |
| **数据集** | 无外部数据集 URL（或使用论文内/合成数据） |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
