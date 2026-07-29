---
title: "Kopaničáková et al. (2024) — ASPQN/MSPQN 方法机制"
created: 2026-07-28
updated: 2026-07-28
type: paper-analysis
tags: [physics-informed, pinn, schwarz-method, nonlinear-preconditioning, quasi-newton, layerwise-decomposition, model-parallelism]
sources: [raw/papers/kopanicakova2024-dd-preconditioning.pdf]
methods: [schwarz-method, nonlinear-preconditioning, quasi-newton, layerwise-decomposition]
confidence: high
---

# ASPQN/MSPQN 方法机制

> 返回 [[kopanicakova2024-dd-preconditioning-analysis]] · 实体 [[schwarz-preconditioned-pinn]] · 对照 [[dolean2024-multilevel-fbpinn-method]]

## 1. 参数空间分解

网络按层分为 `N_sd` 个不重叠组：

$$\theta=[\theta_1,\ldots,\theta_{N_{sd}}]^T,\quad \theta_s=R_s\theta,\quad \theta=\sum_sE_s\theta_s.$$

`R_s` 提取层组参数，`E_s` 将局部增量放回全参数。（PDF p. 6, Equations 3.3–3.4）

## 2. 局部子问题

对第 `s` 组，冻结其他参数并近似求

$$\theta_s^*=\arg\min_{\theta_s}L(\theta_1,\ldots,\theta_s,\ldots,\theta_{N_{sd}}).$$

局部优化器仍为 L-BFGS，固定执行 `k_s` 次；其作用类似非线性局部消元。

## 3. ASPQN：加法 Schwarz

所有子问题从相同全局状态出发并行求解，局部增量经 extension 后同步叠加，再做一次全局 L-BFGS。实现上每个子网对应一张 GPU，使用 NCCL 同步，但每张 GPU 复制完整网络。

## 4. MSPQN：乘法 Schwarz

子域按顺序处理；第 `s+1` 个子问题看到前一子域已更新的参数，因此局部信息传播更强。算法天然串行，面向单 GPU。

## 5. 全局准牛顿与动量

全局 L-BFGS 使用最近 `m=3` 个 secant pairs 的有限内存 Hessian 近似；可在预条件方向上加入递归动量。局部校正处理分块非线性，全局步协调跨层耦合。（PDF p. 8, Equations 3.10–3.13）

## 6. 实现设置

| 项目 | 设置 |
|---|---|
| 框架 | PyTorch + DistTraiNN |
| 通信 | torch.distributed + NCCL |
| 配点 | 每题 10,000 Hammersley |
| 激活 | adaptive tanh |
| 初始化 | Xavier |
| 局部步 | 常用 `k_s=50`，敏感性测 10/50/100 |
| 硬件 | Piz Daint P100 |

## 7. 计算/内存含义

ASPQN 可降低墙钟，但总 GPU-hours 和显存未按单 GPU归一；MSPQN 不增加 GPU 数，更适合判断纯算法效率。完整网络复制是主要扩展瓶颈。

## 8. 与空间域分解的区别

[[fbpinn]]/[[xpinn]] 切输入或 PDE 域，降低局部函数复杂度；本文切参数层，目标是改善 loss 条件性。两者可以嵌套，但通信与局部循环会叠加。

> 页面导航：[[kopanicakova2024-dd-preconditioning-analysis]] · [[kopanicakova2024-dd-preconditioning-results]] · [[kopanicakova2024-dd-preconditioning-critical]] · [[pinn]]