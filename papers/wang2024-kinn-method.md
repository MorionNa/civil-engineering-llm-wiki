---
id: papers--wang2024-kinn-method
title: Wang et al. (2024) KINN 方法机制展开：KAN 替换 MLP + 三种 PDE 形式
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/paper
- method/pinn
keywords:
- automatic-differentiation
- b-spline
- energy-form
- inverse-problem
- kin
- kolmogorov-arnold
- physics-informed
- pinn
- spline
- strong-form
sources:
- sources/papers/wang2024-kinn.md
created: '2026-06-27'
updated: '2026-07-31'
confidence: high
methods:
- kan-backbone
- b-spline-activation
- strong-form-pde
- energy-form-pde
- inverse-form-pde
---

# Wang et al. (2024) — KINN 方法机制展开

> 返回概述 → [[wang2024-kinn-analysis]]

## 核心框架：KINN = KAN + PINN

KINN 将标准 PINN 中的 **MLP 骨干网络替换为 KAN (Kolmogorov–Arnold Network)**，其余 PINN 组件（自动微分 PDE 残差、物理约束损失、两阶段优化）保持不变。

```
标准 PINN:  输入 → [MLP: Linear+σ 堆叠] → 输出 → AD → PDE 残差 loss
                   ↑ 固定激活 σ，权重可学

KINN:       输入 → [KAN: 可学习 B-样条激活的边] → 输出 → AD → PDE 残差 loss
                   ↑ 激活函数本身可学，由 B-样条参数化
```

---

## 方法 1：KAN 骨干网络

### Kolmogorov–Arnold 表示定理

任意多元连续函数 $f(x_1, \ldots, x_n)$ 可表示为：

$$f(x) = \sum_{q=1}^{2n+1} \Phi_q\left(\sum_{p=1}^n \phi_{q,p}(x_p)\right)$$

其中 $\phi_{q,p}$ 和 $\Phi_q$ 是一元连续函数。**核心洞察：** 多元函数可分解为单变量函数的两层组合。

### KAN 架构

```mermaid
graph LR
    A[x₁] --> B1[φ₁,₁(x₁)]
    A --> B2[φ₂,₁(x₁)]
    A --> B3[φ₃,₁(x₁)]
    C[x₂] --> D1[φ₁,₂(x₂)]
    C --> D2[φ₂,₂(x₂)]
    C --> D3[φ₃,₂(x₂)]
    B1 --> E1[+]
    B2 --> E1
    B3 --> E1
    D1 --> E2[+]
    D2 --> E2
    D3 --> E2
    E1 --> F[Φ₁]
    E2 --> G[Φ₂]
    F --> H[+]
    G --> H
    H --> I[f(x)]
```

**MLP vs KAN 的本质差异：**

| 方面 | MLP | KAN |
|------|-----|-----|
| 激活函数位置 | **节点**（固定函数: tanh, ReLU） | **边**（可学习: B-样条） |
| 边的操作 | 线性组合 $wx + b$ | 一元非线性 $\phi(x)$ |
| 节点操作 | 非线性激活 $\sigma(\cdot)$ | 简单求和 $\sum$ |
| 可学习参数 | 权重矩阵 $W$ | 样条系数 $c_i$ |
| 参数化 | 每个神经元共享激活 | 每条边独享激活 |

### B-样条激活函数

KAN 中的每条边使用 B-样条参数化的可学习激活函数：

$$\phi(x) = w_b \cdot \text{silu}(x) + w_s \cdot \sum_{i} c_i B_i(x)$$

其中：
- $B_i(x)$ 是 B-样条基函数（在固定网格上）
- $c_i$ 是可学习的样条系数
- $w_b, w_s$ 是缩放因子
- $\text{silu}(x) = x \cdot \sigma(x)$ 提供非线性基底

**关键参数：**
- **grid size (G):** 样条节点数，控制每条边的表达能力（典型值 5-20）
- **spline order (k):** B-样条阶数（通常 k=3，即三次样条）
- **层数 (L) 和宽度 (N):** 与 MLP 类似的超参数

---

## 方法 2：三种 PDE 形式

PDE 可被表述为数学上等价但**计算上不等价**的三种形式。KINN 在这三种形式下都适用。

### 形式 A：强形式 (Strong Form)

直接最小化 PDE 残差：

