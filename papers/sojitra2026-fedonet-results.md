---
id: papers--sojitra2026-fedonet-results
title: Sojitra et al. (2026) — 结果证据展开
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/paper
- method/neural-operator
keywords:
- allen-cahn
- burgers
- deeponet
- eikonal
- fourier-features
- kuramoto-sivashinsky
- noise-robustness
- pde-benchmark
- poisson
- spectral-accuracy
sources:
- sources/papers/sojitra2026-fedonet.md
created: '2026-06-27'
updated: '2026-07-31'
confidence: high
results:
- relative-l2-error
- burgers-equation
- 2d-poisson
- eikonal-equation
- allen-cahn
- kuramoto-sivashinsky
- data-scaling
- noise-robustness
datasets:
- burgers
- poisson-2d
- eikonal
- allen-cahn
- kuramoto-sivashinsky
---

# Sojitra et al. (2026) — 结果证据展开

> 返回概述 → [[sojitra2026-fedonet-analysis]]

## 验证基准：5 类 PDE 全面覆盖

FEDONet 在覆盖**线性/非线性、椭圆/抛物/双曲、光滑/刚性/混沌**的 5 类 PDE 上系统验证：

| PDE 基准 | 类型 | 关键空间特征 | 挑战 |
|----------|------|-------------|------|
| **Burgers 方程** | 非线性抛物型 | 激波前沿、尖锐梯度 | 激波附近高频分量丰富，标准 DeepONet 难以精确捕捉 |
| **2D Poisson 方程** | 线性椭圆型 | 光滑解，拉普拉斯算子 | 低频主导，检验 Fourier 嵌入在"简单"问题上的增益上限 |
| **Eikonal 方程** | 非线性双曲型 | 波前、特性线、可能的多值解 | 梯度不连续，对空间分辨率要求高 |
| **Allen-Cahn 方程** | 非线性抛物型（刚性） | 相界面、薄过渡层 | 刚性反应项产生极薄界面，需高空间分辨率 |
| **Kuramoto-Sivashinsky (KS) 方程** | 非线性（混沌） | 多尺度时空混沌、从低频到高频全覆盖 | 最具挑战性——频谱极宽，是 Fourier 嵌入优势的最大检验场 |

---

## 核心结果 1：相对 L2 误差全面降低

FEDONet 在**全部 5 个 PDE 基准**上一致优于标准 DeepONet：

| PDE | 标准 DeepONet 相对 L2 误差 | FEDONet 相对 L2 误差 | 误差降低幅度 |
|-----|--------------------------|---------------------|-------------|
| Burgers 方程 | 基准 | 显著降低 | 大幅（激波捕捉提升） |
| 2D Poisson 方程 | 基准 | 略有降低 | 中等（低频主导，增益有限） |
| Eikonal 方程 | 基准 | 明显降低 | 大幅（波前不连续性改善） |
| Allen-Cahn 方程 | 基准 | 显著降低 | **大幅**（刚性界面精度提升） |
| Kuramoto-Sivashinsky | 基准 | **大幅降低** | **最大**（混沌多尺度频谱全覆盖） |

> **关键规律：** Fourier 嵌入的收益与 PDE 解的**频谱复杂度**正相关。混沌和刚性系统（KS、Allen-Cahn）获益最大，光滑线性系统（Poisson）获益最小。这直接验证了 Fourier 嵌入缓解谱偏置的核心假设。

---

## 核心结果 2：数据效率与规模缩放

在**不同训练集规模**下对比 FEDONet vs. 标准 DeepONet：

| 训练数据量 | 标准 DeepONet | FEDONet |
|-----------|-------------|---------|
| 极小（少量样本） | 欠拟合，误差高 | **显著更好** — Fourier 嵌入提供强归纳偏置 |
| 中等 | 收敛慢 | 收敛更快，精度更高 |
| 大量 | 逐步逼近 | 仍然领先 — 谱精度上限更高 |

> **FEDONet 的数据效率优势：** 在**小数据**场景下尤其突出。Fourier 嵌入作为一种强空间先验，在训练样本稀缺时充当正则化器，防止网络学习到非物理解。

---

## 核心结果 3：噪声鲁棒性

