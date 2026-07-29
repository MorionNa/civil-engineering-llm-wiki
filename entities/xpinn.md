---
title: "XPINN — Extended Physics-Informed Neural Network"
created: 2026-07-28
updated: 2026-07-28
type: entity
tags: [physics-informed, pinn, domain-decomposition, xpinn, pde, cross-domain-generalization]
sources: [raw/papers/hu2022-xpinn-generalization.pdf]
confidence: high
---

# XPINN

## 定义

XPINN（Extended Physics-Informed Neural Network）将 PDE 域分成多个通常不重叠的子域，每域由独立 PINN 求解，并通过界面边界、残差连续或通量等 loss 耦合。

## 核心权衡

[[hu2022-xpinn-generalization-analysis]] 指出，XPINN 泛化由两股相反作用决定：

1. 分区使局部目标更简单，降低网络复杂度；
2. 每域样本更少，提升过拟合/Rademacher complexity。

只有第一项超过第二项时，XPINN 才更可能优于 [[pinn]]。

## 好分区与坏分区

| 分区 | 典型结果 |
|---|---|
| 沿移动间断/激波带 | Advection/Euler 改善 |
| 简单上下/均匀切分 | Heat/Euler-TB 可能退化 |
| 界面/边界权重不平衡 | Poisson 中互相牵制 |

## 与 FBPINN 比较

| 维度 | XPINN | [[fbpinn]] |
|---|---|---|
| 子域 | 通常不重叠 | 重叠 |
| 连续性 | 显式界面 loss | 窗函数加和构造 |
| 泛化风险 | 样本稀释 + loss 竞争 | 划分/窗/局部采样 |
| 可扩展方向 | 自适应分区、粗共享 | multilevel 粗层 |

## 适用场景

已知复杂结构位置、间断/多物理界面明确、子域可获得足够训练点的 PDE。实际未知解时应使用 residual/系数/训练动态，而非真解图做分区。

## 局限

域分解不保证改善；泛化界可能较松；分区和 loss 权重高度耦合；oracle 分区会高估真实应用。

## 关联页面

- [[hu2022-xpinn-generalization-method]]
- [[hu2022-xpinn-generalization-results]]
- [[hu2022-xpinn-generalization-critical]]
- [[pinn]] · [[fbpinn]]