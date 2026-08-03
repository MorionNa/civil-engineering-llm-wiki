---
id: paper--leveque2024-all-at-once-rk-results
title: Leveque et al. (2024)：结果
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
- parallel-scaling
- heat-equation
- stokes
- runge-kutta
legacy_sources:
- raw/papers/leveque2024-all-at-once-runge-kutta.pdf
evidence_scope: local workspace source record pending canonical verification
---

# 结果

论文在热方程和 Stokes 问题上展示了高阶 Gauss、Lobatto IIIC、Radau IIA 的顺序与并行实验。大规模并行表报告明显加速，但需要 FGMRES、内部 GMRES、MGRIT/XBraid 以及多节点 MPI；这些数字不能作为单卡结构动力学推理速度的先验。^[raw/papers/leveque2024-all-at-once-runge-kutta.pdf]

对本项目最有用的实证不是具体加速倍数，而是：高阶 RK 的阶段系统确实是主要计算瓶颈，阶段数和阶段求解器质量必须进入资源门，而不能只按时间 FFT 次数估算。

## Related Pages

- [[sources/papers/leveque2024-all-at-once-rk]]
- [[papers/index]]
