---
id: papers--penwarden2024-kolmogorov-n-width-piml-results
title: Penwarden et al. (2024) — Kolmogorov n-width PIML 实验结果
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/paper
- method/neural-operator
- method/pinn
sources:
- sources/papers/penwarden2024-kolmogorov-n-width-piml.md
created: '2026-07-31'
updated: '2026-07-31'
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

## Evidence By Source

### `sources/papers/penwarden2024-kolmogorov-n-width-piml.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/penwarden2024-kolmogorov-n-width-piml-source.md`

^[sources/papers/penwarden2024-kolmogorov-n-width-piml.md]

## Related Indexes

- [[papers/index]]
- [[index]]
