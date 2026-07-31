---
id: papers--sojitra2026-fedonet-method
title: Sojitra et al. (2026) — 方法机制展开
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/paper
- method/neural-operator
- method/pinn
keywords:
- branch-trunk
- deeponet
- fourier-embedding
- neural-operator
- pde-surrogate
- random-fourier-features
- spectral-accuracy
sources:
- sources/papers/sojitra2026-fedonet.md
created: '2026-06-27'
updated: '2026-07-31'
confidence: high
methods:
- fedonet
- fourier-embedding-layer
- deeponet-architecture
- random-fourier-features
- trunk-embedding
- branch-embedding
---

# Sojitra et al. (2026) — 方法机制展开

> 返回概述 → [[sojitra2026-fedonet-analysis]]

## 核心架构：FEDONet

FEDONet = **DeepONet 算子架构** + **Fourier 特征嵌入层**，通过将输入坐标映射到 Fourier 空间，使网络获得谱精度的空间表达能力。

```
输入函数 u (在 m 个传感器点采样)          输出位置 y
         ↓                                      ↓
    [可选: Fourier Embed]              ✨ Fourier Embed γ(y)
         ↓                                      ↓
    Branch Net ──→ [b₁, ..., bₚ]       Trunk Net ──→ [t₁, ..., tₚ]
         ↓                                      ↓
         └──────── Σ b_k · t_k ────────────────┘
                        ↓
                   G(u)(y)  (谱精度输出)
```

**关键改造：** Trunk 网络的最前端插入 Fourier 特征映射层，将低维空间坐标 y ∈ ℝᵈ 映射到高维 Fourier 特征空间，使后续全连接层的工作从"学习坐标到输出的任意映射"变为"在 Fourier 基上的系数回归"。

---

## Fourier 特征嵌入 (Random Fourier Features)

### 数学定义

给定输入坐标 y ∈ ℝᵈ，Fourier 特征映射 γ(y) 定义为：

```
γ(y) = [cos(2π B₁·y), sin(2π B₁·y), ..., cos(2π Bₘ·y), sin(2π Bₘ·y)]
```

其中：
- **B = [B₁, B₂, ..., Bₘ]ᵀ** ∈ ℝᵐˣᵈ 是随机频率矩阵
- 每个频率向量 **Bᵢ ~ N(0, σ²I)** 独立地从高斯分布采样
- **σ** 是频率尺度超参数，控制嵌入的频率范围
- 输出维度 = **2m**（每个频率一个 cos + 一个 sin）

### 为什么有效？

| 机制 | 解释 |
|------|------|
| **升维** | 将 d 维坐标映射到 2m 维（通常 m ≫ d），高维空间使线性可分性增强 |
| **频率增强** | cos/sin 基天然覆盖从低频到高频的完整频谱，σ 控制频率上限 |
| **谱精度来源** | 后续全连接层 `W·γ(y) + b` 等价于**自适应 Fourier 级数**，逼近理论保证指数收敛 |
| **核机器视角** | γ(y₁)·γ(y₂) ≈ k(y₁, y₂)，Fourier 特征实现了平移不变核（如高斯核）的随机近似 |

### 与 NeRF 位置编码的关系

FEDONet 的 Fourier 嵌入与 NeRF（Neural Radiance Fields）中的**位置编码（Positional Encoding）**在数学上同源：

| | NeRF 位置编码 | FEDONet Fourier 嵌入 |
|---|---|---|
| 频率选取 | 确定性：2⁰, 2¹, ..., 2ᴸ⁻¹ 的几何级数 | 随机：从 N(0, σ²) 采样 |
| 频率数量 | 人工指定 L（层数） | 参数 m（嵌入维度的一半） |
| 可学习性 | 不可学习 | 不可学习 |
| 理论基础 | 神经正切核（NTK）谱分析 | 随机 Fourier 特征（RFF）+ Bochner 定理 |

> **区别：** FEDONet 的随机采样策略更灵活，σ 连续调节频率范围，避免了 NeRF 几何级数的频率离散化和人工选 L 的限制。

---

## Trunk 网络的 Fourier 嵌入（核心）

### 改造前 vs 改造后

```
标准 DeepONet Trunk:               FEDONet Trunk:

  y (坐标, ℝᵈ)                       y (坐标, ℝᵈ)
       ↓                                  ↓
  Linear(d, h₁)                    ✨ Fourier Embed γ(y) (ℝ²ᵐ)
       ↓                                  ↓
  ReLU                             Linear(2m, h₁)
       ↓                                  ↓
  Linear(h₁, h₂)                   ReLU
       ↓                                  ↓
  ...                              Linear(h₁, h₂)
       ↓                                  ↓
  Linear(hₗ₋₁, p)                  ...
       ↓                                  ↓
  [t₁, ..., tₚ]                    Linear(hₗ₋₁, p)
                                        ↓
                                   [t₁, ..., tₚ]
```

