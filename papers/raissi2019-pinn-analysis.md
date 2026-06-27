---
title: "Raissi et al. (2019) PINN 开山之作：非线性 PDE 的深度学习求解框架"
created: 2026-06-27
updated: 2026-06-27
type: paper-analysis
tags: [physics-informed, pinn, nonlinear-pde, automatic-differentiation, inverse-problem, data-driven-discovery, scientific-machine-learning]
sources: [raw/papers/10_1016_j_jcp_2018_10_045.xml]
confidence: high
reproducibility: 🟡
code_url: https://github.com/maziarraissi/PINNs
dataset_url: n/a
---

# Raissi et al. (2019) — Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations

> **作者:** M. Raissi, P. Perdikaris, G.E. Karniadakis  
> **期刊:** Journal of Computational Physics, Vol 378, pp 686-707 (2019)  
> **DOI:** 10.1016/j.jcp.2018.10.045 | **引用:** 16,874  
> 🏛️ **PINN 范式奠基之作**

---

## 1. 工程背景

传统数值方法 (FEM/FDM/FVM) 求解非线性 PDE 面临共同困境：
- **线性化迭代** — Newton-Raphson 需 Jacobian 组装 + 迭代求解，收敛依赖初值
- **网格依赖性** — 激波/相界面需自适应网格，非线性越强越难
- **高维灾难** — 网格点数随维度指数增长

深度学习在图像、语言等领域已证明：**神经网络天然适合拟合高维非线性映射**。能否将这一能力引入 PDE 求解？

## 2. Research Gap

- 2017年前：神经网络求解 PDE 主要依赖**数据驱动**（大量仿真数据 → 监督学习），数据获取昂贵
- 物理约束融入神经网络的思想零星出现，但缺乏统一框架
- **非线性 PDE 如何处理**？尚无理论保证和系统验证

## 3. 科学问题

能否构建一个统一的深度学习框架，**无需网格离散化**，以**同一架构**处理从线性到强非线性的各类 PDE？

## 4. 研究目标

提出 Physics-Informed Neural Networks (PINNs)——以 PDE 残差作为损失函数的物理约束项，利用自动微分计算精确导数，统一处理正问题和逆问题中的非线性 PDE。

## 5. 方法摘要

详见 [[raissi2019-pinn-method]]

- **连续时间模型 (Sec 3):** 时空坐标 → 神经网络 → u(x,t)，PDE 残差通过 AD 计算
- **离散时间模型 (Sec 4):** Runge-Kutta 时间步进 + 每步 PINN
- **非线性处理核心:** 自动微分 (AD) 将任意非线性项 $u \cdot u_x$、$\sin(u)$ 等**透明地嵌入**计算图

## 6. ⚡ 非线性 PDE 处理机制（核心）

这是本文对计算力学的**范式级贡献**：

### 传统方法 vs PINN

| 方面 | FEM/FDM | **PINN** |
|------|---------|----------|
| 非线性项 $u \cdot \nabla u$ | 显式/半隐式处理，需迭代 | **AD 精确求导，无任何特殊处理** |
| 网格 | 必须 | **无网格 (mesh-free)** |
| 非线性迭代 | Newton-Raphson 收敛依赖初值 | **梯度下降，无 Jacobian 组装** |
| 高维 | 维数灾难 | **仅受网络容量限制** |

### 非线性如何被"自然吸收"

PINN 不区分线性和非线性 PDE——所有导数都通过 **自动微分 (AD)** 在计算图上求得：

$$\frac{\partial u}{\partial t} + \mathcal{N}[u; \lambda] = 0$$

对于非线性算子 $\mathcal{N}$（如 $u \cdot u_x$, $u^3$, $\sin(u)$），AD 无需任何离散化近似：
```python
u = net(x, t)
u_t = grad(u, t)
u_x = grad(u, x)
f = u_t + u * u_x - nu * grad(u_x, x)  # Burgers 非线性对流项
loss = mean(f**2)                       # 直接作为损失
```

**关键洞察:** 非线性项 $u \cdot u_x$ 对 AD 来说和线性项 $u_x$ **没有本质区别**——都是计算图上的操作。

### 验证的非线性 PDE 谱系

| PDE | 非线性类型 | 难度 |
|-----|-----------|:---:|
| Burgers 方程 | 对流非线性 $u u_x$ | 中等 |
| Schrödinger 方程 | 复值非线性 $|u|^2 u$ | 高 |
| Allen-Cahn 方程 | 反应非线性 $u(u^2-1)$ | 高 |
| Navier-Stokes 方程 | 对流非线性 $u \cdot \nabla u$ | 极高 |
| KdV 方程 | 色散非线性 $u u_x + u_{xxx}$ | 高 |

**所有上述 PDE 使用完全相同的代码框架。**

## 7. 贡献

详见 [[raissi2019-pinn-critical]]

1. **统一非线性 PDE 求解框架** — 首次证明 AD + 物理损失可以同时处理多类非线性 PDE
2. 连续时间 + 离散时间双模型
3. 正问题 + 逆问题统一处理
4. 代码开源 (TensorFlow v1)，激发整个 PINN 研究领域

## 8. 核心知识点

- **自动微分是 PINN 处理非线性的关键** — 替代了传统方法的线性化迭代
- 物理约束通过**软惩罚项**注入损失函数
- 同一框架适用于从 Burgers 到 N-S 的所有 PDE
- **非线性强度不影响方法复杂度** — 激波和光滑解代价相同

## 9. 交叉引用

- [[pinn]] — PINN 实体
- [[jagtap2019-adaptive-activation-analysis]] — 自适应激活加速 PINN
- [[wang2021-pinn-ntk-failure-analysis]] — NTK 解释为何非线性 PDE 训练更难（谱偏差）
- [[goswami2022-variational-deeponet-analysis]] — V-DeepONet：PINN 后继者
- [[notes/lectures/ai4s-pinn-deepxde]] — DeepXDE 教程
