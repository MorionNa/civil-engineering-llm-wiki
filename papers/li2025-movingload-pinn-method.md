---
id: papers--li2025-movingload-pinn-method
title: Li et al. (2025) — 方法机制：PINN 桥梁移动荷载动力响应分析
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
- method/pinn
- method/transformer
keywords:
- collocation-strategy
- deep-learning
- equation-of-motion
- neural-network
- physics-informed
- pinn
- structural-dynamics
sources:
- sources/papers/li2025-movingload-pinn.md
created: '2026-06-27'
updated: '2026-07-31'
confidence: high
methods:
- physics-informed
- pinn
- fourier-embedding
- causal-weight
- collocation-strategy
- gaussian-approximation
- nondimensional-pde
---

# Li et al. (2025) — 方法机制展开

> 返回概述 → [[li2025-movingload-pinn-analysis]]

---

## 方法总览

本文提出了一种基于 PINN 的桥梁移动荷载动力响应分析方法，包含四个核心组件：**无量纲化 PDE → 高斯近似采样 → 傅里叶嵌入 + 因果权重 → 双模式训练**。

```
输入: x (空间坐标), t (时间坐标)
  │
  ▼
傅里叶嵌入层: [x, t, cos(ω₁x), sin(ω₁x), ..., cos(ωₖt), sin(ωₖt)]
  │
  ▼
全连接深度神经网络 (多层 + 激活函数)
  │
  ▼
输出: u(x,t) — 桥梁挠度响应
  │
  ▼
自动微分: ∂u/∂t, ∂²u/∂t², ∂⁴u/∂x⁴ ...
  │
  ▼
PDE 残差 Loss + BC/IC Loss + (可选) 数据拟合 Loss
  │
  ▼
Adam → L-BFGS 两阶段优化
```

---

## 2.1 无量纲化偏微分方程

### 均匀桥梁

原始控制方程（Euler-Bernoulli 梁）：

$$\rho A \frac{\partial^2 u}{\partial t^2} + c\frac{\partial u}{\partial t} + EI\frac{\partial^4 u}{\partial x^4} = P\delta(x-vt)$$

通过引入无量纲变量 $\bar{x}=x/L$, $\bar{u}=u/L$, $\bar{t}=t\cdot\omega_1$（其中 $\omega_1$ 为基频），得到无量纲 PDE：

$$\frac{\partial^2 \bar{u}}{\partial \bar{t}^2} + 2\xi \frac{\partial \bar{u}}{\partial \bar{t}} + \frac{\partial^4 \bar{u}}{\partial \bar{x}^4} = \bar{P}\delta(\bar{x}-\bar{v}\bar{t})$$

其中 $\xi$ 为阻尼比，$\bar{P}$ 为无量纲荷载，$\bar{v}$ 为无量纲速度。

### 非均匀桥梁

截面特性沿跨径变化：$EI(x)$ 和 $\rho A(x)$ 随 $x$ 变化，导出变系数 PDE：

$$\rho A(x)\frac{\partial^2 u}{\partial t^2} + c\frac{\partial u}{\partial t} + \frac{\partial^2}{\partial x^2}\left[EI(x)\frac{\partial^2 u}{\partial x^2}\right] = P\delta(x-vt)$$

> **设计动机：** 无量纲化消除物理量纲差异，使各损失项的尺度统一，避免梯度消失/爆炸。

---

## 2.2 移动荷载近似与采样策略

### Dirac 函数的高斯近似

$$\delta(x-vt) \approx \frac{1}{\sqrt{2\pi}\sigma} \exp\left(-\frac{(x-vt)^2}{2\sigma^2}\right)$$

- 物理含义：将集中力"涂抹"为以荷载位置为中心、宽度为 $\sigma$ 的窄高斯分布
- $\sigma$ 的选择：$\sigma = L/200 \sim L/100$（梁长的 0.5%~1%），既能逼近集中力效果，又不使梯度过于尖锐

### 自适应采样策略

| 区域 | 采样密度 | 策略 |
|------|---------|------|
| 荷载附近 | 高密度 | 在 $x\in[vt-3\sigma, vt+3\sigma]$ 加密 |
| 边界附近 | 中密度 | 捕获边界约束的影响 |
| 其余区域 | 低密度 | 随机均匀采样 |

采样点在时域上也遵循类似策略，在荷载经过的时刻附近加密时间采样。

> **关键洞察：** 荷载位置是解梯度最大的区域——标准均匀采样会导致 PINN 在荷载附近欠拟合。

---

## 3. PINN 架构详解

### 3.1 标准 PINN 回顾

PINN 将 PDE 的残差作为损失函数的一部分：

$$\mathcal{L}_{PDE} = \frac{1}{N_r}\sum_{i=1}^{N_r} \left|\mathcal{N}[u_\theta](x_i, t_i) - f(x_i, t_i)\right|^2$$

