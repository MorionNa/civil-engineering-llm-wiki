---
title: "Li et al. (2025) — 基于物理信息神经网络的桥梁移动荷载动力响应分析：论文分析"
created: 2026-06-27
updated: 2026-06-27
type: paper-analysis
tags: [physics-informed, pinn, structural-dynamics, equation-of-motion, ai4s, physics-simulation, neural-network, deep-learning, collocation-strategy, inverse-problem]
sources: [raw/papers/10_1016_j_aei_2025_103215_extracted.txt]
methods: [physics-informed, pinn, fourier-embedding, causal-weight, collocation-strategy, gaussian-approximation]
results: [bridge-dynamics, moving-load-response, nondimensional-pde, uniform-beam, non-uniform-beam, parameter-identification]
failure_modes: [physics-constraint-weight-tuning]
datasets: [synthetic-data]
reproducibility: medium
code_url:
  - 未公开
dataset_url:
  - 合成数据（数值模拟生成）
confidence: high
---

# 基于物理信息神经网络的桥梁移动荷载动力响应分析

> **作者：** Li Yi-Fan, He Wen-Yu, Ren Wei-Xin, Shao Ya-Hui
> **期刊：** Advanced Engineering Informatics, 2025, Volume 65, 103215
> **DOI：** [10.1016/j.aei.2025.103215](https://doi.org/10.1016/j.aei.2025.103215)

## 1. 工程背景 (Engineering Background)

> 为什么这个问题在工程上重要？不解决会怎样？

桥梁在运营期间承受的主要活载是移动荷载（车辆、列车等），其诱发的动力响应直接关系到桥梁的**安全性、舒适性和疲劳寿命评估**。传统的有限元方法（FEM）虽然精度高，但在需要进行大规模参数扫描（如不同车速、不同桥型）时计算成本极高。更关键的是，桥梁健康监测（SHM）系统采集的实测响应数据往往**仅覆盖少数测点**，从稀疏观测中推断全桥动力响应和未知参数是工程界的迫切需求。若不能高效计算移动荷载下的桥梁动力响应，将无法实时评估桥梁状态，可能导致安全隐患被延误发现。^[raw/papers/10_1016_j_aei_2025_103215_extracted.txt]

## 2. Research Gap

> 已有研究缺了什么？核心矛盾是什么？为什么现有方法不行？

PINN 已在静态荷载结构响应分析中展现了强大能力，但在**移动荷载诱发的桥梁动力响应**问题上尚未被探索。核心矛盾在于：(1) 移动荷载是一个**时空耦合的 Dirac delta 函数**，其奇异性使标准 PINN 的直接应用变得困难；(2) 桥梁偏微分方程为**高阶（四阶）动力方程**，PINN 求解高阶 PDE 仍面临训练不稳定和精度不足的问题；(3) 当桥梁参数（弹性模量、边界条件、荷载大小）未知时，需要同时求解正问题和反问题，对框架的灵活性提出了更高要求。现有 PINN 研究主要集中在流体力学和低频稳态问题上，结构动力学的时域分析是 PINN 应用的一个空白地带。^[raw/papers/10_1016_j_aei_2025_103215_extracted.txt]

## 3. 科学问题 (Scientific Question)

> 现有理论/模型/方法中的核心难题是什么？

**如何利用物理信息神经网络高效、准确地求解移动荷载作用下桥梁的时空动力响应，并在少量观测数据支持下同时识别未知结构参数？** 这涉及三个子问题：(1) 如何处理移动 Dirac 荷载的奇异性使其可被神经网络学习；(2) 如何设计网络架构和训练策略以准确捕捉桥梁振动的高频动态特性；(3) 如何在同一 PINN 框架下统一处理纯物理驱动（正问题）和物理-数据联合驱动（反问题）两种场景。

## 4. 研究目标 (Research Objective)

> 本文想实现什么？

1. 建立统一的 PINN 框架，能够求解均匀/非均匀桥梁在移动荷载下的动力响应（正问题）
2. 在少量监测数据的辅助下，识别桥梁的未知参数——包括移动荷载大小、弹性模量和边界条件（反问题）
3. 通过**傅里叶嵌入层**增强网络对高频振动分量的表达，通过**因果权重**确保物理因果性（先发生后响应）
4. 提出**高斯近似 + 针对性采样策略**解决 Dirac 荷载的奇异性问题

## 5. 方法机制 (Method & Mechanism)

> 本文方法如何工作？输入→输出是什么？为什么这样设计？

**核心思路：** 将桥梁动力 PDE 嵌入神经网络的损失函数，使网络在无标签数据上也能学习物理规律。

三阶段方法体系：（详见 [[li2025-movingload-pinn-method]]）

1. **无量纲化 PDE 推导：** 对均匀和非均匀桥梁分别导出无量纲四阶动力方程，消除量纲对训练稳定性的影响
2. **移动荷载近似：** 用高斯函数 $\delta(x-vt) \approx \frac{1}{\sqrt{2\pi}\sigma}e^{-(x-vt)^2/(2\sigma^2)}$ 近似 Dirac 函数，并提出相应的自适应采样策略（在荷载位置附近加密采样点）
3. **网络增强：** 傅里叶嵌入层 $[x, t, \cos(\omega_1 x), \sin(\omega_1 x), \dots, \cos(\omega_k t), \sin(\omega_k t)]$ 提升网络对高频振动分量的表达能力；因果权重在时间维度上加权损失函数，确保前期误差不会被后期损失掩盖

**两种工作模式：**
- **PINN-DP（纯物理驱动）：** 参数已知，仅需物理约束（PDE + 边界条件 + 初始条件）
- **PINN-DPD（物理-数据联合驱动）：** 部分参数未知，在物理约束基础上加入少量监测数据的拟合项

→ [[li2025-movingload-pinn-method]] 完整方法展开

## 6. 结果证据 (Result & Evidence)

> 什么结果支撑结论？关键指标、对比方法、数值。

五组数值实验验证（详见 [[li2025-movingload-pinn-results]]）：

| 工况 | 未知量 | 工作模式 | 关键结果 |
|------|--------|----------|----------|
| Case 1: 均匀梁 | 无 | PINN-DP | 与 FEM 参考解高度吻合 |
| Case 2: 非均匀梁 | 无 | PINN-DP | 截面变化处响应准确捕获 |
| Case 3: 未知荷载 | 移动荷载大小 | PINN-DPD | 少量测点数据即可准确识别 |
| Case 4: 未知弹性模量 | E | PINN-DPD | 参数推断误差 < 1% |
| Case 5: 未知边界条件 | 约束刚度 | PINN-DPD | 边界条件准确反演 |

→ [[li2025-movingload-pinn-results]] 完整结果展开

## 7. 贡献 (Contribution)

1. **首次将 PINN 扩展到桥梁移动荷载动力响应分析**，填补了 PINN 在结构动力学时域分析中的空白
2. **高斯近似 + 自适应采样策略**：有效处理 Dirac 荷载的奇异性，使 PINN 能够学习包含移动集中力的动力响应
3. **傅里叶嵌入 + 因果权重**：两个简单但有效的增强手段——傅里叶嵌入提升高频表达能力，因果权重强化物理因果性
4. **统一正/反问题框架**：PINN-DP/PINN-DPD 双模式覆盖参数已知和未知两种场景，为 SHM 应用提供了直接路径

## 8. 核心知识点 (Core Knowledge)

1. **Dirac 函数的高斯近似是 PINN 处理集中荷载的通用策略**——不仅适用于移动荷载，任何集中力/点源问题都可借鉴
2. **傅里叶嵌入 = 给神经网络配一副"三角函数眼镜"**——使网络更容易学习周期性/振荡性解，是处理振动问题的高性价比增强
3. **因果权重解决了一个深层问题**：PINN 在时域上的损失是全局的，若不加权，后期误差可能反向"污染"前期解
4. **PINN-DP → PINN-DPD 的渐进路径**：先用已知参数验证物理约束框架的有效性，再逐步引入数据项处理未知参数——这是 PINN 应用于实际工程的可靠范式

## 9. Negative Knowledge

> 论文暴露的失败边界与不该照搬的做法（与 [[li2025-movingload-pinn-critical]] 共享）

- **仅数值验证，无实验验证**：所有案例均为合成数据，真实桥梁的测量噪声、模型误差未测试
- **参数空间有限**：仅验证了单个未知参数（荷载/E/边界），多参数同时未知的工况未探索
- **高频模态截断**：傅里叶嵌入的频率数 k 的选取缺乏理论指导，过高可能导致过拟合
- **因果权重与数据拟合的潜在冲突**：当监测数据在时域上分布不均匀时（如仅后期有数据），因果权重可能削弱数据项的贡献

→ [[li2025-movingload-pinn-critical]] 完整分析

## 10. 可迁移知识 (Transferable Knowledge)

| 知识 | 迁移目标场景 | 迁移方式 |
|------|-------------|----------|
| 高斯近似处理集中力 | 任何 PINN 求解含点荷载的 PDE | 用高斯函数替换 δ 函数，σ 控制在特征尺度的 1/10~1/20 |
| 傅里叶嵌入增强频域表达 | 所有振动/波动类 PINN 问题 | 将傅里叶特征拼接至网络输入层 |
| 因果权重 | 所有时域 PINN | 在时间维度上加递增权重函数 |
| 无量纲化预处理 | 任何含物理参数的 PINN | 先无量纲化再训练，避免量纲差异导致梯度不平衡 |

## 11. 研究机会 (Research Opportunity)

1. **多参数同时反演**：桥梁弹性模量 + 荷载大小 + 边界条件同时未知的工况
2. **真实 SHM 数据验证**：在实测桥梁监测数据上测试 PINN-DPD，评估测量噪声的鲁棒性
3. **自适应傅里叶频率选择**：根据桥梁频谱特性自动选择嵌入频率数 k 的方法
4. **多车/车队移动荷载**：扩展到多移动荷载场景
5. **车-桥耦合**：纳入车辆动力学的车-桥耦合振动分析
6. **3D 桥梁模型**：从 1D 梁模型扩展到板/壳/3D 桥梁模型

## 12. 可复现性 (Reproducibility)

| 项目 | 说明 |
|------|------|
| **等级** | 🟡 中 |
| **官方代码** | 未公开 |
| **数据集** | 合成数据（数值模拟生成），非公开 |
| **协议** | CC BY-NC-ND 4.0 |
| **复现要点** | 论文提供了完整的 PDE 推导和实施流程；高斯近似参数 σ 和傅里叶嵌入频率 ω_k 的选取是关键超参数；因果权重函数形式在论文中有明确描述，可独立复现 |

## 关联页面

- [[pinn]] — 物理信息神经网络综述实体
- [[li2025-movingload-pinn-method]] — 方法机制展开
- [[li2025-movingload-pinn-results]] — 实验结果展开
- [[li2025-movingload-pinn-critical]] — 贡献 / Negative / 可迁移 / 研究机会
- [[zhang2020-phylstm-critical]] — PhyLSTM 物理约束学习，含 PINN 失败模式关联
- [[wang2023-pinn-spurious-analysis]] — PINN 伪解问题与训练失败模式
- [[physics-constrained-training-failure-modes]] — 物理约束训练失败模式对比
- [[notes/lectures/ai4s-pinn-deepxde]] — AI4S PINN 入门讲座（DeepXDE 实战）
