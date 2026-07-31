---
id: entities--at-pinn-hc
title: AT-PINN-HC
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- entity/model
- method/pinn
keywords:
- auxiliary-function
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- entity/model
- hard-constraints
- method/pinn
- physics-informed
- pinn
- structural-dynamics
- time-marching
- vibration-analysis
sources:
- raw/papers/10_1016_j_cma_2024_117691_extracted.txt
created: '2026-06-27'
updated: '2026-07-31'
confidence: medium
---

# AT-PINN-HC

## 概述

AT-PINN-HC（Advanced Time-marching Physics-Informed Neural Networks with Hard Constraints）是一种面向结构振动问题的时间推进 PINN 方法。由 Chen Zhaolin, Lai Siu-Kai 等 6 位于 2025 年在 CMAME 发表。核心创新是将三种硬约束策略（分别针对边界位移、初始位移、初始速度）与五类辅助函数（多项式、幂函数、三角函数、指数函数、对数函数）集成到时间推进 PINN 框架中，实现长时程振动模拟的精度突破——相比标准 PINN 误差降低 1-4 个数量级，训练迭代减少高达 78%。

**首次提出：** Chen et al. (2025), CMAME Vol. 436, 117691

## 核心组件

```
AT-PINN-HC
├── 时间推进框架 (Time-marching)
│   └── 长时程 [0,T] → N 个子区间，每段独立 PINN
├── 三种硬约束策略
│   ├── 边界位移 HC（空间边界）
│   ├── 初始位移 HC（t=0）
│   └── 初始速度 HC（∂u/∂t at t=0）
└── 五类辅助函数
    ├── 多项式  → 通用但非最优
    ├── 幂函数  → 分数阶灵活性
    ├── 三角函数 → ★ 边界位移最优
    ├── 指数函数 → ★ 初始位移/速度最优
    └── 对数函数 → 不推荐（所有场景均差）
```

## 关键设计原则

1. **硬约束 = 架构级保证：** 网络输出显式乘入辅助函数，BC/IC 自动精确满足
2. **辅助函数的导数决定精度：** 不是函数值本身，而是导数在约束点附近的行为
3. **按场景选择：** 空间边界 → 三角函数（导数在边界处为零且平缓）；时间初始条件 → 指数函数（导数快速衰减）
4. **时间推进遏制误差累积：** 分段策略将长时程误差控制在子区间内

## 验证基准

| # | 基准 | 领域 |
|---|------|------|
| 1 | Euler-Bernoulli 梁 | 经典结构动力学 |
| 2 | 超音速飞行器蒙皮面板 | 航空航天（多物理场耦合） |
| 3 | 竖直站立玻璃板（风荷载） | 建筑/土木工程 |

## 与其他方法的关系

- **vs 标准 PINN（软约束）：** AT-PINN-HC 用架构级硬约束替代 loss 级软约束，BC/IC 精度提升 1-4 数量级
- **vs Wang et al. (2023) 伪时间步进：** 互补——伪时间步进解决 PDE 残差伪解问题，AT-PINN-HC 解决 BC/IC 精度问题，可联合使用
- **vs PhyLSTM：** 软约束（PhyLSTM）vs 硬约束（AT-PINN-HC），不同范式——PhyLSTM 的物理约束权重调参问题正是硬约束可规避的

## 关联

- [[chen2025-at-pinn-hc-analysis]] — 完整论文分析（12 维度）
- [[chen2025-at-pinn-hc-method]] — 方法机制展开
- [[chen2025-at-pinn-hc-results]] — 实验结果展开
- [[chen2025-at-pinn-hc-critical]] — 贡献 / Negative / 可迁移 / 研究机会
- [[wang2023-pinn-spurious-analysis]] — PINN 伪解分析（互补方向）
- [[zhang2020-phylstm-analysis]] — PhyLSTM（软约束对比）
- [[pseudo-time-stepping]] — 伪时间步进（潜在结合方向）

## Evidence By Source

### `raw/papers/10_1016_j_cma_2024_117691_extracted.txt`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/10_1016_j_cma_2024_117691_extracted.txt]
