---
id: entity--convolution-quadrature
title: Convolution Quadrature
type: entity
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-01'
updated: '2026-08-01'
confidence: low
legacy_tags:
- spectral-method
- time-marching
- structure-preserving
legacy_sources:
- raw/papers/arxiv_math_0504461v1.pdf
---

# 卷积求积

卷积求积用时间离散符号 (delta(\zeta)) 与 Laplace 域传递函数 (F(s)) 定义离散卷积权重，适合只知传递函数或核具有多尺度/奇异性的系统。

[[schadle2006-fast-convolution-quadrature-analysis]] 给出快速遗忘式实现；[[mtp-mechconv-v2-v18-v19-negative-knowledge]] 记录其在结构动力 V19 中的采用边界；[[structured-state-space-s4]] 是另一类“状态空间到长卷积”路线。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.
