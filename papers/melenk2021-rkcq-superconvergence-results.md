---
id: paper--melenk2021-rkcq-superconvergence-results
title: Melenk & Rieder (2021)：结果
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
- convergence-rate
- wave-equation
legacy_sources:
- raw/papers/melenk2021-rkcq-superconvergence.pdf
evidence_scope: local workspace source record pending canonical verification
---

# 结果

L 形区域数值实验使用 3 阶段和 5 阶段 Radau IIA。标准公式分别观察到约 3、5 阶，而 differentiated-data 公式达到约 5、7 阶，与理论预测相符。实验固定了足够细的空间 BEM 网格，以隔离时间误差。^[raw/papers/melenk2021-rkcq-superconvergence.pdf]

这些结果支持“输入参数化会改变高频误差阶”，但不提供结构矩阵、本构替换、单 GPU 速度或端到端学习证据。

## Related Pages

- [[sources/papers/melenk2021-rkcq-superconvergence]]
- [[papers/index]]
