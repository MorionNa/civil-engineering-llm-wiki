---
title: "Moseley et al. (2023) — FBPINN 实验结果"
created: 2026-07-28
updated: 2026-07-28
type: paper-analysis
tags: [physics-informed, pinn, domain-decomposition, fbpinn, pde, gpu-computing]
sources: [raw/papers/moseley2023-fbpinn.pdf]
results: [cross-domain-generalization, gpu-computing]
datasets: [synthetic-data]
confidence: high
---

# FBPINN 实验结果

> 返回 [[moseley2023-fbpinn-analysis]] · 方法 [[moseley2023-fbpinn-method]] · 实体 [[fbpinn]]

## 1. 证据范围

论文测试低/高频一阶 ODE、多尺度一阶 ODE、二阶 ODE、2D 一阶 PDE、Burgers 和 2+1D 波动方程；指标以测试 L1、训练步数与前向 FLOPs 为主。

## 2. 高频与多尺度

| 问题 | 主要观察 | 定位 |
|---|---|---|
| `du/dx=cos(15x)` | FBPINN 比最佳所测 PINN 更快进入低误差区 | PDF p. 13, Figure 6 |
| `ω1=1,ω2=15` 多尺度 | 三种 PINN 最终误差约高近两个数量级且曲线更不稳 | PDF p. 14, Figure 7 |

这支持局部归一化缓解有效高频，但实验未给多随机种子置信区间。

## 3. 二阶 ODE：调度是决定因素

all-active FBPINN 与 PINN 都在远离边界处偏向错误特解；learning-outwards 使用 500,000 步（每活动模型约 33,333 步）后，能在更多周期范围内恢复正确解，但域边缘仍有小误差。（PDF pp. 14–15, Figure 8）

## 4. Burgers：界面位置不是无关变量

当子域界面与解的陡峭/不连续区域重合时，结果略差于避开间断的划分。域分解不是天然的 discontinuity cure；划分几何必须作为超参数或可学习变量。

## 5. 波动方程

FBPINN 约 460,836 参数，PINN 66,689 参数；两者使用 195,112 个训练点。FBPINN 训练 150k 步、PINN 75k 步，最终精度相近；FBPINN 约使用一半前向 FLOPs，并在训练过程中从 `t=0` 稳健向外传播，而 PINN 早期长时间停在近零特解。（PDF pp. 19–21, Figures 11–13）

## 6. 计算成本解释

| 指标 | 结论 |
|---|---|
| 前向 FLOPs | 局部网络更小，FBPINN 可更低 |
| 单线程墙钟 | FBPINN 通常慢 2–10 倍 |
| 传统数值法 | 波动问题神经训练约 10 h；FD 约 1 min |
| 多线程潜力 | 作者预计可随并行子域数加速，但未实证 |

## 7. 有界结论

证据支持 FBPINN 在高频/大域上比标准 PINN 更稳健，但不支持“所有 PDE 更快”“域分解对间断天然鲁棒”或“已达到传统法效率”。

> 页面导航：[[moseley2023-fbpinn-analysis]] · [[moseley2023-fbpinn-method]] · [[moseley2023-fbpinn-critical]] · [[pinn]]