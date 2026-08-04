---
type: entity
entity_type: algorithm
title: LeanMarathon
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
- entity/model
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
id: entity--leanmarathon
status: active
project: civil-engineering-llm-wiki
keywords:
- language-agents
- large-language-models
- autoformalization
- formalization
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
- algorithm
- arXiv preprint
sources:
- sources/papers/zhang2026-leanmarathon.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# LeanMarathon

^[sources/papers/zhang2026-leanmarathon.md]

## 定义

LeanMarathon 是 Yuanhe Zhang、Yuekai Sun、Taiji Suzuki、Jason D. Lee 和 Fanghui Liu 在 2026 年 arXiv 论文中提出的长时程 Lean 自动形式化多智能体 harness。它不是单一 prover，而是一套围绕动态 proof DAG、共享 blueprint、契约化代理和确定性 CI gate 的工程编排算法。

## 论文证据

- **共享对象**：一个 Lean blueprint 同时保存形式证明骨架、LaTeX/natural-language proof graph 和代理之间的 system of record。
- **代理分工**：Blueprinter 生成初始骨架；Target-Reviewer 审计 canonical target 与 Lean type；Worker 在单节点局部区域证明；Refiner 修复连接 illness sub-DAG。
- **编排顺序**：Stage 1 先做目标保真度审查；Stage 2 从动态 DAG 叶节点向上并行证明，所有 PR 经过 CI 才能合并。
- **结构约束**：CI 检查编译、节点格式、`latexEnv`、标签、依赖 parity 和 lemma closeness；Worker 的冻结类型和局部 refinement region 限制错误传播。
- **实验结果**：论文报告在两篇研究论文、四个 Erdős 问题上，三次运行完成七个目标定理，累计证明 258 个 lemma/theorem，且无 `sorry`。

## 边界与限制

LeanMarathon 可以隔离和恢复代理错误，但不能替代源论文语义审查，也不能凭空补齐 Mathlib 缺少的代数数论、概率论或分析结果。论文的 unit-distance disproof 失败案例显示，dummy object 可能类型检查却不承载真实数学内容。评估只覆盖两篇分析数论论文和 GPT-5.5-xhigh/Codex 设置；提供文本没有独立 dataset URL、精确 Lean/Mathlib commit 或全量运行 artifact，因此实体复现等级为 medium。

## 关联页面

- 论文总览：[[zhang2026-leanmarathon-analysis]]
- 方法机制：[[zhang2026-leanmarathon-method]]
- 结果证据：[[zhang2026-leanmarathon-results]]
- 批判性边界：[[zhang2026-leanmarathon-critical]]

## 官方链接

- Code: https://github.com/YuanheZ/LeanMarathon
- Source paper: https://arxiv.org/abs/2606.05400
