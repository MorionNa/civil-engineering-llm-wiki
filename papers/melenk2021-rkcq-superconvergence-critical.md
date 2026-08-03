---
id: paper--melenk2021-rkcq-superconvergence-critical
title: Melenk & Rieder (2021)：批判性边界
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
- negative-knowledge
- rkcq
- wave-equation
legacy_sources:
- raw/papers/melenk2021-rkcq-superconvergence.pdf
evidence_scope: local workspace source record pending canonical verification
---

# Negative Knowledge

- 超收敛依赖特定边界积分算子、Laplace 扇区界、光滑输入及初始兼容条件。
- 论文采用 Radau IIA；不能把结果转移到显式经典 RK4。
- 时间半离散结论还没有覆盖本项目的空间图分解、矩阵边权和非线性本构。
- V20 采用阶段提升不是为了声称超收敛，而是为了与现有教师 RK4 的每个阶段完全对齐。

^[sources/papers/melenk2021-rkcq-superconvergence]

## Related Pages

- [[sources/papers/melenk2021-rkcq-superconvergence]]
- [[papers/index]]
