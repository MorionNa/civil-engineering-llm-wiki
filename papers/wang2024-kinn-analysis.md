---
id: papers--wang2024-kinn-analysis
title: Wang et al. (2024) KINN：以 Kolmogorov–Arnold 网络替代 MLP 的物理信息神经网络骨干
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/computational-mechanics
- evidence/paper
- method/pinn
keywords:
- computational-mechanics
- forward-problem
- inverse-problem
- kin
- kolmogorov-arnold
- nonlinear-pde
- physics-informed
- pinn
- solid-mechanics
- spline
sources:
- sources/papers/wang2024-kinn.md
created: '2026-06-27'
updated: '2026-07-31'
confidence: high
reproducibility: 🟡
---

# Wang et al. (2024) — Kolmogorov–Arnold-Informed neural network (KINN): 基于 Kolmogorov–Arnold 网络的物理信息深度学习框架

> **作者:** Wang Yizheng, Sun Jia, Bai Jinshuai, Anitescu Cosmin, Eshaghi Mohammad Sadegh, Zhuang Xiaoying, Rabczuk Timon, Liu Yinghua
> **期刊:** Computer Methods in Applied Mechanics and Engineering (CMAME), 2025
> **DOI:** 10.1016/j.cma.2024.117518
> 🏛️ **PINN 骨干网络范式革新 — 用 KAN 替代 MLP**

---

## 1. 工程背景

PINN 自 Raissi et al. (2019) 提出以来已成为求解非线性 PDE 的新范式。然而，标准 PINN 使用**全连接 MLP** 作为骨干网络，面临以下瓶颈：

- **参数效率低** — MLP 的权重矩阵在每个神经元处使用**固定激活函数**（tanh/sigmoid/ReLU），需要大量参数才能表达复杂函数
- **可解释性差** — MLP 是黑箱，难以从训练后的网络权重中提取物理洞察
- **谱偏差** — MLP 倾向于学习低频分量（[[wang2021-pinn-ntk-failure-analysis]] 从 NTK 角度系统分析了此问题），对高频、多尺度、奇异性问题收敛缓慢
- **训练失败** — 梯度病理学导致 PDE 残差损失停滞（[[wang2023-pinn-spurious-analysis]]）

2024 年，Liu et al. 提出 **Kolmogorov–Arnold Network (KAN)** — 一种受 Kolmogorov–Arnold 表示定理启发的全新网络架构：**将可学习的激活函数放在边上（而非节点上）**，用 B-样条 (B-spline) 参数化每个激活函数。KAN 具有**更少参数、更强表达能力、内在可解释性**。

## 2. Research Gap

- MLP 的固定激活函数 + 权重线性组合本质上是**对 Kolmogorov–Arnold 表示定理的离散近似**，表达能力受限于网络宽度和深度
- 已有 PINN 改进工作（自适应激活 [[jagtap2019-adaptive-activation-analysis]]、硬约束 [[chen2025-at-pinn-hc-analysis]]）均在 MLP 框架内修补，未触及骨干网络的根本替代
- KAN 在通用函数逼近上展现出优于 MLP 的**参数效率**和**可解释性**，但其在**物理约束训练**场景（即 PINN 范式）下的表现完全未知
- PINN 的核心操作——通过自动微分计算 PDE 残差——对 KAN 的样条激活是否依然高效？

## 3. 科学问题

**能否用 Kolmogorov–Arnold Network 替代 MLP 作为 PINN 的骨干网络？这种替代在计算固体力学中各类 PDE 的正问题和逆问题上，能否实现更高的精度和更快的收敛？**

子问题：
- KAN 的 B-样条激活函数对 PDE 高阶导数的自动微分计算是否稳定？
- 强形式 (strong form)、能量形式 (energy form)、逆问题形式 (inverse form) 三种 PDE 表述下，KAN 与 MLP 的表现差异如何？
- KAN 的少参数优势能否在物理约束优化中保持？

## 4. 研究目标

(1) 提出 **KINN (Kolmogorov–Arnold-Informed Neural Network)** — 将 KAN 作为 PINN 骨干，系统替换 MLP；(2) 在三种 PDE 形式（强形式/能量形式/逆形式）下验证 KINN 的有效性；(3) 在六类固体力学挑战问题上进行系统性基准测试。

## 5. 方法摘要

详见 [[wang2024-kinn-method]]

- **核心替换：** MLP → KAN——将网络权重固定在边的激活函数上，用 B-样条参数化
- **三种 PDE 形式：** (a) 强形式 — PDE 残差直接作为损失；(b) 能量形式 — 变分能量泛函最小化；(c) 逆问题 — 从观测数据推断未知参数
- **KAN 在 AD 中的适配：** B-样条的解析导数天然可用，自动微分无缝衔接
- 训练协议：Adam + L-BFGS 两阶段，与经典 PINN 一致

