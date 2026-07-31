---
id: papers--gao2025-adaptive-loss-pinn-analysis
title: Gao et al. (2025) — APINNs：多任务自适应损失加权求解非线性 PDE
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/paper
- method/pinn
keywords:
- adaptive-weighting
- collocation-strategy
- neural-network
- nonlinear-systems
- physics-constrained-loss
- physics-constraint-weight-tuning
- physics-informed
- pinn
- soft-constraint
- synthetic-data
sources:
- sources/papers/gao2025-adaptive-loss-pinn.md
created: '2026-07-16'
updated: '2026-07-31'
confidence: high
methods:
- multitask-learning
- adaptive-loss-weighting
- loss-magnitude-normalization
- automatic-differentiation
results:
- relative-l2-error-reduction
- loss-scale-balancing
- convergence-acceleration
failure_modes:
- physics-constraint-weight-tuning
- update-frequency-uncertainty
- loss-scale-imbalance
- reporting-inconsistency
datasets:
- benjamin-ono-analytic-solution
- sine-gordon-analytic-solution
- mukherjee-kundu-analytic-solution
reproducibility: low
---

# Physics-informed neural networks with adaptive loss weighting algorithm for solving partial differential equations

> **论文：** Bo Gao, Ruoxia Yao, Yan Li (2025), *Computers & Mathematics with Applications*, 181, 216–227. DOI: 10.1016/j.camwa.2025.01.007
> **核心定位：** 将 [[pinn]] 的初值、下边界、上边界和 PDE 残差视为四个共享参数的任务，用滑动损失量级动态调节任务权重，形成 APINNs。
> **证据范围：** 本页仅依据出版社全文 XML 与其预提取文本；Algorithm 1 为图片，预提取文本没有保留其中的完整伪代码。

## 1. 工程背景 (Engineering Background)
> **⚠️ 非线性类型：PDE 算子非线性。** 非线性分别来自 Benjamin–Ono 二阶形式中的 $(u^2)_{xx}$、Sine–Gordon 方程中的 $\sin(u)$，以及 Mukherjee–Kundu 方程中的复值非线性耦合项；不涉及塑性、损伤或滞回等材料本构非线性。PINN 通过自动微分把这些项写入 PDE 残差，这与 [[raissi2019-pinn-analysis]] 属于同一类型，而不同于本构约束的结构地震响应问题。

非线性 PDE 广泛出现在水波、非线性光学、凝聚态物理和波传播中。标准 PINN 虽可无网格地逼近解，但初值、边界值和方程残差的量级可能相差很大，使优化器优先降低某些损失而忽视其余约束，最终得到数据或边界拟合良好、内部物理残差仍偏大的解。

## 2. Research Gap
已有方法包括固定损失权重、Pareto 多目标平衡和基于梯度统计的学习率退火。本文认为尚缺少一种直接把 PINN 解释为四任务联合学习、并依据各任务近期损失量级动态平衡训练速度的简洁机制；这正对应 [[wang2021-pinn-ntk-failure-analysis]] 所揭示的多损失收敛失衡问题，但本文没有采用 NTK 分析。

## 3. 科学问题 (Scientific Question)
当 PINN 的初值、两个边界和 PDE 残差在训练中处于不同量级时，能否仅利用各任务的近期损失轨迹动态设置权重，使四项以更接近的速度和量级共同收敛，并提升非线性 PDE 解的精度？

## 4. 研究目标 (Research Objective)
提出 [[adaptive-loss-weighting-pinn]]（APINNs），把四类约束作为共享全连接网络参数的任务，设计损失量级归一化和动态加权规则，并在 Benjamin–Ono 孤立波、Sine–Gordon 呼吸波和 Mukherjee–Kundu 呼吸波上与未加权 PINN 进行同设置对比。

## 5. 方法机制 (Method & Mechanism)
网络分为共享参数的解分支 $net_u:(x,t;\theta)\mapsto u(x,t)$ 与由自动微分构造的残差分支 $net_f$。四任务联合损失为

$$\mathrm{MSE}_{\lambda}=\lambda_1\mathrm{MSE}_{u_0}+\lambda_2\mathrm{MSE}_{lb}+\lambda_3\mathrm{MSE}_{ub}+\lambda_4\mathrm{MSE}_{f}.$$

算法以初始损失 $L_j^0$ 定义初始训练速度，计算最近 $N$ 次迭代的平均损失 $\bar V_j$，再用四任务最大/最小平均损失之比衡量失衡，并以 min–max 归一化得到相对系数 $R_j$。原文结论说明最小损失项权重为 1，其余权重被限制在 1 到 $\alpha+1$；但完整权重更新伪代码只在 Algorithm 1 图片中，本地提取文本无法核对更新频率和全部分支条件。→ [[gao2025-adaptive-loss-pinn-method]]

