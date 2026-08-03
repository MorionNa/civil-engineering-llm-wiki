---
id: entity--mp-pde
title: Message Passing Neural PDE Solver (MP-PDE)
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
- pde
- time-marching
- autoregressive-rollout
legacy_sources:
- raw/papers/arxiv_2202_03376.pdf
---

# MP-PDE

## 定义
MP-PDE 是 encode-process-decode 图时间推进器，通过相对坐标、状态差和 PDE 参数学习局部更新，并用 temporal bundling 与 pushforward training 缓解自回归分布偏移。

## 与结构动力代理的关系
图条件化和训练分布设计可迁移；严格矩阵边、本构状态、动力平衡与优化数值法速度对照仍需另行实现。

## 关联
- [[brandstetter2022-mp-pde-analysis]]
- [[message-passing-reach-contract]]
- [[unrolled-training]]

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.
