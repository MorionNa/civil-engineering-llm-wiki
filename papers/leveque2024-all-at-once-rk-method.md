---
id: paper--leveque2024-all-at-once-rk-method
title: Leveque et al. (2024)：方法
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/leveque2024-all-at-once-rk
created: '2026-08-01'
updated: '2026-08-01'
confidence: low
legacy_tags:
- runge-kutta
- all-at-once
- svd
- schur-complement
legacy_sources:
- raw/papers/leveque2024-all-at-once-runge-kutta.pdf
evidence_scope: local workspace source record pending canonical verification
---

# 方法

对 s 阶 RK，论文同时保留网格状态与每步 s 个阶段导数，形成 2×2 块全时域系统。阶段块在时间步间为块对角，可并行处理；状态 Schur 补再由 MGRIT/XBraid 近似。阶段系统使用 `A_RK=UΣV^T` 的 SVD 预条件，理论分析依赖空间算子性质和 `U^TV` 的谱条件。^[raw/papers/leveque2024-all-at-once-runge-kutta.pdf]

V20 不照搬该迭代器，而只采用“阶段力是独立提升输入”的表示。随后利用经典 RK4 稳定多项式的因式分解，把每个频点化为四个复移位结构系统，避免把整个全时域状态交给 Krylov 迭代。

## Related Pages

- [[sources/papers/leveque2024-all-at-once-rk]]
- [[papers/index]]
