---
id: entities--rl-adaptive-loss-control-pinn
title: RL Adaptive Loss Control for PINN
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- entity/model
- method/pinn
- method/reinforcement-learning
keywords:
- adaptive-weighting
- domain/ai4s
- entity/model
- method/pinn
- method/reinforcement-learning
- physics-informed
- pinn
- reinforcement-learning
sources:
- raw/papers/kolzhetsov2026-accelerating-pinn-training-extracted.txt
created: '2026-07-29'
updated: '2026-07-31'
confidence: high
---

# RL Adaptive Loss Control

RL Adaptive Loss Control 是一种将 PINN 损失权重调整建模为强化学习控制问题的方法。

核心思想：agent 根据训练过程动态修改 PDE、初值和边界条件损失权重，而不是采用固定权重。

## Core mechanism

- state: loss weights
- action: weight perturbation
- reward: 相对于 baseline 的训练领先程度
- agent: DDPG / multi-agent DDPG

## Related

- [[adaptive-loss-weighting-pinn]]
- [[pinn]]
- [[kolzhetsov2026-rl-adaptive-loss-control-analysis]]

## Evidence By Source

### `raw/papers/kolzhetsov2026-accelerating-pinn-training-extracted.txt`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/kolzhetsov2026-accelerating-pinn-training-extracted.txt]
