---
id: entities--causal-attention
title: Causal Attention (CA) Weighting — 自适应因果性时空加权
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- entity/model
- method/pinn
keywords:
- adaptive-weighting
- domain/ai4s
- entity/model
- method/pinn
- physics-informed
- pinn
- temporal-causality
sources:
- raw/papers/10_1016_j_jcp_2026_115071_extracted.txt
created: '2026-06-28'
updated: '2026-07-31'
confidence: high
---

# Causal Attention (CA) Weighting

## 定义

Causal Attention (CA) 是 Zhao, Xie & Chen (2026) 提出的一种 PINN 训练自适应逐点加权方法，通过**仅监测初始条件拟合的相对 L² 误差**来构造时间方向指数衰减的权重，强制网络按照时间因果性学习时变 PDE。

权重公式：
$$\lambda(t, x) = e^{-\epsilon \\xi t}, \\quad \\xi = \\frac{\\sum_i (u_0(x_i) - u_\\theta(0, x_i))^2}{\\sum_i u_0^2(x_i)}$$

其中 ϵ = 1000（固定，无需退火），ξ 为初始条件相对 L² 误差。

## 与 Causal Training [Wang 2024] 的关键区别

| | Causal Training [Wang 2024] | Causal Attention [Zhao 2026] |
|---|---|---|
| **驱动信号** | 前一时刻的累积 PDE 残差 Σ L_{r,i} | 初始条件拟合误差 ξ |
| **配点要求** | 必须在耦合时空网格上 | **完全自由**（与采样分布解耦） |
| **超参** | ϵ 需要退火 | ϵ = 1000 固定 |
| **高维扩展** | 耦合网格遭维度灾难 | 可结合任意重采样 |
| **理论基础** | 经验性 | Turinici [2023] 的数学最优性证明 |

关键创新：用**极小信息代价**（仅初始点 MSE vs 全时空残差累积）驱动因果强制。[[causal-training]] 是"残差驱动"，CA 是"误差驱动"——信息维度大幅降低。

## 核心性质

1. **无梯度**：不涉及 PDE 残差或导数的额外计算
2. **有界**：0 ≤ λ ≤ 1，不引入梯度爆炸风险
3. **单调**：沿时间方向递减——优先早期，逐步释放后期
4. **采样独立**：权重计算不依赖残差点的空间排布
5. **渐进退化**：ξ → 0 时 λ → 1，CA 自动退化为标准 PINN

## 辅助策略

- **重采样集成**：终端权重 λ_min 作为收敛信号，触发均匀重采样（δ 递增，最多 9 轮）
- **时间推进**：长时间/混沌问题分段时间推进，CA 权重做位移修正 λ(t) = exp(-ϵ ξ (t - iΔt))
- **变迭代次数**：前段多迭代 → 减少误差累积；后段少迭代 → 省算力
- **5% 时间域外延**：缓解终端时间缺右侧导数 → 最大误差减半

## 适用与不适用

### ✅ 适用

- 初值敏感的时间依赖 PDE（Allen-Cahn、KdV、Kuramoto-Sivashinsky）
- 有周期性边界条件的问题（配合 Fourier 特征嵌入）
- 高维（2D/3D）时间依赖方程（CA + 重采样不陷入维度灾难）

### ❌ 不适用 / 次优

- 激波/非光滑解（Burgers）→ 初值不敏感，应使用空间自适应加权
- IC-BC 不兼容问题 → 强行拟合 IC 与边界约束冲突
- 高 Re/Ma Navier-Stokes → ϵ=1000 可能太小

## 相关论文

- [[zhao2026-causal-attention-analysis]] ← CA 原论文
- [[wang2024-causal-pinn-analysis]] ← Causal Training 前驱 [Wang 2024]
- Turinici (2023) — 数学证明指数衰减权重对初值敏感问题的最优性

## 代码

https://github.com/Chenrui-Z/Causal-Attention/

## Evidence By Source

### `raw/papers/10_1016_j_jcp_2026_115071_extracted.txt`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/10_1016_j_jcp_2026_115071_extracted.txt]
