---
title: "SevenNet — 可扩展并行等变 GNN 原子势"
created: 2026-07-31
updated: 2026-07-31
type: entity
tags: [graph-neural-network, equivariant-gnn, distributed-computing, machine-learning-potential, molecular-dynamics]
sources: [raw/papers/park2024-sevennet-parallel-gnn-ip-source.md]
confidence: high
---

# SevenNet

SevenNet 是 Park et al. 提出的面向大规模分子动力学模拟的可扩展 GNN interatomic potential 实现。它基于 NequIP 架构，通过针对 message passing 的空间分解并行算法连接 LAMMPS。

## 核心机制

```text
simulation domain
        ↓
spatial decomposition
        ↓
subdomain graph
        ↓
message passing
        ↓
forward communication
(node features)
        ↓
energy
        ↓
reverse communication
(gradients)
        ↓
forces
```

## 与 Allegro 的关系

- [[allegro]]：通过严格局部等变表示减少消息传递带来的扩展问题；
- SevenNet：保留 NequIP message passing，通过通信设计解决并行问题。

## 对结构动力学的启发

- ghost atom ↔ 子结构边界节点；
- spatial decomposition ↔ 大型结构图子域划分；
- node feature exchange ↔ 子图间力学状态交换。

## 关联

- [[park2024-sevennet-parallel-gnn-ip-analysis]]
- [[allegro]]
- [[mechconv]]
