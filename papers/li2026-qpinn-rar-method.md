---
id: paper--li2026-qpinn-rar-method
title: "Li et al. (2026) — QPINN-RAR 方法机制"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/computational-mechanics
- method/pinn
- evidence/paper
keywords:
- residual-based-adaptive-refinement
- parametrized-quantum-circuit
- angle-embedding
- hybrid-quantum-classical
- adam-lbfgs
sources:
- sources/papers/li2026-qpinn-rar.md
created: '2026-08-06'
updated: '2026-08-06'
confidence: high
evidence_scope: full-text
reproducibility: medium
---

# QPINN-RAR 方法机制

## 总体数据流

```text
时空坐标 (t, x[, y, z])
  → 经典前处理网络
  → 参数化量子线路（PQC）
  → 经典后处理网络
  → 预测解 uθ
  → 自动微分得到时空导数
  → 初值 + 边界 + PDE 残差损失
  → Adam 训练
  → 周期性 RAR 加入高残差点
  → L-BFGS 精修
```

该方法不是纯量子求解器，而是经典神经网络、量子线路、自动微分和经典优化器组成的混合量子—经典物理信息网络。^[sources/papers/li2026-qpinn-rar.md]

## 问题输入与输出

论文考虑一般形式：

$$
\mathcal{N}[u(t,\mathbf{x})]=f(t,\mathbf{x}),
$$

并给定初值 $u(0,\mathbf{x})=u_0(\mathbf{x})$ 与边界算子条件 $\mathcal{B}[u]=g(\mathbf{x},t)$。模型输入是一维问题的 $(t,x)$ 或三维热方程的 $(t,x,y,z)$，输出为标量场近似 $u_\theta$。

## 经典前后处理网络

前处理网络为两层全连接网络，每层 20 个神经元，激活函数为 Tanh；后处理网络采用与前处理网络对称的两层、每层 20 神经元结构。论文中的经典 PINN 基线在中部使用单个 20 神经元隐藏层，而 QPINN 用 PQC 替代该中部模块。

## 参数化量子线路

图 3 展示五量子比特电路。经典特征通过 angle embedding 编码到量子态，随后经过可训练的 $R_X$、$R_Z$ 单量子比特旋转门和局部纠缠门。作者将其描述为浅层、硬件高效的 NISQ 友好线路，但正文未完整给出量子层数、纠缠拓扑、测量算子、参数初始化及 shot 设置，因此不能仅凭示意图完全复建电路。

## 物理损失

PDE 残差为：

$$
r(t,\mathbf{x})=\mathcal{N}[u_\theta(t,\mathbf{x})]-f(t,\mathbf{x}).
$$

总损失由三部分组成：

$$
\mathcal{L}(\theta)=
\lambda_{ic}\mathcal{L}_{ic}+
\lambda_{bc}\mathcal{L}_{bc}+
\lambda_f\mathcal{L}_f,
$$

其中初值、边界与方程残差项均采用均方误差。本文设置 $\lambda_{ic}=\lambda_{bc}=\lambda_f=1$，未使用动态损失加权。

## RAR 采样机制

[[residual-based-adaptive-refinement]] 在训练中周期性执行：

1. 在定义域均匀随机生成初始配置点集 $D_0$；
2. 训练固定轮数；
3. 在候选集 $C$ 计算 $s(x)=|r(x)|$；
4. 按残差排序，以比例 $\lambda$ 划分高残差区域 $P$；
5. 从 $P$ 中选取残差最大的 $n$ 个点；
6. 令 $D\leftarrow D_0\cup P_{sel}$，继续训练并重复。

算法 1 的文字把第 2 步写成“Train the PINN”，但标题和上下文均指向 QPINN-RAR；知识库将其记录为可能的表述遗留，而不据此改变方法解释。

## 采样与优化配置

- 初始配置点：500；
- 边界点：50；
- 初值点：50；
- Adam 学习率：0.001；
- Adam 阶段：10000 次迭代；
- 每 2000 次迭代执行一次 RAR；
- 每次追加 100 个高残差配置点；
- 候选点平均残差停止阈值：$5\times10^{-4}$；
- 随后切换 L-BFGS 精修；
- L-BFGS：factor=1000、pgtol=$10^{-14}$、最大 10000 次迭代；
- batch size：64。

候选集规模和高残差比例 $\lambda$ 未清楚报告，是关键复现缺口。

## 评价协议

训练点之外随机抽取 10000 个点作为评价点。论文报告十次独立运行的均值与标准差，指标包括可训练参数量、最终损失、相对 $L_2$ 误差和收敛迭代数。论文没有报告统一硬件上的墙钟训练时间、量子线路模拟开销或真实量子硬件成本。

## 假设与适用边界

- 控制方程、初值和边界条件已知且可自动微分；
- 解足够光滑，PDE 强式残差可作为训练约束；
- 候选点覆盖真实困难区域；
- PennyLane 模拟的 PQC 行为可代表所讨论的混合架构；
- 当前验证是单问题同分布拟合，不是跨参数问题族的算子学习。

## 失败风险

- 残差尺度失衡可能使 RAR 加点偏离真正重要区域；
- 配置点持续增长会增加后续每轮优化成本；
- 五量子比特参数减少可能伴随表达能力瓶颈；
- 真实量子硬件上的噪声、有限 shots 和梯度方差可能改变结果；
- 论文第二算例的显示方程与解析解存在一致性疑问，复现时必须先核对作者实际代码所用方程。

## 关联页面

- [[li2026-qpinn-rar-analysis]]
- [[li2026-qpinn-rar-results]]
- [[li2026-qpinn-rar-critical]]
- [[qpinn-rar]]
- [[residual-based-adaptive-refinement]]
- [[pinn]]
