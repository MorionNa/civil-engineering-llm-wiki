---
id: entity--nonlinear-dd-preconditioning
title: Nonlinear Schwarz Preconditioning for PINN Training (SPQN)
type: entity
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
legacy_reproducibility: medium
legacy_code_url:
- https://bitbucket.org/alena_kopanicakova/DistTraiNN
legacy_tags:
- physics-informed
- pinn
- scientific-machine-learning
- adam-lbfgs
- model-parallelism
- parallel-computing
- distributed-training
- high-stiffness-ratio
- limitation
legacy_sources:
- raw/papers/kopanicakova2024-dd-preconditioning.pdf
- https://epubs.siam.org/doi/10.1137/23M1583375
---

# Nonlinear Schwarz Preconditioning for PINN Training（SPQN）

## 定义

Schwarz preconditioned quasi-Newton（SPQN）是一类把网络参数按层或模块切成多个子空间、先做局部非线性优化、再做全局准牛顿更新的 PINN 训练方法。Kopaničáková 等人在该论文中给出两个核心变体：

- **ASPQN**：additive Schwarz preconditioned quasi-Newton。各局部块从同一全局迭代出发，可并行训练，再通过 extension/synchronization 汇总。
- **MSPQN**：multiplicative Schwarz preconditioned quasi-Newton。局部块顺序训练，后一个块立即看到前一个块的更新，信息传播更快但算法串行。

它们是训练期的右非线性预条件器，不是新的 PINN 解表示，也不是推理阶段的 PDE 直接求解器。[[pinn]] 是其上层问题范式。

## 核心机制

给定参数 \(\theta=[\theta_1,\ldots,\theta_{N_{sd}}]\)，限制/延拓算子满足

\[
\theta_s=R_s\theta,\qquad
G(\theta^{(k)})=\theta^{(k)}+\alpha^{(k)}\sum_sE_s(\theta_s^*-R_s\theta^{(k)}).
\]

局部解由固定其他参数的子问题得到：

\[
\theta_s^*=\arg\min_{\theta_s}L(\theta_1,\ldots,\theta_s,\ldots,\theta_{N_{sd}}).
\]

然后全局优化器求解复合系统 \(F(\theta)=\nabla L(G(\theta))\)。论文的全局 L-BFGS 没有被移除：它仍在半步参数上产生搜索方向、动量和新的割线对；局部 L-BFGS 只是为每个外层周期提供近似块解。

## 关键事实

| 项目 | 论文证据 |
|---|---|
| 分解对象 | 网络参数空间，通常按层；不是物理时空域 \(\Omega\) |
| 局部优化 | L-BFGS，固定 \(k_s\) 次；局部 Hessian 每次局部训练重启 |
| 全局优化 | L-BFGS，保留最近 \(m=3\) 个割线对，并使用 momentum |
| 线搜索 | cubic backtracking + strong Wolfe conditions |
| ASPQN 并行 | torch.distributed/NCCL；每 GPU 一个子网络，复制全局网络后局部训练和同步 |
| MSPQN 并行 | 本质顺序；论文实现面向单 GPU |
| 训练基准 | Burgers、diffusion-advection、Klein–Gordon、Allen–Cahn；每个 10,000 个 Hammersley 配点 |
| 速度结论 | 相比 L-BFGS，论文报告 MSPQN 平均约 10 倍、ASPQN 平均约 28 倍；ASPQN 使用额外 GPU |

## 与相邻实体的关系

[[fbpinn]] 和 [[multilevel-fbpinn]] 也使用 domain-decomposition 语言，但它们切分物理坐标域、局部解网络和多尺度通信；SPQN 切分一个全局网络的参数。三者可以组合成“物理域局部表示 + 参数域训练预条件 + 粗层全局通信”的候选框架，但界面连续性、矩阵物理量和资源成本必须分别验证。

[[neural-tangent-kernel]] 可作为分析工具，检查参数分块是否改变 PINN 残差块的谱平衡；原论文没有给出 NTK 谱证明。相应的论文页为 [[kopanicakova2024-dd-preconditioning-analysis]]、[[kopanicakova2024-dd-preconditioning-method]]、[[kopanicakova2024-dd-preconditioning-results]] 和 [[kopanicakova2024-dd-preconditioning-critical]]。

## 负知识与复用边界

1. ASPQN 的多 GPU speedup 不是固定资源、固定能耗或单卡 speedup；全局网络复制会增加显存，局部 loss 仍需要完整前向。
2. MSPQN 虽然传递块间信息更快，但局部子问题顺序执行，不能把它当成天然并行算法。
3. \(N_{sd}\) 越大不保证越好；局部迭代预算、line search 和梯度评估成本决定收益。diffusion-advection 上标准 L-BFGS 的停滞说明边界条件和问题刚性会改变结论。
4. 参数域 Schwarz 不提供物理域界面连续性、守恒或结构矩阵边作用；不能直接替换 [[fbpinn]] 的窗函数拼接。
5. 训练期预条件不等于推理阶段无迭代求解。固定参数的 PINN 一次前向是函数评估；新问题实例仍可能需要 ASPQN/MSPQN + L-BFGS 训练。

## 来源与复现状态

论文正文给出了算法方程、四个基准、网络和优化器配置、并行实现以及表 3 的主要结果；参考文献列出 [DistTraiNN](https://bitbucket.org/alena_kopanicakova/DistTraiNN)，但正文以“接收后公开本文代码”的表述为主。因此该实体的复现等级为 🟡 medium；没有外部数据集，dataset_url 为空。

## 关联页面

- [[kopanicakova2024-dd-preconditioning-analysis]]
- [[kopanicakova2024-dd-preconditioning-method]]
- [[kopanicakova2024-dd-preconditioning-results]]
- [[kopanicakova2024-dd-preconditioning-critical]]
- [[pinn]]
- [[fbpinn]]
- [[multilevel-fbpinn]]
- [[neural-tangent-kernel]]

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.
