---
title: "Moseley et al. (2023) — FBPINN：可扩展重叠域分解神经 PDE 求解器"
created: 2026-07-28
updated: 2026-07-28
type: paper-analysis
tags: [physics-informed, pinn, domain-decomposition, overlapping-domain-decomposition, fbpinn, pde, scientific-machine-learning]
sources: [raw/papers/moseley2023-fbpinn.pdf]
methods: [domain-decomposition, overlapping-domain-decomposition, hard-constraint-strategies, collocation-strategy]
results: [cross-domain-generalization, gpu-computing]
failure_modes: [architecture-mismatch-failure, physics-constraint-weight-tuning]
reproducibility: medium
code_url: ["论文给出实现说明；本次未独立运行"]
dataset_url: ["解析解与有限差分参考解"]
confidence: high
---

# FBPINN：有限基物理信息神经网络

> **论文：** Ben Moseley, Andrew Markham, Tarje Nissen-Meyer (2023), *Advances in Computational Mathematics* 49:62. DOI: 10.1007/s10444-023-10065-9
> **实体：** [[fbpinn]] · 上位范式：[[pinn]] · 方法展开：[[moseley2023-fbpinn-method]]

## 1. 工程与科学背景

标准 PINN 用一个全域网络满足微分方程残差。域变大、频率升高或解含多尺度时，谱偏置、参数规模和配点数量共同使优化迅速变难。论文以高频正弦问题展示：增加网络宽深仍可能收敛慢且不稳定。（原文 PDF pp. 5–7）

## 2. Research Gap

已有域分解 PINN 往往采用不重叠子域并显式加入界面连续/通量损失。论文希望得到一种本身连续、无需额外界面罚项、且局部网络可并行训练的架构。

## 3. 科学问题

能否把一个困难的全域 PINN 优化重写为多个较小、重叠且相互通信的局部优化，并通过局部坐标归一化降低每个网络看到的有效频率？

## 4. 研究目标

构造 FBPINN：重叠分区、每域局部网络、光滑窗函数、子域独立归一化、可选硬边界算子以及 active/fixed/inactive 训练调度。

## 5. 方法机制

全局近似为局部输出的窗函数加权和：`u_hat=C[Σ_i w_i·unnorm(NN_i(norm_i(x)))]`。窗函数使子网在域外近零，重叠区直接求和保证连续；训练时只在活动子域反传，固定邻域只贡献预测。→ [[moseley2023-fbpinn-method]]

## 6. 结果证据

高频和多尺度正弦问题上，FBPINN 测试误差约比所测 PINN 低近两个数量级；二阶 ODE 中 learning-outwards 调度显著优于 all-active；2+1D 波动问题最终精度相近，但 FBPINN 约用一半前向 FLOPs并更稳健地从初值向外学习。（PDF pp. 13–21）→ [[moseley2023-fbpinn-results]]

## 7. 贡献

1. 将局部神经网络解释为有限个紧支撑神经基函数。
2. 用 partition-of-unity 式窗求和避免额外界面损失。
3. 把局部归一化与训练调度纳入域分解，而不仅是计算并行。
4. 在 1D、2D 和 2+1D 多类方程上展示大域/高频收益。

## 8. 核心知识

FBPINN 的关键不是“网络更多”，而是每个局部网络面对更低频、更小范围的函数。域分解同时改变表示、尺度和信息传播路径。

## 9. Negative Knowledge

- 单线程 FBPINN 实测仍比对应 PINN 慢 2–10 倍；更少 FLOPs 不等于更短墙钟。
- 窗位置、重叠宽度、局部容量与训练调度均需逐题选择。
- 子域界面与 Burgers 间断重合时性能略差。
- 波动问题神经训练约 10 小时，而 FD 参考约 1 分钟。（PDF pp. 21–22）

## 10. 可迁移知识

局部窗求和适合需要连续拼接的神经场；learning-outwards 可迁移到时间推进和高阶边界传播；评价域分解模型应区分 FLOPs、墙钟、GPU 数、通信和传统法成本。

## 11. 边界与限制

验证主要是规则子域和合成 PDE；未证明复杂几何、高维采样、多 GPU 实际效率、逆问题或跨参数泛化。

## 12. 研究机会

将因果时间窗、粗层全局网络和自适应残差细化结合，用于非线性结构动力与局部屈服；详见 [[moseley2023-fbpinn-critical]]。

> 页面导航：[[moseley2023-fbpinn-method]] · [[moseley2023-fbpinn-results]] · [[moseley2023-fbpinn-critical]] · [[fbpinn]]
