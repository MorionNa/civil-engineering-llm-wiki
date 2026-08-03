---
id: paper--gander2024-paradiag-method
title: Gander & Palitta (2024)：方法
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/gander2024-paradiag
created: '2026-08-01'
updated: '2026-08-01'
confidence: low
legacy_tags:
- paradiag
- fft
- alpha-circulant
- low-rank-correction
legacy_sources:
- raw/papers/gander2024-new-paradiag.pdf
evidence_scope: local workspace source record pending canonical verification
---

# 方法

Backward Euler 的时间差分矩阵可写成循环矩阵减一个秩一边界项。循环部分由 FFT 对角化，各频点变成独立移位空间系统；秩一项由 Sherman-Morrison-Woodbury 和投影法恢复。α-circulant 用缩放 FFT 改变修正强度，高阶 BDF 则把低秩从 1 提升到阶数 s。^[raw/papers/gander2024-new-paradiag.pdf]

这说明“FFT 频点独立”只解决循环主体，初值因果边界仍需精确处理。V20 的零填充轮廓 z 变换不删除该边界，而以单边生成函数直接构造前 T 步。

## Related Pages

- [[sources/papers/gander2024-paradiag]]
- [[papers/index]]
