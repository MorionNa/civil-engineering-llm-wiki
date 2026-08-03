---
id: paper--caliari2021-rexii-method
title: Caliari et al. (2021)：方法
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
- rexi
- shifted-systems
- matrix-exponential
- gpu
legacy_sources:
- raw/papers/caliari2021-rexii.pdf
evidence_scope: local workspace source record pending canonical verification
---

# 方法

REXII 先用 Gaussian 和有理函数展开逼近标量 `exp(ix)`，再把标量变量替换为虚谱矩阵。对可对角化 A，误差界含特征向量条件数；所需有理项数由终止时间与谱半径控制。每一项需要两个复移位线性系统，但各项互相独立，适合 GPU 并行。^[raw/papers/caliari2021-rexii.pdf]

V20 不近似 `exp(tA)`；它精确因式分解教师 RK4 的四阶稳定多项式。共同点仅是复移位系统和并行归约，因而不会引入 REXII 的截断近似作为第二个误差源。

## Related Pages

- [[sources/papers/caliari2021-rexii]]
- [[papers/index]]
