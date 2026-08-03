---
id: paper--melenk2021-rkcq-superconvergence-method
title: Melenk & Rieder (2021)：方法
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/melenk2021-rkcq-superconvergence
created: '2026-08-01'
updated: '2026-08-01'
confidence: low
legacy_tags:
- rkcq
- radau-iia
- laplace-domain
legacy_sources:
- raw/papers/melenk2021-rkcq-superconvergence.pdf
evidence_scope: local workspace source record pending canonical verification
---

# 方法

论文使用矩阵值 RK-CQ 符号，并假设 RK 方法 A 稳定、系数矩阵可逆、stiffly accurate，且稳定函数在非零虚轴满足严格衰减。收敛阶由经典阶 p、阶段阶 q 和 Laplace 域算子增长指数共同决定。通过把 Dirichlet-to-Neumann 算子分解为阻抗算子与恒等项，解释了对输入求导后出现的超收敛。^[raw/papers/melenk2021-rkcq-superconvergence.pdf]

V20 使用显式经典 RK4 的精确离散多项式，并不满足论文的 A 稳定/stiffly accurate 假设；其正确性只能来自“与教师同一 RK4 的代数等价”，不能引用该定理。

## Related Pages

- [[sources/papers/melenk2021-rkcq-superconvergence]]
- [[papers/index]]
