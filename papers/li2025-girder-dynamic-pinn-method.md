---
title: "Li et al. (2025) — 方法机制：双代理模型PINN斜拉桥动态线形重建"
created: 2026-06-27
updated: 2026-06-27
type: paper-analysis
tags: [physics-informed, pinn, structural-dynamics, cable-stayed-bridge, neural-network, deep-learning, collocation-strategy, fourier-embedding, causal-weight, two-surrogate-model]
sources: [raw/papers/10_1016_j_aei_2025_103581_extracted.txt]
methods: [physics-informed, pinn, fourier-embedding, causal-weight, two-surrogate-model, cable-simplification, elastic-support, dimensionless-pde, spatial-causal-weight]
confidence: high
---

# Li et al. (2025) — 方法机制展开

> 返回概述 → [[li2025-girder-dynamic-pinn-analysis]]

---

## 方法总览

本文提出了一种基于 PINN 的斜拉桥主梁动态线形（MGDA）间接重建方法，包含四个核心组件：**斜拉桥简化模型 → 双代理网络架构 → 傅里叶嵌入 + 时空因果权重 → 差异化损失函数**。

```
输入: (x, t) — 空间坐标与时间坐标
  │
  ▼
傅里叶嵌入层: [x, t, cos(ω₁x), sin(ω₁x), ..., cos(ωₖt), sin(ωₖt)]
  │
  ▼
┌──────────────┐     ┌──────────────┐
│  Netᵤ (MGDA)  │     │ Net_f (激励)  │
│ 输入 → MLP    │     │ 输入 → MLP    │
│ 输出: u(x,t)  │     │ 输出: f(x,t)  │
└──────┬───────┘     └──────┬───────┘
       │                    │
       ▼                    ▼
  自动微分: ∂u/∂t, ∂²u/∂t², ∂⁴u/∂x⁴
       │                    │
       ▼                    ▼
  PDE残差 = Netᵤ导数 + 弹性支撑项 + 阻尼项 - Net_f
       │
       ▼
  总损失 = w₁·L_PDE + w₂·L_BC + w₃·L_IC + w₄·L_data
       │
       ▼
  Adam → L-BFGS 两阶段优化
```

与 [[li2025-movingload-pinn-analysis]] 的单网络模式不同，本文是**双网络并行**架构。

---

## 1. 斜拉桥简化模型

### 1.1 从离散索到连续弹性支撑

斜拉桥由主梁 + 多个沿跨径分布的离散斜拉索组成。本文的核心简化：

$$
\text{离散索系 } \rightarrow \text{ 连续弹性支撑 } k(x)
$$

- 每根索对主梁提供竖向支撑刚度 $k_i$，沿跨径方向将所有索的刚度连续化
- 支撑刚度函数 $k(x)$ 可通过索的几何参数（索长、倾角、截面积、弹性模量）导出
- 同时考虑索的水平分力对主梁产生的轴向压力 $N$

### 1.2 简化后的控制方程

原始动力学方程为 Euler-Bernoulli 梁 + 弹性地基 + 轴向力：

$$\rho A \frac{\partial^2 u}{\partial t^2} + c\frac{\partial u}{\partial t} + EI\frac{\partial^4 u}{\partial x^4} + N\frac{\partial^2 u}{\partial x^2} + k(x)u = f(x,t)$$

其中：
- $\rho A$：线密度，$c$：阻尼系数，$EI$：抗弯刚度
- $N$：索水平分力产生的轴向压力
- $k(x)$：等效连续弹性支撑刚度
- $f(x,t)$：待推断的外部激励（随机荷载或车辆荷载）

### 1.3 无量纲化

引入无量纲变量 $\bar{x}=x/L$, $\bar{u}=u/L$, $\bar{t}=t\cdot\omega_1$，得到：

