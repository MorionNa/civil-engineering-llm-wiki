---
id: paper--kopanicakova2024-dd-preconditioning-method
title: Kopaničáková et al. (2024) — SPQN 方法机制
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/kopanicakova2024-dd-preconditioning
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
legacy_methods:
- nonlinear-right-preconditioning
- additive-schwarz
- multiplicative-schwarz
- layer-wise-parameter-decomposition
- lbfgs
- momentum
legacy_results:
- local-global-optimization
- model-parallelism
- memory-cost
legacy_failure_modes:
- full-network-replication
- local-gradient-cost
- line-search-stagnation
legacy_datasets:
- burgers-equation
- diffusion-advection
- klein-gordon
- allen-cahn
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
- hard-constraint-strategies
- high-stiffness-ratio
legacy_sources:
- raw/papers/kopanicakova2024-dd-preconditioning.pdf
- https://epubs.siam.org/doi/10.1137/23M1583375
evidence_scope: local workspace source record pending canonical verification
---

# SPQN：层式参数分解上的非线性 Schwarz 预条件

> 证据范围：本页按本地 arXiv:2306.17648v2 全文的第 2、3、5 节整理；正式发表版本为 SIAM Journal on Scientific Computing 46(5), S46–S67（2024），DOI: 10.1137/23M1583375。正文中的“domain decomposition”指参数空间分解，除特别说明外不指物理时空域分解。

## 1. PINN 优化对象

论文从一般 PDE

\[
\mathcal P(u(x))=f(x),\qquad \mathcal B_k(u(x))=g_k(x)
\]

出发，用带跳连的多层网络 \(u_{NN}(\theta,x)\) 近似 \(u\)。隐藏层使用

\[
y_l=y_{l-1}+\sigma_l(W^l y_{l-1}+b^l),
\]

输出层线性映射。标准 PINN 目标由 PDE 内点损失和边界损失组成；论文采用长度因子把边界条件硬编码进输出：

\[
u_{NN}(\theta,x)=\text{边界延拓}(x)+\frac{\tilde\ell(x)}{\max_{x\in\Omega}\tilde\ell(x)}\tilde u_{NN}(\theta,x),
\]

因此训练时只需最小化内点 PDE 残差的均方平均。这个位置关系可与 [[pinn]] 的软/硬约束区分开来。

## 2. 从网络到参数子空间

论文把网络参数按层分为 \(N_{sd}\) 个互不重叠的块：

\[
\theta=[\theta_1,\ldots,\theta_s,\ldots,\theta_{N_{sd}}]^\top,
\qquad \theta_s=R_s\theta .
\]

其中 \(R_s:\mathbb R^n\to\mathbb R^{n_s}\) 是 restriction，\(E_s:\mathbb R^{n_s}\to\mathbb R^n\) 是 extension，满足全局量可由各块延拓后组合。默认图示是 layer-wise decomposition；作者也指出，带重叠或不带重叠的 intra-layer decomposition 也可用于构造预条件器。

给定当前全局参数，块 \(s\) 的局部问题为

\[
\theta_s^*=\arg\min_{\theta_s}L(\theta_1,\ldots,\theta_s,\ldots,\theta_{N_{sd}}),
\]

即只优化该块，其他块固定。理论上局部问题可由 Adam、L-BFGS 或 Newton 求解；本文统一采用 L-BFGS，并只做固定 \(k_s\) 次的近似局部求解，而非把每个局部问题精确解到收敛。

## 3. 右非线性预条件器

原始最小化问题的一阶条件是

\[
\nabla L(\theta)=0.
\]

论文构造右预条件的复合系统

\[
F(\theta):=\nabla L(G(\theta)),
\]

其中 \(G\) 先通过局部块求解得到更好的半步迭代：

\[
\theta^{(k+1/2)}=G(\theta^{(k)})
=\theta^{(k)}+\alpha^{(k)}\sum_{s=1}^{N_{sd}}E_s\big(\theta_s^*-R_s\theta^{(k)}\big).
\]

这样做的含义是把“每个层块的局部非线性和局部曲率”先消化一部分，再让全局优化器处理剩余耦合。它不是对 PDE 在推理阶段做一次矩阵求逆，也不是替换 PINN 前向网络；它是训练参数的右预条件。

## 4. Additive 与 multiplicative Schwarz

| 维度 | ASPQN（additive Schwarz） | MSPQN（multiplicative Schwarz） |
|---|---|---|
| 局部起点 | 所有块都从同一 \(\theta^{(k)}\) 的限制 \(R_s\theta^{(k)}\) 开始 | 第 \(s+1\) 块看到前面块已经更新后的参数 |
| 局部求解 | 各 \(\theta_s^*\) 可同时求解 | \(s=1,\ldots,N_{sd}\) 依次求解 |
| 信息传递 | 在同步步骤统一汇总 | 局部更新立即传给后续块，通常更快传播块间信息 |
| 并行性 | 天然并行；论文实现为多 GPU | 本质串行；论文实现面向单 GPU |
| 代价 | 需要复制全局网络并承担同步/通信 | 牺牲并行度，固定资源下可能更划算 |

两种版本都在局部预条件后执行全局 L-BFGS；区别不在是否使用全局优化器，而在局部 Schwarz 校正的生成方式。算法实体见 [[nonlinear-dd-preconditioning]]。

## 5. 与 L-BFGS 的关系

