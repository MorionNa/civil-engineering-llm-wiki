---
title: "物理约束训练的失败模式对比 — PhyLSTM vs PINN"
created: 2026-06-10
updated: 2026-06-10
type: comparison
tags: [physics-constrained-loss, failure-modes, pinns, phylstm2, phylstm3, pseudo-time-stepping, spurious-solutions, architecture-mismatch-failure, loss-function-weakness]
sources: [raw/papers/zhang2020-phylstm.md, raw/papers/muller2023-pinn-spurious.md]
results: [cross-domain-generalization, extrapolation-ability, spurious-solution-avoidance, adaptive-step-size]
failure_modes: [architecture-mismatch-failure, finite-difference-error, physics-constraint-weight-tuning, loss-function-weakness, step-size-sensitivity, optimization-vs-accuracy-tradeoff]
confidence: high
---

# 物理约束训练的失败模式对比 — PhyLSTM vs PINN

## 失败原因对比

| 失败类型 | PhyLSTM | PINN |
|----------|---------|------|
| **核心原因** | 架构-物理不匹配 (architecture-mismatch-failure) | PDE 残差 loss 接受伪解 (loss-function-weakness) |
| **表现** | PhyLSTM2 在率相关滞回 γ=0.19 | Baseline loss → 0 但 L2 error 不降 |
| **是否可修复** | 换 PhyLSTM3 ✓ | 伪时间步进 ✓ |
| **诊断难度** | 中等（需知道滞回类型） | 高（loss 不可靠） |

## 共同问题

| 问题 | PhyLSTM | PINN | 严重度 |
|------|---------|------|--------|
| 有限差分数值误差 | ✓ (Tensor Differentiator) | ✓ (Jacobian 估计) | 🟡 |
| 超参数调参 | α/β/γ 手动 | 步长 τ 手动（固定步长） | 🔴 |
| 仅低维/稳态验证 | 3-DOF/SDOF | 稳态 PDE 为主 | 🟡 |

## 互补方案

| 方案 | PhyLSTM 受益 | PINN 受益 |
|------|------------|----------|
| 自适应伪时间步进 | 替代手动 α/β/γ 调参 | 已有 |
| 多网络架构 | 已有 (PhyLSTM2/3) | 可用于多保真度 PDE |
| 跨域泛化验证 | 已有 (BLWN→地震) | 可借鉴验证策略 |

## 判决

两篇论文都揭示了**物理约束训练的根本问题不在优化，而在约束本身的弱点**：
- PhyLSTM：约束与架构的匹配
- PINN：约束 loss 的伪解容忍性

> 核心教训：**物理信息 ≠ 无代价。理解失败模式比调参更重要。**

## 关联

- [[zhang2020-phylstm-analysis]] — PhyLSTM 概述
- [[zhang2020-phylstm-critical]] — PhyLSTM failure_modes
- [[muller2023-pinn-spurious-analysis]] — PINN 概述
- [[muller2023-pinn-spurious-critical]] — PINN failure_modes
- [[pseudo-time-stepping]] — 伪时间步进方法
