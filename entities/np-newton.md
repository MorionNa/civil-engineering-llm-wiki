---
id: entity--np-newton
title: NP-Newton — Neural-Operator Preconditioned Newton
type: entity
status: verified
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- domain/ai4s
- entity/model
- method/neural-operator
keywords:
- nonlinear-right-preconditioning
- Newton
- trust-region
- line-search
sources:
- sources/papers/lee2025-np-newton.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
---

# NP-Newton

## 定义

NP-Newton 用预训练的 [[fixed-point-neural-operator]] 对当前非线性迭代点进行右预条件，再由原始 Newton 线搜索或信赖域方法求解原残差。神经网络改变收敛路径，但最终接受条件仍由原方程 (F(u)=0) 判定。

## 项目价值

- 对强非线性、Newton 停滞或需要大量回退的场景，可能减少迭代次数并形成速度交叉点。
- 原残差与切线仍由可插拔本构/力学内核计算，适合与 [[one-structure-one-model-contract-2026-08-03]] 结合。
- 对容易收敛的弱非线性问题，神经预条件开销可能导致负加速，因此必须使用残差/难度门控。

## 证据边界

原论文只验证非线性 Poisson 与准静态 Neo-Hookean 问题；它没有证明动力学时间推进、Bouc-Wen 历史变量、50kDOF、OpenSeesPy 或高频结构响应。

## 关联

- [[lee2025-np-newton-analysis]]
- [[fixed-point-neural-operator]]
- [[rathore2024-pinn-loss-landscape-analysis]]
- [[current-structural-pinn-ranking-2026-08-03]]

## Evidence By Source

^[sources/papers/lee2025-np-newton.md]
