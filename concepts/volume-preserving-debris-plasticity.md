---
id: concept--volume-preserving-debris-plasticity
title: 体积保持碎屑塑性 — 真实体积历史驱动的 Drucker–Prager 回映射
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- drucker-prager
- non-associated-flow
- true-volume-history
- volume-preservation
sources:
- sources/papers/liu2025-incompressible-crack-mpm.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
---

# 体积保持碎屑塑性

## 定义

体积保持碎屑塑性使用非关联 Drucker–Prager 回映射模拟完全损伤后的摩擦碎屑，并通过额外体积变形梯度记录真实体积比，避免依据被塑性修正的弹性变形梯度误判膨胀/压缩。^[sources/papers/liu2025-incompressible-crack-mpm.md]

## 机制

- 屈服面控制摩擦强度；
- 非关联流动只校正偏应力，使塑性流动近似等体积；
- 额外体积变形梯度随速度梯度独立更新；
- 其行列式用于判断当前是真实膨胀还是压缩；
- 膨胀状态直接卸载，压缩状态执行回映射。

## 为什么有效

若只看弹性变形梯度，塑性重置可能让下一步错误地产生压应力，持续把粒子推开并造成体积增长。真实体积历史将几何体积变化与弹性试应变分离，减少这种累积误差。

## 边界

该模型不保证严格不可压缩，也没有给出离散体积误差界。完全损伤碎屑仍使用单一速度场和连续颗粒本构，不能替代离散块体、颗粒级碰撞或孔隙率演化模型。

## 关联页面

- [[entities/incompressible-crack-mpm]]
- [[concepts/compression-aware-damage-transition]]
- [[papers/liu2025-incompressible-crack-mpm-results]]
- [[papers/liu2025-incompressible-crack-mpm-critical]]