在输入函数 u(x) 中添加不同程度的高斯噪声，考察 FEDONet 的鲁棒性：

| 噪声水平 | 标准 DeepONet | FEDONet |
|---------|-------------|---------|
| 无噪声 | 基准 | 优于基准 |
| 低噪声 | 轻微退化 | **几乎无退化** |
| 中等噪声 | 明显退化 | 退化程度显著更低 |
| 高噪声 | 严重退化 | 仍有优势，但优势缩小 |

> **Fourier 嵌入的抗噪机制：** cos/sin 映射平滑了高频噪声分量。适当的 σ 选择使嵌入层天然起到低通滤波效应，在信号重建中抑制噪声。

---

## 逐 PDE 结果深度分析

### Burgers 方程：激波捕捉

- **物理特征：** 非线性对流项产生激波（shock），解在激波处有跳跃不连续，频谱极宽
- **FEDONet 表现：** 激波前沿的梯度捕捉精度显著优于标准 DeepONet。标准 DeepONet 的激波过渡区模糊（Gibbs 式振荡被平滑），FEDONet 保持陡峭的激波剖面
- **原因：** Fourier 嵌入使 trunk 网络能用高频基函数精确表示激波附近的快速变化

### 2D Poisson 方程：低频基准

- **物理特征：** Δu = f，解完全由源项 f 和边界条件决定，解通常光滑
- **FEDONet 表现：** 略有提升，但不显著。这是预期内的——当解以低频为主时，标准 DeepONet 的谱偏置不是瓶颈
- **教训：** Fourier 嵌入不是万能药，在光滑椭圆问题上常规 DeepONet 已足够

### Eikonal 方程：波前不连续性

- **物理特征：** |∇u| = 1，解表示最短到达时间，在源点附近有导数不连续
- **FEDONet 表现：** 在波前不连续区域精度明显提升。标准 DeepONet 会过度光滑波前，FEDONet 保持锐利特征
- **关键：** 导数不连续产生高频 Fourier 分量，Fourier 嵌入精确捕捉

### Allen-Cahn 方程：刚性相界面

- **物理特征：** 反应-扩散，参数 ε ≪ 1 产生宽度 O(ε) 的薄相界面
- **FEDONet 表现：** 界面宽度被精确保持，标准 DeepONet 的界面模糊化问题被消除
- **关键：** 薄界面 = 极高空间频率，Fourier 嵌入的谱精度在此天然适配

### Kuramoto-Sivashinsky 方程：混沌多尺度

- **物理特征：** 时空混沌，能量从低频到高频呈连续谱分布，无特征尺度
- **FEDONet 表现：** **误差降低幅度最大**——这是最直接的谱偏置缓解证据
- **核心洞察：** KS 的宽频谱使标准 DeepONet 的谱偏置问题暴露无遗，FEDONet 的 Fourier 嵌入在此"全频段"问题上全面释放潜能

---

## 与 V-DeepONet (Goswami et al., 2022) 的结果特点对比

| | FEDONet | V-DeepONet |
|---|---|---|
| 精度提升机制 | **空间表达能力增强**（Fourier 嵌入） | **物理约束正则化**（变分能量损失） |
| 对数据依赖 | 需要数据（纯数据驱动） | 少量数据 + 物理 |
| 对物理知识依赖 | 零 | 需要控制方程的能量泛函 |
| 适用 PDE 类型 | 任何有数据可生成的 PDE | 有能量泛函的 PDE |
| 互补性 | 可与 V-DeepONet 结合 | 可与 FEDONet 结合 |

> **FEDONet + V-DeepONet = 空间表达增强 + 物理约束正则化**，是未探索但潜力巨大的方向。

---

## 关联

- [[sojitra2026-fedonet-analysis]] — 概述
- [[sojitra2026-fedonet-method]] — 方法展开
- [[deeponet]] — DeepONet 神经算子
- [[goswami2022-variational-deeponet-results]] — V-DeepONet 结果对比
- [[fedonet]] — FEDONet 实体页

## Evidence By Source

### `sources/papers/sojitra2026-fedonet.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/10_1016_j_jcp_2026_114931_extracted.txt`

^[sources/papers/sojitra2026-fedonet.md]
