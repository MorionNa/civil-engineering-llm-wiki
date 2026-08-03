---
id: paper--gu2022-s4-critical
title: Gu et al. (2022) S4 — 批判与迁移边界
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/gu2022-s4
created: '2026-08-01'
updated: '2026-08-01'
confidence: low
legacy_tags:
- sequence-modeling
- spectral-method
- future-work
- limitation
legacy_sources:
- raw/papers/arxiv_2111_00396v3.pdf
evidence_scope: local workspace source record pending canonical verification
---

# S4 Negative Knowledge

- NPLR/DPLR 是可学习状态矩阵的特殊参数化，不等于任意真实 (M,C,K) 的精确对角化。
- 论文理论的近线性 Cauchy 算法并非其实际 GPU 主路径；实际采用朴素、并行友好的计算。因此必须单独报告理论复杂度和代码实测。
- LRA/图像/语言成功不能证明低频、高频结构响应、矩阵边内力或本构替换。
- 卷积视图天然适合整段训练，但严格因果仍需 future-to-prefix 扰动/JVP 审计，不能只依据“理论卷积是因果的”。^[raw/papers/arxiv_2111_00396v3.pdf]

## 对 V19 的结论

采用 11 层因果 edge-TCN 而非扩大 S4 状态，是成本门中的保守选择；V19 的失败来自显存工作区，不应通过扩大状态维数补救。

## 关联页面

- [[gu2022-s4-analysis]]
- [[schadle2006-fast-convolution-quadrature-critical]]
- [[mtp-mechconv-v2-v18-v19-negative-knowledge]]
