---
title: "Functional Scaling Law (FSL)"
created: 2026-07-28
updated: 2026-07-28
type: entity
tags: [scaling-law, deep-learning, stochastic-gradient-descent, learning-rate-schedule]
sources: [raw/papers/li2025-functional-scaling-laws.pdf]
confidence: high
---

# Functional Scaling Law

Functional Scaling Law (FSL) 是 Li et al. (NeurIPS 2025) 提出的训练轨迹级 scaling law。

## 核心思想

传统 scaling law 预测最终 loss；FSL 用函数形式描述整个训练过程。

## 关键概念

- intrinsic time：学习率调整后的有效训练时间；
- forgetting kernel：描述随机噪声随训练过程消散的记忆核；
- signal learning：有效知识/信号提取过程；
- noise accumulation：随机梯度噪声影响。

## 关联

- [[li2025-functional-scaling-laws-analysis]]
- [[wang2021-pinn-ntk-failure-analysis]]
- [[li2026-sgno-analysis]]
