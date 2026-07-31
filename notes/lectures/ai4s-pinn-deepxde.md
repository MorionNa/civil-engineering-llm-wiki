---
id: notes--lectures--ai4s-pinn-deepxde
title: AI如何求解物理问题 — PINN 入门到实战 (AI4S第一课)
type: lecture
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/transcript
- method/neural-operator
- method/pinn
keywords:
- ai4s
- automatic-differentiation
- deepxde
- g-pinn
- inverse-problem
- pde
- physics-informed
- pinn
sources:
- raw/articles/avbd-siggraph2025-bilibili.md
created: '2026-06-10'
updated: '2026-07-31'
confidence: high
methods:
- pinn
- g-pinn
- deepxde
- hard-constraints
- rar
- deeponet
---

# AI如何求解物理问题 — PINN 入门到实战

> **来源：** [B站 BV1vbAsznEvX](https://www.bilibili.com/video/BV1vbAsznEvX) | 主讲：陆路（耶鲁大学）
> **活动：** Hello Universe! AI4S 第一课 VOL.03

---

## 视频概述

90 分钟完整教程，从 PINN 的历史发展到 DeepXDE 代码实战。主讲人陆路是 DeepXDE 发起人和核心作者。

## 核心内容

### 一、PINN 基础

**定义：** $\text{Data} + \text{Neural Networks} + \text{Physical Laws} = \text{PINNs}$

**PDE 一般形式：** $\mathcal{L}[u]=f$ in $U$；$\mathcal{B}[u]=g$ on $\partial U$

**损失函数：** $\text{Loss} = \frac{1}{m_r}\sum(\mathcal{L}[h_\theta]-f)^2 + \frac{1}{m_b}\sum(\mathcal{B}[h_\theta]-g)^2$

**网络结构：** 输入 → NN → 输出 u → Autodiff 求导 → 代入 PDE 计算残差 → Loss → 优化

**发展史：** 1995 年已有将 PDE 与 NN 结合的思想 → 2017 年 Raissi 提出 PINN → 2019 年发表在 Journal of Computational Physics

### 二、Physics-Informed Learning 三种场景

| 场景 | 数据量 | 物理约束 |
|------|--------|---------|
| Small Data + Lots of Physics | 少 | 多 |
| Some Data + Some Physics | 中 | 中 |
| Big Data + No Physics | 多 | 无（传统 DL）|

### 三、PINN 优化技巧

#### 1. 软约束 vs 硬约束
- **软约束：** 在损失函数中加权惩罚边界条件
- **硬约束：** 通过网络设计自动满足 BC
  - Dirichlet BC: 试解 $u = g(x) + \ell(x) \cdot N(x)$
  - 周期性 BC: 傅里叶基替换输入 $\{1, \cos(\frac{2\pi x}{P}), \sin(\frac{2\pi x}{P}), ...\}$
  - 线性约束: 无散度网络 $f = \nabla \times g$

#### 2. 自适应权重 (Self-Adaptive Weights)
- Allen-Cahn 方程验证
- 动态调整 PDE 残差和数据项的权重

#### 3. gPINN（梯度增强 PINN）
- 在 PDE 残差基础上增加梯度残差项
- **结果：** Burgers 方程/反问题中精度显著优于标准 PINN

#### 4. 残差自适应细化 (RAR)
1. 初始训练若干轮
2. 计算域内 PDE 残差绝对值
3. 在残差最大区域新增训练点
4. 重复直至平均残差 < 阈值

### 四、Why PINNs?

1. **简单易实现：** 在标准 NN 上加 PDE 残差项
2. **无网格：** 不需 FEM/FDM 网格
3. **逆问题强：** 直接反推未知参数/源项
4. **借力 DL 生态：** GPU 加速 + 自动微分

### 五、DeepXDE 实战

**三大模块：**
| 模块 | 功能 |
|------|------|
| PINN | 求解正/逆向 ODE/PDE/IDE/fPDE |
| DeepONet | 算子学习 |
| MFNN | 多保真度神经网络 |

**后端支持：** TensorFlow 1.x/2.x, PyTorch, Paddle, JAX

**9 步工作流：**
```
Geometry → PDE → IC/BC → Data → Network → Model → Compile → Train → Predict
```

**Demo 1: 一维泊松方程**
$$\frac{d^2 u}{dx^2} + \pi^2 \sin(\pi x) = 0, \quad u(-1)=u(1)=0$$
精确解: $u(x) = \sin(\pi x)$

**Demo 2: 扩散方程**
$$\frac{\partial u}{\partial t} = \frac{\partial^2 u}{\partial x^2} - e^{-t}(\sin(\pi x) - \pi^2\sin(\pi x))$$
精确解: $u(x,t) = e^{-t}\sin(\pi x)$

### 六、进阶方法

- **逆问题：** 从数据反推 $k(x)$（空间依赖的反应率）
- **域分解：** 复杂区域分而治之
- **分数阶 PINN：** 非整数阶导数
- **误差分析：** 优化误差 vs 近似误差 vs 泛化误差

### 七、逆设计/拓扑优化

约束优化 → 无约束：
$$\mathcal{L}_{\mathcal{F}} = \frac{1}{MN}\sum|\mathcal{F}_j[\hat{u}; \hat{\gamma}]|^2$$
$$\mathcal{L}_h = \mathbb{I}_{\{h(\hat{u}, \hat{\gamma}) > 0\}} h^2$$

## 核心知识点

1. **PINN 本质：** 神经网络 + PDE 残差损失 + 自动微分 = 无网格 PDE 求解器
2. **约束处理是核心：** 软约束权重调参 vs 硬约束结构设计
3. **gPINN + RAR 精度提升显著**
4. **DeepXDE 一行代码定义 PDE**，自动处理自动微分
5. **正问题（求解）和反问题（推断参数）用同一框架**
6. **逆设计用损失函数替代约束**

## 关联

- [[zhang2020-phylstm-analysis]] — PhyLSTM 物理约束学习
- [[wang2023-pinn-spurious-analysis]] — PINN 训练失败模式（梯度病理）
- [[physics-constrained-training-failure-modes]] — 物理约束训练失败对比

## Evidence By Source

### `raw/articles/avbd-siggraph2025-bilibili.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/articles/avbd-siggraph2025-bilibili.md]
