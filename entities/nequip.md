---
id: entity-nequip
title: "NequIP — E(3) 等变图神经网络原子势"
type: entity
status: verified
project: civil-engineering-llm-wiki
tags: [neural-network, deep-learning, physics-simulation, scientific-machine-learning, ai4s, material-design, se3-equivariance]
sources: [raw/papers/batzner2022-nequip-source.md]
created: 2026-07-31
updated: 2026-07-31
confidence: high
---

# NequIP

## Definition

NequIP（Neural Equivariant Interatomic Potential）是一种 E(3) 等变图神经网络原子势。它把原子结构表示为局部邻接图，在节点隐藏状态中保留标量、向量和高阶几何张量，并通过球谐函数、径向网络与 Clebsch–Gordan 张量积构造旋转、反射和平移一致的消息传递。^[raw/papers/batzner2022-nequip-source.md]

提出论文：[[batzner2022-nequip-analysis]]。

## Role In This Knowledge Base

NequIP 是“物理图表示”知识链的起点：

```text
NequIP：等变表示与数据效率
          ↓
Allegro：严格局部高阶表示
          ↓
SevenNet：多 GPU 消息传递并行
          ↓
大规模结构图学习与物理信息动力求解
```

## Inputs And Outputs

```text
原子种类 Z_i + 原子坐标 r_i
              ↓
局部邻接图
              ↓
E(3)-equivariant interaction blocks
              ↓
每原子势能 E_i
              ↓
总势能 E = ΣE_i
              ↓
F_i = -∂E/∂r_i
```

模型先预测标量总势能，再通过自动微分得到力，因此力场与势能保持一致，而不是将每个力分量独立回归。^[raw/papers/batzner2022-nequip-source.md]

## Key Mechanisms

- **O(3) 不可约表示：** 按旋转阶数 $l$ 和奇偶性 $p$ 组织隐藏特征；
- **径向网络：** 从原子间距离生成旋转不变权重；
- **球谐方向基：** 编码边方向；
- **等变张量积：** 按对称选择规则组合邻居特征与方向滤波器；
- **门控非线性和残差更新：** 在保持等变性的同时提高深层表达能力；
- **势能梯度：** 保证预测力来自同一势能函数。

## Evidence

论文在 MD-17、水/冰、反应表面、非晶磷酸锂和 LiPS 超离子导体上验证。水/冰任务中，NequIP 用 133 个训练构型获得低于使用 133,500 个构型的 DeepMD 的力误差；LiPS 扩散率与 AIMD 相差约 9%。^[raw/papers/batzner2022-nequip-source.md]

## Relationship To Allegro And SevenNet

| 模型 | 主要解决的问题 |
|---|---|
| NequIP | 用 E(3) 等变消息传递提高精度与数据效率 |
| [[allegro]] | 取消跨层 atom-centered message passing，以严格局部表示提高超大规模扩展性 |
| [[sevennet]] | 保留 NequIP 类消息传递，通过正向特征通信和反向梯度通信实现多 GPU 空间分解 |

## Boundary And Caveats

- 多层消息传递扩大有效感受野，分布式推理需要逐层通信；
- 固定 cutoff 不能自动覆盖长程静电和色散；
- 等变性不保证材料本构、数据覆盖或时间积分稳定；
- 原子能分解不是唯一可解释物理分解；
- 更高旋转阶增加计算成本，未必具有普遍最优性。

## Structural-Dynamics Transfer

以下为迁移推论：

1. 将节点位移、速度、内力、方向和局部坐标系组织为具有明确变换规律的特征；
2. 用几何等变聚合替代只依赖标量边权的普通 GNN；
3. 由局部能量或势函数求导得到保守内力，并为滞回/损伤另设耗散与内部变量模块；
4. 与矩阵边权、子结构划分和动力平衡残差组合，形成大规模结构图 PINN；
5. 根据重力、支座和构件局部轴定义适合结构工程的对称群，而不是机械照搬完整 E(3)。

## Related Pages

- [[batzner2022-nequip-analysis]]
- [[batzner2022-nequip-method]]
- [[batzner2022-nequip-results]]
- [[batzner2022-nequip-critical]]
- [[allegro]]
- [[sevennet]]
- [[pinn]]
- [[seisgpt]]
