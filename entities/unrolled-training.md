---
id: entity--unrolled-training
title: Unrolled Training for Neural Physics Simulators
type: entity
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-07-31'
updated: '2026-07-31'
confidence: low
legacy_tags:
- sequence-modeling
- time-marching
- autoregressive-rollout
- long-horizon-rollout
legacy_sources:
- raw/papers/10_1016_j_cma_2024_117441.pdf
---

# Unrolled Training

## 定义
展开训练在训练阶段连续调用神经模拟器，使模型看到部署时会遇到的自预测状态。它可分为单步 ONE、截断时间梯度的 NOG 和完整反向传播的 WIG。

## 关键判断
- NOG 主要处理训练/部署状态分布偏移；
- WIG 额外利用长程梯度，但显存、可微求解器和稳定性要求更高；
- 它针对自回归闭环，不应未经验证迁移到整段时间并行算子。

## 关系
- [[list2025-unrolled-training-analysis]]
- [[mp-pde]]
- [[neural-operator]]

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.
