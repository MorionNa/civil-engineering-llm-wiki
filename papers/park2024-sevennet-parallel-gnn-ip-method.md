---
title: "Park et al. (2024) SevenNet Method"
created: 2026-07-31
updated: 2026-07-31
type: paper-method
---

# SevenNet 方法机制

## GNN-IP 基础

GNN-IP 使用原子图：

- 节点：原子；
- 边：cutoff 半径内原子连接；
- message passing：更新节点特征。

论文采用 NequIP 作为基础架构。

## 并行核心

传统空间分解：

```text
processor domain
      ↓
ghost atoms
      ↓
local computation
```

SevenNet 扩展：

```text
Initial communication
(r, Z)
      ↓
Message passing
      ↓
Forward communication
(node features h)
      ↓
Energy
      ↓
Reverse communication
(∇hE)
      ↓
Forces
```

## Forward communication

在 message passing 后续层中交换 ghost atom 的节点特征，使每个子域可以继续计算。

## Reverse communication

由于力由：

\[
F_i=-\nabla_i E
\]

获得，需要反向传播能量梯度，并交换跨子域梯度信息。

## SevenNet 实现

- PyTorch；
- e3nn 保证等变运算；
- TorchScript 集成 LAMMPS；
- 支持 GPU 多节点模拟。

## 与结构图网络迁移

对应关系：

| SevenNet | 结构动力图模型 |
|-|-|
| atom node | structural node |
| atomic edge | beam/wall connection |
| message passing | mechanical interaction |
| ghost atom | substructure boundary node |
| distributed MD | large-scale graph dynamics |