全局更新不是“先用 ASPQN/MSPQN、再另起一个无关优化器”，而是每个外层周期的固定顺序：

1. 在当前 \(\theta^{(k)}\) 上解各局部问题，得到 \(\theta_s^*\)。
2. 以步长 \(\alpha^{(k)}\) 做局部到全局的同步，形成 \(\theta^{(k+1/2)}=G(\theta^{(k)})\)。
3. 在半步参数上计算全局梯度，执行一次准牛顿搜索方向
   \[
   p^{(k+1/2)}=-(B^{(k+1)})^{-1}\nabla L(\theta^{(k+1/2)}).
   \]
4. 用动量 \(v^{(k+1/2)}=(1-\mu)v^{(k-1/2)}+\mu p^{(k+1/2)}\) 更新全局参数。
5. 用
   \[
   s^{(k)}=\theta^{(k+1)}-\theta^{(k+1/2)},\quad
   y^{(k)}=\nabla L(\theta^{(k+1)})-\nabla L(\theta^{(k+1/2)})
   \]
   更新 L-BFGS 割线对。

全局和局部 L-BFGS 都只保留 \(m=3\) 个最近割线对。局部 Hessian 近似在每次局部训练重新开始；两类步长都用带强 Wolfe 条件的 cubic backtracking line search。也就是说，SPQN 的关键是**预条件器改变 L-BFGS 看到的迭代点和割线对**，并非把 L-BFGS 的曲率近似删除。

## 6. 一轮训练的计算流

全局参数 \(\theta^{(k)}\)

1. restriction \(R_s\)：把参数送到各层块。
2. 局部 L-BFGS：每块固定 \(k_s\) 次；ASPQN 所有块并行，MSPQN 按块 1 到块 \(N_{sd}\) 顺序求解。
3. extension \(E_s\) 和 Schwarz synchronization，形成 \(\theta^{(k+1/2)}=G(\theta^{(k)})\)。
4. 全局 L-BFGS、momentum、line search 更新 \(\theta^{(k+1)}\)。
5. 更新 \(S/Y\) 割线历史，进入下一轮。

局部子问题的 loss 仍需要输入通过完整网络，因为被更新的层块嵌在完整前向图中；论文因此在多 GPU 上复制全局网络，每张卡只负责一个子网络的参数局部优化。这个实现与“每卡只存一段网络”的常见模型并行不同，显存优势不能想当然。

## 7. 并行性、数据并行与成本

论文以 PyTorch 和 DistTraiNN 实现 SPQN。ASPQN 使用 torch.distributed 的 NCCL 后端，把 GPU 数设置为子网络数；局部训练后执行同步，随后所有节点并发做全局 L-BFGS。作者还指出 SPQN 可与 data parallel 无缝组合，但这不等于 ASPQN 已经证明了任意集群上的线性扩展。

每个设备的更新成本可拆成全局 L-BFGS 部分、局部优化部分和同步部分。若各块参数数目相同，ASPQN 的局部更新成本按 \((n_s/n)k_s UC_s\) 缩放；MSPQN 因串行求和为 \(k_sUC_s\)。但 loss 的前向评估仍遍历完整网络，不能把 loss/gradient 次数简单按参数比例缩小；论文明确说表 2 的梯度评估次数估计偏保守，进一步的局部梯度代码优化没有在本文中实现。

## 8. 论文实际配置

| 基准 | 深度 \(L\) | 宽度 \(n_h\) | Adam 学习率 | ASPQN \(N_{sd},k_s\) | MSPQN \(N_{sd},k_s\) |
|---|---:|---:|---:|---:|---:|
| Burgers | 8 | 20 | \(5\times10^{-4}\) | 8, 50 | 8, 50 |
| Diffusion-advection | 10 | 50 | \(1\times10^{-4}\) | 10, 10 | 10, 10 |
| Klein–Gordon | 6 | 50 | \(1\times10^{-3}\) | 6, 50 | 6, 50 |
| Allen–Cahn | 6 | 64 | \(2.5\times10^{-4}\) | 6, 50 | 6, 50 |

所有算例使用 10,000 个均匀、非自适应 Hammersley 配点；网络用自适应 tanh 和 Xavier 初始化。敏感性实验另取 \(k_s\in\{10,50,100\}\)，比较 2 块、相邻两层成块和一层一块三种分解。

## 9. 与空间域分解 PINN 的边界

[[fbpinn]] 在物理坐标小重叠子域上放局部网络并用窗函数合成解；[[multilevel-fbpinn]] 再用粗层恢复跨域通信。本文的子网并不各自拥有一个物理空间子域，所有局部块仍服务于同一个全局 \(L(\theta)\)。因此：

- 可以把本文当作“参数域/模块域预条件”与空间域分解的互补候选；
- 不能把 ASPQN 的参数同步误写成 FBPINN 的界面连续性或 XPINN 的子域 stitching；
- 若两者组合，至少需要分别验证参数局部校正、物理界面约束和全局粗空间的作用。

## 关联页面

- [[kopanicakova2024-dd-preconditioning-analysis]]
- [[kopanicakova2024-dd-preconditioning-results]]
- [[kopanicakova2024-dd-preconditioning-critical]]
- [[nonlinear-dd-preconditioning]]
- [[pinn]]
- [[fbpinn]]
- [[multilevel-fbpinn]]

^[sources/papers/kopanicakova2024-dd-preconditioning]
