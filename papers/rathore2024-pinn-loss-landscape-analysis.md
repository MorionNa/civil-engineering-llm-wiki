---
id: papers--rathore2024-pinn-loss-landscape-analysis
title: Rathore et al. (2024) — PINN 训练挑战：损失景观、病态性与二阶优化
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/paper
- method/pinn
keywords:
- adam-lbfgs
- hessian-spectrum
- hessian-vector-product
- ill-conditioning
- loss-landscape
- newton-cg
- nystrom-preconditioning
- physics-informed
- pinn
- quasi-newton
- scientific-machine-learning
- second-order-optimization
sources:
- sources/papers/rathore2024-pinn-loss-landscape.md
created: '2026-07-29'
updated: '2026-07-31'
confidence: high
methods:
- hessian-spectral-density
- lbfgs-preconditioning
- adam-lbfgs
- nysnewton-cg
- gradient-damped-newton-descent
results:
- near-zero-loss-required
- 1000x-conditioning-improvement
- adam-lbfgs-superiority
- nncg-post-training-improvement
failure_modes:
- trivial-low-loss-solution
- lbfgs-early-termination
- second-order-cost
- local-theory
- benchmark-scope
datasets:
- convection-pde
- reaction-ode
- wave-pde
reproducibility: high
code_url:
- https://github.com/pratikrathore8/opt_for_pinns
---

# Challenges in Training PINNs: A Loss Landscape Perspective

> **作者：** Pratik Rathore, Weimu Lei, Zachary Frangella, Lu Lu, Madeleine Udell
> **会议：** ICML 2024，PMLR 235
> **一句话定位：** 本文从 Hessian 谱和优化病态性解释 PINN 为什么难以训练，证明微分算子的病态会传递到 PINN 损失，并提出实用的三级优化流程：Adam 负责全局探索，L-BFGS 改善局部条件数，NysNewton-CG 在 L-BFGS 停滞后继续做高精度后训练。

## 1. 工程背景 (Engineering Background)

PINN 将 PDE residual、边界条件和初始条件写入非线性最小二乘损失。理论上，前向 PDE 没有观测噪声，正确解可使训练损失接近零；但实践中，Adam 经常下降缓慢，L-BFGS 也可能提前停滞，导致网络架构或物理建模本身尚未充分检验，就被优化失败掩盖。

## 2. Research Gap

已有研究已经指出 PINN 存在梯度失衡、NTK 谱偏差和病态性，但仍缺少三个关键环节：

1. 对有限宽 PINN 的实际 Hessian 谱进行直接经验验证；
2. 解释微分算子的条件数如何传递到经验 PINN 损失；
3. 给出能在 Adam+L-BFGS 之后继续降低 loss 的高精度优化方法。

## 3. 科学问题 (Scientific Question)

为什么 PINN 的 residual loss 在参数空间中会形成极陡与极平方向并存的损失景观？这种病态性是否源自 PDE 微分算子本身？第一阶与拟二阶方法为什么各自失败，又如何组合才能稳定逼近近零训练损失？

## 4. 研究目标 (Research Objective)

论文目标包括：

- 建立 PINN loss 与解误差之间的经验关系；
- 用 Hessian spectral density 衡量损失病态性；
- 比较 Adam、L-BFGS 与 Adam+L-BFGS；
- 解释 L-BFGS 如何充当右预条件器；
- 设计 NysNewton-CG，在不显式存储 Hessian 的条件下做阻尼 Newton 后训练；
- 理论证明病态微分算子导致 PINN objective 病态，并证明 first-order→damped Newton 的组合具有与条件数无关的快速局部收敛。

## 5. 方法机制 (Method & Mechanism)

→ 详见 [[rathore2024-pinn-loss-landscape-method]]

论文研究标准 PINN 最小二乘损失：

$$
L(w)=\frac{1}{2n_{res}}\sum_i D[u(x_i^r;w)]^2+
\frac{1}{2n_{bc}}\sum_j B[u(x_j^b;w)]^2.
$$

核心分析链为：

```text
微分算子 D
  → residual Jacobian / Gauss–Newton matrix
  → Hessian 谱跨越多个数量级
  → first-order method 局部收敛慢
  → L-BFGS 近似逆 Hessian 改善条件数
  → L-BFGS line search 仍可能提前终止
  → NysNewton-CG 用 Hessian-vector products + Nyström PCG 继续求阻尼 Newton 步
```

## 6. 结果证据 (Result & Evidence)

→ 详见 [[rathore2024-pinn-loss-landscape-results]]

- PINN 通常必须达到极小训练 loss 才能获得较小 L2 relative error；
- convection、reaction、wave 的 Hessian 均同时存在接近零的谱密度和 $10^3$–$10^5$ 量级的离群大特征值；
- residual loss 是最病态的损失分量；
- L-BFGS 预条件后，最大特征值或条件数至少下降约 $10^3$；
- Adam+L-BFGS 在不同网络宽度下总体优于单独 Adam 或 L-BFGS；
- Adam+L-BFGS+NNCG 进一步将三类问题的 loss 和 L2RE 显著降低；
- NNCG 每步远慢于 L-BFGS，因此适合作为末期后训练，而非从头替代。

## 7. 贡献 (Contribution)

