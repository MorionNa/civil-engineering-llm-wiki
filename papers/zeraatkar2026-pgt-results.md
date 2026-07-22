---
title: "PGT 结果与验证"
created: 2026-07-16
updated: 2026-07-16
type: paper-analysis
---

# PGT 实验结果

## Benchmark

论文验证包括：

- 一维 heat equation；
- 二维 incompressible Navier–Stokes cylinder wake。

## 主要结论

PGT 在稀疏观测条件下能够同时降低：

- PDE residual；
- 场重构误差。

论文报告 heat equation 和 Navier–Stokes 中均优于仅依赖传统 PINN loss 的方法。

## 对结构工程的启示

当前实验并未验证结构动力学，但说明：

> 如果物理规律能够进入网络的信息传播过程，可能比单纯增加 physics loss 更有效。

这为结构动力 PINN 中设计 physics-aware attention 提供了方向。

## 关联页面

- `[[zeraatkar2026-pgt-analysis]]`
- `[[zeraatkar2026-pgt-method]]`