## 6. 结果摘要

详见 [[wang2024-kinn-results]]

| 问题类型 | MLP-PINN | KINN (KAN) | 改进幅度 |
|----------|:--------:|:----------:|:--------:|
| 多尺度问题 | 中 | **优** | 精度↑50-100% |
| 奇异性问题 | 差 | **优** | 误差↓数倍 |
| 应力集中 | 中 | **优** | 收敛加速 |
| 非线性超弹性 | 中 | **优** | 参数减半+精度提升 |
| 非均匀/异质 | 中 | **优** | 稳定收敛 |
| 复杂几何 | 中 | ≈ | **无优势** |

**核心发现：** KINN 在 5/6 类问题上显著优于 MLP-PINN，参数更少但精度更高。唯一例外是复杂几何——KAN 的样条基函数在非规则域上不如 MLP 灵活。

## 7. 贡献

详见 [[wang2024-kinn-critical#7-贡献]]

1. **PINN 骨干网络的范式转移** — 首次将 KAN 引入物理信息深度学习，证明可替换 MLP 且普遍更优
2. 在三种 PDE 形式（强/能量/逆）上系统性验证 KAN 的适应性
3. 揭示 KAN 在固体力学 PDE 的关键优势：多尺度、奇异性、应力集中
4. 诚实报告 KAN 在复杂几何上的局限性 — 给出适用边界

## 8. 核心知识点

- **KAN vs MLP 的本质差异：** MLP 在节点上做固定激活 + 边上做线性组合；KAN 在边上做**可学习激活（B-样条）** + 节点上做求和
- KAN 的样条基天然适合表示**光滑且局部的 PDE 解**，因此对多尺度和奇异性问题有优势
- **能量形式**特别适合 KINN——变分的一致性使 KAN 的样条表达得到最大发挥
- KINN 的参数效率来自 KAN 的**组合表达**：用少量样条基的张量积覆盖高维函数空间
- 复杂几何上 KAN 退化的原因：B-样条在规则网格上定义，非规则域需映射，引入额外误差

## 9. Negative Knowledge

详见 [[wang2024-kinn-critical#9-negative-knowledge]]

- 复杂几何无优势（甚至略差）
- KAN 训练速度在浅层时与 MLP 相当，但深层时 B-样条求值开销增大
- 样条节点数 (grid size) 是敏感超参数

## 10. 可迁移知识

| 知识 | 迁移方向 |
|------|----------|
| KAN 替代 MLP 的 PINN 设计模式 | 任何 PINN 应用可尝试 KINN 改造 |
| 能量形式 × KAN 的协同效应 | 变分 PINN、Deep Energy Method 等 |
| 样条激活的 AD 稳定性 | 其他样条基网络（如 SplineCNN）的物理约束训练 |
| 复杂几何的反面教训 | 规则域优先用 KINN，非规则域保留 MLP |

## 11. 研究机会

详见 [[wang2024-kinn-critical#11-研究机会]]

1. KAN 在复杂几何上的改进（映射函数设计、混合 KAN-MLP 架构）
2. KINN + NTK 分析 — 类比 [[wang2021-pinn-ntk-failure-analysis]]，从谱偏差角度解释 KAN 为何更优
3. 自适应样条节点分布（类比自适应激活函数 [[jagtap2019-adaptive-activation-analysis]]）
4. KINN 在流体力学、电磁学等非固体力学领域的扩展
5. 大规模 3D KINN 的 GPU 优化

---

## 交叉引用

- [[kin]] — KINN/KAN 实体
- [[raissi2019-pinn-analysis]] — PINN 奠基之作
- [[wang2021-pinn-ntk-failure-analysis]] — NTK 视角的 PINN 训练失败分析（KAN 的谱偏差优势尚未分析）
- [[jagtap2019-adaptive-activation-analysis]] — 自适应激活（MLP 框架内的激活函数改进，可对比 KAN 的可学习激活）
- [[chen2025-at-pinn-hc-analysis]] — 硬约束 PINN（可与 KINN 结合）
- [[wang2023-pinn-spurious-analysis]] — PINN 伪解（KAN 是否也能缓解伪解？）

## 12. 可复现性 (Reproducibility)

- 复现应以本页列出的原始来源、代码、数据与超参数为准。
- 未公开实现细节应记录为复现缺口，不以模型推测补齐。

## Paper Family Pages

- [[wang2024-kinn-critical]]

## Evidence By Source

### `sources/papers/wang2024-kinn.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/10_1016_j_cma_2024_117518_extracted.txt`

^[sources/papers/wang2024-kinn.md]
