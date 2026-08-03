---
id: entity--structured-state-space-s4
title: Structured State Space Sequence Model (S4)
type: entity
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-01'
updated: '2026-08-01'
confidence: low
legacy_tags:
- sequence-modeling
- spectral-method
- long-horizon-rollout
- parallel-computing
legacy_sources:
- raw/papers/arxiv_2111_00396v3.pdf
---

# S4

S4 是把连续状态空间模型通过 NPLR/DPLR 结构转化为高效长卷积核的序列层。训练可使用 FFT 卷积，生成可切换到状态递推。

在结构动力 PINN 中，它更适合作为共享历史编码器，而不是替代真实矩阵边物理层。参见 [[gu2022-s4-analysis]]、[[mtp-mechconv-v2]] 与 [[schadle2006-fast-convolution-quadrature-analysis]]。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.
