---
id: papers--chen2025-at-pinn-hc-method
title: Chen et al. (2025) — AT-PINN-HC 方法机制展开
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
- method/pinn
keywords:
- auxiliary-function
- deep-learning
- hard-constraints
- physics-informed
- pinn
- structural-dynamics
- time-marching
sources:
- sources/papers/chen2025-at-pinn-hc.md
created: '2026-06-27'
updated: '2026-07-31'
confidence: medium
methods:
- hard-constraint-strategies
- time-marching
- auxiliary-function
- trigonometric-auxiliary
- exponential-auxiliary
---

# Chen et al. (2025) — AT-PINN-HC 方法机制展开

> 返回概述 → [[chen2025-at-pinn-hc-analysis]]

## 核心框架：AT-PINN + HC

AT-PINN-HC = **Advanced Time-marching PINN** + **Hard Constraints**。将长时程振动问题分解为多个时间子区间，每个子区间内用 PINN 求解，硬约束保证每个子区间的边界条件和初始条件自动精确满足。

```
时间推进循环:
  t₀ → t₁ → t₂ → ... → t_N
   ↓      ↓      ↓         ↓
  PINN₁  PINN₂  PINN₃    PINN_N
   (每段内 HC 自动满足 BC + IC)
```

---

## 三种硬约束策略

针对结构振动问题的三类约束条件，分别设计专用策略：

### 策略 1：边界位移硬约束 (Boundary Displacement)

针对空间边界条件（如梁的固支/简支边界）。通过构造满足边界条件的辅助函数 `g(x)`，使网络输出形式为：

```
u(x, t) = g(x) · N(x, t; θ) + u_b(x)
```

其中 `u_b(x)` 是边界位移的显式表达式，`g(x)` 在边界上为零（确保网络输出自动满足边界条件）。

**关键：** `g(x)` 的导数 `g'(x)` 在边界处的行为影响精度——导数过小会"过度压制"网络自由度，导数过大会导致边界附近振荡。

### 策略 2：初始位移硬约束 (Initial Displacement)

针对时间初始条件 `u(x, 0) = u_0(x)`。构造：

```
u(x, t) = u_0(x) + h(t) · N(x, t; θ)
```

其中 `h(0) = 0`，保证 `t=0` 时网络输出退化为 `u_0(x)`。

### 策略 3：初始速度硬约束 (Initial Velocity)

针对时间导数初始条件 `∂u/∂t(x, 0) = v_0(x)`。需同时满足位移和速度的初始条件，更复杂：

```
u(x, t) = u_0(x) + t · v_0(x) + k(t) · N(x, t; θ)
```

其中 `k(0) = k'(0) = 0`，保证 `t=0` 时位移和速度都精确满足。

---

## 五类辅助函数

| 类型 | 形式示例 | 导数特性 | 适用场景 |
|------|----------|----------|----------|
| **多项式** | `t^n` | 导数在原点行为可控（n 可调） | 通用 |
| **幂函数** | `t^α`（α 可非整数） | 分数阶导数灵活性 | 特殊边界层 |
| **三角函数** | `sin(πt/T)` 或 `1-cos(πt/T)` | 导数在原点为 0 且平滑过渡 | **最优：边界位移** |
| **指数函数** | `1 - e^(-λt)` 或 `e^(-λt)` | 导数在原点非零，快速衰减 | **最优：初始位移/速度** |
| **对数函数** | `log(1 + βt)` | 导数在原点有限，缓慢增长 | 长时程稳定性 |

---

## 辅助函数导数→精度关系（核心理论发现）

论文最重要的理论贡献是建立了辅助函数导数与解精度之间的定量关系：

| 约束类型 | 最优辅助函数的导数行为 | 原理 |
|----------|------------------------|------|
| 边界位移（空间） | 在边界处为 0，但**接近边界时缓慢变化** | 避免过度约束网络自由度，让网络在域内自由拟合 PDE |
| 初始位移（时间） | 在 t=0 处为 0，且**快速回到 ~1** | 快速释放约束，让 PDE 残差 loss 主导后续训练 |
| 初始速度（时间） | 在 t=0 处函数值和一阶导数均为 0 | 同时满足位移+速度双约束 |

**经验法则：**
- 三角函数 `1-cos(πt/T)`：在 t=0 处平坦（导数=0），适合边界位移（空间边界）
- 指数函数 `1-e^(-λt)`：导数为 λ 且快速衰减，适合初始条件（时间边界）

---

## 训练策略

- **时间推进分段：** 将总仿真时长 `[0, T]` 分为 N 个子区间，每段独立训练一个 PINN
- **段间连续性：** 前一段的末端解作为下一段的初始条件
- **硬约束合入：** 每段 PINN 的架构中直接嵌入硬约束（非 loss 项），BC/IC 自动精确满足
- **优化：** 标准 Adam + L-BFGS 两阶段优化（与 [[wang2023-pinn-spurious-method]] 中描述的 adam-lbfgs, two-phase-optimization 一致）

---

## 与已有工作的关系

| | Wang et al. (2023) PINN 伪解 | Chen et al. (2025) AT-PINN-HC |
|---|---|---|
| 问题域 | 稳态 PDE | 动态振动 PDE |
| 策略 | 伪时间步进（避伪解） | 硬约束（自动满足 BC/IC） |
| 物理约束 | PDE 残差 loss（软） | 架构级硬编码 BC/IC（硬） |
| 辅助机制 | 自适应步长 | 辅助函数导数设计 |

二者互补：Wang 解决"loss 小但解错"问题，Chen 解决"BC/IC 软约束精度不足"问题。理论上可结合：用硬约束消除 BC/IC 误差 + 伪时间步进避免 PDE 残差伪解。

## 关联

- [[chen2025-at-pinn-hc-analysis]] — 论文概述
- [[chen2025-at-pinn-hc-results]] — 结果展开
- [[at-pinn-hc]] — AT-PINN-HC 实体页
- [[wang2023-pinn-spurious-method]] — 共享 adam-lbfgs, two-phase-optimization

## Evidence By Source

### `sources/papers/chen2025-at-pinn-hc.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/10_1016_j_cma_2024_117691_extracted.txt`

^[sources/papers/chen2025-at-pinn-hc.md]
