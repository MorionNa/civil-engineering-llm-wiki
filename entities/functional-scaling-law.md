---
id: entities--functional-scaling-law
title: Functional Scaling Law (FSL)
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- entity/model
- method/pinn
keywords:
- deep-learning
- domain/ai4s
- entity/model
- learning-rate-schedule
- method/pinn
- scaling-law
- stochastic-gradient-descent
sources:
- raw/papers/li2025-functional-scaling-laws.pdf
created: '2026-07-28'
updated: '2026-07-31'
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

## Evidence By Source

### `raw/papers/li2025-functional-scaling-laws.pdf`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/li2025-functional-scaling-laws.pdf]
