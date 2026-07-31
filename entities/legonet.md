---
id: entities--legonet
title: LegONet
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- entity/model
- method/neural-operator
keywords:
- domain/ai4s
- entity/model
- method/neural-operator
- neural-operator
- operator-learning
- operator-splitting
- structure-preserving
sources:
- raw/papers/2603.07882v1.pdf
created: '2026-07-28'
updated: '2026-07-31'
confidence: high
---

# LegONet

LegONet 是 Zhang et al. 提出的组合式结构保持神经算子框架。

## 核心思想

区别于为单个 PDE 训练完整模型，LegONet 学习共享表示上的可插拔 operator blocks。

## 关键机制

- boundary-adapted baseplate
- E/H/R structure-preserving blocks
- trajectory-free operator matching
- Strang splitting composition

## 关联

- [[zhang2026-legonet-analysis]]
- [[neural-operator]]

## Evidence By Source

### `raw/papers/2603.07882v1.pdf`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/2603.07882v1.pdf]
