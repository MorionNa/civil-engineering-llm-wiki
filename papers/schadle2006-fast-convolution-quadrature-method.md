---
id: paper--schadle2006-fast-convolution-quadrature-method
title: Schädle et al. (2006) 快速卷积求积 — 方法
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

# Fast and Oblivious CQ 方法

卷积求积权重由生成函数 (sum_{n\ge0}\omega_n\zeta^n=F(\delta(\zeta)/h)) 定义。论文将权重写成复轮廓积分，并按几何增长的历史块使用 Talbot/双曲轮廓求积。^[raw/papers/arxiv_math_0504461v1.pdf]

每个轮廓点维护一个 (y'=\lambda y+g) 的辅助量，因而不保存完整输入历史。对 sectorial (F(s))，轮廓求积点数随误差容限对数增长，给出 (O(N\log N)) 乘法和 (O(\log N)) 活跃内存。

V19 的固定长度圆轮廓 RFFT 是离线全时程变体：它对所有频点直接求真实结构 resolvent。两者共享生成函数思想，但 V19 不具备论文在线遗忘内存结论。

## 关联页面

- [[schadle2006-fast-convolution-quadrature-analysis]]
- [[convolution-quadrature]]
- [[schadle2006-fast-convolution-quadrature-critical]]
