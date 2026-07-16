---
title: "Seismic Site Response PINN — 地震场地反应物理信息神经求解器"
created: 2026-07-16
updated: 2026-07-16
type: entity
tags: [neural-network, physics-informed, deep-learning, soft-constraint, structural-dynamics, seismic-response, equation-of-motion, ground-motion, physics-constraint-weight-tuning, neural-tangent-kernel, pinn, ai4s, physics-simulation]
sources: [raw/papers/10_1016_j_compgeo_2025_107137.xml, raw/papers/extracted/10_1016_j_compgeo_2025_107137_extracted.txt]
methods: [lumped-mass-formulation, fourier-feature-embedding, nondimensionalization, hyperparameter-search, automatic-differentiation]
results: [linear-site-response, rk45-agreement, newmark-beta-agreement, multi-layer-response]
failure_modes: [finite-collocation-nonuniqueness, per-scenario-retraining, no-speed-benchmark, linear-soil-only, sigma-sensitivity]
datasets: [NGA-West2-ground-motion-records, synthetic-layered-soil-profiles]
reproducibility: low
code_url: []
dataset_url: []
confidence: high
---

# Seismic Site Response PINN

## 定义

**Seismic Site Response PINN** 是 Liu、Macedo 与 Rodríguez（2025）提出并评估的线性一维场地反应神经求解流程。它把土柱先离散成集中质量系统，再用时间连续 [[pinn]] 近似节点位移；Fourier 特征处理地震响应宽频谱，无量纲化与超参数搜索提高训练稳定性。

## 已验证物理范围

| 维度 | 已验证 | 未验证 |
|------|--------|--------|
| 土体 | 线性弹性 Kelvin–Voigt，常数刚度/黏性阻尼 | 模量退化、阻尼演化、循环滞回、塑性 |
| 空间模型 | 1/3/10 层集中质量系统 | 连续二维/三维场地、复杂地形 |
| 输入 | PGA 0.003–1.8 g；$D_{5-95}$ 2–148 s | 输入不确定性与真实传感器噪声 |
| 基线 | RK45 与 Newmark-beta | 实验/现场观测 |
| 扩展 | 等效线性仅作串行线性分析建议 | 全非线性为未来工作 |

高 PGA 只表示线性模型受到大幅值输入，不代表土体本构非线性已被建模。

## 核心管线

```text
soil layers + ground motion
        │
        ├─► lumped M,C,K ─► nondimensional ODE
        │
timestamps ─► Fourier(m,σ) ─► MLP + BatchNorm + tanh ─► u(t)
                                                        │
                                         AD ─► u̇(t), ü(t)
                                                        │
                                      IC + motion residual loss
```

训练使用 70/30 划分和 TPE 搜索，最终以全时间点重训。$m$ 建议搜索 50–200，$\sigma$ 搜索 0.1–2，且后者更敏感。详见 [[liu2025-site-response-pinn-method]]。

## 方法定位

- 它是**每实例神经时间积分器**：新土层或新地震动必须重训。
- 它不是跨场地通用代理模型，也没有证明速度快于 RK45/NB。
- 它在时间上给出连续可微表示，但空间仍采用集中质量离散。
- 它借助 [[neural-tangent-kernel]] 的谱偏置认识选择 Fourier 特征；本文主实验没有实施 NTK 自适应权重。

## 验证准则

1. 在训练点之外计算运动方程残差，避免有限配点伪解。
2. 同时比较位移、速度、加速度和 Fourier 幅值谱。
3. 与显式 RK45 和隐式 NB 双基线核验。
4. 明确区分“逐场景训练稳健”与“跨场景泛化”。
5. 对非线性扩展必须增加本构状态/应力—应变约束，而不是只换输入 PGA。

## 已知限制

- 有限样本零损失不能保证连续域唯一正确解。
- $\sigma$ 选择错误会造成过度平滑或高频振荡。
- 每实例 TPE + 重训可能比成熟积分器更昂贵；论文未做速度基准。
- 未见公开代码；Data availability 声明 “No data was used”，精确复现实验输入仍需补充。

## 关联页面

- [[liu2025-site-response-pinn-analysis]] — 12 维度论文总览
- [[liu2025-site-response-pinn-results]] — 定量精度与覆盖范围
- [[liu2025-site-response-pinn-critical]] — 不可外推边界和研究路线
- [[pinn]] — PINN 基础方法
