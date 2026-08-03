---
id: entity--physics-informed-multiple-input-operators-2025
title: PIMIONet：物理信息 Multiple-Input Operators 结构动力响应预测
type: entity
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-02'
updated: '2026-08-02'
confidence: low
legacy_paper_id: arXiv:2505.07090
legacy_download_status: local_pdf_verified
legacy_manifest_status: absent_from_manifest
legacy_si_status: not_recorded
legacy_pdf_pages: 50
legacy_source_files:
- literature/github_20260802_next/PDFs/Physics-informed_Multiple-Input_Operators_for_efficient_dynamic_response_prediction_of_structures.pdf
legacy_source_urls:
- https://arxiv.org/abs/2505.07090
legacy_github_status: related_structural_vibration_repository_checked
legacy_github_sources:
- https://github.com/ecker-lab/Learning_Vibrating_Plates
legacy_tags:
- operator-learning
- structural-dynamics
- multiple-input-operator
- temporal-query
- schur-complement
- equilibrium
---

# PIMIONet：物理信息 Multiple-Input Operators 结构动力响应预测

## 方法摘要

论文提出 MIONet，在 DeepONet 式结构中增加第二个 trunk 显式编码时间动态，使网络从移动荷载参数、速度、空间离散和时间输入连续映射到结构响应，而不是依赖固定时间步的 RNN rollout。物理信息训练使用预计算的质量、阻尼和刚度矩阵约束动态平衡；Schur complement 将训练域降到 reduced domain，再恢复全域响应。论文在梁和 KW-51 桥上报告 FEM 级响应、亚秒级预测和相对于 GRU-DeepONet 的时间连续性。

## 相关代码证据

`ecker-lab/Learning_Vibrating_Plates` 已浅克隆，commit `399f74a17a69fa4cfdc8b956703b91c603ff09a2`，README 与 `acousticnn` 目录均可检查。仓库是谐激励板频响 benchmark/Frequency-Query Operator 实现，包含约 12,000 个几何/材料/边界/荷载组合的数据说明；它不是论文中的矩阵边 MechConv，也不证明硬 EOM 或可替换非线性本构。

## 对当前 MechConv PINN 的可执行启示

1. 引入显式 time/frequency query 分支，把激励频率、相位、时间尺度和初始条件作为条件，而不是让主干从固定长度序列自行猜测；这有助于正常高频响应和连续时间查询。
2. Schur/reduced-domain 思想可转成训练期的 coarse graph/owned-node loss：先在可审计的 reduced graph 学习，再用矩阵边 MechConv 恢复全图，但必须验证 halo stitching 和全图 `r_F`。
3. 预计算的 `M,C,K` 只能作为线性基线或 conditioning；最终结构力必须仍由 edge constitutive plugin + MechConv 装配，才能支持换本构和非线性历史。

## 不能直接满足的要求

- 固定 M/C/K 的 equilibrium loss 不覆盖可替换 Bouc–Wen、双线性或大变形本构；它更接近线性结构响应 surrogate。
- reduced-domain 恢复不等于任意子图独立训练/推理等价，特别是边界历史状态和跨子图边力。
- 论文/仓库的 FEM-level 或亚秒级结果不能直接与当前 90 序列 forward、Newmark 或独立力 RMS 门一一比较。

## 当前轮裁决

PIMIONet 最值得借用的是**时间/频率条件编码和 reduced-domain 训练组织**，而不是替换 MechConv/EOM。它可作为下一轮 virtual broadband 数据接口的结构响应基线。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[entities/index]]
- [[index]]