### 关键设计选择

1. **嵌入仅在 trunk 的第一层**：Fourier 特征层后接标准 MLP，不做多层 Fourier 变换
2. **频率矩阵 B 在初始化时随机采样，训练期间固定**：不参与梯度更新，保证训练稳定性
3. **嵌入维度 2m 通常取输入维度 d 的 5-20 倍**：太低则频率覆盖不足，太高则冗余
4. **σ 是唯一新增的敏感超参数**：控制频率范围上限

---

## Branch 网络的可选 Fourier 嵌入

Branch 网络接收输入函数 u 在 m 个传感器位置的采样值 `[u(x₁), u(x₂), ..., u(xₘ)]`。对于输入函数富含高频成分的情况（如 Burgers 激波、Kuramoto-Sivashinsky 混沌），可对传感器坐标 x 也施加 Fourier 嵌入：

```
传感器坐标 x₁, ..., xₘ           传感器值 u(x₁), ..., u(xₘ)
       ↓
✨ Fourier Embed γ(xᵢ)
       ↓
拼接 [γ(x₁), u(x₁), ..., γ(xₘ), u(xₘ)]
       ↓
    Branch Net (MLP) → [b₁, ..., bₚ]
```

> **注意：** Trunk 嵌入对空间表达能力的提升是首要的，Branch 嵌入是增强选项，对输入函数高频特征明显的 PDE（激波、混沌）更有效。

---

## 训练策略

### 损失函数

FEDONet 保持 DeepONet 的标准数据驱动训练：

```
Loss = (1/N) Σᵢ Σⱼ ||G_θ(uᵢ)(yⱼ) - G(uᵢ)(yⱼ)||²
```

其中 `G_θ` 是 FEDONet 预测的算子，`G` 是真值算子（由传统数值方法预先计算），`(uᵢ, yⱼ)` 遍历训练集中的输入函数和评估位置。

### 训练流程

```
1. 随机采样频率矩阵 B ~ N(0, σ²I)（固定）
2. 对每个训练样本 (u, {(y, G(u)(y))}):
   a. Trunk: y → γ(y) → MLP → [t₁(y), ..., tₚ(y)]
   b. Branch: [u(x₁), ..., u(xₘ)] → MLP → [b₁, ..., bₚ]
   c. 内积: G_θ(u)(y) = Σ bₖ · tₖ(y)
   d. 计算 MSE 损失
3. Adam / L-BFGS 优化
4. 训练完成 → 对任意新输入函数 u，一次前向传播即可预测全域解
```

### 超参数空间

| 超参数 | 作用 | 典型范围 |
|--------|------|----------|
| σ（频率尺度） | 控制嵌入的频率范围 | 0.1 ~ 100（依赖 PDE 特征频率） |
| m（嵌入维度/2） | 频率数量 | 32 ~ 512 |
| DeepONet 分支数 p | 基函数数量 | 50 ~ 200 |
| Branch/Trunk 网络深度/宽度 | 非线性表达能力 | 3-5 层，64-256 神经元 |

---

## 与相关方法的对比

| | FEDONet (本文) | 标准 DeepONet | FNO | PINN |
|---|---|---|---|---|
| 核心机制 | Fourier 嵌入 trunk | 全连接 trunk | Fourier 空间积分 | PDE 残差损失 |
| 空间表达 | **谱精度** | 代数精度 | 谱精度 | 依赖网络容量 |
| 参数效率 | 高（零额外可训练参数） | 基准 | 中（Fourier 层有参数） | 低（逐问题重训练） |
| 物理约束 | 无（纯数据） | 无（纯数据） | 无（纯数据） | 强（PDE 残差） |
| 算子学习 | ✓ | ✓ | ✓ | ✗（单函数求解） |
| 实现复杂度 | **低**（仅加一层） | 低 | 中（需 FFT） | 中（需自动微分算导数） |

> FEDONet 的独特优势：以**最小实现复杂度**（仅一层 cos/sin 映射 + 随机矩阵）换取**最大精度增益**。

---

## 关联

- [[sojitra2026-fedonet-analysis]] — 概述
- [[fedonet]] — FEDONet 实体页
- [[deeponet]] — DeepONet 神经算子基础
- [[goswami2022-variational-deeponet-method]] — V-DeepONet 方法对比（物理约束 vs 空间表达增强）

## Evidence By Source

### `sources/papers/sojitra2026-fedonet.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/10_1016_j_jcp_2026_114931_extracted.txt`

^[sources/papers/sojitra2026-fedonet.md]
