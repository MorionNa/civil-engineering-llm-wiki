---
id: concept--local-elastoplastic-potential-family
title: 局部弹塑性势能族
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- domain/ai4s
keywords:
- local-integrability
- expansion-point
- gradient-matching
sources:
- sources/papers/plasticitynet-2022.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
---

# 局部弹塑性势能族

## 定义

当目标塑性力场不可由一个全局标量势积分得到时，为每个展开点 $F_0$ 学习一个局部势 $\Psi(F,F_0)$，在 $F_0$ 处精确匹配目标力，并只在邻域内近似其变化。^[sources/papers/plasticitynet-2022.md]

## 机制

展开点参数打破了“单一全局势必须同时拟合所有非对称 Jacobian”的不可能要求；外层迭代不断移动 $F_0$，内层仍可使用标准能量最小化。

## 适用条件

- 目标力/应力可计算；
- 局部邻域可采样；
- 有外层迭代使展开点逼近新状态；
- 需要监控局部误差与固定点收敛。

## 风险

局部势不自动保证全局下界、凸性、耗散一致性或固定点收敛；有限迭代时路径可能受正则和展开误差影响。

## 关联页面

- [[plasticitynet-2022-method]]
- [[concepts/fixed-point-optimization-plasticity]]
- [[entities/plasticitynet]]
