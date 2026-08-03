---
id: paper--schadle2006-fast-convolution-quadrature-analysis
title: Schädle et al. (2006) — Fast and Oblivious Convolution Quadrature
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/schadle2006-fast-convolution-quadrature
created: '2026-08-01'
updated: '2026-08-01'
confidence: low
legacy_methods:
- convolution-quadrature
- contour-integration
- laplace-transform
legacy_results:
- quasi-optimal-complexity
- logarithmic-active-memory
legacy_failure_modes:
- sectorial-transform-assumption
- contour-parameter-sensitivity
- no-structural-gpu-benchmark
legacy_reproducibility: medium
legacy_tags:
- spectral-method
- parallel-computing
- time-marching
- structure-preserving
legacy_sources:
- raw/papers/arxiv_math_0504461v1.pdf
evidence_scope: local workspace source record pending canonical verification
---

# Fast and Oblivious Convolution Quadrature

## 1. 工程背景

长历史卷积的直接计算需要二次工作量并保存全部历史。卷积求积通过 Laplace 域传递函数生成稳定离散权重，适用于多尺度或奇异核。^[raw/papers/arxiv_math_0504461v1.pdf]

## 2. Research Gap

普通 FFT 可减少卷积乘法，却不自动减少传递函数评估数和在线历史内存。论文研究如何在时间推进时忘掉绝大部分历史。

## 3. 科学问题

能否只通过对 Laplace 传递函数的少量复数评估，以近似最优复杂度在线计算卷积求积？

## 4. 研究目标

给出 fast-and-oblivious 算法，使 (N) 步卷积求积达到 (O(N\log N)) 乘法、(O(\log N)) 活跃内存和 (O(\log N)) 次传递函数评估。

## 5. 方法机制

→ [[schadle2006-fast-convolution-quadrature-method]]。算法把历史分块，并用双曲线或 Talbot 轮廓离散逆 Laplace 积分；每块只保留少量复数辅助状态。

## 6. 结果证据

→ [[schadle2006-fast-convolution-quadrature-results]]。论文给出轮廓积分指数收敛误差界，并以非线性 Volterra 方程和亚扩散透明边界问题演示。

## 7. 贡献

其贡献是“在线遗忘式卷积求积”，不是一次全局 FFT，也不是神经网络。

## 8. 核心知识点

频域传递函数可以避免显式生成时域核；但效率需要传递函数满足解析/sectorial 条件以及合适轮廓。

## 9. Negative Knowledge

→ [[schadle2006-fast-convolution-quadrature-critical]]。该论文不直接证明无阻尼结构系统、GPU 频点批解或可替换非线性本构的速度与稳定性。

## 10. 可迁移知识

V19 迁移了“用真实传递函数而非全谱低阶多项式”的思想，并通过有限半径 z 轮廓并行计算固定时程；它没有照搬论文的在线分块算法。

## 11. 研究机会

若未来重新开放探索，可研究 separator 稀疏因子与分块轮廓的组合，但必须先解决 V19 已实测的显存增长。

## 12. 可复现性

数学推导与参数实验完整，但未提供面向 GPU 结构动力学的官方实现；等级为中。

## 关联页面

- [[convolution-quadrature]]
- [[gu2022-s4-analysis]]
- [[mtp-mechconv-v2-v18-v19-negative-knowledge]]
