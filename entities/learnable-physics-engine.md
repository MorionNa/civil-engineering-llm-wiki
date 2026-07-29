---
title: "Learnable Physics Engine — 可解释图网络物理引擎"
created: 2026-07-28
updated: 2026-07-28
type: entity
tags: [scientific-machine-learning, graph-neural-network, message-passing-neural-network, learnable-physics-engine, peridynamics, elastoplasticity, constitutive-model, geomaterials]
sources: [raw/papers/zhou2025-learnable-physics-engine.xml]
confidence: high
---

# Learnable Physics Engine

## 定义

Learnable Physics Engine（LPE）把物理系统表示为可推进的图，只用神经网络学习具有明确物理语义的未知函数，同时保留状态更新、守恒/聚合和数值修正等显式结构。

本文实体特指 [[zhou2025-learnable-physics-engine-analysis]] 的 OSB-PD Drucker–Prager 弹塑性引擎。

## 三段结构

1. MPNN1：从材料点图计算键应变；
2. MPNN2：学习体积/偏变能与屈服面，计算键力并作 Newton 塑性修正；
3. MPNN3：聚合键力、更新节点和位置。

## 可解释性来源

- 网络输出对应能量与 signed-distance 屈服函数；
- H2 Sobolev loss 约束能量值、一阶应力与二阶切线；
- 塑性乘子仍由可微 Newton 更新；
- 节点/边对应材料点与 peridynamic 键。

## 与 PINN 的区别

[[pinn]] 通常在每个 PDE 实例上优化 residual；LPE 先监督学习可复用物理模块，再对图状态滚动推进。二者可组合：LPE 作快速可微正演，PINN/观测 loss 作反演。

## 关键证据

三类岩土边值问题与 OSB-PD 场接近；100 个 2000 步案例中，点数从 3,600 到 90,000 时 LPE 约 10→45 s，PD 约 200→3000 s。→ [[zhou2025-learnable-physics-engine-results]]

## 局限

同源模拟监督；未计训练摊销；缺统一场误差和 UQ；真实材料、循环外推、热力学稳定性和公开复现未验证。

## 关联页面

- [[zhou2025-learnable-physics-engine-method]]
- [[zhou2025-learnable-physics-engine-critical]]
- [[pinn]] · [[schwarz-preconditioned-pinn]]