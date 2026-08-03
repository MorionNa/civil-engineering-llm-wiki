---
id: paper--schadle2006-fast-convolution-quadrature-critical
title: Schädle et al. (2006) 快速卷积求积 — 批判与迁移边界
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
- limitation
- future-work
legacy_sources:
- raw/papers/arxiv_math_0504461v1.pdf
evidence_scope: local workspace source record pending canonical verification
---

# Fast and Oblivious CQ Negative Knowledge

- 主要理论假设是 sectorial Laplace 变换；无阻尼结构 resolvent 在虚轴具有极点，不能不加论证地套用全部误差定理。
- 论文的 (O(\log N)) 是在线分块算法的活跃内存，不属于一次保存 2049 个结构频点和 TCN 工作区的全时程 RFFT。
- 非线性算例不等于非线性结构本构的全部频域并行化；逐时点非线性耦合仍是额外问题。
- 轮廓参数会影响误差与条件数，正式实验必须预冻结，不能失败后调参。^[raw/papers/arxiv_math_0504461v1.pdf]

V19 正确把该论文当作生成函数和轮廓算法依据，而没有把其复杂度定理当作任意图证明；最终显存否决也说明这种证据边界是必要的。

## 关联页面

- [[schadle2006-fast-convolution-quadrature-analysis]]
- [[gu2022-s4-critical]]
- [[mtp-mechconv-v2-v18-v19-negative-knowledge]]
