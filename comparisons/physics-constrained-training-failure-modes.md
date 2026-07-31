---
id: comparisons--physics-constrained-training-failure-modes
title: 物理约束训练的失败模式对比 — PhyLSTM vs PINN
type: comparison
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- method/evaluation
- method/pinn
keywords:
- architecture-mismatch-failure
- limitation
- loss-function-weakness
- phylstm2
- phylstm3
- physics-constrained-loss
- pinn
- pseudo-time-stepping
- spurious-solutions
sources:
- raw/papers/zhang2020-phylstm.md
- raw/papers/wang2023-pinn-spurious.md
created: '2026-06-10'
updated: '2026-07-31'
confidence: high
results:
- cross-domain-generalization
- extrapolation-ability
- spurious-solution-avoidance
- adaptive-step-size
failure_modes:
- architecture-mismatch-failure
- finite-difference-error
- physics-constraint-weight-tuning
- loss-function-weakness
- step-size-sensitivity
- optimization-vs-accuracy-tradeoff
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
- [[wang2023-pinn-spurious-analysis]] — PINN 概述
- [[wang2023-pinn-spurious-critical]] — PINN failure_modes
- [[pseudo-time-stepping]] — 伪时间步进方法

## Evidence By Source

### `raw/papers/zhang2020-phylstm.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/zhang2020-phylstm.md]