其中 $\mathcal{N}[\cdot]$ 是 PDE 算子，$u_\theta$ 是神经网络近似解。边界条件和初始条件同样作为损失项：

$$\mathcal{L}_{total} = \mathcal{L}_{PDE} + \lambda_{BC}\mathcal{L}_{BC} + \lambda_{IC}\mathcal{L}_{IC}$$

### 3.2 本文提出的 PINN 增强

**傅里叶嵌入层（Fourier Embedding Layer）：**

受 Transformer 位置编码启发，在输入层拼接傅里叶基函数：

$$\gamma(x,t) = [x, t, \cos(\omega_1 x), \sin(\omega_1 x), \dots, \cos(\omega_k x), \sin(\omega_k x), \cos(\omega_1 t), \sin(\omega_1 t), \dots, \cos(\omega_k t), \sin(\omega_k t)]$$

- $\omega_j = 2\pi j$（j=1,...,k）
- k 的典型值：5~10
- **原理：** 傅里叶特征使 MLP 能更高效地学习高频函数，本质上是将输入映射到高维频域空间

**因果权重（Causal Weight）：**

在时间维度上对 PDE 残差损失加权：

$$\mathcal{L}_{PDE}^{causal} = \frac{1}{N_r}\sum_{i=1}^{N_r} w(t_i) \cdot \left|\mathcal{N}[u_\theta](x_i, t_i) - f(x_i, t_i)\right|^2$$

$$w(t) = \exp\left(-\epsilon \sum_{k=1}^{n_t} \mathcal{L}_{PDE}(t_k)\right)$$

其中 $\epsilon$ 是因果强度参数。随着时间推进，早期时刻的损失必须充分降低后，后期时刻的损失才会获得较大权重。

> **原理：** 桥梁振动是一个因果过程——t 时刻的响应依赖于 t' < t 时刻的状态。不加权的全局损失允许网络通过"作弊"（先拟合后期再用后期结果反推前期）来降低总损失，但实际上违反了物理因果性。

---

## 4. 损失函数总成

### PINN-DP（纯物理驱动）

$$\mathcal{L}_{DP} = w_{PDE}\mathcal{L}_{PDE}^{causal} + w_{BC}\mathcal{L}_{BC} + w_{IC}\mathcal{L}_{IC}$$

- $\mathcal{L}_{BC}$: 边界条件残差（简支/固支/弹性支撑）
- $\mathcal{L}_{IC}$: 初始条件残差（$u(x,0)=0$, $\dot{u}(x,0)=0$）

### PINN-DPD（物理-数据联合驱动）

$$\mathcal{L}_{DPD} = \mathcal{L}_{DP} + w_{data}\mathcal{L}_{data}$$

$$\mathcal{L}_{data} = \frac{1}{N_d}\sum_{i=1}^{N_d} \left|u_\theta(x_i^{obs}, t_i^{obs}) - u_i^{obs}\right|^2$$

未知参数 $\Theta$（如弹性模量 E、荷载 P、边界刚度 k）作为可训练变量，与网络权重同时优化。

---

## 5. 训练策略

| 阶段 | 优化器 | 迭代数 | 学习率 | 作用 |
|------|--------|--------|--------|------|
| 第一阶段 | Adam | ~10,000 | 1e-3 | 全局探索，快速收敛到合理区域 |
| 第二阶段 | L-BFGS | ~5,000 | — | 精调，利用二阶信息达到高精度 |

- 配点总数：~10,000（空间×时间网格，结合自适应采样）
- 网络结构：输入 → 傅里叶嵌入（2+4k 维）→ 8×50 隐藏层（tanh 激活）→ 输出（1 维）
- 训练时间：单个工况约 10-30 分钟（GPU）

---

## 关键设计思想总结

| 组件 | 解决的问题 | 原理 |
|------|-----------|------|
| 无量纲化 | 量纲差异导致的梯度不平衡 | 所有变量缩放到 O(1) |
| 高斯近似 | Dirac 奇异性的不可微性 | 光滑近似 + 可控带宽 |
| 自适应采样 | 集中荷载附近的欠拟合 | 在解梯度大的区域加密采样 |
| 傅里叶嵌入 | 高频振动分量学习困难 | 频域特征映射，提升 MLP 高频表达力 |
| 因果权重 | 违反物理因果性的伪解 | 时间逐次加权，先解前期再解后期 |

## 关联页面

- [[li2025-movingload-pinn-analysis]] — 返回概述
- [[li2025-movingload-pinn-results]] — 实验结果
- [[li2025-movingload-pinn-critical]] — 贡献 / Negative / 可迁移
- [[pinn]] — 物理信息神经网络实体
- [[notes/lectures/ai4s-pinn-deepxde]] — DeepXDE 实战参考

## Evidence By Source

### `sources/papers/li2025-movingload-pinn.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/10_1016_j_aei_2025_103215_extracted.txt`

^[sources/papers/li2025-movingload-pinn.md]
