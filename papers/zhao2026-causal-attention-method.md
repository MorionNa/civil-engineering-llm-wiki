---
id: papers--zhao2026-causal-attention-method
title: Casual Attention 方法展开：CA 权重 + mMLP + Fourier 特征 + 重采样
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/paper
- method/pinn
keywords:
- adaptive-weighting
- causal-attention-weighting
- fourier-feature-embedding
- modified-mlp
- resampling
- temporal-causality
- time-marching
sources:
- sources/papers/zhao2026-causal-attention.md
created: '2026-06-28'
updated: '2026-07-31'
confidence: high
---

# CA 方法展开：核心 CA 权重 + 辅助增强技术

## 1. Causal Attention 权重定义

### 1.1 动机：初始条件误差是全球误差的经验下界

本文核心观察：在时间依赖 PDE 中，训练过程中**全局相对 L² 误差与初始条件相对误差呈正相关**。这是因为初始条件仅构成数据拟合，编码了真实解在 t=0 的信息——如果初始条件都没学准，全局解不可能更准。因此 ξ（初始条件相对 L² 误差）可作为全局误差的经验下界。

### 1.2 权重公式

```
ξ = Σ_i (u_0(xⁱ_c) - u_θ(0, xⁱ_c))² / Σ_i u_0²(xⁱ_c)   # 初始条件相对 L² 误差
λ(t, x) = exp(-ϵ ξ t)                                    # CA 权重
```

残差损失重构为：
```
L_r(θ) = (1/N_r) Σ_i λ(tⁱ, xⁱ) (∂_t u_θ(tⁱ, xⁱ) + N[u_θ](tⁱ, xⁱ))²
```

### 1.3 与其他因果权重的关键区别

| 方法 | 权重公式 | 与配点关系 | 超参 |
|------|----------|-----------|------|
| Causal PINN [17] | λ(t_k) = exp(-ϵ Σ L_{r,i}) | **强耦合**（需耦合时空网格） | ϵ 退火 |
| Turinici [23] | 数学证明最优指数衰减形式 | 理论框架 | — |
| **CA (本文)** | λ(t,x) = exp(-ϵ ξ t) | **完全解耦**（只依赖初始点） | ϵ=1000 固定 |

### 1.4 权重行为

- **ξ 大**（初始条件未学好）→ λ 快速衰减 → 远期残差贡献近零 → 网络被迫优先优化早期时间
- **ξ 减小**（初始条件逐渐学准）→ λ 缓慢上升到 1 → 远期残差逐步纳入优化
- **ξ→1e-3**：终端权重开始上升
- **ξ→1e-5**：所有权重趋近 1，CA 退化为标准 PINN

ϵ=1000 下，这一动态在实际实验中表现稳定且无需调整。

## 2. 重采样集成策略 (Algorithm 1)

CA 权重的最大优势：**计算与配点时空排布完全解耦**，可以随时任意重采样。

### 2.1 终端权重驱动的重采样

- 终端权重 λ_min 指示全局收敛程度
- 初始化 δ = 0.1
- 每 K=5000 iterations 检查 λ_min > δ → 触发重采样（从均匀分布重采残差点）→ δ += 0.1
- 重采样在第 9 轮（45,000 iterations）后结束
- 重采样点数与初始点数一致（内存不受影响）

### 2.2 核心优势

- **早期：** 频繁重采样 → 防止优化陷入局部极小 → 等价于利用 10 倍残差信息
- **晚期：** 停止重采样 → 避免干扰高精度收敛
- **高维：** 网格采样遭维度灾难 → 重采样从均匀分布随机采点 → 关键优势

## 3. 辅助增强技术

### 3.1 Modified MLP (mMLP)

标准 MLP 基础上引入两个额外编码器 U 和 V：

```
U = tanh(W_U x + b_U)
V = tanh(W_V x + b_V)
H₁ = tanh(W₁ x + b₁)
Z₁ = H₁
Z_l = tanh(W_l H_{l-1} + b_l),  2 ≤ l ≤ L-1
H_l = (1 - Z_{l-1}) ⊙ U + Z_{l-1} ⊙ V,  2 ≤ l ≤ L
f_θ(x) = W_{L+1} H_L + b_{L+1}
```

U 和 V 在层间前向传播中注入额外非线性，通常优于等宽 MLP。

### 3.2 Fourier 特征嵌入

对周期边界问题，将输入 (t, x) 映射为：

```
1D: v(t,x) = [1, t, cos(ωx), sin(ωx), …, cos(m ωx), sin(m ωx)]
2D: v(t,x,y) = [t, cos(iω_xx)cos(jω_yy), cos(iω_xx)sin(jω_yy), sin(iω_xx)cos(jω_yy), sin(iω_xx)sin(jω_yy)]  (i,j=0,…,m)
3D: 同理 8 项组合 (i,j,k=0,…,m)
```

- **硬约束**：自动满足周期性边界条件（无需采样边界点、无需边界损失）
- **反谱偏差**：引入高频分量缓解标准网络的谱偏差
- **双刃剑**：过多 Fourier 特征 (m=10) 引入训练不稳定——高次导数产生大梯度，扰乱优化

### 3.3 时间推进 + 变迭代次数 (Algorithm 2)

针对长时间 PDE 或混沌方程：

1. 将 [0,T] 分为 N_s 段，每段单独训练一个网络
2. 前一段 t=Δt 的输出作为后一段的初始条件
3. CA 权重做位移修正：λ(t,x) = exp(-ϵ ξ (t - iΔt)), i=0,…,N_s-1
4. **变迭代次数**：前段多迭代 → 提高精度 → 减少误差累积；后段少迭代 → 省算力

## 4. 关键实现细节

### 4.1 初始损失权重 w_ic

高阶空间导数方程（KdV 的 u_xxx, KS 的 u_xxxx）需要更大的 w_ic 来平衡梯度贡献：
- 1D Allen-Cahn: w_ic = 100
- 1D KdV (u_xxx): w_ic = 500
- 1D KS (u_xxxx): w_ic = 1000

### 4.2 学习率策略

- CA 权重 ≤ 1 不会放大梯度 → 可安全使用更高的初始学习率
- 所有实验使用 lr=0.002 + 指数衰减（decay rate 0.93, step 2500-3000）
- 仅在纯 mMLP 对照实验中使用 lr=0.001

### 4.3 5% 时间域外延

KdV 终止时间误差集中的根因：t=T 处仅有左导数，缺右导数信息。
解决：将时间采样域从 [0,1] 延至 [0,1.05]，误差最大降为原来一半。

### 4.4 三维 Fourier 特征限制

Nyquist 采样定理约束：m=2 需 199,494+ 点才能解析最高频率；76,800 点只够 m=1。故 3D 实验中设 m=1。

## Evidence By Source

### `sources/papers/zhao2026-causal-attention.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/10_1016_j_jcp_2026_115071_extracted.txt`

^[sources/papers/zhao2026-causal-attention.md]

## Related Indexes

- [[papers/index]]
- [[index]]
