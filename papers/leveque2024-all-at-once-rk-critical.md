---
id: paper--leveque2024-all-at-once-rk-critical
title: Leveque et al. (2024)：批判性边界
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
- negative-knowledge
- parallel-in-time
- runge-kutta
legacy_sources:
- raw/papers/leveque2024-all-at-once-runge-kutta.pdf
evidence_scope: local workspace source record pending canonical verification
---

# Negative Knowledge

- 全时域 RK 并不自动等于直接求解；论文依靠外层/内层迭代与预条件器。
- 论文分析和实验以热方程、Stokes 为主，不能证明无阻尼振荡结构的长时幅相精度。
- 高阶 A 稳定 RK 的存在不能证明任意阶段系统在单 GPU 上比顺序 RK4 快。
- V20 必须单独验证复移位根、因子条件数、轮廓混叠、四次空间求解成本和严格因果性。

^[sources/papers/leveque2024-all-at-once-rk]

## Related Pages

- [[sources/papers/leveque2024-all-at-once-rk]]
- [[papers/index]]
