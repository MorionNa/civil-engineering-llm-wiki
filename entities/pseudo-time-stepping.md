---
title: "Pseudo Time Stepping"
created: 2026-06-10
updated: 2026-06-13
type: entity
tags: [pinn, collocation-strategy, physics-informed]
sources: [raw/papers/wang2023-pinn-spurious.md]
---

# Pseudo-Time Stepping

## 概述

伪时间步进（Pseudo-Time Stepping）将稳态 PDE 转化为伪时间演化问题 `∂u/∂τ = N[u]`，通过逐步增大 τ 引导网络避开伪解（spurious solutions），最终收敛到真解。自适应变体通过局域残差 Jacobian 估计自动选最优步长，零调参。

**首次系统分析：** Wang et al. (2023), "When PINNs Go Wrong"

## 核心机制

```
随机初始化 → τ小(凸化loss, 避伪解) → τ中 → τ大(快速收敛) → PDE真解
```

- 小步长：凸化 loss landscape → 避开 trivial/spurious solutions
- 大步长：更快收敛，但风险跳进伪解
- 自适应：每步根据局域 Jacobian 谱半径选最大稳定步长

## 关键参数

| 参数 | 含义 | 选择方式 |
|------|------|----------|
| τ | 伪时间步长 | 自适应: `Δτ ≤ C / ρ(J)` |
| Collocation 重采样频率 | 每步/每N步 | 推荐每步 |

## 与其他物理约束方法的关系

- PINNs：伪时间步进是训练 stabilization 技术
- PhyLSTM：物理约束权重调参（physics-constraint-weight-tuning）的潜在解决方案——用自适应伪时间替代手动 α/β/γ 调参

## 关联

- [[wang2023-pinn-spurious-analysis]] — 论文分析
- [[wang2023-pinn-spurious-method]] — 方法展开
- [[zhang2020-phylstm-critical]] — PhyLSTM 的权重调参问题
- [[physics-constrained-training-failure-modes]] — 失败模式对比
