---
title: "Allegro — 严格局部等变原子势"
created: 2026-07-31
updated: 2026-07-31
type: entity
tags: [deep-learning, neural-network, scientific-machine-learning, physics-simulation, gpu-computing, material-design, cross-domain-generalization]
sources: [raw/papers/musaelian2023-allegro-source.md]
confidence: high
---

# Allegro

## 定义

Allegro 是一种用于机器学习原子间势的严格局部等变神经网络。它不依赖以原子为中心的跨层消息传递，而是在每个中心原子的固定截断邻域内，对有序邻居对建立标量潜空间与等变张量潜空间，并通过迭代张量积学习多体相互作用。

提出论文：[[musaelian2023-allegro-analysis]]。

## 核心结构

```text
原子种类 + 邻居距离
          ↓
Two-body MLP → 标量 pair latent
          ↓
球谐方向表示 → 等变 pair latent
          ↓
局部环境加权聚合 + 张量积
          ↓
标量/张量双潜空间逐层更新
          ↓
pair energy E_ij
          ↓
总能量求和 + 自动微分
          ↓
原子力
```

Allegro 将系统总能量分解为原子能，再将原子能分解为有序 pair energy。虽然记号是 $E_{ij}$，它仍可依赖中心原子 $i$ 的完整局部邻域，因此不是普通二体势。

## 与相邻方法的区别

| 方法 | 信息传播 | 可扩展性要点 |
|---|---|---|
| NequIP 等 MPNN | 多层节点消息传递，感受野随层数扩大 | 精度高，但并行时需更大 ghost 区域或层间通信 |
| ACE | 固定径向—化学基上的系统体阶展开 | 系统性强，但基维度随体阶和元素数增长 |
| Allegro | 固定截断内的 pair-centered 等变张量积 | 严格局部，可直接使用空间分解并行 |
| [[sevennet]] | 保留 NequIP 消息传递，通过正反向特征通信并行 | 解决消息传递模型并行，而非删除消息传递 |

## 计算性质

- 对原子数近似线性扩展；
- 对每个原子的邻居数近似线性；
- 模型通道数可设计为与元素种类数无关；
- 严格局部使不同中心原子邻域的能量与力贡献可以并行计算；
- 代价是 pair-centered 特征通常比相同通道数的 atom-centered 特征占用更多显存。

## 对结构动力学的迁移

Allegro 的关键启示不是直接把原子势用于结构，而是：

1. **局部高阶机制不必依赖多跳消息传递。** 可在构件或节点局部邻域内，通过几何张量积学习多构件耦合；
2. **严格局部骨干可与显式全局物理项组合。** 对结构动力可将局部非线性构件算子与全局平衡方程、模态或长程耦合项分开；
3. **分区边界通信可以固定在一层邻域。** 有利于千自由度以上结构的子图训练和并行推理；
4. **输出应保持能量一致性。** 可由势能或局部恢复能量求导得到内力，而不是直接独立预测不守恒的力。

## 风险与边界

- 严格局部模型不能自动表示超出截断半径的静电、弹性或其他长程作用；
- 局部高阶张量积的表达能力受截断、最大旋转阶、层数和通道数控制；
- 百万/亿原子扩展实验依赖规则空间分解和高性能 GPU 集群，不能直接外推到任意图拓扑；
- 原子系统的 E(3) 对称性与建筑结构图的边界、方向和构件类型约束并不完全相同。

## 关联页面

- [[musaelian2023-allegro-analysis]]
- [[musaelian2023-allegro-method]]
- [[musaelian2023-allegro-results]]
- [[musaelian2023-allegro-critical]]
- [[sevennet]]
- [[neural-operator]]
- [[pinn]]
