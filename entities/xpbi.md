---
id: entity--xpbi
title: XPBI — 基于平滑核的扩展位置非弹性动力学
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- entity/model
- evidence/paper
keywords:
- xpbd
- position-based-inelasticity
- updated-lagrangian
- continuum-plasticity
sources:
- sources/papers/yu2024-xpbi.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
---

# XPBI

## 定义

XPBI（eXtended Position-Based Inelasticity）是 Yu 等提出的纯粒子连续介质非弹性框架。它在 XPBD 中引入更新拉格朗日变形梯度、平滑核速度梯度与塑性回映射，使经典弹塑性和黏塑性本构能够作为逐粒子约束参与求解。^[sources/papers/yu2024-xpbi.md]

## 核心组件

- 速度主变量 XPBD；
- [[concepts/velocity-gradient-updated-lagrangian]]；
- Wendland 核与一阶梯度修正；
- [[concepts/plasticity-in-the-loop-xpbd]]；
- 着色 Gauss–Seidel；
- XSPH 阻尼与粒子距离修正；
- 标准 PBD 碰撞、布料和流体约束耦合。

## 支持材料

论文演示 Von Mises、Drucker–Prager、非关联 Cam-Clay、Herschel–Bulkley 和 StVK-Hencky 弹性。

## 适用场景

自由表面、颗粒、黏塑性材料、雪、塑性体、视觉断裂以及需要与 PBD 物体直接交互的混合场景。

## 边界

当前证据主要来自图形学模拟；塑性固定点未设置严格收敛监控，高刚度依赖小时间步和稳定化，工程级守恒与材料标定尚未建立。

## 项目角色

XPBI 可作为结构倒塌后碎屑与接触阶段的候选粒子框架，也可用于比较 MPM、AEM、DEM 和约束动力学路线。但其用于 RC 框架仍需混凝土损伤、钢筋、粘结滑移和实验验证。

## 关联页面

- [[yu2024-xpbi-analysis]]
- [[yu2024-xpbi-method]]
- [[yu2024-xpbi-results]]
- [[yu2024-xpbi-critical]]
