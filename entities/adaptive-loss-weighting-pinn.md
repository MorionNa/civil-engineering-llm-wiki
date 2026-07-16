---
title: "Adaptive Loss Weighting PINN (APINNs) — 多任务自适应损失加权 PINN"
created: 2026-07-16
updated: 2026-07-16
type: entity
tags: [physics-informed, pinn, adaptive-weighting, physics-constrained-loss, soft-constraint, neural-network, physics-constraint-weight-tuning]
sources: [raw/papers/10_1016_j_camwa_2025_01_007.xml, raw/papers/extracted/10_1016_j_camwa_2025_01_007_extracted.txt]
confidence: high
---

# Adaptive Loss Weighting PINN (APINNs)

## 定义

APINNs 是 Gao、Yao、Li（2025）提出的 [[pinn]] 变体。它把初值损失、下边界损失、上边界损失和 PDE 残差损失视为四个共享网络参数的任务，根据各任务近期损失量级动态调整 $\lambda_j$，目标是避免某项损失主导联合训练。

提出论文：[[gao2025-adaptive-loss-pinn-analysis]]。

## 核心机制

联合损失为

$$\mathcal{L}=\lambda_1\mathrm{MSE}_{u_0}+\lambda_2\mathrm{MSE}_{lb}+\lambda_3\mathrm{MSE}_{ub}+\lambda_4\mathrm{MSE}_{f}.$$

机制使用三个统计量：最近 $N$ 次任务损失均值 $\bar V_j$、最大/最小均值比 Ratio、以及 min–max 归一化系数 $R_j$。高损失任务获得更高关注；论文结论称最小损失项权重为 1，其余项被限制在 $1$ 到 $\alpha+1$。

完整伪代码位于原论文 Algorithm 1 图片中，当前提取文本没有保留。因此更新频率、窗口 $N$、零分母处理和全部权重分支不能从本地文本确认，详见 [[gao2025-adaptive-loss-pinn-method]]。

## 与既有 `adaptive-weighting` 的关系

`adaptive-weighting` 是本知识库 taxonomy 中的上位内容标签，表示训练过程中自动改变损失或样本权重的策略；APINNs 是其中一种**任务级、损失量级驱动**的具体实现，不等同于所有自适应加权。

| 路线 | 加权粒度 | 驱动信号 | 与 APINNs 的关系 |
|---|---|---|---|
| APINNs | 初值/边界/PDE 四任务 | 近期标量损失量级 | 本实体 |
| [[wang2021-pinn-ntk-failure-analysis]] | 不同损失分量 | NTK 特征值/训练动力学 | 同样解决收敛失衡，但信号更接近梯度机制 |
| [[causal-attention]] | 时空残差点 | 初值相对误差与时间坐标 | 属于时空因果加权，不是任务量级平衡 |
| [[jagtap2019-adaptive-activation-analysis]] | 激活函数斜率 | 反向传播学习 | 名称含“adaptive”，但不属于损失加权 |

## 适用场景

- PINN 含多个软约束且各分量损失量级长期分离；
- 希望避免 NTK/Hessian 额外计算，先建立低成本调权基线；
- 能逐项记录原始损失并允许动态改变权重的训练框架。

## 风险与边界

- 损失量级并不等价于梯度范数、任务重要性或真实误差；高损失可能来自噪声或不可满足的冲突约束。
- $\alpha$、窗口 $N$ 和更新频率仍是超参数；原论文对三种 PDE 使用不同 $\alpha$，没有给出自动选择规则。
- 原论文只验证一维解析非线性波方程，尚无高维、噪声、复杂几何或工程数据证据。
- 当前没有官方代码，复现必须明确区分论文已披露机制与实现者自行补充的训练细节。

## 证据状态

在三个解析 PDE 表格中，同配置 APINNs 的相对 $L_2$ 误差均低于标准 PINN；完全对齐首组的改进约为 43.29 倍、10.29 倍和 3.16 倍。数字与文内不一致核查见 [[gao2025-adaptive-loss-pinn-results]]。

## 关联页面
- [[gao2025-adaptive-loss-pinn-analysis]] — 原始论文 12 维分析
- [[pinn]] — 基础 PINN 实体
- [[wang2021-pinn-ntk-failure-analysis]] — 多损失训练失衡的理论背景
- [[jagtap2019-adaptive-activation-analysis]] — 另一种 PINN 自适应机制