$$\frac{\partial^2 \bar{u}}{\partial \bar{t}^2} + 2\xi\frac{\partial \bar{u}}{\partial \bar{t}} + \frac{\partial^4 \bar{u}}{\partial \bar{x}^4} + \bar{N}\frac{\partial^2 \bar{u}}{\partial \bar{x}^2} + \bar{k}(\bar{x})\bar{u} = \bar{f}(\bar{x},\bar{t})$$

> **设计动机：** 无量纲化消除物理量纲差异，弹性地基项 $\bar{k}(\bar{x})\bar{u}$ 是无量纲化后的关键附加项——区别于标准梁方程。

---

## 2. 双代理模型架构

### 2.1 为什么需要两个网络？

在 MGDA 重建中，外部激励 $f(x,t)$ 通常是未知的——PINN 需要同时解决两个未知量：
- $u(x,t)$：主梁动态线形（位移场）
- $f(x,t)$：外部激励（荷载场）

**单网络方案（如 [[li2025-movingload-pinn-analysis]] 的反问题模式）** 假设激励的数学形式已知（如 $P\delta(x-vt)$），仅推断参数（$P$, $v$, $E$）。本文场景中，随机荷载和车辆荷载**无固定数学形式**，需要将激励视为一个时变空间场来推断——因此需要独立的网络来代理。

### 2.2 网络结构

| 组件 | Netᵤ（MGDA 网络） | Net_f（激励网络） |
|------|-------------------|---------------------|
| 输入 | $(x,t)$ | $(x,t)$ |
| 嵌入 | 傅里叶嵌入层 | 傅里叶嵌入层 |
| 隐藏层 | 8 × 50 神经元，tanh 激活 | 6 × 40 神经元，tanh 激活 |
| 输出 | $u(x,t)$（标量） | $f(x,t)$（标量） |
| 导数需求 | $\partial u/\partial t$, $\partial^2 u/\partial t^2$, $\partial^4 u/\partial x^4$, $\partial^2 u/\partial x^2$ | 无（激励直接代入 PDE） |

### 2.3 网络耦合机制

两个网络通过 PDE 残差耦合：

$$\mathcal{L}_{PDE} = \frac{1}{N_r}\sum \left|\mathcal{N}[u_\theta](x_i,t_i) - f_\phi(x_i,t_i)\right|^2$$

其中 $\mathcal{N}[u_\theta]$ 是包含 $\partial^2 u/\partial t^2$, $\partial u/\partial t$, $\partial^4 u/\partial x^4$, $\partial^2 u/\partial x^2$, $k(x)u$ 的微分算子，$f_\phi$ 是激励网络的输出。

> **关键洞察：** PDE 充当两个网络的"通信协议"——MGDA 网络提供位移导数，激励网络提供荷载值，PDE 残差约束两者的物理一致性。

---

## 3. 傅里叶嵌入层

与 [[li2025-movingload-pinn-method]] 共享技术：

$$\gamma(x,t) = [x, t, \cos(\omega_1 x), \sin(\omega_1 x), \dots, \cos(\omega_k x), \sin(\omega_k x), \cos(\omega_1 t), \sin(\omega_1 t), \dots, \cos(\omega_k t), \sin(\omega_k t)]$$

- $\omega_j = 2\pi j$（j=1,...,k），本文 k=8
- 两个网络共享相同的傅里叶嵌入层结构（但权重独立）
- **本文的附加价值：** 弹性地基项 $k(x)u$ 引入空间变化的刚度分布——傅里叶嵌入帮助网络学习空间非均匀的振型

---

## 4. 时空因果权重

### 4.1 时间因果权重

与 [[li2025-movingload-pinn-method]] 一致：

$$w_t(t) = \exp\left(-\epsilon_t \sum_{k=1}^{n_t} \mathcal{L}_{PDE}(t_k)\right)$$

### 4.2 空间因果权重（本文新增）

$$\mathcal{L}_{PDE}^{causal} = \frac{1}{N_r}\sum_{i=1}^{N_r} w_t(t_i) \cdot w_s(x_i) \cdot \left|\mathcal{N}[u_\theta](x_i,t_i) - f_\phi(x_i,t_i)\right|^2$$

