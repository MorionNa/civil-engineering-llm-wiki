---
id: paper--gander2024-paradiag-critical
title: Gander & Palitta (2024)：批判性边界
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
- negative-knowledge
- alpha-circulant
- paradiag
legacy_sources:
- raw/papers/gander2024-new-paradiag.pdf
evidence_scope: local workspace source record pending canonical verification
---

# Negative Knowledge

- α 越小，低秩修正越弱，但缩放 Fourier 特征向量条件数会恶化；不能用极小 α 免费获得精度与速度。
- 论文主体是 BDF/抛物型问题，Runge-Kutta 只作为可推广方向。
- Sherman-Morrison-Woodbury 路线仍需要投影/Krylov 修正，不满足本项目“直接推理优先”的默认合同。
- 对无阻尼波动和非线性本构，必须重新审计稳定性、幅相和迭代次数，不能继承论文结论。

^[sources/papers/gander2024-paradiag]

## Related Pages

- [[sources/papers/gander2024-paradiag]]
- [[papers/index]]
