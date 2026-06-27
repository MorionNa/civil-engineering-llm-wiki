---
title: "Linka et al. (2022) — Bayesian PINNs: 方法机制展开"
created: 2026-06-27
updated: 2026-06-27
type: paper-analysis
tags: [physics-informed, pinn, bayesian-inference, neural-network, hamiltonian-monte-carlo, self-adaptive-pinn]
sources: [raw/papers/10_1016_j_cma_2022_115346_extracted.txt]
confidence: high
---

# BPINN 方法机制详解

> 回主页面：[[linka2022-bayesian-pinn-analysis]]

---

## 模型问题：阻尼谐振子 + COVID-19

### 物理方程

阻尼谐振子 ODE：

$$\ddot{x} + c\dot{x} + k(x - x_0) = 0$$

或标准化形式：

$$\ddot{x} + 2\zeta\omega_0\dot{x} + \omega_0^2(x - x_0) = 0$$

其中 $c$ 为阻尼系数，$k$ 为刚度，$x_0$ 为平衡位置偏移，$\omega_0 = \sqrt{k/m}$ 为固有频率，$\delta = c/(2m)$ 为衰减率，$T = 2\pi/\omega_0$ 为周期。

**物理直觉：** COVID-19 疫情被建模为受阻尼谐振子驱动的振荡——季节性因素（阻尼+刚度）叠加长期趋势（偏移 $x_0$），感染波峰间隔约 0.325 年（≈4 个月）。

### 数据

Johns Hopkins University COVID-19 全球日新增确诊病例（2021 全年）。训练/测试按时间分割。

---

## 六大模型架构

### 神经网络家族（无贝叶斯）

#### 1. NN（纯神经网络）
- **输入：** 时间 t → 全连接前馈网络 → **输出：** 预测病例数 x(t)
- **参数：** 网络权重 θ = {W_k, b_k}
- **损失函数：** $L = L_{data} = \|x̂ - x(t)\|$
- **特点：** 无物理，无不确定量化，最简单

#### 2. PINN（Physics Informed Neural Network）
- **输入：** 时间 t → 全连接前馈网络 → **输出：** x(t)
- **参数：** 网络权重 θ = {W_k, b_k} + 物理参数 ϑ = {c, k, x₀}（可学习）
- **损失函数：**

$$L = (1 - \varepsilon)L_{data} + \varepsilon L_{phys}$$

$$L_{data} = \|\hat{x} - x(t)\|, \quad L_{phys} = \|r\|$$

其中物理残差 $r = \ddot{x} + c\dot{x} + k(x - x_0)$，通过自动微分从网络输出计算 $\dot{x}, \ddot{x}$。

- **ε 网格搜索：** ε ∈ [10⁻∞, 10⁻⁵, 10⁻⁴, 10⁻³, 10⁻², 10⁰]（6 个候选值）
- **关键缺陷：** ε 固定，需人工选择，性能敏感

#### 3. SAPINN（Self-Adaptive PINN）
- **与 PINN 相同，但 ε → ε(t)：** 权重系数随训练时间自适应调整
- **机制：** 使用 soft attention mechanism，在训练过程中自动平衡 $L_{data}$ 和 $L_{phys}$
- **优势：** 无需网格搜索 ε，对小训练集更鲁棒
- **来源：** McClenny & Braga-Neto (2020)

### 贝叶斯推理家族

#### 4. BI（Bayesian Inference，无网络）
- **不训练神经网络，直接拟合物理模型参数的后验分布**
- **参数：** 仅物理参数 ϑ = {c, k, x₀}
- **后验：** $P(ϑ|x̂) ∝ P(x̂|ϑ) · P(ϑ)$
- **采样：** HMC (Hamiltonian Monte Carlo)
- **特点：** 模型简单（仅 3 个参数），提供参数可信区间，无网络映射能力
- **先验：** 物理参数使用无信息先验

#### 5. BNN（Bayesian Neural Network，无物理）
- **贝叶斯化标准 NN：** 对网络权重 θ 学习后验分布（而非点估计）
- **参数：** 仅网络权重 θ = {W_k, b_k}
- **后验：** $P(θ|x̂) ∝ P(x̂|θ) · P(θ)$
- **采样：** HMC
- **特点：** 提供预测可信区间，但无物理约束 → 外推差
- **先验：** 网络权重使用高斯先验

#### 6. BPINN（Bayesian Physics Informed Neural Network）✨ 本文核心
- **完整融合：** 贝叶斯网络 + 物理似然
- **参数：** 网络权重 θ = {W_k, b_k} + 物理参数 ϑ = {c, k, x₀}（联合推断）
- **后验：**

$$P(Θ|x̂, r) ∝ P(x̂|Θ) · P(r|Θ) · P(Θ)$$

其中 $Θ = \{θ, ϑ\}$，$P(x̂|Θ)$ 为数据似然，$P(r|Θ)$ 为**物理残差似然**（创新点），$P(Θ)$ 为先验。

- **物理似然：** 将物理残差 $r = \ddot{x} + c\dot{x} + k(x - x_0)$ 视为"虚拟观测"，假设服从零均值高斯分布
- **采样：** HMC 在高维联合空间采样
- **计算成本：** 最高——需同时采样所有网络权重 + 物理参数

### 物理残差似然的关键设计

| 组件 | NN | PINN | SAPINN | BI | BNN | BPINN |
|------|:--:|:----:|:------:|:--:|:---:|:-----:|
| 网络权重 θ | 点估计 | 点估计 | 点估计 | — | 后验 | 后验 |
| 物理参数 ϑ | — | 点估计 | 点估计 | 后验 | — | 后验 |
| 数据似然 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 物理似然 | — | ✓ (loss) | ✓ (loss) | — | — | ✓ (likelihood) |
| 不确定量化 | — | — | — | ✓ | ✓ | ✓ |
| ε 自适应 | — | — | ✓ | — | — | — |

---

## 训练策略

### HMC 采样设置
- **采样器：** Hamiltonian Monte Carlo (No-U-Turn Sampler 变体)
- **实现：** PyMC3 + ArviZ（Python 概率编程生态）
- **链数 × 采样数：** 多链并行，每链数千次采样
- **预热期（burn-in）：** 前 N 次采样丢弃

### 评估指标
- 训练/测试集上的 $L_{data}$（数据拟合误差）
- 物理参数后验均值 ± 标准差
- 预测的 95% 可信区间（credible interval）
- 外推性能（训练时间窗口外的预测能力）
