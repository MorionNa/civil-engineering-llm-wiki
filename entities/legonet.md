---
title: "LegONet"
created: 2026-07-28
updated: 2026-07-28
type: entity
tags: [neural-operator, structure-preserving, operator-learning, operator-splitting]
sources: [raw/papers/2603.07882v1.pdf]
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
