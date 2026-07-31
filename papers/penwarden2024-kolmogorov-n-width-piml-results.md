---
title: "Penwarden et al. (2024) — Kolmogorov n-width PIML 实验结果"
created: 2026-07-31
updated: 2026-07-31
type: paper-analysis
sources: [raw/papers/penwarden2024-kolmogorov-n-width-piml-source.md]
confidence: high
---

# Results

## 任务

论文测试：

- 1D Poisson multitask PDE
- 2D nonlinear Allen-Cahn multitask PDE

比较：

- Multihead PINN
- Physics-informed DeepONet
- sine/tanh activation
- Kolmogorov n-width regularization

## 关键发现

### 采样误差低估最坏情况误差

在 1D Poisson 中：

- MH-PINN(sine) 与 MH-PINN(tanh) 的采样均值差距约 3.1 倍；
- Kolmogorov n-width 差距约 16.2 倍。

说明离散任务评价会隐藏模型泛化差异。

### PI-DeepONet

PI-DeepONet 在部分采样任务中误差更低，但 n-width 显示其共享基函数对最困难任务覆盖不足。

### 正则化效果

加入 $K$ regularization 后：

- 所有测试架构 n-width 均下降；
- 基函数更加丰富；
- 减少有限任务过拟合。

### 基函数分析

论文通过学习基函数 SVD 观察：

- regularization 后奇异值谱更加合理；
- 冗余基函数减少；
- 高复杂度空间模式增加。

## 结论

平均测试误差不能替代连续任务族泛化评价，Kolmogorov n-width 提供了一种评价共享物理表示质量的新方式。
