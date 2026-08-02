---
id: entity--unified-sparse-mpm
title: Unified Sparse MPM — 架构解耦的活跃网格框架
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/computational-mechanics
- entity/model
- evidence/paper
keywords:
- active-grid
- block-sparse
- hash-based
- scan-based
- sparse-mpm
sources:
- sources/papers/zhao2026-unified-sparse-mpm.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
---

# Unified Sparse MPM

## 定义

Unified Sparse MPM 是 Zhao 等提出的背景网格存储框架。它把当前受粒子支撑影响的节点组成活跃集合，并用紧凑索引保存节点数据；MPM 的控制方程、形函数、粒子–网格传递与本构更新保持不变。^[sources/papers/zhao2026-unified-sparse-mpm.md]

## 核心组成

- [[concepts/active-node-compact-indexing]]：物理网格坐标与内存位置解耦；
- 块级活跃网格：以 $4^3$ 节点块降低索引元数据和改善局部性；
- CPU 扫描式实现：二值活动掩码、并行 prefix scan 与连续数组；
- GPU 哈希式实现：64 位 key、混合哈希、线性探测和原子插入；
- 运行时每步根据粒子位置重建活跃块集合。

## 数值与性能角色

框架不改变标准显式 APIC-MPM 的数值结果。其价值主要出现在材料占据区域远小于潜在运动域的强稀疏问题；Blatten 案例显示单机 CPU/GPU 的时间和内存可降低一至两个数量级。

## 开源实现

- CPU：Matter，GPL-3.0；
- GPU：sparse_MPM，MIT，构建于 GeoWarp。

## 适用边界

当前证据集中于单节点、显式 APIC-MPM、弹性与 Drucker–Prager 材料。低稀疏度下可能没有收益；多 GPU、隐式求解、多相耦合和结构–颗粒混合模型仍需扩展。

## 项目角色

可作为大范围地质流动和局部 MPM 倒塌区域的底层内存/索引模块，并与 [[mpm-lite]]、[[stabilized-fractional-step-two-phase-mpm]] 形成互补研究链，但组合性能尚未验证。

## 关联页面

- [[zhao2026-unified-sparse-mpm-analysis]]
- [[zhao2026-unified-sparse-mpm-method]]
- [[zhao2026-unified-sparse-mpm-results]]
- [[zhao2026-unified-sparse-mpm-critical]]
- [[comparisons/scan-vs-hash-sparse-mpm]]
