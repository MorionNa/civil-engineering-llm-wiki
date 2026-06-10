---
title: "Müller et al. (2023) — 结果证据展开"
created: 2026-06-10
updated: 2026-06-10
type: concept
tags: [pinns, pseudo-time-stepping, spurious-solutions, benchmark, helmholtz, klein-gordon, navier-stokes, rayleigh-taylor, pde]
sources: [raw/papers/muller2023-pinn-spurious.md]
results: [spurious-solution-avoidance, adaptive-step-size, zero-tuning]
datasets: [pde-benchmarks, helmholtz, klein-gordon, navier-stokes, rayleigh-taylor]
confidence: high
---

# Müller et al. (2023) — 结果证据展开

> 返回概述 → [[muller2023-pinn-spurious-analysis]]

## 验证的 PDE 基准

| 方程 | 类型 | 难度 |
|------|------|------|
| Helmholtz | 椭圆型 | 高频震荡，易出伪解 |
| Klein-Gordon | 双曲型 | 非线性波动 |
| Navier-Stokes (Lid-driven cavity) | 抛物-椭圆耦合 | 经典流体 benchmark |
| Rayleigh-Taylor instability | 时变多相流 | 界面不稳定性 |
| Allen-Cahn | 相场 | 陡峭界面 |
| Poisson (2D/3D) | 椭圆型 | 基础验证 |

## 核心结果

### 1. 伪时间步进 vs Baseline PINN

**所有 benchmark 上伪时间步进一致优于 baseline PINN。**

关键发现：baseline PINN 即使 L2 误差收敛到平台期，PDE 残差仍在下降——**loss 不是误差的可靠代理**。

### 2. 自适应 vs 固定步长

| 方法 | Helmholtz | Navier-Stokes | Rayleigh-Taylor |
|------|-----------|---------------|-----------------|
| Baseline PINN | 失败 | 较差 | 失败 |
| 固定步长 (τ=0.1) | 可行但慢 | 好 | 一般 |
| 固定步长 (τ=10) | **失败** | 好 | 一般 |
| **自适应步长** | **最优** | **最优** | **最优** |

> 固定步长在某个 benchmark 上最优，在另一个上可能失败——印证了"无法从 loss 曲线选步长"的论点。

### 3. Rayleigh-Taylor 不稳定性

| 指标 | Baseline | 自适应伪时间 |
|------|----------|-------------|
| 温度场预测质量 | 模糊 | 清晰还原 |
| Rel. L2 error (T) | 大 | **显著降低** |
| 步长调参 | — | 零 |

伪时间步长在训练中自动从 ~0.1 增大到 ~3，说明网络初期需要小步长（避开伪解），后期可以用大步长（加速收敛）。

---

## 与 PhyLSTM 的结果对比

| | PhyLSTM | PINN 自适应伪时间 |
|--|---------|-------------------|
| 问题域 | 结构动力学 ODE | 通用 PDE |
| 关键指标 | 相关系数 γ | Rel. L2 error |
| 调参需求 | 手动调 α/β/γ | **零调参** |
| 跨域泛化 | BLWN→地震 ✓ | 跨 PDE 类型 ✓ |
| 推理速度 | >10³x FEM | — |

> PhyLSTM 的 physics-constraint-weight-tuning 是待解决问题，而 PINN 的自适应步长提供了解决方向。

## 关联

- [[muller2023-pinn-spurious-analysis]] — 概述
- [[muller2023-pinn-spurious-method]] — 方法展开
- [[zhang2020-phylstm-results]] — PhyLSTM 结果对比
- [[physics-constrained-training-failure-modes]] — 失败模式对比
