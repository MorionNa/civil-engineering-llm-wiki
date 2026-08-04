---
type: entity
title: FormalScience
authors:
- Jordan Meadows
- Lan Zhang
- André Freitas
year: 2026
venue: arXiv preprint
tags:
- domain/ai4s
- entity/model
methods:
- human-in-the-loop
- autoformalization
- theorem-proving
- lean-4
- mathlib
- language-agents
results:
- formalization
- evaluation
- benchmark
failure_modes:
- large-language-models
- physics-formalization
- evaluation
datasets:
- physics
- benchmark
- formalization
reproducibility: medium
code_url:
- https://github.com/jmeadows17/formal-science
dataset_url: []
id: entity--formalscience
status: active
project: civil-engineering-llm-wiki
keywords:
- formal-science
- autoformalization
- human-in-the-loop
- language-agents
- theorem-proving
- proof-assistant
- lean-4
- mathlib
- scientific-reasoning
- formalization
- evaluation
- benchmark
- large-language-models
- physics-formalization
- physics
- arXiv preprint
sources:
- sources/papers/meadows2026-formalscience.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# FormalScience

^[sources/papers/meadows2026-formalscience.md]

## 定义

FormalScience 是 Meadows、Zhang 与 Freitas 提出的 domain-agnostic、human-in-the-loop agentic semi-autoformalisation pipeline。它把 informal scientific reasoning 转换为 Lean4 formal code，并将编译正确性与领域专家的 semantic alignment 判断分开处理。

## 机制

1. 用少量 gold statement-proof pairs 对 equation-only derivations 做上下文扩展。
2. 用 Lean4 + Mathlib 编译代码，并把 fatal errors 返回给 LLM 迭代纠正。
3. 由领域专家判断 formal code 是否仍与 informal statement/proof 对齐，最多 patience=3。
4. 拆分独立 proof、重新编译并修复后处理错误。

## 证据

FormalScience 在论文的 physics 实例中生成 200 个 FormalPhysics examples；论文报告 FormalScience 产物的 FV 为 100.0%。代码地址为 https://github.com/jmeadows17/formal-science。论文没有在提供文本中给出单独的数据集 URL。

## 边界

该算法的“可扩展”和“domain-agnostic”是设计目标；经验结果只覆盖 physics。它不能自动补齐 Lean4/Mathlib 对 vector calculus、Dirac notation 和部分 calculus 的库缺口，因此高 FV 可能伴随 Notational Collapse 或 Abstraction Elevation。

## 关联

- 论文总览：[[meadows2026-formalscience-analysis]]
- 方法展开：[[meadows2026-formalscience-method]]
- 产出数据集：[[entities/formalphysics]]
- 结果与失败边界：[[meadows2026-formalscience-results]]、[[meadows2026-formalscience-critical]]
