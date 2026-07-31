---
id: entity-sevennet
title: "SevenNet — 分布式等变 GNN 原子势"
type: entity
status: verified
project: civil-engineering-llm-wiki
tags: [neural-network, deep-learning, physics-simulation, scientific-machine-learning, ai4s, material-design, distributed-training, gpu-computing]
sources: [raw/papers/park2024-sevennet-parallel-gnn-ip-source.md]
created: 2026-07-31
updated: 2026-07-31
confidence: high
---

# SevenNet

## Definition

SevenNet 是一个面向等变图神经网络原子势的软件与模型体系。其并行算法把模拟空间划分为多个子域，在每个 message-passing 层交换边界节点隐藏特征，并在能量求导的反向阶段交换对应梯度，从而保持分布式能量和力与完整图计算一致。^[raw/papers/park2024-sevennet-parallel-gnn-ip-source.md]

提出论文：[[park2024-sevennet-parallel-gnn-ip-analysis]]。

## Role In This Knowledge Base

SevenNet 是“保留多跳消息传递时如何并行”的代表路线：

```text
[[nequip]]：等变消息传递骨干
          ↓
SevenNet：逐层正向特征 + 反向梯度通信
          ↓
大规模分布式 MD
```

它与 [[allegro]] 的严格局部路线互补：Allegro 改变架构以取消跨层通信，SevenNet 保留架构并优化通信。

## Parallel Data Flow

```text
owned atoms + cutoff ghost atoms
          ↓
本地第 l 层 message passing
          ↓
交换边界 h^(l+1)
          ↓
下一层
          ↓
owned 原子能求和
          ↓
反向逐层交换 feature gradients
          ↓
坐标梯度与原子力
```

## Evidence

论文报告 32 GPU 弱扩展并行效率超过 80%，并以 SevenNet-0 在非晶 SiO$_2$ 与约 112,000 原子 Si$_3$N$_4$ 体系中开展验证。SevenNet-0 使用 Materials Project/M3GNet 数据训练并覆盖 89 种元素。^[raw/papers/park2024-sevennet-parallel-gnn-ip-source.md]

## Key Distinctions

| 对象 | 含义 |
|---|---|
| SevenNet 并行算法 | 多层 GNN-IP 的空间分解、正向特征通信和反向梯度通信 |
| SevenNet 软件 | 训练、推理、预训练模型和 LAMMPS 集成实现 |
| SevenNet-0 | 使用特定多元素数据训练的通用预训练原子势 |

三者相关但不能互相替代：并行算法正确不表示预训练模型对所有材料准确。

## Boundary And Caveats

- 通信轮数随 message-passing 深度增长；
- 隐藏特征越宽、张量阶越高，通信量越大；
- 子域过小会导致 GPU underutilization；
- 不均匀密度和异构体系会造成负载失衡；
- 89 元素覆盖不等于任意组合与相态可靠；
- 本知识页基于 arXiv v1，后续软件和论文版本需单独核对。

## Structural-Dynamics Transfer

以下为迁移推论：

1. 按楼层、构件簇或子结构划分大规模结构图；
2. 把共享自由度和边界节点作为 ghost nodes；
3. 在每层图聚合后同步边界隐藏状态；
4. 在训练反向阶段汇总跨子图梯度；
5. 分别约束子域动力平衡、接口位移协调和界面力平衡；
6. 比较逐层通信与 Allegro 式严格局部骨干的通信—精度权衡。

## Related Pages

- [[park2024-sevennet-parallel-gnn-ip-analysis]]
- [[park2024-sevennet-parallel-gnn-ip-method]]
- [[park2024-sevennet-parallel-gnn-ip-results]]
- [[park2024-sevennet-parallel-gnn-ip-critical]]
- [[nequip]]
- [[allegro]]
- [[pinn]]
- [[seisgpt]]
