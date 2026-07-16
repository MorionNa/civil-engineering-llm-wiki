---
title: "Gao et al. (2025) — APINNs 方法机制展开"
created: 2026-07-16
updated: 2026-07-16
type: paper-analysis
tags: [physics-informed, pinn, adaptive-weighting, physics-constrained-loss, soft-constraint, collocation-strategy, neural-network, nonlinear-systems, physics-constraint-weight-tuning]
sources: [raw/papers/10_1016_j_camwa_2025_01_007.xml, raw/papers/extracted/10_1016_j_camwa_2025_01_007_extracted.txt]
methods: [multitask-learning, adaptive-loss-weighting, loss-magnitude-normalization, automatic-differentiation]
results: [loss-scale-balancing, convergence-acceleration]
failure_modes: [physics-constraint-weight-tuning, update-frequency-uncertainty, incomplete-training-recipe]
datasets: [benjamin-ono-analytic-solution, sine-gordon-analytic-solution, mukherjee-kundu-analytic-solution]
reproducibility: low
code_url: []
dataset_url: []
confidence: high
---

# Gao et al. (2025) — APINNs 方法机制展开

> 返回概述 → [[gao2025-adaptive-loss-pinn-analysis]]；方法实体 → [[adaptive-loss-weighting-pinn]]

## 1. 从标准 PINN 到四任务学习

标准 [[pinn]] 用解网络 $net_u$ 表示 $u_\theta(x,t)$，再通过自动微分建立残差网络

$$f_\theta(x,t)=u_t+\mathcal{N}[u_\theta].$$

这里的 $net_f$ 不是独立拟合器，而是从 $net_u$ 的输出及导数构造的计算分支，二者共享参数 $\theta$。作者把四类约束分别视作任务：

| 任务 | 损失 | 作用 |
|---|---|---|
| 初值 | $\mathrm{MSE}_{u_0}$ | 拟合 $u(x,t_0)=h(x)$ |
| 下边界 | $\mathrm{MSE}_{lb}$ | 拟合一侧边界条件 |
| 上边界 | $\mathrm{MSE}_{ub}$ | 拟合另一侧边界条件 |
| 内部物理 | $\mathrm{MSE}_{f}$ | 令 PDE 残差接近零 |

联合目标为

$$\mathrm{MSE}_{\lambda}=\sum_{j=1}^{4}\lambda_j L_j.$$

## 2. 自适应信号

算法不直接计算 NTK 或每任务梯度，而是读取损失历史：

1. 以初始损失定义初始训练速度：$V_j^0=L_j^0$。
2. 在当前迭代 $M$ 处，计算最近 $N$ 次任务损失平均值：

$$\bar V_j=\frac{1}{N}\sum_{i=M-N+1}^{M}L_j^i.$$

3. 以

$$\mathrm{Ratio}=\frac{\max_j\bar V_j}{\min_j\bar V_j}$$

衡量四任务的量级失衡。
4. 对近期平均损失做 min–max 归一化：

$$R_j=\frac{\bar V_j-\min_k\bar V_k}{\max_k\bar V_k-\min_k\bar V_k}.$$

损失越大，$R_j$ 越接近 1，算法就应提高该任务的权重；最小损失项保持权重 1。论文结论说明其余权重被控制在 $[1,\alpha+1]$ 内。

## 3. 不能从本地全文文本核对的步骤

Algorithm 1 在 XML 中只以图片链接存在，预提取文本没有保留图内伪代码。因此下列关键细节不能据本地文本确认，不能擅自补写：

- $R_j$ 到 $\lambda_j$ 的完整分支更新式；
- 何时触发权重更新以及更新频率；
- 滑动窗口长度 $N$ 的具体取值；
- $\max\bar V_j=\min\bar V_j$ 时如何处理零分母；
- 权重是否平滑、是否停止梯度以及是否跨迭代保留状态。

作者在结论中也明确把“如何准确确定调整频率、如何保证更稳定收敛”列为未解决问题。

## 4. 三个 PDE 残差

| 基准 | PDE 残差核心 | 算子非线性 |
|---|---|---|
| Benjamin–Ono 二阶形式 | $u_{tt}+2(u^2)_{xx}+u_{xxxx}$ | 二次非线性及四阶导数 |
| Sine–Gordon | $u_{tt}-u_{xx}+\sin u$ | 非线性反应项 $\sin u$ |
| Mukherjee–Kundu | $u_{xt}+2iu(uu_x^*-u^*u_x)$ | 复值耦合非线性 |

这些项均由自动微分嵌入 $\mathrm{MSE}_f$，沿用 [[raissi2019-pinn-analysis]] 的基本范式。

## 5. 披露的算例配置

| 基准 | 网络 | $\alpha$ | 代表采样 |
|---|---|---:|---|
| Benjamin–Ono | 原文称“a hidden layer consisting of 50 neurons” | 7 | 正文图示称 $N_0=2000,N_b=200,N_f=20000$ |
| Sine–Gordon | 10 个隐藏层，每层 50 神经元 | 4 | $N_0=50,N_b=50,N_f=15000$ |
| Mukherjee–Kundu | 5 个隐藏层，每层 100 神经元 | 5 | $N_0=100,N_b=100,N_f=20000$ |

Benjamin–Ono 的正文图示配置与表 1 首行的 $N_b=2000$ 不一致，详见 [[gao2025-adaptive-loss-pinn-results]]。论文没有披露优化器、学习率、激活函数或随机种子。

## 6. 与既有自适应策略的区别

| 方法 | 调整对象 | 信号 | 特点 |
|---|---|---|---|
| 本文 APINNs | 四个损失项权重 | 近期标量损失量级 | 计算便宜，但不直接反映梯度冲突 |
| [[wang2021-pinn-ntk-failure-analysis]] | 不同损失的训练速率/权重 | NTK 特征值与训练动力学 | 理论解释更强，计算更重 |
| [[jagtap2019-adaptive-activation-analysis]] | 激活函数斜率 | 反向传播学习 | 改变网络表达与梯度流，不直接平衡复合损失 |

## 7. 实现时的最低审计要求

若复现，应保存每次迭代的四项原始损失、四个权重、$\bar V_j$、Ratio 与总损失，并同时报告固定权重 PINN。由于原文没有给出完整训练配方，任何自行选择的优化器、$N$、更新间隔、零分母保护和权重平滑都必须标成“复现实现选择”，不能归于原论文。

## 关联页面
- [[gao2025-adaptive-loss-pinn-analysis]] — 12 维论文概述
- [[gao2025-adaptive-loss-pinn-results]] — 全部数值与一致性核查
- [[pinn]] — 标准 PINN 结构
- [[adaptive-loss-weighting-pinn]] — APINNs 实体
