---
id: paper--caliari2021-rexii-critical
title: Caliari et al. (2021)：批判性边界
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
- negative-knowledge
- rexi
- oscillatory-pde
legacy_sources:
- raw/papers/caliari2021-rexii.pdf
evidence_scope: local workspace source record pending canonical verification
---

# Negative Knowledge

- 理论要求线性、可对角化且谱位于虚轴；阻尼、非正规矩阵和非线性本构会改变误差界。
- 有理项数随终止时间和谱半径增加，长时/高频并不免费。
- GPU 加速是相对其 CPU 实现，不能替代本项目与同设备 RK4/Newmark 的比较。
- 高并行度伴随显著复数中间量；大图必须做频点和空间双分块。

^[sources/papers/caliari2021-rexii]

## Related Pages

- [[sources/papers/caliari2021-rexii]]
- [[papers/index]]
