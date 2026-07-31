---
title: "Penwarden et al. (2024) — Kolmogorov n-width PIML 方法"
created: 2026-07-31
updated: 2026-07-31
type: paper-analysis
tags: [physics-informed, pinn, neural-operator, kolmogorov-n-width, operator-learning]
sources: [raw/papers/penwarden2024-kolmogorov-n-width-piml-source.md]
confidence: high
---

# Method

## 基函数视角

论文将多任务 PIML 网络解释为学习全局基函数：

$$u(x)=\sum_i c_i\phi_i(x)$$

其中：

- $\phi_i$：网络 body/trunk 学习的共享基函数；
- $c_i$：任务相关系数。

Multihead PINN 与 PI-DeepONet 的区别主要体现在系数生成方式，而共享表示本质都是学习一个覆盖任务族的有限维函数空间。

## Kolmogorov n-width

传统定义：

$$
K(M,A)=\inf_{M_n}\sup_{x\in A}\inf_{y_n\in M_n}||x-y_n||
$$

表示寻找最佳 n 维子空间逼近整个解流形。

PIML 中改写为：

$$
\tilde K=\inf_{W_1}\sup_c\inf_{W_2}||u(c)-\tilde u(W_1,W_2)||
$$

对应：

```text
学习共享 basis
        ↓
寻找最难 task
        ↓
寻找最佳 task coefficient
        ↓
得到 worst-case approximation error
```

## Competitive bi-optimization

步骤：

1. 正常训练多任务模型；
2. 保存 learned basis；
3. 固定 basis，竞争优化任务系数；
4. 最大化任务难度；
5. 最小化模型逼近误差。

## Kolmogorov regularization

将近似 n-width 加入原始 physics-informed loss：

$$
L=L_R+L_B+\lambda_KL_K
$$

形成 tri-optimization：

- 网络参数优化；
- 最坏任务系数优化；
- 模型系数优化。

## 与 PINN 训练流程关系

论文指出实际 PINN 常采用：

Adam → L-BFGS

因为 Adam 适合初期探索，而 L-BFGS 更适合局部精修。

加入 n-width regularization 后采用多阶段优化策略。

## 工程迁移

对于结构动力问题，可以将：

- basis → 动力响应共享模态/图特征；
- task coefficient → 结构参数与地震输入条件；
- worst-case task → 极端结构-地震组合。
