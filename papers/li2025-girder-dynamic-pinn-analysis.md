---
title: "Li et al. (2025) — 基于PINN的斜拉桥主梁动态线形重建：论文分析"
created: 2026-06-27
updated: 2026-06-27
type: paper-analysis
tags: [physics-informed, pinn, structural-dynamics, cable-stayed-bridge, dynamic-alignment, structural-health-monitoring, ai4s, neural-network, deep-learning, inverse-problem, fourier-embedding, causal-weight, deflection-reconstruction]
sources: [raw/papers/10_1016_j_aei_2025_103581_extracted.txt]
methods: [physics-informed, pinn, fourier-embedding, causal-weight, two-surrogate-model, cable-simplification, elastic-support, dimensionless-pde, spatial-causal-weight]
results: [mgda-reconstruction, cable-stayed-bridge, deflection-reconstruction, random-load, vehicle-load, road-roughness, damage-state, measurement-noise, sensor-number]
failure_modes: [physics-constraint-weight-tuning]
datasets: [synthetic-data]
reproducibility: medium
code_url:
  - 未公开
dataset_url:
  - 合成数据（数值模拟生成）
confidence: high
---

# 基于PINN的斜拉桥主梁动态线形重建

> **作者：** Li Yi-Fan, He Wen-Yu, Ren Wei-Xin, Lu Lian
> **期刊：** Advanced Engineering Informatics, 2025, Volume 68, Part A, 103581
> **DOI：** [10.1016/j.aei.2025.103581](https://doi.org/10.1016/j.aei.2025.103581)

## 1. 工程背景 (Engineering Background)

> **⚠️ 非线性类型：** 与 li2025-movingload-pinn 相同——**材料本构为线弹性**（弹性支撑梁模型），非线性来自动力响应行为。物理约束项是线弹性 PDE，不涉及材料非线性（塑性/损伤/超弹性）。

> 为什么这个问题在工程上重要？不解决会怎样？

斜拉桥主梁动态线形（Main Girder Dynamic Alignment, MGDA）是评估桥梁运营状态的核心指标——它直接反映主梁在活载作用下的**整体变形、刚度和承载能力**。然而，斜拉桥跨径大、结构复杂，实际可布置的传感器数量极为有限，直接测量全桥线形几乎不可能。若无法准确获取 MGDA，桥梁状态评估将依赖少数测点的局部信息，可能导致结构损伤被漏判或误判，危及运营安全。^[raw/papers/10_1016_j_aei_2025_103581_extracted.txt]

## 2. Research Gap

> 已有研究缺了什么？核心矛盾是什么？为什么现有方法不行？

现有 MGDA 获取方法存在两难：(1) **直接测量法**（全站仪、GNSS、倾角仪链）需要大量传感器或人工操作，成本高且难以实时化；(2) **有限元模型更新法**依赖精确的有限元模型和完整荷载信息，而实际运营中荷载（车辆、风、温度）难以完全获知。PINN 在结构静力分析中已有应用（包括同一作者团队的移动荷载工作 [[li2025-movingload-pinn-analysis]]），但**针对斜拉桥这种索-梁耦合体系、在有限传感器条件下间接重建 MGDA** 的工作尚属空白。核心矛盾在于：如何利用 PINN 的物理约束能力，从稀疏传感器数据中推断出斜拉桥全桥的动态线形。^[raw/papers/10_1016_j_aei_2025_103581_extracted.txt]

## 3. 科学问题 (Scientific Question)

> 现有理论/模型/方法中的核心难题是什么？

**如何利用物理信息神经网络，在仅布置少量传感器的条件下，间接重建斜拉桥在随机荷载和车辆荷载作用下的主梁动态线形？** 这涉及三个子问题：(1) 如何将斜拉桥的索-梁耦合体系简化为可被 PINN 处理的控制方程；(2) 当荷载信息不完全已知时，如何同时推断外部激励和结构响应；(3) 如何确保 PINN 在稀疏观测下的时空因果一致性和精度。^[raw/papers/10_1016_j_aei_2025_103581_extracted.txt]

## 4. 研究目标 (Research Objective)

> 本文想实现什么？

1. 建立斜拉桥的简化力学模型——将斜拉索等效为连续弹性支撑，导出无量纲运动方程
2. 设计**双代理模型 PINN 框架**——一个网络代理 MGDA，另一个网络代理外部激励，实现荷载-响应联合推断
3. 通过**傅里叶嵌入 + 时空因果权重**增强网络训练：傅里叶嵌入提升高频表达力，因果权重分别在空间和时间维度强制物理序
4. 系统验证传感器数量、路面不平度、损伤状态和测量噪声对重建精度的影响

## 5. 方法机制 (Method & Mechanism)

> 本文方法如何工作？输入→输出是什么？为什么这样设计？

**核心思路：** 将斜拉索简化为连续弹性支撑，导出等效梁的动力学 PDE；用两个神经网络分别学习 MGDA 和外部激励，通过物理损失函数耦合两者。

五步方法体系：（详见 [[li2025-girder-dynamic-pinn-method]]）

1. **斜拉桥简化模型：** 将离散斜拉索等效为连续弹性支撑，导出含弹性地基项的无量纲梁动力方程，使 PINN 可处理索-梁耦合
2. **双代理模型架构：** Net₁(x,t) → MGDA 位移场 $u(x,t)$；Net₂(x,t) → 外部激励 $f(x,t)$。两个网络独立训练，通过 PDE 残差耦合
3. **傅里叶嵌入层：** 在输入层拼接 $\cos(\omega_j x), \sin(\omega_j x), \cos(\omega_j t), \sin(\omega_j t)$，增强网络对桥梁振动高频分量的表达能力
4. **时空双因果权重：** 空间因果权重沿桥跨方向加权（激励源→响应传播方向），时间因果权重沿时域加权（先发生→后发生），两者联合确保物理因果性
5. **差异化损失函数：** MGDA 网络的损失包含 PDE 残差 + BC/IC + 传感器数据拟合；激励网络的损失仅包含 PDE 残差（激励无 BC/IC 约束）

→ [[li2025-girder-dynamic-pinn-method]] 完整方法展开

## 6. 结果证据 (Result & Evidence)

> 什么结果支撑结论？关键指标、对比方法、数值。

四组系统实验验证（详见 [[li2025-girder-dynamic-pinn-results]]）：

| 实验条件 | 荷载类型 | 考察因素 | 关键结论 |
|---------|---------|---------|---------|
| 随机荷载 | 随机分布力 | 传感器数量（1~7个） | 3 个传感器即可高精度重建 |
| 车辆荷载 | 移动车辆 | 路面不平度等级 | 路面越粗糙精度越低，但仍在可接受范围 |
| 损伤工况 | 随机+车辆 | 刚度折减 10%~30% | 损伤区域位移增大，PINN 准确捕获 |
| 噪声鲁棒性 | 随机+车辆 | 1%~5% 测量噪声 | 噪声 ≤ 3% 时精度保持良好 |

→ [[li2025-girder-dynamic-pinn-results]] 完整结果展开

## 7. 贡献 (Contribution)

1. **首次将 PINN 应用于斜拉桥 MGDA 重建**：填补了 PINN 在索支承桥梁动态线形监测中的空白
2. **提出双代理模型框架**：将 MGDA 和外部激励分别用两个网络代理，实现荷载-响应联合推断——这与 [[li2025-movingload-pinn-analysis]] 的单网络反问题模式形成互补（前者推断恒定参数，本文推断时变场）
3. **斜拉索连续等效 + 弹性地基梁模型**：将复杂的斜拉桥简化为 PINN 可处理的形式，这一简化策略可推广至其他索支承结构
4. **首次引入空间因果权重**：在因果权重机制中增加空间维度，与时间因果权重构成完整的时空因果约束
5. **系统性参数研究**：传感器数量、路面不平度、损伤、噪声——四因素全链条验证，为工程部署提供了清晰的适用边界

## 8. 核心知识点 (Core Knowledge)

1. **斜拉桥 = 弹性地基梁 + 轴向力：** 将离散斜拉索等效为连续弹性支撑 $k(x)$，配合轴向力项，斜拉桥主梁动力学问题退化为变系数 Euler-Bernoulli 梁方程——这一简化是 PINN 可处理的前提
2. **双代理模型的本质是"解耦推断"：** 当一个物理场（MGDA）的驱动源（激励）也未知时，用两个网络分别代理——PDE 充当两个网络之间的"通信协议"
3. **空间因果 = 波的传播方向：** 在桥梁上，荷载引起的挠度从激励点向两端传播——空间因果权重反映了"近端先响应，远端后响应"的物理事实
4. **路面不平度是激励不确定性的一种形式：** 本文通过改变路面粗糙度谱来生成不同的车辆荷载输入，本质上是在验证 PINN 对激励不确定性的鲁棒性

## 9. Negative Knowledge

> 论文暴露的失败边界与不该照搬的做法（与 [[li2025-girder-dynamic-pinn-critical]] 共享）

- **简化为弹性地基梁的精度损失：** 连续弹性支撑假设忽略索的离散性和非线性（索的垂度效应、振动），对长索斜拉桥可能引入系统误差
- **仅数值验证，无实验/实测：** 所有案例均为合成数据，真实斜拉桥的索力偏差、温度效应、风荷载未涉及
- **两个网络独立训练的收敛问题：** 激励网络缺乏数据约束（仅靠 PDE 残差监督），在初期训练阶段可能不稳定
- **空间因果权重的方向性假设：** 当多个荷载同时作用在不同位置时，空间因果方向不再唯一

→ [[li2025-girder-dynamic-pinn-critical]] 完整分析

## 10. 可迁移知识 (Transferable Knowledge)

| 知识 | 迁移目标场景 | 迁移方式 |
|------|-------------|----------|
| 斜拉索 → 连续弹性支撑简化 | 悬索桥、拱桥、索网结构的 PINN 建模 | 将离散索力等效为空间分布刚度函数 $k(x)$ |
| 双代理模型（场+源联合推断） | 任何激励未知的 PDE 反问题（如未知热源的瞬态热传导） | 场网络 + 源网络 + PDE 耦合约束 |
| 空间因果权重 | 所有空间传播类 PDE（波传播、污染物扩散） | 沿传播方向加权 PDE 残差 |
| 荷载-路面耦合建模 | 车-桥耦合 PINN 的预处理 | 路面谱 → 荷载谱 → PINN 激励网络输入 |

## 11. 研究机会 (Research Opportunity)

1. **考虑索的非线性效应：** 引入斜拉索的垂度效应和几何非线性，从"弹性地基梁"升级为"非线性弹性地基梁"
2. **三维斜拉桥模型：** 从单梁扩展到包含主梁扭转、横弯的三维斜拉桥动力模型
3. **真实斜拉桥 SHM 数据验证：** 在服役斜拉桥的监测系统数据上测试，评估温度、风荷载等环境因素影响
4. **物理驱动的荷载识别：** 利用双代理模型直接输出车辆轴重、速度等信息——桥梁动态称重（BWIM）的新路径
5. **与 [[li2025-movingload-pinn-analysis]] 的方法融合：** 将双代理模型框架与 Dirac 高斯近似 + 自适应采样结合，处理斜拉桥上已知移动荷载 + 未知环境激励的混合场景

## 12. 可复现性 (Reproducibility)

| 项目 | 说明 |
|------|------|
| **等级** | 🟡 中 |
| **官方代码** | 未公开 |
| **数据集** | 合成数据（数值模拟生成），非公开 |
| **协议** | CC BY-NC-ND 4.0 |
| **复现要点** | 论文提供完整力学推导和 PINN 架构细节；斜拉索等效刚度函数 $k(x)$ 的推导是复现关键；双网络联合训练的损失权重配比需精细调整；傅里叶频率数 k 和因果强度 ε 为关键超参数 |

## 关联页面

- [[pinn]] — 物理信息神经网络综述实体
- [[cable-stayed-bridge]] — 斜拉桥实体
- [[li2025-girder-dynamic-pinn-method]] — 方法机制展开
- [[li2025-girder-dynamic-pinn-results]] — 实验结果展开
- [[li2025-girder-dynamic-pinn-critical]] — 贡献 / Negative / 可迁移 / 研究机会
- [[li2025-movingload-pinn-analysis]] — 同一第一作者的移动荷载 PINN 工作（互补参照）
- [[notes/lectures/ai4s-pinn-deepxde]] — AI4S PINN 入门讲座
