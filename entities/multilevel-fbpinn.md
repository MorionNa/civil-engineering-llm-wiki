---
id: entity--multilevel-fbpinn
title: Multilevel FBPINN
type: entity
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-07-31'
updated: '2026-07-31'
confidence: low
legacy_tags:
- physics-informed
- pinn
- spatial-partitioning
- multi-scale-context
- spectral-bias
legacy_sources:
- raw/papers/10_1016_j_cma_2024_117116.pdf
---

# Multilevel FBPINN

## 定义
多层 FBPINN 在多个尺度的重叠域分解上放置局部网络，通过窗函数求和形成全局解。粗层提供全局通信，细层用局部归一化缓解高频谱偏差。

## 可迁移原则
- 局部化与全局通信必须同时存在；
- 粗层不替代高频细层；
- 扩展性需用强/弱缩放与 wall-clock 共同验证；
- 图结构迁移必须保留矩阵边和本构状态语义。

## 关联
- [[dolean2024-multilevel-fbpinn-analysis]]
- [[fbpinn]]
- [[message-passing-reach-contract]]

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.
