---
id: entities--pinn
title: PINN — 物理信息神经网络 (Physics-Informed Neural Network)
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/computational-mechanics
- entity/tool
- method/pinn
keywords:
- ai4s
- deep-learning
- deepxde
- domain/ai4s
- domain/computational-mechanics
- entity/tool
- inverse-problem
- method/pinn
- neural-network
- physics-informed
- physics-simulation
- pinn
sources:
- raw/papers/10_1016_j_aei_2025_103215_extracted.txt
- raw/papers/10_1016_j_camwa_2025_01_007.xml
- raw/papers/10_1007_s11071-024-10359-7.pdf
- raw/papers/10_1007_s10462-025-11322-7.pdf
- raw/papers/10_1016_j_compgeo_2025_107137.xml
- raw/papers/10_1016_j_engappai_2025_113640.xml
- raw/papers/10_1016_j_cma_2025_118422.xml
- raw/papers/extracted/10_1007_s00466-024-02554-5_abstract_extracted.txt
- raw/papers/extracted/10_1007_s10518-026-02408-w_abstract_extracted.txt
- notes/lectures/ai4s-pinn-deepxde.md
created: '2026-06-27'
updated: '2026-07-31'
confidence: high
---

# PINN — 物理信息神经网络

## 定义

物理信息神经网络（Physics-Informed Neural Network, PINN）是一种将**物理定律（以偏微分方程 PDE 形式）嵌入神经网络损失函数**的深度学习框架。其核心思想是：利用自动微分计算神经网络的导数，将 PDE 的残差作为损失项，使网络在无标签数据的情况下也能学习物理上一致的解。

$$\mathcal{L}_{PINN} = \underbrace{\mathcal{L}_{PDE}}_{\text{物理残差}} + \underbrace{\mathcal{L}_{BC/IC}}_{\text{边界/初始条件}} + \underbrace{\mathcal{L}_{data}}_{\text{数据拟合（可选）}}$$

**本质公式：** Data + Neural Networks + Physical Laws = PINNs

## 历史脉络

| 时间 | 事件 |
|------|------|
| 1995 | 首次出现将 PDE 与神经网络结合的思想 |
| 2017 | Raissi 等人正式提出 PINN 概念 |
| 2019 | Raissi et al. 发表在 Journal of Computational Physics (引用 >6000) |
| 2021 | DeepXDE 库发布（陆路/耶鲁），降低 PINN 使用门槛 |
| 2023 | Wang et al. 揭示 PINN 的伪解问题和训练失败模式 |
| 2025 | 扩展至桥梁动力学、非线性 PDE 调权、跨方程变换和地震场地反应 |
| 2026 | 结构响应分支出现 HCFF-PINN、FPIKAN 与架构内物理残差 Phy-RLK |

## 核心优势

1. **无网格（Mesh-free）：** 不需要传统 FEM/FDM 的网格划分，直接在整个时空域内采样训练
2. **统一正/反问题框架：** 同一个网络和损失函数可以同时求解 PDE（正问题）和推断未知参数（反问题）
3. **数据效率：** 物理约束可作为"数据替代品"，大幅减少对标注数据的需求
4. **自动微分：** 利用 DL 框架的自动微分能力精确计算 PDE 所需的高阶导数
5. **GPU 加速：** 天然享受 DL 生态的硬件加速

## 关键挑战与解决方案

| 挑战 | 表现 | 解决方案 | 来源 |
|------|------|---------|------|
| 伪解（Spurious Solutions） | PDE 残差 loss → 0 但 L2 误差不降 | 伪时间步进、自适应步长 | [[wang2023-pinn-spurious-analysis]] |
| Dirac 奇异性处理 | 集中力/点源不可微 | 高斯近似 + 自适应采样 | [[li2025-movingload-pinn-analysis]] |
| 高频分量学习困难 | 标准 MLP 偏向低频函数 | 傅里叶嵌入层 | [[li2025-movingload-pinn-method]] |
| 时域因果违反 | 网络"先猜后期再反推前期" | 因果权重 | [[li2025-movingload-pinn-method]] |
| 物理约束权重调参 | 不同损失项的量级不匹配 | APINNs 自适应权重、硬约束 | [[gao2025-adaptive-loss-pinn-analysis]] |
| 宽频地震响应 | 低频优先、初值/ODE 梯度失衡 | 结构频率 Fourier 特征 + 初值硬约束 | [[du2026-hcff-pinn-analysis]] |
| 有限配点低损失非唯一 | 采样点残差小但连续域解可能错误 | 独立验证点 + 传统积分器交叉核验 | [[liu2025-site-response-pinn-critical]] |
| 每实例重训成本 | 土层、激励或参数改变即成为新方程实例 | 元学习、迁移学习或神经算子 | [[liu2025-site-response-pinn-analysis]] |

## PINN 的应用领域

