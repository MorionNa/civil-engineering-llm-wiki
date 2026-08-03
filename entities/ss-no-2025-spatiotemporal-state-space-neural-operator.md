---
id: entity--ss-no-2025-spatiotemporal-state-space-neural-operator
title: SS-NO：融合记忆与空间的时空状态空间神经算子
type: entity
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-02'
updated: '2026-08-02'
confidence: low
legacy_paper_id: arXiv:2507.23428v5
legacy_publication: Transactions on Machine Learning Research, 03/2026
legacy_download_status: open_access_downloaded
legacy_si_status: not_found
legacy_source_files:
- papers/literature_20260802_next/ST_SSM_2025/manifest.json
- papers/literature_20260802_next/ST_SSM_2025/PDFs/Merging_Memory_and_Space_A_Spatiotemporal_State_Space_Neural_Operator.pdf
legacy_source_urls:
- https://arxiv.org/pdf/2507.23428v5
legacy_github_status: not_found_in_supplied_manifest
legacy_tags:
- neural-operator
- state-space-model
- long-memory
- frequency-modulation
- damping
- spatiotemporal
---

# SS-NO：融合记忆与空间的时空状态空间神经算子

## 基本信息

- **论文**：Merging Memory and Space: A State Space Neural Operator；PDF 首页简称为 State Space Neural Operator（SS-NO）。
- **作者**：Nodens F. Koren、Samuel Lanthaler；ETH Zürich、University of Vienna。
- **论文状态**：arXiv:2507.23428v5；PDF 首页标注发表于 Transactions on Machine Learning Research（03/2026）。目录名称保留下载任务的 `ST_SSM_2025`。
- **来源状态**：manifest 标记 `open_access_downloaded`；SI 请求状态为 `not_found`，且 manifest 说明直链未指向 supporting-information 页面。

## 摘要与核心机制（论文直接证据）

SS-NO 将 structured state-space model（SSM）扩展到联合时空域，用两个机制增强可控性：可学习阻尼用于局部化 receptive field，learnable frequency modulation 用于数据驱动选择频率。空间方向使用双向 SSM，时间方向使用一个带隐藏状态的 S4 memory 模块；输入历史被压缩为隐藏状态，再与空间处理结合预测未来轨迹（PDF pp.1、3–4）。

## 方法与公式（论文直接证据）

连续 SSM 写为

\[
\dot v(t)=Av(t)+Bu(t),\qquad y(t)=Cv(t)+Du(t),
\]

S4D 将 \(A\) 取为对角形式，以较低的计算/存储保留长程依赖；其离散卷积可由 FFT 并行计算（PDF p.3）。空间双向模块分别计算正向与反向 SSM，再将两路结果相加；二维网格沿各轴顺序处理，从而让每个位置获得 full field of view（PDF pp.3–4）。

作者将空间核写成带阻尼和频率的指数振荡形式：

\[
\kappa(x)=\sum_k c_k e^{-\rho_k|x|}e^{i\omega_kx},
\qquad \rho_k\ge 0.
\]

\(\rho_k\) 可以在近似全局卷积与局部 CNN 式卷积间调节，\(\omega_k\) 则自适应选择重要频率（PDF pp.5–6，Eq.4–5）。论文还给出 full field of view 是卷积神经算子普适性的充分条件，并指出单向扫描不满足该条件（PDF p.6，Theorem 4.1）。

## 实验与结果（论文直接证据）

- 1D KS 在 \(N=128\) 上，SS-NO 相对于次优 FFNO 的误差改善为：\(\nu=0.075\) 时 22%、\(\nu=0.1\) 时 42%、\(\nu=0.125\) 时 58%；在 \(N=32,256,512\) 上也保持较低误差（PDF pp.8–9）。论文使用相对 \(\ell_2\) 误差，不是 R²。
- 消融表显示，64-state 的全配置 KS 误差为 `0.0086/0.0026/0.0013`（三种黏性）；去掉 damping 和 frequency 后分别退化，低容量 16-state 时阻尼的重要性更明显（PDF p.9）。
- 2D 表 2 中，SS-NO 参数量为 `369,665`，在 TorusLi、TorusVis、TorusVisForce、CE-RM、GCE-RT 上的相对 \(\ell_2\) 误差分别为 `0.0345/0.0218/0.0263/0.0583/0.0138`；其参数量明显小于 2D FNO 的 `67,197,700`，但这不是结构动力学或 MechConv 的直接比较（PDF p.12）。
- 论文把所有主要基线都配上 MemNO 的 temporal S4（memory window=4）以隔离空间混合差异（PDF p.7 及 Appendix K）。这意味着结果不能简单归因于 SS-NO 单独提供了全部长记忆收益。

## 作者明确的局限（论文直接证据）

1. 自回归训练时梯度随状态维度和序列长度线性累积，超大 hidden state/长序列需要 truncated BPTT 或 gradient checkpointing（PDF p.38）。
2. 顺序扫描带有方向性归纳偏置，核心混合块不保证旋转/反射等变性；作者只讨论了对称嵌入或坐标变换的缓解（PDF p.38）。
3. 阻尼到不规则几何的系统性联系尚未建立；原生图/网格扫描和多物理扩展列为未来工作（PDF pp.13、38）。

## 面向本项目的推论（不是论文结论）

- **候选放置位置**：SSM 可作为 MechConv 前的时序记忆/频谱特征编码器，输入可以包含节点状态、外力、材料参数和本构历史摘要；最终边力仍由可替换本构插件和矩阵边权 MechConv 装配，避免 SSM 直接“生成不受约束的力”。
- **高频策略**：learnable frequency 与 adaptive damping 可作为正常结构高频的表示通道，但必须增加 Nyquist 附近频带、相位和加速度 R² 的独立审计；论文的 KS/流体相对 \(\ell_2\) 结果不能证明 `a` 通道高频闭合。
- **子图边界**：原论文针对规则网格/结构化扫描；若迁移到子图，必须为 owned nodes/halo 定义明确的扫描顺序或采用图原生 SSM。论文没有证明任意图划分下状态拼接等价。

## 证据边界

SS-NO 证明的是卷积神经算子的 full-field-of-view 普适性条件和若干 PDE benchmark 的误差/参数结果；没有报告 `kx+cv+ma=F`、可替换本构、MechConv 矩阵边权、子图训练等项目指标。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[entities/index]]
- [[index]]
