---
id: paper--du2024-embedded-ipc-critical
title: "Du et al. (2024) — Embedded IPC 批判性分析"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- locking
- heuristic-embedding
- action-at-distance
- benchmark-fairness
sources:
- sources/papers/du2024-embedded-ipc.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
---

# Embedded IPC 批判性分析

## 核心贡献
将细碰撞表面和粗弹性状态分离，是比简单网格粗化更有价值的设计；链式投影保留 IPC 接触机制。^[sources/papers/du2024-embedded-ipc.md]

## 优点
保留细几何接触；统一多个 IPC 约化层级；推导清晰；实验直接覆盖软体夹持和薄结构密集接触。

## 局限
预印本；小子空间锁定；嵌入网格启发式；只支持体积软体；IPC 激活层存在作用距离；速度比较受并行实现差异影响；现实校准误差显著。

## 不应照搬
不能用单一粗四面体表示明显局部屈曲/断裂；不能把“无穿透”误写为“真实接触完全无近似”；不能把机器人小规模案例直接外推到建筑倒塌。

## 工程迁移推论
适合作为完全脱离碎片或近刚性构件的降阶碰撞模块；大变形破坏区需要动态扩充模态、切换到 MPM/FEM 或重新嵌入。

## 关联页面
- [[du2024-embedded-ipc-analysis]]
- [[du2024-embedded-ipc-method]]
- [[du2024-embedded-ipc-results]]
- [[entities/embedded-ipc]]
- [[concepts/coarse-elasticity-fine-contact-embedding]]
