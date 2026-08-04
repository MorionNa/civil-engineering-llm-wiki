---
id: paper--du2024-embedded-ipc-method
title: "Du et al. (2024) — Embedded IPC 方法"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- subspace-dynamics
- barycentric-embedding
- ipc
- ccd
sources:
- sources/papers/du2024-embedded-ipc.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
---

# Embedded IPC 方法

## 约化动力学
设全空间位置 $x=\phi(q)$，约化质量矩阵 $M_q=J^TMJ$。后向 Euler 写成约化增量势最小化。^[sources/papers/du2024-embedded-ipc.md]

## 接触能
在高分辨率表面上枚举点–三角形和边–边对，计算 IPC 障碍能和滞后摩擦势，再复合为 $B(\phi(q))$ 与 $D(\phi(q),x^n)$。

## 线性嵌入
每个碰撞表面顶点位于一个粗四面体内，初始时计算重心权重，之后保持 $x_k=\sum_j\omega_j^k q_{i_j(k)}$，因此 $x=Jq$。

## 弹性能与外力
弹性能在粗四面体上用聚合体积积分；全空间外力通过 $J^Tf_{ext}$ 投影。梯度和 Hessian 分别为 $J^T\nabla_xE$ 和 $J^T\nabla_x^2EJ$。

## 非穿透求解
Projected Newton 求解；每个 Newton 步用 CCD 找到安全步长，线性映射允许使用 ACCD。

## 特例
$J=I$ 时退化为全空间 IPC；单四面体包裹表面时与 Affine Body Dynamics 对应；中间分辨率形成精度–效率连续谱。

## 假设与边界
初始嵌入关系固定，粗四面体不能自然表达所有大变形模态；拓扑变化与共维对象未处理。

## 关联页面
- [[du2024-embedded-ipc-analysis]]
- [[du2024-embedded-ipc-results]]
- [[du2024-embedded-ipc-critical]]
- [[entities/embedded-ipc]]
- [[concepts/coarse-elasticity-fine-contact-embedding]]
- [[concepts/reduced-coordinate-ipc]]
