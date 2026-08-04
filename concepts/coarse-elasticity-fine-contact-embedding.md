---
id: concept--coarse-elasticity-fine-contact-embedding
title: 粗弹性–细接触嵌入
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
keywords:
- coarse-dynamics
- fine-collision-surface
- barycentric-embedding
sources:
- sources/papers/du2024-embedded-ipc.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
---

# 粗弹性–细接触嵌入

动力学用少量粗自由度表示，但碰撞距离仍在高分辨率表面上计算；通过固定重心权重将细表面位置写成粗节点的线性组合。^[sources/papers/du2024-embedded-ipc.md]

该设计避免“降阶必然粗化碰撞几何”，但表达能力受粗空间限制，可能出现锁定。

## 关联页面
- [[du2024-embedded-ipc-method]]
- [[concepts/reduced-coordinate-ipc]]
- [[entities/embedded-ipc]]
