---
id: concept--rotation-free-stretch-reconstruction
title: 旋转无关伸长重构 — 从 Kirchhoff 应力恢复隐式参考态
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- isotropic-hyperelasticity
- kirchhoff-stress
- polar-decomposition
- stress-to-stretch
sources:
- sources/papers/feng2026-mpm-lite.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
---

# 旋转无关伸长重构

## 定义

旋转无关伸长重构不把粒子变形梯度直接平均到积分点，而是先传递广延 Kirchhoff 应力 $V\tau$，再求正定伸长张量 $S$，使 $P(S)S^\top=\tau$，并把 $S$ 作为增量势时间积分的基准变形。^[sources/papers/feng2026-mpm-lite.md]

## 为什么需要

变形梯度既不是强度量也不是广延量，混合不同旋转和伸长会破坏客观性并产生非物理应力。对各向同性材料，单步弹性能和切线只依赖伸长，旧旋转可被丢弃；论文证明相对于保留旋转，速度解的单步差异为 $O(\Delta t^2)$。

## 实现

- 对 Hencky 应变 StVK，主 Kirchhoff 应力到对数主伸长具有闭式反演；
- 对偏–体积分裂 Neo-Hookean，体积比由球应力恢复，偏应力给出主伸长平方的偏量，三维归结为选择正伸长分支的三次方程；
- 多材料在同一单元中心保留各自的 $(V_{c,k},\tau_{c,k})$ 并分别贡献能量。

## 边界

方法依赖各向同性。纤维增强、正交各向异性等材料的旋转携带材料方向，不能丢弃；极端压缩、近不可压缩与更复杂本构还可能需要迭代反演和条件数控制。

## 关联页面

- [[entities/mpm-lite]]
- [[concepts/particle-independent-grid-integration]]
- [[papers/feng2026-mpm-lite-method]]
- [[papers/feng2026-mpm-lite-critical]]
