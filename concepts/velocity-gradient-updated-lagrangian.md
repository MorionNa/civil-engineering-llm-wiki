---
id: concept--velocity-gradient-updated-lagrangian
title: 速度梯度驱动的更新拉格朗日粒子状态
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- deformation-gradient
- updated-lagrangian
- velocity-gradient
- meshless
sources:
- sources/papers/yu2024-xpbi.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
---

# 速度梯度驱动的更新拉格朗日粒子状态

## 定义

该机制以当前构形为参考，通过速度梯度更新粒子变形梯度：$F^{n+1}=(I+\Delta t\nabla v^{n+1})F^n$。它不依赖固定材料网格，因此适合大变形和拓扑变化。^[sources/papers/yu2024-xpbi.md]

## 实现要点

在 XPBI 中，速度是主未知量；速度梯度由 Wendland 平滑核和一阶一致性修正矩阵估计。约束关于粒子速度/位置的导数可由该离散梯度直接获得。

## 优势

- 不必维护初始网格拓扑；
- 可复用连续介质变形梯度与本构回映射；
- 与纯粒子碰撞和约束系统兼容；
- 把 MPM 风格状态追踪与 XPBD 求解解耦。

## 风险

一阶导数对邻域缺失、边界和粒子聚集敏感。梯度修正、SVD 伪逆、位置修正和合理采样均是稳定性的必要条件，而非可选优化。

## 关联页面

- [[entities/xpbi]]
- [[concepts/plasticity-in-the-loop-xpbd]]
- [[yu2024-xpbi-method]]
- [[yu2024-xpbi-critical]]
