---
id: concept--particle-independent-grid-integration
title: 粒子无关的网格积分 — MPM 求解阶段解耦
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- fixed-quadrature
- grid-integration
- particle-independent-solve
- ppc-independent
sources:
- sources/papers/feng2026-mpm-lite.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
---

# 粒子无关的网格积分

## 定义

该思想把 MPM 粒子从求解阶段的积分点降为状态与历史载体：粒子状态先重采样到固定网格积分点，之后力、Jacobian/Hessian 作用和时间积分只访问网格。^[sources/papers/feng2026-mpm-lite.md]

## 机制

传统隐式 MPM 的每次梯度或 Hessian–向量积都需要 G2P2G 循环，成本随 PPC 增长。MPM Lite 在单元中心保存质量、速度梯度、体积与 Kirchhoff 应力，并用紧凑 Q1 模板进行六面体 FEM 式积分，使隐式系统的稀疏模式和求解器内存主要由网格决定。

## 收益

- 求解阶段成本与 PPC 解耦；
- 可直接使用 PCG、multigrid、VBD 等现成非线性/优化求解器；
- 线性节点基具有清晰边界语义；
- 固定模板有利于并行 gather 和差分/可微工作流。

## 边界

这不等于整个算法与粒子数无关：P2C/C2P、平流和本构更新仍随粒子数增长。固定单点积分也可能欠解析薄结构、弯曲和强子单元变化。

## 关联页面

- [[entities/mpm-lite]]
- [[concepts/rotation-free-stretch-reconstruction]]
- [[papers/feng2026-mpm-lite-method]]
- [[papers/feng2026-mpm-lite-critical]]