$$\mathcal{L}_{\text{strong}} = \frac{1}{N_r} \sum_{i=1}^{N_r} \left| \mathcal{N}[u_\theta(x_i)] - f(x_i) \right|^2 + \lambda_{BC} \mathcal{L}_{BC}$$

其中 $\mathcal{N}$ 是微分算子，$u_\theta$ 是 KAN 网络的输出。

**适用场景：** 一般 PDE 正问题，有解析 PDE 表达式

**KINN 优势：** KAN 的样条基天然光滑，PDE 残差中高阶导数的自动微分更稳定

### 形式 B：能量形式 (Energy Form / Variational Form)

最小化能量泛函（等价于 PDE 的弱形式）：

$$\mathcal{L}_{\text{energy}} = \Pi(u_\theta) = \int_\Omega \left[ \frac{1}{2} \nabla u_\theta \cdot \nabla u_\theta - f u_\theta \right] d\Omega$$

$$\delta \Pi = 0 \iff \text{原 PDE}$$

**适用场景：** 固体力学（弹性、超弹性），其中能量泛函已建立

**KINN 特别优势：** 能量形式仅需一阶导数（vs 强形式的二阶），KAN 的样条导数计算更经济；变分一致性使 KAN 的全局样条表达精确满足能量最小原理

### 形式 C：逆问题形式 (Inverse Form)

从观测数据推断未知参数 $\lambda$：

$$\mathcal{L}_{\text{inverse}} = \frac{1}{N_d} \sum_{i=1}^{N_d} |u_\theta(x_i) - u_{\text{obs}}(x_i)|^2 + \lambda_{PDE} \mathcal{L}_{PDE}$$

参数 $\lambda$ 作为**可训练变量**与网络权重联合优化（与 [[raissi2019-pinn-method]] 的逆问题框架一致）。

**KINN 优势：** 更少参数 → 参数发现中过拟合风险更低

---

## 方法 3：自动微分与 KAN

### B-样条的解析导数

B-样条基函数的导数有**解析递推公式**：

$$B_i'(x) = \frac{k}{\xi_{i+k} - \xi_i} B_i^{k-1}(x) - \frac{k}{\xi_{i+k+1} - \xi_{i+1}} B_{i+1}^{k-1}(x)$$

这意味着 KAN 边的激活函数 $\phi(x)$ 的任意阶导数都可在计算图中**精确计算**，无需有限差分近似。

### 与 MLP 中 AD 的对比

| 操作 | MLP-PINN | KINN |
|------|----------|------|
| 一阶导 $\partial u / \partial x$ | AD 通过 tanh' | AD 通过 B-样条导数递推 |
| 二阶导 $\partial^2 u / \partial x^2$ | grad(grad(net)) | grad(grad(net)) ← 样条 C² 连续性保证 |
| 复合非线性 $\mathcal{N}[u]$ | 无差异（AD 同样处理） | 无差异 |
| 计算开销 | 低 | 中等（样条求值 + 递推） |

---

## 训练协议

与标准 PINN 一致的两阶段优化（继承自 [[raissi2019-pinn-method]]）：

1. **第一阶段：Adam** — 学习率 $10^{-3} \to 10^{-5}$，全局探索
2. **第二阶段：L-BFGS** — 准牛顿法局部精调

**KINN 特有：** 样条节点数 (grid size) 是新增关键超参。论文中的典型配置：
- 浅层 KAN: 2-3 层，宽度 5-10，grid=5-8
- 深层 KAN: 4-6 层，宽度 5-8，grid=10-20

---

## 与现有方法的对比矩阵

| | MLP-PINN | 自适应激活 PINN | KINN (本文) |
|---|---|---|---|
| 激活函数 | 固定 (tanh) | 每层可调缩放因子 | **每条边独立可学 (B-样条)** |
| 参数效率 | 低 | 中 | **高** |
| 可解释性 | 黑箱 | 有限 | **样条可视化 → 物理洞察** |
| AD 开销 | 低 | 低 | 中 |
| 理论根基 | 通用近似定理 | 无 | **Kolmogorov–Arnold 表示定理** |

---

## 页内导航

- [[wang2024-kinn-analysis|← 总览]]
- [[wang2024-kinn-results|结果展开 →]]
- [[wang2024-kinn-critical|批判分析 →]]

## Evidence By Source

### `sources/papers/wang2024-kinn.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/10_1016_j_cma_2024_117518_extracted.txt`

^[sources/papers/wang2024-kinn.md]
