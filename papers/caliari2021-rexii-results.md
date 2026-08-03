---
id: paper--caliari2021-rexii-results
title: Caliari et al. (2021)：结果
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/caliari2021-rexii
created: '2026-08-01'
updated: '2026-08-01'
confidence: low
legacy_tags:
- gpu-speed
- oscillatory-pde
- accuracy
legacy_sources:
- raw/papers/caliari2021-rexii.pdf
evidence_scope: local workspace source record pending canonical verification
---

# 结果

二维旋转浅水实验中，REXII 在合适谱半径覆盖下达到接近机器精度；GPU 相对 CPU 的加速约为 7–15 倍。论文还显示长时间场景下 REXII 可明显优于显式 RK4，但比较依赖其线性虚谱、Fourier 空间实现和单个大时间跨度。^[raw/papers/caliari2021-rexii.pdf]

论文同时报告 REXII 的中间复数矩阵可能需要约 90 GB，实际 12 GB GPU 必须分块。这支持本项目采用频点分块/owner-separator，而不是把所有频点和子图一次驻留显存。

## Related Pages

- [[sources/papers/caliari2021-rexii]]
- [[papers/index]]
