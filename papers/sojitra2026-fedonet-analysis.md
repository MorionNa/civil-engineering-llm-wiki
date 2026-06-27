---
title: "Sojitra et al. (2026) — FEDONet: Fourier-Embedded DeepONet for Spectrally Accurate Operator Learning: 论文分析"
created: 2026-06-27
updated: 2026-06-27
type: paper-analysis
tags: [deeponet, fourier-features, operator-learning, spectral-accuracy, neural-operator, ai4s, deep-learning, pde-surrogate]
sources: [raw/papers/10_1016_j_jcp_2026_114931_extracted.txt]
methods: [fedonet, fourier-embedding, random-fourier-features, deeponet, branch-trunk-architecture]
results: [l2-error-reduction, burgers, poisson-2d, eikonal, allen-cahn, kuramoto-sivashinsky, noise-robustness, data-scaling]
failure_modes: [frequency-hyperparameter-sensitivity, linear-pde-limitation, spectral-bias]
datasets: [burgers-equation, 2d-poisson, eikonal-equation, allen-cahn, kuramoto-sivashinsky]
reproducibility: medium
code_url: []
dataset_url: []
confidence: high
---

# Sojitra et al. (2026) — FEDONet: Fourier-Embedded DeepONet for Spectrally Accurate Operator Learning

