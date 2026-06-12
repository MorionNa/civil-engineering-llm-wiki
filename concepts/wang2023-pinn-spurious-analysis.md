---
title: "Wang et al. (2023) — When PINNs Go Wrong: Pseudo-Time Stepping Against Spurious Solutions"
created: 2026-06-10
updated: 2026-06-10
type: concept
tags: [pinns, physics-informed, spurious-solutions, pseudo-time-stepping, pde, physics-constrained-loss, soft-constraint, collocation-strategy, adam-lbfgs, two-phase-optimization, deep-learning]
sources: [raw/papers/wang2023-pinn-spurious.md]
methods: [pseudo-time-stepping, adaptive-pseudo-time-stepping, collocation-resampling, finite-difference-jacobian]
results: [spurious-solution-avoidance, adaptive-step-size]
failure_modes: [loss-function-weakness, step-size-sensitivity, optimization-vs-accuracy-tradeoff]
datasets: [pde-benchmarks, navier-stokes, rayleigh-taylor]
reproducibility: high
code_url:
  - https://github.com/sifanexisted/jaxpi2
dataset_url: []
confidence: high
---

# Wang et al. (2023) — When PINNs Go Wrong

> **Authors:** Sifan Wang, Shawn Koohy, Yiping Lu, Paris Perdikaris  
> **Code:** [sifanexisted/jaxpi2](https://github.com/sifanexisted/jaxpi2)

---

## 1. 工程背景

PINNs（物理信息神经网络）已被广泛用于求解 PDE、反问题、数据同化等科学计算任务。实际应用中用户经常发现：即使训练 loss 降到很低，预测结果在物理上却是错的。这不是收敛问题，而是**损失函数本身的缺陷**。理解为什么失败、如何修复，对 PINN 的工程落地至关重要。

## 2. Research Gap

已有工作大多把 PINN 失败归因于优化困难（非凸 loss、病态梯度），但作者论证：**即使 PDE 残差 loss 极小，仍可能收敛到物理上错误的伪解**。这是 PDE 残差 loss 的固有弱点——它允许 trivial/spurious solutions。伪时间步进虽已被实验证明有效，但其**为什么有效、步长如何选择**缺乏理论理解。

→ 已有 PhyLSTM 也讨论过物理约束的局限性：[[zhang2020-phylstm-critical#9-negative-knowledge]]（物理约束必须可微、权重调参难）。PINN 的 spurious-solutions 是物理约束失败的另一类原因。

## 3. 科学问题

**为什么 PDE 残差 loss 可以很小但解却是错的？伪时间步进是如何避开伪解的？如何自动选择最优步长？**

## 4. 研究目标

(1) 从理论上揭示伪解的成因；(2) 阐明伪时间步进的机制——不是优化技巧而是避免伪解的策略；(3) 提出自适应步长方法，不需要手动调参。

## 5. 方法机制

将稳态 PDE 视为动态系统的稳态极限，引入伪时间变量 τ 逐步逼近真解：
- 小步长 → 凸化 loss landscape，避开伪解
- 大步长 → 更快但可能跳进伪解
- **自适应步长：** 用局域残差 Jacobian 的有限差分估计选步长，保证局部稳定且最大步长

→ [[wang2023-pinn-spurious-method]] 完整架构 + 公式

训练：collocation-point 重采样（每步重采样配点）→ 这与 PhyLSTM 的配点策略共享同一设计模式：[[zhang2020-phylstm-method]]（collocation-strategy）。优化：Adam → L-BFGS，同 PhyLSTM：[[zhang2020-phylstm-method]]（adam-lbfgs, two-phase-optimization）。

## 6. 结果证据

在 Helmholtz、Klein-Gordon、Navier-Stokes、Rayleigh-Taylor 等多个 PDE 上验证：自适应伪时间步进一致优于固定步长和 baseline PINN，且不需要逐问题调参。

→ [[wang2023-pinn-spurious-results]] 完整数据

## 7. 贡献

1. 从理论上指出 PDE 残差 loss 的缺陷——会接受伪解
2. 阐明伪时间步进的真正机制（避开伪解，非优化辅助）
3. 提出自适应伪时间步长（Jacobian 有限差分估计），零调参
4. 开源 JAX 实现 jaxpi2

→ [[wang2023-pinn-spurious-critical#7-贡献]]

## 8. 核心知识点

1. PDE 残差 loss 小 ≠ 解正确——这是 loss 的固有缺陷
2. 伪时间步进 = 凸化 loss landscape + 避开伪解（不是优化加速）
3. 步长是关键：太小慢，太大可能跳到伪解，自适应选最优
4. Collocation 重采样 + 伪时间 = 双重保护

## 9. Negative Knowledge

- 伪时间步进对步长敏感，固定步长不可靠
- 自适应步长依赖 Jacobian 的有限差分估计（引入数值误差，同 PhyLSTM 的有限差分问题：[[zhang2020-phylstm-critical#9-negative-knowledge]]，finite-difference-error）
- 目前验证限于稳态 PDE，动态系统的扩展未充分探索

→ [[wang2023-pinn-spurious-critical#9-negative-knowledge]]

## 10. 可迁移知识

| 知识 | 迁移方向 |
|------|----------|
| 伪时间步进 + collocation 重采样 | 任何物理约束训练的稳定性问题 |
| 自适应步长 (Jacobian 有限差分) | 其他需要步长调参的物理约束方法 |
| PDE 残差 loss 缺陷分析 | 设计新的物理 loss 时的警示 |

## 11. 研究机会

动态系统扩展、高阶自适应步长（不依赖有限差分）、与其他物理约束训练方法（如 PhyLSTM 的 soft-constraint）结合、多保真度伪时间

→ [[wang2023-pinn-spurious-critical#11-研究机会]]

---

## 12. 可复现性 (Reproducibility)

**🟢 高复现性** — 代码开源，标准数学 PDE 无需外部数据集

| 项目 | 说明 |
|------|------|
| **等级** | 🟢 高 |
| **官方代码** | `https://github.com/sifanexisted/jaxpi2`（JAX） |
| **数据集** | 标准数学 PDE（Helmholtz / Klein-Gordon / Navier-Stokes / Rayleigh-Taylor），无外部数据集依赖 |
| **协议** | 开源 |

**复现要点**：JAX 实现，验证覆盖多个经典 PDE benchmark。自适应步长依赖 Jacobian 有限差分估计，无需逐问题调参。伪时间步进对步长敏感，固定步长不可靠。

## 关联页面

- [[wang2023-pinn-spurious-method]] — 方法展开
- [[wang2023-pinn-spurious-results]] — 结果展开
- [[wang2023-pinn-spurious-critical]] — 贡献/知识/Negative/可迁移/机会
- [[zhang2020-phylstm-analysis]] — PhyLSTM：同属物理约束训练
- [[zhang2020-phylstm-method]] — 共享 collocation-strategy, adam-lbfgs
- [[zhang2020-phylstm-critical]] — 共享 finite-difference-error, 物理约束局限
- [[physics-constrained-training-failure-modes]] — 两篇论文的失败模式对比