## 6. 结果证据 (Result & Evidence)
在表格中完全对齐的首组设置下，Benjamin–Ono 的相对 $L_2$ 误差由 PINN 的 $6.442025\times10^{-1}$ 降至 APINNs 的 $1.488114\times10^{-2}$（约 43.29 倍），且迭代数由 8000 降至 4400；Sine–Gordon 由 $2.125225\times10^{-1}$ 降至 $2.065112\times10^{-2}$（约 10.29 倍）；Mukherjee–Kundu 由 $3.556391\times10^{-1}$ 降至 $1.124187\times10^{-1}$（约 3.16 倍）。三组全部设置、训练损失和文内数值不一致见 [[gao2025-adaptive-loss-pinn-results]]。

## 7. 贡献 (Contribution)
1. 将标准 PINN 明确重述为四任务共享表示学习问题，而不是笼统的“数据项 + 物理项”。
2. 用近期损失量级构造低开销的动态权重信号，并用 $\alpha$ 限制权重范围。
3. 在三种不同形式的非线性波方程上给出与标准 PINN 的逐设置对比，证明该机制在这些解析解基准上能降低误差。→ [[gao2025-adaptive-loss-pinn-critical]]

## 8. 核心知识点 (Core Knowledge)
APINNs 的核心不是修改网络表达能力，而是修改多约束优化的资源分配：损失大的任务获得更高关注，损失小的任务不再独占训练。它与 [[jagtap2019-adaptive-activation-analysis]] 的“让激活函数斜率可训练”作用位置不同，也比 NTK 权重更直接，但理论解释更弱。

## 9. Negative Knowledge
原文明确承认尚不能准确确定权重调整频率，也不能保证如何调整才能获得更稳定的收敛。三个算例均为一维、具有解析解的合成 PDE，没有噪声、复杂几何、高维或真实观测验证；$\alpha$ 分别取 7、4、5，仍需按方程选择。论文未给出代码、优化器、学习率、激活函数、随机种子及完整更新频率；部分正文与表格的样本数、区域和误差配对还存在不一致，因此不应把“至少一个数量级提升”外推到一般 PDE。

## 10. 可迁移知识 (Transferable Knowledge)

| 知识 | 可迁移方向 | 迁移方式 |
|---|---|---|
| 把复合损失写成显式任务集合 | 多物理场、界面条件、反问题 | 分别记录每项近期损失与收敛速度，避免只观察总损失 |
| 有界动态权重 | 易梯度爆炸的多约束模型 | 给权重设置上下界，防止单任务权重无限放大 |
| 量级平衡诊断 | 任意 physics-constrained model | 同时画出各分量损失，而不是只报告加权总损失 |
| APINNs + 表达侧自适应 | 高频或多尺度 PDE | 可与 [[jagtap2019-adaptive-activation-analysis]] 组合，但需做独立消融 |

## 11. 研究机会 (Research Opportunity)
应优先补齐权重更新频率、$N$ 与 $\alpha$ 的敏感性和消融研究，并与基于梯度统计、NTK 特征值、自适应采样和硬约束方法公平比较。随后可测试高维、多尺度、噪声数据、复杂边界和逆问题，并研究“平衡损失量级”是否真的等价于“平衡梯度或任务学习速度”。

## 12. 可复现性 (Reproducibility)

| 项目 | 说明 |
|---|---|
| **等级** | 🔴 低 |
| **官方代码** | 未提供 |
| **数据集** | 无外部数据集；三组解析解 PDE 基准由方程和采样点生成，论文声明 “No data was used” |
| **已披露信息** | 方程、区域、部分网络宽深、采样数、迭代数和各算例 $\alpha$ |
| **关键缺口** | Algorithm 1 图片未进入提取文本；未披露优化器、学习率、激活函数、随机种子、滑动窗口 $N$、更新频率和代码 |
| **复现风险** | 正文与表格存在若干配置/误差配对不一致，复现时必须以逐行对齐的表格条件为准并报告多随机种子统计 |

## 关联页面
- [[adaptive-loss-weighting-pinn]] — APINNs 方法实体与 adaptive-weighting 谱系
- [[pinn]] — 标准 PINN 基础范式
- [[wang2021-pinn-ntk-failure-analysis]] — 多损失训练失衡的 NTK 解释
- [[jagtap2019-adaptive-activation-analysis]] — 表达侧自适应的对照路线

## Evidence By Source

### `sources/papers/gao2025-adaptive-loss-pinn.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/10_1016_j_camwa_2025_01_007.xml`, `raw/papers/extracted/10_1016_j_camwa_2025_01_007_extracted.txt`

^[sources/papers/gao2025-adaptive-loss-pinn.md]
