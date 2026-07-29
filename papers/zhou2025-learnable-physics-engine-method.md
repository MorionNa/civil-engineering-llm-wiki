---
title: "Zhou & Feng (2025) — Learnable Physics Engine 方法机制"
created: 2026-07-28
updated: 2026-07-28
type: paper-analysis
tags: [scientific-machine-learning, graph-neural-network, message-passing-neural-network, learnable-physics-engine, peridynamics, elastoplasticity, constitutive-model, drucker-prager, sobolev-training]
sources: [raw/papers/zhou2025-learnable-physics-engine.xml]
methods: [message-passing-neural-network, sobolev-training, peridynamics, constitutive-model]
confidence: high
---

# Learnable Physics Engine 方法机制

> 返回 [[zhou2025-learnable-physics-engine-analysis]] · 实体 [[learnable-physics-engine]] · 对照 [[pinn]]

## 1. 图表示

在 OSB-PD 中，节点 `V` 是材料点，边 `E` 是 horizon 内的键与相互作用。MPNN 采用边更新—聚合—节点更新：

$$e'_k=NN_e([e_k,v_{r_k},v_{s_k}]),\quad \bar e'_i=\sum_{k:r_k=i}e'_k,\quad v'_i=NN_v([\bar e'_i,v_i]).$$

（原文 Equation 28, Figures 3–4）

## 2. 三段物理引擎

| 模块 | 输入 | 输出 | 角色 |
|---|---|---|---|
| MPNN1 | 图节点/边 | 体积应变与键偏应变 | 运动学 |
| MPNN2 | 键应变/历史变量 | 能量、力状态、屈服判定 | 本构与塑性 |
| MPNN3 | 键力/图 | 更新节点与位置 | 动力推进 |

MPNN1/3 的部分函数显式给定，降低训练复杂度；主要学习集中在 MPNN2。（原文 Figure 7, Algorithm 3）

## 3. 能量网络与 H2 Sobolev 训练

体积与偏变能采用两个独立 MLP，作者称比双输出单网更易优化。loss 同时约束

$$\|\psi-\hat\psi\|^2+\|\partial\psi-\partial\hat\psi\|^2+\|\partial^2\psi-\partial^2\hat\psi\|^2,$$

权重 `γ1=γ2=γ3=1`。一阶导对应应力/力，二阶导对应切线，因此仅拟合能量值不足。（原文 Equation 29, Figure 5）

## 4. 屈服面 level set

将屈服函数写为 signed distance：面外为正、面上为零、面内为负。硬化通过 Hamilton–Jacobi 伪时间演化 `∂Φ/∂t+F|∇Φ|=0` 表示；在 `(p,q,ζ)` 不变量空间采样并插值生成训练数据。（原文 Equations 30–36, Figure 6, Algorithm 2）

## 5. 可微塑性修正

当 `f_hat>0` 时，网络权重冻结，自动微分获得 `∂f_hat/∂dλ`，用 Newton 迭代

$$d\lambda\leftarrow d\lambda-\hat f/(\partial\hat f/\partial d\lambda)$$

更新塑性变量与键力。（原文 Equations 37–38, Algorithm 1）

## 6. 网络与优化

MPNN2 的 `φ_e` 为 5 个 30 单元 tanh 隐层，输出 `N_e×2`；`φ_v` 结构相近、输出 `N_e×1`。Adam 初始学习率 `0.0005`，每 100 epoch 乘 0.1；PyTorch Geometric 实现。

## 7. 与 PINN 的区别

[[pinn]] 在每个问题上最小化 PDE residual；本文先监督学习能量/屈服模块，再以图消息传递推进。物理来自模块结构与显式更新，而不是单一 residual loss。

## 8. 方法边界

可解释性建立在 OSB-PD/Drucker–Prager 语义正确的前提上；若真实材料超出该本构族，模块仍可解释但可能系统性有偏。

> 页面导航：[[zhou2025-learnable-physics-engine-analysis]] · [[zhou2025-learnable-physics-engine-results]] · [[zhou2025-learnable-physics-engine-critical]] · [[learnable-physics-engine]]