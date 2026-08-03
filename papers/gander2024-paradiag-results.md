---
id: paper--gander2024-paradiag-results
title: Gander & Palitta (2024)：结果
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
- accuracy
- parallel-cost
legacy_sources:
- raw/papers/gander2024-new-paradiag.pdf
evidence_scope: local workspace source record pending canonical verification
---

# 结果

论文在热方程和对流扩散问题上给出约 `1e-12` 级残差的多组结果，并比较不同 parallel-in-time loops 的成本。作者同时明确当前数值部分没有采用真正的时间并行实现，报告重点是循环次数和算法鲁棒性，而不是本项目可直接采用的 GPU wall time。^[raw/papers/gander2024-new-paradiag.pdf]

因此 V20 只接受其结构分解证据；单卡速度必须与同设备向量化 RK4 正式实测。

## Related Pages

- [[sources/papers/gander2024-paradiag]]
- [[papers/index]]
