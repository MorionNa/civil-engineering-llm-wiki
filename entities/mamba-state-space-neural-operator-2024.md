---
id: entity--mamba-state-space-neural-operator-2024
title: Mamba 状态空间神经算子：动力系统长记忆与线性成本
type: entity
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-02'
updated: '2026-08-02'
confidence: low
legacy_paper_id: arXiv:2409.03231v2
legacy_download_status: open_access_downloaded
legacy_si_status: not_found
legacy_source_files:
- papers/literature_20260802_next/State_Space_Neural_Operator_2024/manifest.json
- papers/literature_20260802_next/State_Space_Neural_Operator_2024/PDFs/State-space_models_are_accurate_and_efficient_neural_operators_for_dynamical_systems.pdf
legacy_source_urls:
- https://arxiv.org/pdf/2409.03231v2
legacy_github_url: https://github.com/zheyuanhu01/State_Space_Model_Neural_Operator
legacy_github_clone_status: failed_connection_timeout_or_reset
legacy_tags:
- mamba
- state-space-model
- neural-operator
- long-time-integration
- extrapolation
- physics-informed
---

# Mamba 状态空间神经算子：动力系统长记忆与线性成本

## 基本信息

- **论文**：State-space models are accurate and efficient neural operators for dynamical systems
- **作者**：Zheyuan Hu、Nazanin Ahmadi Daryakenari、Qianli Shen、Kenji Kawaguchi、George Em Karniadakis。
- **定位**：状态空间/Mamba 动力系统算子学习方法论文；arXiv:2409.03231v2。论文正文称代码将在接收后提供。
- **代码状态**：网页仓库为 `https://github.com/zheyuanhu01/State_Space_Model_Neural_Operator`；本轮 clone 连接超时/重置，未拉取代码，不能声称代码已获取。
- **来源状态**：manifest 标记 `open_access_downloaded`；SI 请求状态为 `not_found`。

## 摘要与方法（论文直接证据）

论文使用 Mamba 作为动力系统的序列到序列神经算子，重点处理长时间积分、长程依赖、混沌、刚性解和分布外外推。Mamba 在 SSM 递推上加入输入选择机制，并通过重参数化兼顾长程建模与并行训练；论文与 RNN、Transformer、DeepONet、FNO、LNO、Oformer、GNOT 等 11 个基线比较（PDF pp.1–2）。

离散 SSM 的基本递推为

\[
h_t=\bar A h_{t-1}+\bar Bx_t,\qquad y_t=Ch_t,
\]

其中 \(\bar A,\bar B\) 由连续系统矩阵和步长离散化得到；同一递推可改写为因果卷积并用 FFT 并行训练（PDF p.6，Eq.2–3）。Mamba block 由线性投影、1D convolution、非线性、SSM 分支和带门控/跳连分支组成（PDF p.5）。

## 实验与关键结果（论文直接证据）

- 实验在 80 GB A100 上进行，涵盖 1D 动力系统、有限正则/不连续解、OOD、长时间积分、长时间外推、混沌 Lorenz 和 PK/PD 真实应用（PDF pp.2–3）。
- 10K 参数量级的基础任务中，Mamba 在反导数、非线性 ODE、重力摆的 MSE 分别为 `3.333e-9`、`4.351e-8`、`1.301e-9`，优于表 2 的大多数对比模型；Mamba 训练约 35 min，显存约 1,425 MiB（PDF p.8）。这些结果是 ODE/序列 benchmark，不是结构动力学证明。
- 长时间摆实验将序列长度从 2,048 扩展到 32,768（终止时间约 20.48 到 327.68）。表 6 中 Mamba 训练时间从 11 min 增至 115 min，显存从 1,751 MiB 增至 5,187 MiB；标准 Transformer 在长度 8,192 以上超过 80 GB，无法继续（PDF pp.16–17）。
- 在阻尼摆上，长度 32,768 时 Mamba 的相对 L2 误差约为 `3.461e-2`、`4.992e-3`、`2.030e-3`（阻尼 `c=0.1/0.3/0.5`，PDF p.18）。在无阻尼或高频/混沌测试中，论文指出 LNO 有时优于 Mamba，且 Mamba 误差会随时间增长（PDF p.15）。
- PK/PD 的有限标注实验中，单独 physics loss 的误差约 `8.791e-1`，data+physics hybrid 降到 `1.872e-2`；这说明物理项不能自动替代数据锚定（PDF p.30）。

## 作者的局限与未来方向（论文直接证据）

论文总结指出当前工作主要覆盖 ODE/动力系统，未来拟扩展到 PDE，并将 Mamba 与 DeepONet 或 U-Net 的空间表示结合（PDF p.31）。其长序列的线性成本仍随序列长度增长；现有结果也显示在无阻尼、混沌、高频瞬态上并非所有设置都稳定（PDF pp.15–18）。

## 面向本项目的推论（不是论文结论）

- **可复用点**：在当前 MechConv 框架中，Mamba/SSM 更适合作为 causal history encoder，记忆外力、节点状态和本构内部变量的长程影响；输出再进入可替换本构插件，力仍由矩阵边权 MechConv 与节点装配计算。
- **高频风险**：论文自身的高频/无阻尼案例并非总胜出，因此不能直接把 Mamba 当作高频保证。候选实验必须同时看 `u/v/a/edge_force` 四通道、高频频带和相位漂移。
- **物理闭合边界**：Mamba 的序列输出不自动满足 `kx+cv+ma=F`；若用它直接输出加速度或力，仍可能复现本项目此前独立加速度/力误差偏高的问题。物理闭合必须留在 MechConv/EOM 构造中。

## 证据边界

论文报告的是 ODE/PK-PD 等序列的 MSE 或相对 L2、训练成本和长序列扩展；没有报告结构动力学四通道 R²、独立力平衡、矩阵边权或子图拼接等项目要求。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[entities/index]]
- [[index]]
