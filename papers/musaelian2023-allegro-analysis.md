---
title: "Musaelian et al. (2023) — Allegro：局部等变表示实现超大规模图动力学"
created: 2026-07-31
updated: 2026-07-31
type: paper-analysis
tags: [equivariant-gnn, graph-neural-network, local-representation, large-scale-simulation, message-passing, computational-mechanics]
sources: [raw/papers/musaelian2023-allegro-source.md]
confidence: high
---

# Learning local equivariant representations for large-scale atomistic dynamics

## 核心定位

本文提出 Allegro，一种严格局部（strictly local）的等变深度神经网络原子势模型，在保持等变 GNN 精度的同时突破 message passing 在超大规模模拟中的通信瓶颈。论文指出传统 atom-centered MPNN 通过多轮消息传播扩大感受野，限制并行扩展；Allegro 通过局部等变表示避免该问题。fileciteturn95file0L10-L19

## 主要贡献

1. 提出不依赖 atom-centered message passing 的局部等变表示；
2. 使用迭代 tensor product 学习多体相互作用；
3. 保持线性规模扩展能力；
4. 在百万至亿级原子模拟中验证可扩展性。

## 与结构动力学的关联

Allegro 的核心思想：

```
局部邻域
 ↓
等变表示
 ↓
图节点能量/响应
 ↓
全局动力学
```

对应结构动力学：

```
局部构件环境
 ↓
局部力学状态表示
 ↓
节点/构件响应预测
 ↓
大规模结构动力分析
```

关联：[[sevennet]], [[mechconv]], [[pinn]], [[neural-operator]].
