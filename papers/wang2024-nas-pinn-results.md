---
title: "Wang & Zhong (2024) — NAS-PINN results"
created: 2026-07-30
updated: 2026-07-30
type: paper-analysis
tags: [pinn, neural-architecture-search, poisson-equation, burgers-equation, advection-equation]
sources: [raw/papers/wang2024-nas-pinn-source.md]
confidence: high
---

# Results

## Benchmarks

论文测试：Poisson、Burgers、Advection 方程以及非规则计算域。fileciteturn23file0L257-L259

## Main findings

- NAS-PINN 找到搜索空间内误差最低结构；
- 网络深度增加不一定提高 PINN 性能；
- 不同 PDE 偏好的架构不同。

Poisson实验中，NAS-PINN 架构 L2 error 为 4.46×10⁻⁴，优于比较架构。fileciteturn23file0L350-L358

复杂非规则区域中，作者发现残差连接更有利，且深层网络并非总是最佳。fileciteturn23file0L336-L343

## Conclusions

论文总结指出：不同 PDE 需要不同网络结构，人工设计难以覆盖这种多样性。fileciteturn23file0L550-L559
