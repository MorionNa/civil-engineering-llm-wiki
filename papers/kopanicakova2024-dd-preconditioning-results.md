---
id: paper--kopanicakova2024-dd-preconditioning-results
title: Kopaničáková et al. (2024) — SPQN 实验结果
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
- aspqn
- mspqn
- lbfgs-baseline
- hammersley-collocation
- adaptive-tanh
legacy_results:
- relative-l2-error
- convergence
- gradient-evaluations
- update-cost
- training-time
- speedup
legacy_failure_modes:
- line-search-stagnation
- resource-dependent-speedup
- adam-baseline-exclusion
- diffusion-advection-stagnation
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
- benchmark
- high-stiffness-ratio
- limitation
legacy_sources:
- raw/papers/kopanicakova2024-dd-preconditioning.pdf
- https://epubs.siam.org/doi/10.1137/23M1583375
evidence_scope: local workspace source record pending canonical verification
---

# SPQN 实验结果：误差、成本与速度

> 数值证据边界：本页只转录本地 arXiv:2306.17648v2 预抽取全文中的表 1–3、图 3–7 及正文描述；没有从图像坐标反推未给出的精确数值。正式出版元数据为 SIAM Journal on Scientific Computing 46(5), S46–S67（2024），DOI: 10.1137/23M1583375。

## 1. 评价定义与对照

论文监控 PDE loss 和相对 \(L^2\) 误差

\[
E_{rel}(u_{NN},u^*)=
\frac{\Vertu_{NN}-u^*\Vert_{L^2(\Omega)}}{\Vertu_{NN}\Vert_{L^2(\Omega)}}.
\]

这里的分母按原文是 \(\Vertu_{NN}\Vert\)，不是常见的 \(\Vertu^*\Vert\)；复现时不可悄悄替换。Klein–Gordon 的 \(u^*\) 来自解析表达式，Burgers、diffusion-advection 和 Allen–Cahn 的参考解由高保真有限元求得。

SPQN 的敏感性实验使用 ASPQN/MSPQN；state-of-the-art 对照是 Adam 和带相同 \(m=3\)、line-search、momentum 设置的标准 L-BFGS。所有 Adam/L-BFGS 对照在确定性设置下使用数据集中的全部样本。

## 2. 四个 PDE 基准

| 基准 | 方程与参数 | 区间/边界信息 | 参考解 |
|---|---|---|---|
| Burgers | \(u_t+u\nabla u-\nu\nabla^2u=0\)，\(\nu=0.01/\pi\) | \(t\in(0,1],x\in(-1,1)\)；初值 \(-\sin(\pi x)\)，两端 \(u=0\) | 高保真有限元 |
| Diffusion-advection | \(-\nabla\cdot(\mu\nabla u)+b\cdot\nabla u=f\)，\(\mu=10^{-2}, b=(1,1)^\top,f=1\) | \((x_1,x_2)\in(0,1)^2\)，全边界 \(u=0\) | 高保真有限元 |
| Klein–Gordon | \(u_{tt}+\alpha\nabla^2u+\beta u+\gamma u^2=f\)，\(\alpha=-1,\beta=0,\gamma=1\) | \(t\in(0,12],x\in(-1,1)\)；初值 \(u=x,u_t=0\)，端点 \(-\cos t,+\cos t\) | \(u=x\cos t\) 解析解 |
| Allen–Cahn | \(u_t-D\nabla^2u-5(u-u^3)=0\)，\(D=0.001\) | \(t\in(0,1],x\in(-1,1)\)；初值 \(x^2\cos(\pi x)\)，两端 \(u=-1\) | 高保真有限元 |

这些问题同时覆盖非线性输运、非线性反应/波动和线性对流扩散；因此“SPQN 有效”不能简化为只在一种非线性 PDE 上调参成功。

## 3. 统一训练设置

- 每个问题使用 10,000 个内点配点；采样为均匀、非自适应 Hammersley 低差异序列。作者刻意提高配点数，以尽量压低离散误差，观察优化误差。
- 网络宽度/深度通过标准 L-BFGS 的超参数搜索选择：宽度候选 \(\{20,32,50,64,100,128\}\)，深度候选 \(\{4,6,8,10,12\}\)。采用自适应 tanh 和 Xavier 初始化。
- 表 1 的最终网络与优化器配置如下；SPQN 的 \(N_{sd}\) 为子网络数，\(k_s\) 为每个局部 L-BFGS 的固定迭代数。

| 基准 | 深度 | 宽度 | Adam 学习率 | ASPQN \(N_{sd},k_s\) | MSPQN \(N_{sd},k_s\) |
|---|---:|---:|---:|---:|---:|
| Burgers | 8 | 20 | \(5\times10^{-4}\) | 8, 50 | 8, 50 |
| Diffusion-advection | 10 | 50 | \(1\times10^{-4}\) | 10, 10 | 10, 10 |
| Klein–Gordon | 6 | 50 | \(1\times10^{-3}\) | 6, 50 | 6, 50 |
| Allen–Cahn | 6 | 64 | \(2.5\times10^{-4}\) | 6, 50 | 6, 50 |

