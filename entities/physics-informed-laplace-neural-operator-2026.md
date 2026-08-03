---
id: entity--physics-informed-laplace-neural-operator-2026
title: PILNO：物理信息 Laplace 神经算子
type: entity
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-02'
updated: '2026-08-02'
confidence: low
legacy_paper_id: arXiv:2602.12706
legacy_download_status: local_pdf_verified
legacy_manifest_status: absent_from_manifest
legacy_si_status: not_recorded
legacy_pdf_pages: 38
legacy_source_files:
- literature/github_20260802_next/PDFs/Physics-Informed_Laplace_Neural_Operator_for_Solving_Partial_Differential_Equations.pdf
legacy_source_urls:
- https://arxiv.org/abs/2602.12706
legacy_github_status: related_LNO_repository_checked
legacy_github_sources:
- https://github.com/qianyingcao/Laplace-Neural-Operator
legacy_tags:
- neural-operator
- laplace-operator
- pole-residue
- causal-weighting
- broadband
- high-frequency
---

# PILNO：物理信息 Laplace 神经算子

## 基本信息与证据

- **论文**：Physics-Informed Laplace Neural Operator for Solving Partial Differential Equations；arXiv:2602.12706；本地 PDF 38 页。
- **本地证据**：标题和摘要可提取，PDF 签名有效；SHA-256 为 `870c6bc46e3a78a70e63b61a3af0dd9b0c7422d8eba6a6b67b07e2b4ef0eb5e4`。
- **相关代码**：`qianyingcao/Laplace-Neural-Operator` 已浅克隆到本轮目录，commit `78c64ef7edc47f343352251d15f7d1341e6732ba`。README 与 1D ODE/PDE 示例显示显式 pole-residue 层；该仓库不是 PILNO 论文的结构 MechConv 实现。

## 方法摘要

PILNO 在 Advanced LNO（ALNO）上加入 PDE、边界和初始条件残差。ALNO 保留 pole-residue 的瞬态表示，并用 FNO 风格 Fourier multiplier 替换稳态分支。论文的两个关键训练机制是：

- **virtual inputs**：生成覆盖宽频谱的无标签输入函数，用 physics-only residual 监督补充稀疏标注和 OOD 频段；
- **temporal-causality weighting**：对时间残差衰减加权，优先稳定早期瞬态，再逐步关注后续时间。

论文在 Burgers、Darcy、reaction–diffusion 和 forced KdV 上报告小数据与 OOD 泛化改善。

## 对当前方案的可执行启示

1. 为结构动力学训练集加入因果的 virtual broadband excitation：低频、正常结构高频、随机相位、初始位移/速度组合必须分层采样；virtual input 只用于训练，不可成为测试泄漏。
2. 对 `r_F`、速度-位移一致性和加速度误差使用时间/频带权重；早期瞬态、共振峰和高频相位应分别审计，不能只优化 pooled R²。
3. 可把 pole-residue/稳定 causal SSM 作为历史特征编码器，但它只生成 latent history；矩阵边 MechConv 仍负责边力装配，constitutive plugin 仍负责本构状态，硬 EOM 仍负责 `a`。

## 不能直接满足的要求

- PILNO/LNO 面向规则时空场或 PDE operator，不提供矩阵边权、halo/owned-node 子图拼接和任意结构本构接口。
- Fourier/Laplace 频域表示不能自动保证时间因果；直接复用非因果 FFT 层会污染本轮的未来扰动因果 gate。
- PDE residual training 并不等于一次输出严格满足 `kx+cv+ma=F`；必须在 MechConv forward 内重新计算边力和 EOM。

## 当前轮裁决

PILNO 对当前高频/长记忆失败是**训练分布与权重设计启发**，不是可直接替换的主干。下一轮若使用，应固定 causal 版本、virtual broadband 清单和频带指标，并把独立加速度/力 RMS 作为硬门。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[entities/index]]
- [[index]]
