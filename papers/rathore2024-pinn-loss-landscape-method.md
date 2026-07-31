---
id: papers--rathore2024-pinn-loss-landscape-method
title: PINN 损失景观与 NysNewton-CG 方法
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
- method/pinn
keywords:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
- method/pinn
sources:
- sources/papers/rathore2024-pinn-loss-landscape.md
created: '2026-07-31'
updated: '2026-07-31'
confidence: medium
---

# PINN 损失景观与 NysNewton-CG 方法

## PINN Objective

论文研究残差与边界/初值组成的非线性最小二乘目标：

$$
L(w)=\frac{1}{2n_r}\sum_i D[u(x_i;w)]^2+\frac{1}{2n_b}\sum_j B[u(x_j;w)]^2.
$$

其 Hessian 由 residual Jacobian 的 Gauss–Newton 项和二阶 residual 项共同组成。微分算子的高频放大与谱衰减会传递到参数空间曲率。

## Hessian Spectral Density

作者通过 Hessian–vector product 和随机谱估计分析有限宽网络，而不是只依赖无限宽 NTK。重点观察：

- 接近零特征值形成的大面积平坦方向；
- $10^3$–$10^5$ 量级离群大特征值；
- residual loss 相比边界项更病态；
- L-BFGS 预条件后的谱变化。

## Optimization Pipeline

```text
Adam
  ↓ 全局探索、避开部分鞍点
L-BFGS
  ↓ 近似逆 Hessian、改善局部条件数
NysNewton-CG
  ↓ L-BFGS 停滞后的高精度阻尼 Newton 精修
```

## L-BFGS As Right Preconditioner

论文不仅把 L-BFGS 看作 optimizer，还分析其隐式逆 Hessian 近似对后续曲率的预条件效果。经验上，预条件后最大特征值/条件数可降低至少约三个数量级。

## NysNewton-CG

NNCG 近似求解阻尼 Newton 系统：

$$
(H+\mu I)p=-g.
$$

核心组件：

1. 用 Hessian–vector products 避免显式存储 Hessian；
2. Nyström 随机低秩 sketch 捕获主导谱子空间；
3. 以该低秩近似构造 PCG 预条件器；
4. 用 conjugate gradient 求近似 Newton 步；
5. 用 Armijo line search 和 damping 控制步长。

## Gradient Damped Newton Descent Theory

理论部分在局部 PŁ* 等条件下说明：先由一阶方法进入合适邻域，再使用阻尼 Newton，可获得不显式依赖原始条件数的快速局部收敛。该结论主要针对线性微分算子及局部假设。

## Hyperparameters And Cost

NNCG 引入 sketch size、预条件更新频率、damping、CG tolerance、最大 CG 步和 line search 参数。其每一步显著贵于 L-BFGS，因此设计定位是 terminal-stage optimizer。

## Structural-Dynamics Use

对多损失结构 PINN，可分别估计平衡、本构、能量、初值和数据块的谱，采用 block-Nyström 或子结构预条件。只有在表示、采样和物理建模基本正确时，二阶精修才值得投入。

## Related Pages

- [[rathore2024-pinn-loss-landscape-analysis]]
- [[rathore2024-pinn-loss-landscape-results]]
- [[rathore2024-pinn-loss-landscape-critical]]
- [[nysnewton-cg]]

## Evidence By Source

### `sources/papers/rathore2024-pinn-loss-landscape.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/rathore24a.pdf`

^[sources/papers/rathore2024-pinn-loss-landscape.md]
