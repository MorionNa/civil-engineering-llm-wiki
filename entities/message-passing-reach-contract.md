---
id: entity--message-passing-reach-contract
title: Physics-Guided Message-Passing Reach Contract
type: entity
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-07-31'
updated: '2026-07-31'
confidence: low
legacy_tags:
- message-passing
- physics-simulation
- spatial-partitioning
legacy_sources:
- raw/papers/10_1016_j_cma_2025_118476.pdf
---

# Message-Passing Reach Contract

## 定义
在每个预测/算子更新中，图消息的有效传播范围必须不小于该更新所需的物理影响范围；否则模型处于 under-reaching，增加宽度无法弥补缺失的信息路径。

## 工程化
- 细层：用波速、时间尺度和构件尺度给出局部下界；
- 子图：halo 覆盖实际 receptive field；
- 大域：用粗层图或分区摘要缩短远距离路径；
- 验证：固定参数量改变消息迭代，检查阈值与误差饱和。

## 关联
- [[tesan2025-under-reaching-analysis]]
- [[mp-pde]]
- [[multilevel-fbpinn]]

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.
