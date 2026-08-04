---
type: entity
title: FormalPhysics
authors:
- Jordan Meadows
- Lan Zhang
- André Freitas
year: 2026
venue: arXiv preprint
tags:
- domain/ai4s
- entity/dataset
methods:
- human-in-the-loop
- autoformalization
- theorem-proving
- lean-4
- mathlib
results:
- benchmark
- evaluation
- formalization
- physics-formalization
failure_modes:
- physics-formalization
- evaluation
- large-language-models
datasets:
- physics
- benchmark
- formalization
- lean-4
reproducibility: medium
code_url:
- https://github.com/jmeadows17/formal-science
dataset_url: []
id: entity--formalphysics
status: active
project: civil-engineering-llm-wiki
keywords:
- physics
- physics-formalization
- formal-science
- benchmark
- evaluation
- formalization
- lean-4
- theorem-proving
- human-in-the-loop
- autoformalization
- mathlib
- large-language-models
- arXiv preprint
sources:
- sources/papers/meadows2026-formalscience.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# FormalPhysics

^[sources/papers/meadows2026-formalscience.md]

方法实体与该数据集的生成关系见 [[entities/formalscience]]；完整管线说明见 [[meadows2026-formalscience-method]]。

## 定义

FormalPhysics 是由 FormalScience 管线构造的 physics formalization benchmark，包含 200 个 university-level physics statements、informal LaTeX solutions 和完整 Lean4 formal proofs。样本主要涉及 quantum mechanics 与 electromagnetism，也包括 Other physics 子域。

## 构造

作者从 Meadows et al. (2024) derivations 中随机选择 200 个例子，使用 5 个 gold-standard statement-proof pairs 形成 few-shot context，按每批 5 个组织为 40 个 prompts。中间结果经过 GPT-5.1 生成/扩展、人工 alignment、Lean4/Mathlib 编译和后处理复编译；正式化阶段使用 GPT-5.1 与 Claude-Opus-4.5。

## 已报告属性

在 Table 2 中，FormalPhysics 平均每个自然语言 statement 含 6.41 ± 2.34 个对象和 6.22 ± 2.13 个公式；FV=100.0%、FQ=73.5%、LP=72.0%、MC=72.5%。论文将其定位为 evaluation benchmark，而非 fine-tuning corpus。

## 边界

FormalPhysics 的高 FV 不等于完整物理语义保持。超过 75% 的 QM proofs 出现 Notational Collapse；Lean4/Mathlib 对 vector calculus、Dirac notation 和部分 calculus 的支持缺口会使形式证明退化为 surrogate mathematics。数据集规模、physics 子域和模型/库版本也限制外推。

## 关联

- 论文总览：[[meadows2026-formalscience-analysis]]
- 结果表与 drift 证据：[[meadows2026-formalscience-results]]
- 生成算法：[[entities/formalscience]]
- 失败边界与研究机会：[[meadows2026-formalscience-critical]]
