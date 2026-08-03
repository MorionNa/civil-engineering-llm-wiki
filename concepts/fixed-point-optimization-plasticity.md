---
id: concept--fixed-point-optimization-plasticity
title: 固定点外循环的优化塑性积分
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
keywords:
- fixed-point
- implicit-plasticity
- optimization-integrator
sources:
- sources/papers/plasticitynet-2022.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
---

# 固定点外循环的优化塑性积分

## 定义

把难以直接能量化的塑性更新拆成“固定内部状态时的能量最小化”和“根据新解更新内部状态/展开点”两个交替步骤，直至两者一致。^[sources/papers/plasticitynet-2022.md]

## 计算结构

1. 固定 $F_0,h$；
2. 求解隐式动力学最小化；
3. 更新 $F_0,h$；
4. 检查固定点残差并重复。

## 优点与风险

优点是复用 Newton、线搜索、接触和空间离散；风险是外循环可能不收敛，有限循环会带来分裂误差和正则黏性。

## 关联页面

- [[plasticitynet-2022-method]]
- [[concepts/local-elastoplastic-potential-family]]
- [[concepts/plasticity-in-the-loop-xpbd]]
- [[entities/plasticitynet]]
