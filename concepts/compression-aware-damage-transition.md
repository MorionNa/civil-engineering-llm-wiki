---
id: concept--compression-aware-damage-transition
title: 压缩感知损伤–碎屑状态转换
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- complete-damage-threshold
- damage-transition
- tensile-softening
- volume-retention
sources:
- sources/papers/liu2025-incompressible-crack-mpm.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
---

# 压缩感知损伤–碎屑状态转换

## 定义

该机制把材料粒子划分为部分损伤与完全损伤两类：部分损伤阶段只软化拉伸主应力；当损伤超过阈值后，粒子依据当前体积状态重置变形并切换到碎屑塑性模型。^[sources/papers/liu2025-incompressible-crack-mpm.md]

## 动机

传统 CDM 在压缩下继续降低刚度会导致损伤区体积塌缩和粒子聚集，反而阻止裂纹张开。状态转换让完全损伤区域不再作为极软固体，而是成为能够传递压应力、保持体积并发生摩擦流动的碎屑。

## 关键参数

- 完全损伤阈值 $\xi$：控制何时进入碎屑相；
- 体积保留参数 $\eta$：控制压缩状态下重置后的体积和残余弹性能；
- Weibull 失效应力：控制微观缺陷和起裂位置随机性。

## 边界

状态转换是局部且不可逆的。它没有显式裂纹面，也没有区分粉末、细碎屑与仍具刚度的大块碎片；阈值和体积参数需要针对材料、网格和加载率重新标定。

## 关联页面

- [[entities/incompressible-crack-mpm]]
- [[concepts/volume-preserving-debris-plasticity]]
- [[papers/liu2025-incompressible-crack-mpm-method]]
- [[papers/liu2025-incompressible-crack-mpm-critical]]
