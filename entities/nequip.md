---
title: "NequIP — E(3) 等变图神经网络原子势"
created: 2026-07-31
updated: 2026-07-31
type: entity
tags: [graph-neural-network, equivariant-gnn, physics-simulation, scientific-machine-learning, ai4s, material-design]
sources: [raw/papers/batzner2022-nequip-source.md]
confidence: high
---

# NequIP

## 定义

NequIP（Neural Equivariant Interatomic Potential）是一种用于机器学习原子间势的 E(3) 等变图神经网络。它把原子结构表示为局部邻接图，在节点特征中同时保留标量、向量和更高阶几何张量，并通过球谐函数、径向网络与 Clebsch–Gordan 张量积构造旋转、反射和平移对称的卷积。

提出论文：[[batzner2022-nequip-analysis]]。

## 输入与输出

```text
原子种类 Z_i + 原子坐标 r_i
              ↓
局部邻接图（cutoff）
              ↓
E(3)-equivariant interaction blocks
              ↓
每原子势能 E_i
              ↓
总势能 E = ΣE_i
              ↓
F_i = -∂E/∂r_i
```

模型先预测标量总势能，再通过自动微分得到力，因此力场与势能一致，而不是将每个力分量独立回归。

## 核心构件

- **O(3) 不可约表示：** 内部特征按旋转阶数与奇偶性组织；
- **径向网络：** 从原子间距离生成可学习的旋转不变权重；
- **球谐函数：** 表示邻接边的方向；
- **等变张量积：** 将邻居特征与方向滤波器按对称选择规则组合；
- **门控非线性与残差更新：** 在保持等变性的同时提高深层网络表达能力；
- **局部截断：** 控制计算量，但多层消息传递仍会扩大有效感受野。

## 数据效率含义

NequIP 的关键价值不只是降低单个基准误差，而是把已知几何对称性直接写入网络。与只使用旋转不变标量的模型相比，等变模型不必从数据中重新学习坐标变换规律，因此在少量第一性原理样本下表现出更快的学习曲线。

## 与 Allegro 和 SevenNet 的关系

| 模型 | 主要解决的问题 |
|---|---|
| NequIP | 以 E(3) 等变消息传递提高精度与数据效率 |
| [[allegro]] | 移除跨层 atom-centered message passing，以严格局部表示提高超大规模扩展性 |
| [[sevennet]] | 保留 NequIP 类消息传递，通过正向特征通信和反向梯度通信实现多 GPU 空间分解 |

因此三者形成“高质量表示—严格局部替代—分布式并行保留”三条互补路线。

## 对结构动力学的迁移

1. 将节点位移、速度、内力、方向和局部坐标系分成具有明确变换规律的标量/向量/张量特征；
2. 用几何等变聚合替代仅依赖标量边权的普通 GNN；
3. 由局部能量或势函数求导得到恢复力，提高能量一致性；
4. 与 MechConv 的矩阵边权、子结构划分和动力平衡残差组合，形成大规模结构图 PINN；
5. 对建筑边界、支座、构件局部轴和材料方向性，需要定义适合结构工程的等变群，而不能机械照搬原子系统的完整 E(3) 对称性。

## 风险与边界

- 多层消息传递扩大有效感受野，分布式推理需要更宽 ghost 区域或逐层通信；
- 固定 cutoff 不能自动覆盖静电、弹性等长程作用；
- 最大旋转阶、通道数、邻域半径和能量/力损失权重均影响精度与成本；
- 几何等变并不自动保证材料本构、边界条件和动力平衡正确；
- 深度原子势的物理可解释性仍弱于显式经验势。

## 关联页面

- [[batzner2022-nequip-analysis]]
- [[batzner2022-nequip-method]]
- [[batzner2022-nequip-results]]
- [[batzner2022-nequip-critical]]
- [[allegro]]
- [[sevennet]]
- [[pinn]]