## 4. 子网络数和局部迭代数敏感性

图 3–6 对四个基准分别扫描 \(k_s\in\{10,50,100\}\) 和三种层式分解：

1. 最小分解：2 个子网络；
2. 相邻两层组成一个子网络；
3. 最大层式分解：每层一个子网络。

得到的共同结论是：

- **ASPQN**：最大层式分解在四个问题上都持续给出更低的 \(E_{rel}\)，且这一趋势对 \(k_s\) 不敏感。作者将其归因于更充分的参数解耦，允许更局部的学习率和 Hessian 近似；最低误差通常出现在 \(k_s=50\) 或 \(100\)。
- **MSPQN**：增大子网络数和 \(k_s\) 通常减少达到相近精度所需的外层迭代数；按估算更新成本 \(UC\)，最大分解配合 \(k_s=50\) 或 \(100\) 表现最好。
- **梯度评估数**：MSPQN 中较少子域有时比最大分解更优或相当，因为 loss/梯度评估并不随局部参数数目线性缩放；全网络前向是重要成本。
- 这些图的均值来自 10 次独立运行。论文没有在正文表格中列出每条曲线的完整终点数字，因此本页不把曲线读数伪装成精确表格。

## 5. 与 Adam/L-BFGS 的比较

对照实验采用最大分解；通常 \(k_s=50\)，但 diffusion-advection 使用 \(k_s=10\)，因为该设置对该问题最好。正文报告：

- SPQN 得到的解更准确，\(E_{rel}\) 的差异平均约为一个数量级；
- diffusion-advection 上标准 L-BFGS 停滞，line search 给出很小步长，而 SPQN 只在训练初期的一个特定子网络上观察到很小步长，并能达到接近 \(10^{-2}\) 的 \(E_{rel}\)；
- SPQN 在梯度评估次数和估算 \(UC\) 上更高效，且 \(UC\) 与执行时间的排序较接近；
- Adam 在比较中没有达到 L-BFGS 所达到的低 \(E_{rel}\)，因此表 3 没有给出 Adam 的 time-to-solution；diffusion-advection 因 L-BFGS 停滞也不纳入该表。

## 6. 表 3：达到 L-BFGS 参考误差的时间

表 3 给出每个问题的 L-BFGS 最低平均误差，以及所有优化器达到该误差所需时间。时间单位为分钟；L-BFGS 和 MSPQN 使用单 GPU，ASPQN 使用括号中的多 GPU。

| 问题 | L-BFGS 最低平均 \(E_{rel}\) | L-BFGS | Adam | ASPQN | MSPQN |
|---|---:|---:|---:|---:|---:|
| Burgers | \(4.6\times10^{-4}\) | 558.5 | – | 14.4（8 GPU） | 40.7 |
| Klein–Gordon | \(6.1\times10^{-4}\) | 236.5 | – | 6.8（6 GPU） | 26.9 |
| Allen–Cahn | \(6.0\times10^{-4}\) | 1,001.6 | – | 79.2（6 GPU） | 117.5 |

由表中三行直接计算，ASPQN 的 L-BFGS 时间比约为 38.8、34.8、12.6 倍，平均约 28 倍；MSPQN 约为 13.7、8.8、8.5 倍，平均约 10 倍。论文的“约 28/10 倍”结论与这些表中数字一致，但 ASPQN 的速度提升是在增加 GPU 资源后取得的。

## 7. 结果的正确解读

1. ASPQN 的优势是**吞吐/墙钟时间 + 模型并行**的组合，不是固定 GPU 数下必然优于 MSPQN；论文明确指出，在固定资源量下 MSPQN 可以更高效。
2. MSPQN 的 sequential information transfer 可能减少外层迭代，但牺牲并行度；它适合单 GPU 或资源受限情形。
3. 误差提升包含优化器行为、硬边界、网络结构、配点和 line search 的共同作用，不能把全部收益归因于“Schwarz”三个字。
4. 论文没有把训练后一次前向评估的成本与 FEM/Newton 的在线迭代求解成本做成同一张基准表，因此不能把这些 speedup 解释成推理阶段无迭代求解的证明。

## 关联页面

- [[kopanicakova2024-dd-preconditioning-analysis]]
- [[kopanicakova2024-dd-preconditioning-method]]
- [[kopanicakova2024-dd-preconditioning-critical]]
- [[nonlinear-dd-preconditioning]]
- [[pinn]]
- [[neural-tangent-kernel]]

^[sources/papers/kopanicakova2024-dd-preconditioning]
