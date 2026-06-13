---
title: "Wang et al. (2023) — 贡献 / 知识点 / Negative / 可迁移 / 研究机会"
created: 2026-06-10
updated: 2026-06-10
type: paper-analysis
tags: [pinns, spurious-solutions, pseudo-time-stepping, loss-function-weakness, step-size-sensitivity, zero-tuning, future-work]
sources: [raw/papers/wang2023-pinn-spurious.md]
methods: [pseudo-time-stepping, adaptive-pseudo-time-stepping]
results: [spurious-solution-avoidance, adaptive-step-size]
failure_modes: [loss-function-weakness, step-size-sensitivity, optimization-vs-accuracy-tradeoff]
confidence: high
---

# Wang et al. (2023) — 贡献 / 知识点 / Negative / 可迁移 / 研究机会

> 返回概述 → [[wang2023-pinn-spurious-analysis]]

---

## 7. 贡献

1. **从理论上揭示 PDE 残差 loss 的固有缺陷**——会接受 trivial/spurious solutions（不只是优化问题）
2. **阐明伪时间步进的真正机制**——不是优化辅助，而是通过逐步增加问题难度避开伪解
3. **自适应步长方法**——基于局域残差 Jacobian 有限差分估计，零调参，保证局部稳定
4. 在多个 PDE benchmark 上一致优于固定步长和 baseline
5. 开源 JAX 实现 jaxpi2

> 与 PhyLSTM 的贡献对比：PhyLSTM 贡献了物理约束嵌入新架构；PINN 贡献了物理约束训练稳定性的通用方法。互补而非竞争。

---

## 8. 核心知识点

1. **PDE 残差 loss 小 ≠ 解正确**——这是 loss 函数的固有弱点，不是优化问题
2. **伪时间步进 = 凸化 + 避伪解**——小步长凸化 loss landscape，逐步逼近真解
3. **步长选择是关键**——太小太慢，太大跳到伪解，自适应是最优解
4. **Collocation 重采样 + 伪时间 = 双重保护**——两者配合效果最佳
5. **自适应步长的本质**——用局域 Jacobian 估计保证局部稳定性，零调参

---

## 9. Negative Knowledge

### 方法局限

| 局限 | 细节 | 严重度 |
|------|------|--------|
| 步长敏感 | 固定步长在一个 benchmark 最优，另一个可能失败 | 🔴 高 |
| Jacobian 有限差分误差 | 步长估计依赖数值微分精度 | 🟡 中 |
| 稳态 PDE 为主 | 动态系统扩展未充分验证 | 🟡 中 |
| Collocation 重采样的随机性 | 可能引入方差 | 🟢 低 |

### 未解决的问题

- 自适应步长依赖 Jacobian 的有限差分估计 → 引入数值误差（与 PhyLSTM 相同：[[zhang2020-phylstm-critical]]，finite-difference-error）
- 仅验证稳态 PDE，动态/时变系统的伪时间策略待探索
- 伪时间步进的**数学收敛性证明**不完整

### 不该照搬的做法

1. ❌ 不要相信 loss 曲线——PDE 残差下降不代表解在变好
2. ❌ 不要在所有问题用同一个固定步长
3. ❌ 不要在无 collocation 重采样的情况下使用伪时间步进

---

## 10. 可迁移知识

| 知识 | 迁移方向 |
|------|----------|
| 伪时间步进 + collocation 重采样 | 任何物理约束训练的稳定性问题（包括 PhyLSTM 的权重调参问题：[[zhang2020-phylstm-critical]]，physics-constraint-weight-tuning） |
| 自适应步长 (Jacobian 有限差分) | 任何需要步长/权重调参的物理约束方法 |
| PDE 残差 loss 缺陷分析 | 设计新物理 loss 时的警示——必须考虑伪解 |
| Collocation 每步重采样 | 任何基于配点的物理信息训练 |

---

## 11. 研究机会

| # | 方向 | 具体思路 | 难度 |
|---|------|----------|------|
| 1 | **动态 PDE 扩展** | 将伪时间步进推广到时变 PDE | 🔴 高 |
| 2 | 高阶自适应 (autodiff Jacobian) | 用自动微分替代有限差分估计 | 🟢 低 |
| 3 | **与 PhyLSTM 结合** | 用伪时间步进替代 PhyLSTM 的手动权重调参 | 🟡 中 |
| 4 | 多保真度伪时间 | 结合低保真+高保真物理约束 | 🟡 中 |
| 5 | 收敛性理论 | 伪时间步进的数学收敛性证明 | 🔴 高 |
| 6 | 非稳态 PDE 的自适应 | Rayleigh-Taylor 是第一步，推广到更复杂瞬态问题 | 🟡 中 |

---

## 关联

- [[wang2023-pinn-spurious-analysis]] — 概述
- [[zhang2020-phylstm-critical]] — PhyLSTM 的 failure_modes / 物理约束局限
- [[physics-constrained-training-failure-modes]] — 两篇论文的失败模式对比
