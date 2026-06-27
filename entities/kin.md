---
title: "KINN — Kolmogorov–Arnold-Informed Neural Network (KAN + PINN)"
created: 2026-06-27
updated: 2026-06-27
type: entity
tags: [physics-informed, pinn, kan, kolmogorov-arnold, spline, b-spline, solid-mechanics, neural-operator, ai4s]
sources: [raw/papers/10_1016_j_cma_2024_117518_extracted.txt]
confidence: high
---

# KINN — Kolmogorov–Arnold-Informed Neural Network

## 定义

**KINN (Kolmogorov–Arnold-Informed Neural Network)** 是一种将 **KAN (Kolmogorov–Arnold Network)** 作为骨干网络替代 MLP 的物理信息神经网络（PINN）。由 Wang Yizheng 等人（2024, CMAME）提出，其核心创新在于：**将 PINN 中的全连接 MLP 替换为 KAN，从而实现参数效率更高、精度更好、且内在可解释的 PDE 求解器。**

$$u_\theta(x) = \text{KAN}(x; \theta) \quad \text{替代} \quad u_\theta(x) = \text{MLP}(x; \theta)$$

KINN 保留了 PINN 的全部其余组件：自动微分 (AD) 计算 PDE 残差、物理约束损失函数、两阶段优化（Adam + L-BFGS）。

## KAN (Kolmogorov–Arnold Network) 的本质

### 数学根基：Kolmogorov–Arnold 表示定理

任意多元连续函数 $f(x_1, \ldots, x_n)$ 可分解为：

$$f(x) = \sum_{q=1}^{2n+1} \Phi_q\left(\sum_{p=1}^n \phi_{q,p}(x_p)\right)$$

关键洞察：**多元函数 = 两层单变量函数的组合。**

### KAN 的实现

KAN 将此定理实现为神经网络：
- **边（Edge）：** 放置可学习的一元非线性激活函数 $\phi(x)$，用 **B-样条 (B-spline)** 参数化
- **节点（Node）：** 仅做简单求和 $\sum$
- **这与 MLP 恰好相反：** MLP 在边上做线性组合 $Wx+b$，在节点上做固定非线性 $\sigma(\cdot)$

```
MLP:  输入 → [Linear: Wx+b] → [Node: σ(·)] → [Linear] → ... → 输出
KAN:  输入 → [Edge: φ(x) (B-spline)] → [Node: Σ] → [Edge: Φ(x)] → ... → 输出
```

### B-样条激活函数

$$\phi(x) = w_b \cdot \text{silu}(x) + w_s \cdot \sum_{i} c_i B_i(x)$$

- $B_i(x)$: B-样条基函数（在固定网格上）
- $c_i$: 可学习的样条系数（每条边独享一组系数）
- 超参数: grid size (G) — 样条节点数；spline order (k) — 样条阶数

## KINN 的核心优势

| 维度 | 说明 |
|------|------|
| **参数效率** | 同精度下参数数为 MLP-PINN 的 1/3 到 1/10 |
| **多尺度能力** | B-样条的多分辨率 → 天然适合含多频率分量的解 |
| **奇异性处理** | B-样条的局部支撑性 → 奇异性附近不污染全局 |
| **导数精度** | B-样条 C² 连续性 → 应力/梯度恢复更准确 |
| **可解释性** | 样条函数可可视化 → 提取物理洞察 |
| **能量形式协同** | KAN + 变分能量原理 = 最佳组合 |

## 已知局限

| 局限 | 说明 |
|------|------|
| **复杂几何退化** | B-样条定义在规则张量积网格 → 非规则域需映射，优势消失 |
| **训练速度** | 深层 KAN 的 B-样条求值比 MLP 慢 |
| **超参数敏感** | grid size (G) 需逐问题调优 |
| **理论缺失** | KAN-PINN 的 NTK 谱偏差特性尚未分析（vs [[wang2021-pinn-ntk-failure-analysis]]） |

## 适用场景判断

```
是否规则域？
├── 是 → 用 KINN（几乎总是优于 MLP-PINN）
└── 否 → 用 MLP-PINN，或 KAN-MLP 混合架构

是否含多尺度/奇异性？
├── 是 → 强烈推荐 KINN
└── 否 → KINN 可能有小幅优势

是否需要能量形式？
├── 是 → KINN + 能量形式 = 最优
└── 否 → KINN 强形式也有优势
```

## 三种 PDE 形式

KINN 支持 PDE 的三种数学上等价、计算上不等价的表述：

| 形式 | 损失函数 | 最佳匹配场景 |
|------|----------|------------|
| 强形式 (Strong) | $\mathcal{L} = \|\mathcal{N}[u] - f\|^2$ | 一般 PDE |
| 能量形式 (Energy) | $\mathcal{L} = \Pi(u)$（变分泛函） | 固体力学（弹性/超弹性） |
| 逆形式 (Inverse) | $\mathcal{L} = \|u_{\text{pred}} - u_{\text{obs}}\|^2 + \lambda \mathcal{L}_{PDE}$ | 参数发现 |

## 历史脉络

| 时间 | 事件 |
|------|------|
| 1957 | Kolmogorov–Arnold 表示定理提出 |
| 2019 | Raissi et al. 提出 PINN（MLP 骨干） |
| 2021 | Wang et al. 从 NTK 解释 MLP-PINN 训练失败 |
| 2024 | Liu et al. 提出 KAN (arXiv:2404.19756) |
| 2024 | Wang Yizheng et al. 提出 KINN — 首次将 KAN 引入 PINN |
| 2025 | KINN 发表于 CMAME |

## 关联论文（本 Wiki）

- [[wang2024-kinn-analysis]] — KINN 论文分析总览
- [[wang2024-kinn-method]] — KINN 方法展开（KAN 架构 + 三种 PDE 形式）
- [[wang2024-kinn-results]] — KINN 结果展开（六类对比测试）
- [[wang2024-kinn-critical]] — 贡献/Negative/可迁移/研究机会
- [[raissi2019-pinn-analysis]] — PINN 奠基之作（MLP-PINN 基线）
- [[wang2021-pinn-ntk-failure-analysis]] — NTK 视角的 PINN 失败分析（KAN 的谱偏差优势理论缺口）
- [[jagtap2019-adaptive-activation-analysis]] — 自适应激活 PINN（MLP 框架内激活函数的改进，对比 KAN 的可学习激活）
- [[chen2025-at-pinn-hc-analysis]] — 硬约束 PINN（可与 KINN 结合的约束策略）
- [[pinn]] — PINN 实体
- [[deeponet]] — DeepONet（另一种神经算子，可混合 KAN 表达）