1. 以有限宽网络 Hessian 谱直接展示 PINN 损失病态性；
2. 定位 residual differential operator 为主要病态来源；
3. 实证比较并支持 Adam→L-BFGS 的两阶段训练范式；
4. 提出 NysNewton-CG，将 Nyström 低秩预条件、PCG、Hessian-vector product 与 Armijo line search 结合；
5. 证明微分算子的谱衰减会使 PINN 条件数随 residual points 数量多项式增长；
6. 给出 Gradient Damped Newton Descent 理论，为一阶全局阶段与二阶局部阶段组合提供收敛依据。

## 8. 核心知识点 (Core Knowledge)

- **PINN 不只是“梯度不平衡”，而是局部曲率极度不均匀。** Hessian 中大特征值和近零特征值并存，使单一学习率难以兼顾所有方向。
- **增加 residual points 不一定让优化更容易。** 理论和实验均表明，条件数可能随 $n_{res}$ 增长。
- **低 loss 通常是高精度解的必要条件，但不是充分条件。** 某些 PDE 存在 residual 为零的平凡常数解，若边界项未真正满足，仍可出现低 loss、高 L2RE。
- **Adam 与 L-BFGS 解决不同阶段的问题。** Adam 更适合避开鞍点和做全局探索；L-BFGS 更适合在局部改善条件数。
- **L-BFGS 停止不代表已达到临界点。** 强 Wolfe line search 可能返回零步长，而梯度范数仍为 $10^{-2}$–$10^{-3}$。
- **NNCG 是“末端精修器”。** 它利用二阶信息继续下降，但单步成本高，应在 Adam+L-BFGS 充分收敛后启用。

## 9. Negative Knowledge

→ 详见 [[rathore2024-pinn-loss-landscape-critical]]

- 论文并未证明所有 PINN 失败都由 Hessian 病态性造成；采样、表示能力、因果传播和 loss 权重仍可能主导；
- 理论主要面向线性微分算子和局部 PŁ* 条件；
- NNCG 在 wave 问题每步约为 L-BFGS 的 322 倍，不适合无条件长时间运行；
- 只测试 convection、reaction、wave 三类低维问题；
- near-zero empirical loss 仍不能自动保证连续域上的全局正确性；
- NNCG 需要 damping、sketch size、更新频率和 CG tolerance 等额外超参数。

## 10. 可迁移知识 (Transferable Knowledge)

| 机制 | 向结构动力 PINN 迁移 |
|---|---|
| Hessian spectral density | 判断高自由度扩展后是表示不足还是优化病态 |
| residual component spectrum | 分别分析平衡方程、初值、数据、能量和本构 loss 的曲率 |
| Adam→L-BFGS | 先全局探索，再做拟二阶局部收敛 |
| NNCG terminal stage | 在 L-BFGS 停滞后做少量高精度阻尼 Newton 精修 |
| Nyström low-rank sketch | 利用结构动力 Hessian 的快速谱衰减构造低秩预条件器 |
| condition number vs collocation count | 防止盲目增加时空配点反而恶化训练 |

## 11. 研究机会 (Research Opportunity)

1. 对非线性结构动力 PINN 分别估计运动方程、本构、能量、初值和数据 loss 的 Hessian 谱；
2. 研究自由度数、时间步、模态数量和配点数对条件数的缩放规律；
3. 将 [[jordan2024-muon-optimizer]] 用于 Adam 阶段的隐藏层矩阵，再用 L-BFGS/NNCG 完成局部收敛；
4. 将 [[song2025-rl-pinns-analysis]] 的自适应采样与 Hessian 病态诊断结合，选择既有高物理误差又不恶化条件数的配点；
5. 利用块结构或图分区构造 block-Nyström、substructure-CG 或模态预条件器；
6. 以 loss、梯度范数、物理误差和 wall-clock 联合定义自动 optimizer switching；
7. 检验强化学习是否适合学习 Adam→L-BFGS→NNCG 的切换时机，而不是直接替代梯度更新。

## 12. 可复现性 (Reproducibility)

| 项目 | 评价 |
|---|---|
| 等级 | 🟢 高 |
| 代码 | 作者公开 `opt_for_pinns` 仓库 |
| 模型 | 3 层 tanh MLP，宽度 50/100/200/400，Xavier normal |
| 优化 | Adam LR 网格；L-BFGS memory=100、strong Wolfe；三个切换时机 |
| 重复 | 每个 PDE×optimizer×width 使用 5 个随机种子 |
| 数据 | 10,000 residual points；边界/初值点数与网格说明完整 |
| 硬件 | 单 NVIDIA Titan V，PyTorch 2.0.0，CUDA 11.8 |
| NNCG | sketch size、update frequency、damping 搜索、CG 与 Armijo 参数均给出 |

## 关联页面

- [[nysnewton-cg]]
- [[rathore2024-pinn-loss-landscape-method]]
- [[rathore2024-pinn-loss-landscape-results]]
- [[rathore2024-pinn-loss-landscape-critical]]
- [[wang2021-pinn-ntk-failure-analysis]]
- [[optimizer-for-ai4s-and-physics-models]]
- [[song2025-rl-pinns-analysis]]

## Evidence By Source

### `sources/papers/rathore2024-pinn-loss-landscape.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/rathore24a.pdf`

^[sources/papers/rathore2024-pinn-loss-landscape.md]
