---
type: entity
title: AutoformBot
entity_type: algorithm
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
- entity/model
methods:
- task-DAG planning
- multi-agent orchestration
- isolated git worktrees
- dependency-aware scheduling
- layered evaluation
results:
- framework applied to 26 open-access textbooks
- open-source framework release
failure_modes:
- hidden axioms and sorry chains
- context degradation
- duplicate work
- infrastructure panic
datasets:
- open-access mathematical textbooks
- ATLAS
reproducibility: medium
code_url:
- https://github.com/facebookresearch/autoform-bot
dataset_url: []
id: entity--autoformbot
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
- mathematics-at-scale
- evaluation
- human-in-the-loop
- task-DAG planning
- multi-agent orchestration
- isolated git worktrees
- dependency-aware scheduling
- layered evaluation
- framework applied to 26 open-access textbooks
- open-source framework release
- hidden axioms and sorry chains
- context degradation
- duplicate work
- infrastructure panic
- open-access mathematical textbooks
- ATLAS
- algorithm
- arXiv preprint
sources:
- sources/papers/rammal2026-autoformbot-atlas.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# AutoformBot

^[sources/papers/rammal2026-autoformbot-atlas.md]

## 定义

AutoformBot 是 Ahmad Rammal 等人在 *Formalizing Mathematics at Scale* 中提出并发布的开源多智能体框架。它将教材数学形式化视为 Lean 4 中的协作软件工程项目：orchestrator 建立带逻辑依赖的 task DAG，workers 在独立 git worktrees 中形式化局部目标，reviewers、supervisor、trace analyzer、triage agent 和 merge queue 共同维持质量反馈。

## 论文证据

- 摘要称 AutoformBot 可协调 thousands of LLM agents，配备 formal verification tools、dependency-aware task scheduling 和 collaborative version control。
- Figure 2 展示 textbook orchestrator、task DAG、skill guides、workers、reviewers、trace analyzer、supervisor 和主代码库之间的规划—执行—评价反馈。
- 框架主要使用用户提供的 frontier-model endpoint；论文实验主要由 Opus 4.6 驱动，并用 Gemini 3.1 Pro 做模型比较。
- 工具层包括 Lean REPL、Lean LSP、filesystem/search、Loogle mathlib search、git/worktree、task tracker、job scheduling、trace inspection 和 visualizer。
- 评价 harness 通过编译门控、目标匹配、依赖图、结构标签及 faithfulness/proof integrity/code quality 三类 judges 检查目标。

## 边界与限制

AutoformBot 不是独立的数学真值判定器。Lean kernel 可检查已经给出的形式命题和证明，但自然语言到 Lean statement 的 faithfulness 仍需额外审查。论文记录的风险包括隐藏 axiom、sorry 链、弱化假设、过度简化 manifold 或 scheme、orchestrator fatigue、infrastructure panic 和 Lean 版本不兼容。

论文未披露一个不依赖外部模型服务的统一运行配置；代码开放不代表拥有与论文相同的 frontier-model 权重、endpoint 状态或 provider pricing。

## 关联页面

- 论文总览：[[rammal2026-autoformbot-atlas-analysis]]
- 方法展开：[[rammal2026-autoformbot-atlas-method]]
- 结果证据：[[rammal2026-autoformbot-atlas-results]]
- 共同产物：[[entities/atlas-lean]]

## 官方链接

- Framework: https://github.com/facebookresearch/autoform-bot
- Source paper: https://arxiv.org/abs/2605.29955