> **Authors:** Arth Sojitra, Mrigank Dhingra, Omer San
> **Venue:** Journal of Computational Physics (JCP), 2026
> **DOI:** [10.1016/j.jcp.2026.114931](https://doi.org/10.1016/j.jcp.2026.114931)

---

## 1. 工程背景 (Engineering Background)

偏微分方程（PDE）的快速求解是科学计算与工程仿真的核心需求。传统数值方法（FEM、FDM、谱方法）虽然精度高，但对参数化 PDE（如不同初始条件、边界条件、材料参数下的重复求解）需要**每次独立运行**，计算代价极高。近年来，神经算子（Neural Operator）作为一种学习**函数空间到函数空间映射**的数据驱动方法，使一次训练即可覆盖整个参数空间，推理仅需毫秒级前向传播。

然而，标准 DeepONet 的全部连接线性层在捕捉 PDE 解的**复杂空间结构**（高频振荡、尖锐梯度、混沌行为）方面存在固有局限——这是低频主导的谱偏置（spectral bias）问题。

## 2. Research Gap

标准 DeepONet 使用全连接网络作为 trunk network 编码空间坐标，其**谱偏置**使网络优先学习低频分量，难以高效捕捉高频、多尺度空间特征。要提升空间分辨率，传统做法是增加网络深度/宽度，但这带来参数膨胀和训练困难。**如何在不大幅增加网络规模的前提下，使 DeepONet 获得谱精度（spectral accuracy）级别的空间表达能力**，是尚待解决的关键问题。Fourier 特征嵌入在其他网络（如 NeRF 中的位置编码）中已被证明可缓解谱偏置，但在 DeepONet 算子学习框架中的系统研究尚属空白。

## 3. 科学问题 (Scientific Question)

**能否通过 Fourier 特征嵌入增强 DeepONet 的 trunk（及 branch）网络，在不增加网络规模的条件下实现谱精度的算子学习？** 核心假设：Fourier 嵌入将低维空间坐标映射到高维 Fourier 特征空间，使后续线性层可以高效表达任意频率分量，从而突破标准 DeepONet 的谱偏置瓶颈。

## 4. 研究目标 (Research Objective)

提出 **FEDONet（Fourier-Embedded DeepONet）**：将随机 Fourier 特征（Random Fourier Features, RFF）嵌入 DeepONet 的 trunk 网络（可选地嵌入 branch 网络），使算子学习获得**谱精度**，并在多种 PDE 基准（Burgers、2D Poisson、Eikonal、Allen-Cahn、Kuramoto-Sivashinsky）上系统验证其优于标准 DeepONet 的性能，包括不同数据量和噪声水平下的鲁棒性。

## 5. 方法机制 (Method & Mechanism)

FEDONet = DeepONet 的 branch-trunk 架构 + **Fourier 特征嵌入层**。核心改造：在 trunk 网络接收空间坐标 y 后、进入全连接层之前，先通过一个 Fourier 特征映射 `γ(y) = [cos(By), sin(By)]`，其中 B 是从某分布（通常为高斯分布 N(0, σ²)）采样的随机频率矩阵。这个映射将低维坐标升维到 Fourier 基空间，使后续的全连接层本质上在进行 Fourier 级数逼近——这正是谱精度的来源。可选的，branch 网络的输入也可施加 Fourier 嵌入以增强对输入函数高频成分的编码能力。训练完全保持 DeepONet 的标准数据驱动流程，无额外物理损失。

→ [[sojitra2026-fedonet-method]] 完整架构 + 公式

## 6. 结果证据 (Result & Evidence)

在 5 类 PDE 基准上（Burgers 方程、2D Poisson 方程、Eikonal 方程、Allen-Cahn 方程、Kuramoto-Sivashinsky 方程），FEDONet 相比标准 DeepONet 一致且显著地降低了相对 L2 误差。在**混沌与刚性系统**（如 Kuramoto-Sivashinsky）上，误差降低尤为突出。FEDONet 在**不同训练集规模**和**不同输入噪声水平**下均保持优势，展现了良好的鲁棒性和数据效率。

→ [[sojitra2026-fedonet-results]] 完整数据

## 7. 贡献 (Contribution)

1. 提出 **FEDONet** — 将随机 Fourier 特征嵌入 DeepONet 架构，首次系统验证 Fourier 嵌入在算子学习中的有效性
2. 证明 Fourier 嵌入可以在**不增加网络规模**的条件下实现谱精度的空间表达
3. 在 **5 类 PDE 基准**上系统对比 FEDONet vs. 标准 DeepONet，覆盖线性/非线性、椭圆/抛物/双曲、刚性/混沌系统
4. 验证 FEDONet 在**小数据**和**噪声干扰**下的鲁棒性优势
5. 为神经算子学习提供了一种通用的、即插即用的空间表达能力增强方法

→ [[sojitra2026-fedonet-critical#7-贡献]]

## 8. 核心知识点 (Core Knowledge)

1. **Fourier 特征嵌入缓解谱偏置** — 将坐标映射到高维 Fourier 空间，使 MLP 能高效学习高频分量
2. **谱精度的本质** — 傅里叶基是光滑周期函数的最优基，Fourier 嵌入后的全连接层等价于自适应傅里叶级数展开
3. **trunk 嵌入是关键** — trunk 网络编码空间位置，Fourier 嵌入 trunk 直接提升空间表达能力
4. **零额外参数增长** — Fourier 嵌入层的频率矩阵 B 是随机采样且固定的（不可训练），不增加可训练参数
5. **混沌/刚性系统获益最大** — 这些系统的解含丰富的高频和多尺度成分，Fourier 嵌入的优势在此类问题上最显著

## 9. Negative Knowledge

- Fourier 嵌入的频率尺度 σ（高斯分布标准差）是敏感超参数：σ 太小→低频主导（退化为标准 DeepONet），σ 太大→过拟合高频噪声
- Fourier 嵌入对**光滑解为主的线性椭圆 PDE**（如 2D Poisson）提升有限，因为解本身以低频为主
- 随机 Fourier 特征是**固定不可学习的**，无法自适应调整频率分布，可能在多尺度问题上不是最优
- 相比 FNO（Fourier Neural Operator）在 Fourier 空间进行全局积分，FEDONet 仍受限于 DeepONet 的点态内积形式
- 未讨论与可学习 Fourier 特征（如 SIREN 式的周期性激活函数）的对比

→ [[sojitra2026-fedonet-critical#9-negative-knowledge]]

## 10. 可迁移知识 (Transferable Knowledge)

| 知识 | 迁移方向 |
|------|----------|
| Fourier 嵌入作为 trunk 增强 | 任何 DeepONet 类架构（MIONet、V-DeepONet、PI-DeepONet） |
| 随机 Fourier 特征层 | 任何需要坐标编码的神经网络（NeRF、INR、GNN 位置编码） |
| 谱精度瓶颈诊断 | 如果标准 DeepONet 无法拟合高频解，优先尝试 Fourier 嵌入而非增加层数 |
| 频率尺度调参经验 | σ 的选取可通过解的频谱分析（FFT of training data）指导 |
| 数据效率提升 | 小样本场景下 Fourier 嵌入可显著降低所需训练数据量 |
| 噪声鲁棒性 | Fourier 嵌入天然对中等噪声具有鲁棒性（高噪声时 σ 需调小） |

## 11. 研究机会 (Research Opportunity)

可学习 Fourier 特征（将频率矩阵 B 设为可训练参数，自适应学习最优频率分布）；与 FNO 的混合架构（FEDONet + Fourier 层）；多尺度 Fourier 嵌入（多个 σ 的并行嵌入分支）；与物理约束结合（FEDONet + 变分能量 / PDE 残差）；扩展到 MIONet（多输入函数算子）和时序算子；自适应频率尺度选择（基于训练数据频谱分析的自动化 σ 选取）；三维 PDE 和工业级复杂几何上的验证。

→ [[sojitra2026-fedonet-critical#11-研究机会]]

---

## 12. 可复现性 (Reproducibility)

**🟡 中复现性** — 方法论清晰，Fourier 嵌入实现简单，但无公开代码

| 项目 | 说明 |
|------|------|
| **等级** | 🟡 中 |
| **官方代码** | 未公开 |
| **数据集** | 5 类标准 PDE 基准（Burgers、Poisson、Eikonal、Allen-Cahn、Kuramoto-Sivashinsky），均可由开源 PDE 求解器生成 |
| **协议** | 无 |

**复现要点**：DeepONet 架构可通过 DeepXDE 或自实现，Fourier 嵌入层实现简单（torch.cos / torch.sin + 随机高斯矩阵）。关键调参点：频率矩阵 B 的采样标准差 σ、嵌入维度（应大于输入维度 2-10 倍）。训练为纯数据驱动，无需物理损失。

## 关联页面

- [[sojitra2026-fedonet-method]] — 方法展开
- [[sojitra2026-fedonet-results]] — 结果展开
- [[sojitra2026-fedonet-critical]] — 贡献/知识/Negative/可迁移/机会
- [[fedonet]] — FEDONet 实体页
- [[deeponet]] — DeepONet 神经算子基础
- [[goswami2022-variational-deeponet-analysis]] — V-DeepONet：变分 DeepONet（物理约束互补方向）
