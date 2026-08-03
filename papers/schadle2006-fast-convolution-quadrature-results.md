---
id: paper--schadle2006-fast-convolution-quadrature-results
title: Schädle et al. (2006) 快速卷积求积 — 结果
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/schadle2006-fast-convolution-quadrature
created: '2026-08-01'
updated: '2026-08-01'
confidence: low
legacy_tags:
- spectral-method
- time-marching
- parallel-computing
legacy_sources:
- raw/papers/arxiv_math_0504461v1.pdf
evidence_scope: local workspace source record pending canonical verification
---

# Fast and Oblivious CQ 结果证据

论文证明双曲轮廓离散具有指数型收敛，并指出达到误差容限所需轮廓点数为 (O(\log(1/\varepsilon)))。数值例覆盖非线性 Volterra 方程和带透明边界条件的亚扩散问题。^[raw/papers/arxiv_math_0504461v1.pdf]

这些实验说明算法能处理某些非线性积分方程，但非线性通常仍在当前时间步求解；它没有展示端到端神经本构，也没有与 Newmark/RK4 在 GPU 上比较。

本项目独立 V19 结果显示 z 轮廓可极快：完整两载体流水线 warm 0.01709 s，对 RK4 0.67603 s；但 397.9 MB 峰值显存使预注册扩展门失败。参见 [[mtp-mechconv-v2-v18-v19-negative-knowledge]]。

## 关联页面

- [[schadle2006-fast-convolution-quadrature-analysis]]
- [[schadle2006-fast-convolution-quadrature-critical]]
- [[convolution-quadrature]]