空间权重函数 $w_s(x)$ 的设计逻辑：
- 荷载作用位置附近的损失权重最高（激励→响应的因果源头）
- 远离荷载位置，权重逐渐降低
- 在随机荷载场景中，$w_s(x)$ 根据传感器观测到的响应分布自适应调整

> **原理：** 桥梁挠度响应从加载点向两端传播——空间因果权重反映了"近激励源先响应、远端后响应"的波动传播物理。

---

## 5. 差异化损失函数

### 5.1 Netᵤ（MGDA 网络）损失

$$\mathcal{L}_u = \lambda_{PDE}\mathcal{L}_{PDE}^{causal} + \lambda_{BC}\mathcal{L}_{BC} + \lambda_{IC}\mathcal{L}_{IC} + \lambda_{data}\mathcal{L}_{data}$$

- $\mathcal{L}_{BC}$：边界条件（简支/固支/弹性支撑）
- $\mathcal{L}_{IC}$：初始条件（$u(x,0)=0$, $\dot{u}(x,0)=0$）
- $\mathcal{L}_{data}$：少量传感器数据拟合项

$$\mathcal{L}_{data} = \frac{1}{N_d}\sum_{i=1}^{N_d} \left|u_\theta(x_i^{obs}, t_i^{obs}) - u_i^{obs}\right|^2$$

### 5.2 Net_f（激励网络）损失

$$\mathcal{L}_f = \lambda_{PDE}\mathcal{L}_{PDE}^{causal}$$

激励网络**不需要**边界条件、初始条件和数据拟合项——它仅通过 PDE 残差接受监督。这是本文的一个设计选择：激励被建模为"自由场"，仅受物理一致性约束。

> ⚠️ **潜在风险：** Net_f 缺乏独立的数据约束，在训练早期可能输出非物理解。论文通过两阶段优化（Adam 全局探索 → L-BFGS 精调）缓解这一问题。

---

## 6. 训练策略

| 阶段 | 优化器 | 迭代数 | 学习率 | 备注 |
|------|--------|--------|--------|------|
| 第一阶段 | Adam | ~10,000 | 1e-3 | 两个网络联合训练 |
| 第二阶段 | L-BFGS | ~5,000 | — | 切换至二阶精调 |

- 配点总数：空间 × 时间网格，~10,000 collocation points
- 传感器数据：3~7 个测点（位移传感器），每测点 ~200 时步
- 训练时间：双网络略慢于单网络，单工况约 20-40 分钟（GPU）
- 损失权重：$\lambda_{PDE}=1.0$, $\lambda_{BC}=10$, $\lambda_{IC}=10$, $\lambda_{data}=100$（数据项权重大，因其稀疏但精确）

---

## 关键创新总结

| 组件 | 解决的问题 | 与 [[li2025-movingload-pinn]] 的关系 |
|------|-----------|-----------------------------------|
| 斜拉桥简化模型 | 索-梁耦合难以直接建模 | 本文特有：弹性地基梁 + 轴向力 |
| 双代理模型 | 激励场未知，需联合推断 | 本文特有：场-场联合反演 vs 参数反演 |
| 傅里叶嵌入 | 高频振动表达 | 共享，本文用于空间非均匀振型 |
| 时空因果权重 | 时间因果 + 空间传播因果 | 扩展：时间因果共享 + 空间因果新增 |
| 差异化损失 | 激励网络无数据约束 | 本文特有设计 |

## 关联页面

- [[li2025-girder-dynamic-pinn-analysis]] — 返回概述
- [[li2025-girder-dynamic-pinn-results]] — 实验结果
- [[li2025-girder-dynamic-pinn-critical]] — 贡献 / Negative / 可迁移
- [[pinn]] — 物理信息神经网络实体
- [[cable-stayed-bridge]] — 斜拉桥实体
- [[li2025-movingload-pinn-method]] — 单网络 PINN 方法（互补参照）
- [[notes/lectures/ai4s-pinn-deepxde]] — DeepXDE 实战参考
