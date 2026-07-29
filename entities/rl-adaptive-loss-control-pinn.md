---
title: "RL Adaptive Loss Control for PINN"
created: 2026-07-29
updated: 2026-07-29
type: entity
tags: [physics-informed, pinn, reinforcement-learning, adaptive-weighting]
sources: [raw/papers/kolzhetsov2026-accelerating-pinn-training-extracted.txt]
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
