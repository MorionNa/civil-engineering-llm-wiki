---
id: entity-allegro
title: Allegro — 严格局部等变原子势
type: entity
status: verified
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- entity/tool
- method/pinn
keywords:
- ai4s
- deep-learning
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- entity/tool
- gpu-computing
- material-design
- method/pinn
- neural-network
- physics-simulation
- scientific-machine-learning
- se3-equivariance
sources:
- raw/papers/musaelian2023-allegro-source.md
created: '2026-07-31'
updated: '2026-07-31'
confidence: high
---

# Allegro

## Definition

Allegro 是一种用于机器学习原子势的严格局部等变神经网络。它不依赖以原子为中心的跨层消息传递，而是在每个中心原子的固定 cutoff 邻域内，对有序邻居对维护标量潜空间和等变张量潜空间，并通过学习环境嵌入与迭代张量积表示高阶多体相互作用。^[raw/papers/musaelian2023-allegro-source.md]

提出论文：[[musaelian2023-allegro-analysis]]。

## Role In This Knowledge Base

Allegro 位于以下知识链中：

```text
[[nequip]]：高精度与数据效率的等变消息传递
          ↓
Allegro：严格局部高阶等变表示
          ↓
[[sevennet]]：保留消息传递时的分布式并行
```

它为用户的大规模结构动力研究提供“固定通信半径下提高局部表示复杂度”的架构参照。

## Core Representation

```text
中心—邻居有向 pair (i,j)
      ↓
距离/元素 → invariant scalar latent
方向球谐 → equivariant tensor latent
      ↓
中心局部环境的可学习加权聚合
      ↓
迭代等变张量积
      ↓
pair energy E_ij
      ↓
总能量与能量梯度力
```

## Evidence

论文在 revised MD-17、3BPA 和 QM9 上展示竞争精度；在 Li$_3$PO$_4$ 上恢复 AIMD 的结构与 Li 动力学；在 128 张 A100 GPU 上完成超过一亿个 Ag 原子的分子动力学模拟。^[raw/papers/musaelian2023-allegro-source.md]

## Key Differences

| 方法 | 局部表示机制 | 扩展性特征 |
|---|---|---|
| [[nequip]] | 多层 atom-centered 等变消息传递 | 表达强，但有效感受野和通信随层数扩大 |
| Allegro | 固定邻域内 pair-centered 迭代张量积 | 通信半径固定，适合空间分解 |
| ACE | 固定径向—化学基的系统体阶展开 | 可系统提升，但基维随体阶增长 |
| [[sevennet]] | 保留 NequIP 类消息传递并逐层通信 | 在不改变模型输出的前提下并行化 |

## Boundary And Caveats

- 严格局部不能自动表示 cutoff 外长程作用；
- pair-centered 特征随有向边数增长，显存可能成为瓶颈；
- 不同精度与 scaling 结果使用不同网络容量；
- 亿原子模拟依赖特定 HPC 软件栈和规则空间分解；
- 学习到的 pair energy 不是唯一可解释二体势。

## Structural-Dynamics Transfer

以下为迁移推论：

1. 在梁柱端、节点—构件接口维护有向 pair 状态；
2. 在固定一跳邻域内用高阶几何交互替代多跳消息传播；
3. 将材料内部变量放在标量潜空间，将方向相关力学量放在等变潜空间；
4. 由局部势能得到保守内力，并以耗散模块处理塑性和损伤；
5. 增加显式全局模态或动力平衡通道，补足严格局部的远程耦合缺口。

## Related Pages

- [[musaelian2023-allegro-analysis]]
- [[musaelian2023-allegro-method]]
- [[musaelian2023-allegro-results]]
- [[musaelian2023-allegro-critical]]
- [[nequip]]
- [[sevennet]]
- [[pinn]]
- [[seisgpt]]
