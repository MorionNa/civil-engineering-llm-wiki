---
title: "LegONet 方法机制：结构保持 operator blocks 与组合式 PDE 求解"
created: 2026-07-28
updated: 2026-07-28
type: paper-analysis
tags: [neural-operator, structure-preserving, operator-splitting, spectral-method]
sources: [raw/papers/2603.07882v1.pdf]
confidence: high
---

# LegONet 方法机制

## 1. Boundary-adapted baseplate

LegONet 首先通过 lifting 处理非齐次边界：

$$u=u_{lift}+u_0$$

随后将 $u_0$ 表示在边界适配谱基中：

$$u_0(x,t)=\sum_k a_k(t)\phi_k^{(b)}(x)$$

所有 operator block 均作用于共享 coefficient state $a$，因此边界条件由表示保证，而不是由 penalty loss 学习。

## 2. Structure-preserving blocks

每个机制块定义为：

$$F_i^\theta(a)=-G_i\nabla E_i(a)+J_i\nabla H_i(a)+R_i(a)$$

其中：

- E-block：耗散机制；
- H-block：守恒机制；
- R-block：无法写成生成元形式的残差机制。

## 3. Trajectory-free pretraining

不同于直接拟合完整 PDE trajectory，LegONet 只学习瞬时 operator matching：

$$F_i^\theta(a)\approx F_i^{ref}(a)$$

因此机制块可以独立训练并复用。

## 4. Plug-and-play deployment

新的 PDE 通过选择 block 并采用 symmetric Strang splitting 组合：

- 不需要重新训练完整网络；
- 可以增加、删除或调整机制；
- 可以分析 block mismatch 和 splitting error。

## 关联

- [[zhang2026-legonet-analysis]]
- [[zhang2026-legonet-results]]
- [[legonet]]