| 领域 | 代表工作 | 关键贡献 |
|------|---------|----------|
| 流体力学 | Raissi et al. (2019) | 奠基性工作：Navier-Stokes 方程求解 |
| 固体力学/结构动力学 | Li et al. (2025) | 桥梁移动荷载动力响应，首次 PINN 结构时域分析 |
| 热传导 | — | 瞬态/稳态热传导 |
| 电磁学 | — | Maxwell 方程求解 |
| 逆问题 | — | 参数推断、源项识别、边界反演 |

## 变体与增强

- **gPINN（梯度增强 PINN）：** 在 PDE 残差基础上增加梯度残差项，显著提升精度
- **硬约束 PINN：** 通过网络结构设计自动满足边界条件（如 $u = g(x) + \ell(x) \cdot N(x)$），避免权重调参
- **RAR（残差自适应细化）：** 在 PDE 残差大的区域自适应增加训练点
- **cPINN（Conservative PINN）：** 保证物理量的守恒性
- **BPINN（Bayesian PINN）：** 引入贝叶斯推理进行不确定性量化

## 2025–2026 白名单论文证据地图

| 工作 | 机制位置 | 已验证范围 | 最重要边界 |
|------|----------|------------|------------|
| [[gao2025-adaptive-loss-pinn-analysis|APINNs]] | 损失层：按近期任务损失量级调权 | 三类一维非线性 PDE 解析基准 | 调权窗口/频率、优化器和代码未披露 |
| [[li2025-localized-waves-pinn-analysis|Bäcklund PINN]] | 约束层：双 PDE + 跨方程变换残差 | mKdV 单/双孤子与 Gaussian 初波 | 目标解无独立真值，逆变换唯一性未证明 |
| [[zhang2025-mrf-pinn|MRF-PINN]] | 架构/离散：多感受野 + 高阶差分 | 摘要称覆盖多类 PDE 与 Navier–Stokes | 仅摘要证据；作者承认尚未达到 FEM/FVM 竞争力 |
| [[luo2025-pinn-pde-review-analysis|PINN-PDE Review]] | 综述：架构、采样、损失、域分解 | 跨学科方法地图 | 无系统检索协议、公开语料或统一复跑 |
| [[liu2025-site-response-pinn-analysis|Site-response PINN]] | 输入/训练：Fourier 特征 + TPE | 线性 1/3/10 层 Kelvin–Voigt 土柱 | 每场景重训、无速度基准、全非线性未验证 |
| [[du2026-hcff-pinn-analysis|HCFF-PINN]] | 表示/约束：频率先验 + IC 硬约束 | 线性 SDOF/MDOF 与钢框架 | 复杂边界、真实材料非线性和无先验频率未验证 |
| [[tao2026-fpikan|FPIKAN]] | 表示：Fourier 输入 + Fourier-series KAN 激活 | 摘要称面向多频/噪声/缺失样本 | 仅摘要证据，无法判断材料本构非线性与量化性能 |
| [[guo2026-phy-rlk-analysis|Phy-RLK]] | 架构：Newmark-β 残差注入 LSTM-KAN | OpenSees 双向非线性 RC 响应代理 | 仍是强监督、合成标签与逐结构训练，不是无标签方程求解 |

## 关联论文（本 Wiki）

- [[li2025-movingload-pinn-analysis]] — Li et al. (2025) 桥梁移动荷载 PINN 分析（首次 PINN 结构动力学时域应用）
- [[li2025-movingload-pinn-method]] — 方法机制：高斯近似 + 傅里叶嵌入 + 因果权重
- [[wang2023-pinn-spurious-analysis]] — PINN 伪解问题分析
- [[gao2025-adaptive-loss-pinn-analysis]] — APINNs 多任务损失平衡
- [[li2025-localized-waves-pinn-analysis]] — Bäcklund 变换约束的非线性 PDE 联立求解
- [[liu2025-site-response-pinn-analysis]] — 线性地震场地反应神经求解器
- [[du2026-hcff-pinn-analysis]] — Fourier + 硬约束的结构动力 PINN
- [[guo2026-phy-rlk-analysis]] — 与 PINN 对照的架构内物理残差监督代理
- [[physics-constrained-training-failure-modes]] — PINN vs PhyLSTM 物理约束训练失败模式对比
- [[zhang2020-phylstm-analysis]] — PhyLSTM：另一种物理约束学习范式

## 关联资源

- [[notes/lectures/ai4s-pinn-deepxde]] — AI4S 第一课：PINN 入门到 DeepXDE 实战（90 分钟视频笔记）
- [[avbd]] — AVBD 硬约束物理仿真（PINN 软约束的对照范式）
- [[pseudo-time-stepping]] — 伪时间步进（PINN 伪解问题的解决方案之一）

## Evidence By Source

### `raw/papers/10_1016_j_aei_2025_103215_extracted.txt`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/10_1016_j_aei_2025_103215_extracted.txt]
