---
id: concept--active-node-compact-indexing
title: 活跃节点紧凑索引 — 物理网格坐标与存储位置解耦
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- active-node-set
- compact-index-map
- sparse-background-grid
- sparse-storage
sources:
- sources/papers/zhao2026-unified-sparse-mpm.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
---

# 活跃节点紧凑索引

## 定义

在粒子–网格方法中，活跃节点集由所有粒子局部形函数支撑的并集构成：$A=\bigcup_pS(p)$。紧凑索引映射 $\phi:A\rightarrow\{0,\ldots,|A|-1\}$ 把物理网格节点坐标映射到连续内存位置，只为当前参与计算的节点保存数据。^[sources/papers/zhao2026-unified-sparse-mpm.md]

## 核心意义

结构网格仍负责定义节点物理位置、邻接关系和形函数；紧凑索引只负责数据布局。两者分离后，P2G、节点更新和 G2P 的物理公式无需修改，稀疏集合的构造则可由扫描、哈希或其他硬件适配算法完成。

## 实现层次

- 节点级：内存最紧凑，但掩码、索引和随机访问成本可能更高；
- 块级：对活跃块内部节点连续分配，牺牲少量额外空间换取更小元数据和更好局部性；
- 分布式扩展：还需增加块所有权、ghost 区域和跨设备通信映射。

## 收益条件

收益取决于稠密候选节点数与活跃节点数之比。长距离流动、局部材料带和大范围空域通常适合；材料接近填满计算域时，重建索引的开销可能抵消节省。

## 失效与风险

紧凑索引不能减少粒子遍历、本构更新或粒子支撑枚举成本；也不会自动提高物理模型精度。动态集合变化还可能引入哈希竞争、扫描同步、内存重分配和负载不均衡。

## 关联页面

- [[entities/unified-sparse-mpm]]
- [[comparisons/scan-vs-hash-sparse-mpm]]
- [[zhao2026-unified-sparse-mpm-method]]
- [[zhao2026-unified-sparse-mpm-critical]]
