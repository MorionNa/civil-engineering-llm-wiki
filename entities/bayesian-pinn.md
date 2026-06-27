---
title: "Bayesian Physics Informed Neural Network (BPINN)"
created: 2026-06-27
updated: 2026-06-27
type: entity
tags: [physics-informed, pinn, bayesian-inference, uncertainty-quantification, hamiltonian-monte-carlo, neural-network, ai4s]
sources: [raw/papers/10_1016_j_cma_2022_115346_extracted.txt]
---

# Bayesian Physics Informed Neural Network (BPINN)

## 概述

BPINN 将物理信息神经网络（PINN）与贝叶斯推理融合，使网络不仅能利用物理定律约束训练，还能对权重、物理参数和预测输出提供完整的后验分布与可信区间（credible intervals）。

**首次提出：** Linka et al. (2022), CMAME 402, 115346

**核心思想：** 将物理残差从 PINN 的 loss 正则项提升为贝叶斯似然的一个独立因子：

$$P(Θ|\text{data}, \text{physics}) ∝ P(\text{data}|Θ) · P(\text{physics}|Θ) · P(Θ)$$

其中 Θ = {网络权重 θ, 物理参数 ϑ}。

## 与相关方法的区别

| 方法 | 物理约束 | 不确定量化 | 参数类型 |
|------|:---:|:---:|------|
| NN | — | — | 网络权重点估计 |
| PINN | loss 正则项 | — | 网络权重+物理参数点估计 |
| BNN | — | 权重后验 | 网络权重分布 |
| **BPINN** | **似然因子** | **权重+参数+预测后验** | **联合分布** |

**关键区别：** BPINN 中的物理残差 $r = \ddot{x} + c\dot{x} + k(x - x_0)$ 被建模为高斯似然 $P(r|Θ) = \mathcal{N}(0, σ²)$，而非仅作为 loss 的加权项。这使得物理信息在贝叶斯框架中获得正式的"证据"地位。

## 推理方法

- **采样器：** Hamiltonian Monte Carlo (HMC) / No-U-Turn Sampler (NUTS)
- **实现栈：** PyMC3 + ArviZ (Python)
- **计算复杂度：** 高 — 每次 HMC 步需通过整个网络计算梯度
- **适用条件：** 中等以上数据量（≥100 点）、充足算力、需要完整 UQ

## BPINN 的能力边界

```
✅ 适用
├── 需要网络表达能力 + 物理一致性 + 不确定量化
├── 数据量 ≥100 点
├── 物理模型为光滑可微 ODE/PDE
└── 离线分析场景（训练时间可接受）

⚠️ 谨慎使用
├── 小数据量（<30 点）→ 用 BI 或 SAPINN
├── 高维网络（>1000 权重）→ HMC 混合困难
└── 实时推理 → HMC 太慢

❌ 不适用
├── 物理模型未知或错误指定
├── 非光滑动力学（间断/突变）
└── 极端算力受限环境
```

## 已知局限性

1. **计算成本最高：** 6 种模型中 BPINN 是最慢的（HMC 采样数 × 网络前向传播）
2. **参数可辨识性：** 网络权重和物理参数存在混淆 → 物理参数后验比纯 BI 更宽
3. **需要大训练集：** 小数据下后验不可靠
4. **物理残差的高斯假设：** 实际残差可能非高斯/异方差

## 与其他方法的关联

- [[pinn]] — PINN (Physics Informed Neural Networks): BPINN 的前身
- [[hamiltonian-monte-carlo]] — HMC: BPINN 的核心采样器
- [[pseudo-time-stepping]] — 伪时间步进：BPINN 潜在训练稳定性改进方向
- [[self-adaptive-pinn]] — SAPINN: 自适应 ε，可替代 BPINN 中固定物理权重的方案

## 关联论文

- [[linka2022-bayesian-pinn-analysis]] — 原始论文分析
- [[linka2022-bayesian-pinn-method]] — 方法展开
- [[linka2022-bayesian-pinn-results]] — 结果展开
- [[linka2022-bayesian-pinn-critical]] — 批判分析
- [[wang2023-pinn-spurious-analysis]] — PINN 伪解问题（互补失败模式）
- [[zhang2020-phylstm-analysis]] — PhyLSTM（同类物理约束方法）
