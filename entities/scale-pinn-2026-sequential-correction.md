---
id: entity--scale-pinn-2026-sequential-correction
title: Scale-PINN：通过序贯校正学习高效 PINN
type: entity
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-02'
updated: '2026-08-02'
confidence: low
legacy_paper_id: arXiv:2602.19475
legacy_download_status: local_pdf_verified
legacy_manifest_status: absent_from_manifest
legacy_si_status: not_recorded
legacy_pdf_pages: 29
legacy_source_files:
- literature/github_20260802_next/PDFs/Scale-PINN_Learning_Efficient_Physics-Informed_Neural_Networks_Through_Sequential_Correction.pdf
legacy_source_urls:
- https://arxiv.org/abs/2602.19475
legacy_github_status: cloned_readme_and_data_only_no_python_source
legacy_github_sources:
- https://github.com/chiuph/SCALE-PINN
legacy_github_commit: 5ff8219d2604de8a57a5b7a9c7db9b435c5c3257
legacy_tags:
- pinn
- sequential-correction
- residual-learning
- optimization
- training-efficiency
---

# Scale-PINN：通过序贯校正学习高效 PINN

## 方法摘要

Scale-PINN 将数值求解器中的 iterative residual-correction principle 放入 PINN loss/训练策略，通过序贯校正改善 PDE PINN 的收敛速度。论文摘要报告在流体、空气动力学和城市科学问题上显著缩短训练时间，并保持较高精度。

## GitHub 证据边界

本轮从 `chiuph/SCALE-PINN` 浅克隆 commit `5ff8219d2604de8a57a5b7a9c7db9b435c5c3257` 成功；工作树干净，但该 commit 有 532 个文件、0 个 `.py` 文件，主要为 README 和数据文件。因此只能把论文摘要/README 作为可执行策略线索，不能声称已检查其训练实现或复现实验。

## 对当前 MechConv PINN 的可执行启示

1. 将训练拆成 proposal → residual target → correction target → hard-EOM audit 的序贯阶段；先让模型学会稳定低频/基线，再用高频和独立力残差 target 做后续校正。
2. 每一阶段都保留同一 constitutive plugin、matrix-edge MechConv 和硬 EOM，避免把“校正”实现成推理时的第二个求解器。
3. 把 residual correction 作为 curriculum/梯度预条件，而不是未经证明的第三个 forward correction head；这能吸收上一轮 A′ 速度通过但独立加速度/力仍失败的教训。

## 不能直接满足的要求

- 论文是通用 PDE PINN 训练策略，没有结构矩阵边、子图 halo、可替换本构或 `kx+cv+ma=F` 的直接证据。
- 序贯训练加速不等于推理加速，也不保证真实结构高频响应和跨本构泛化。
- 本轮仓库没有 Python 实现，不能从代码确认 residual target 的具体定义、数据泄漏风险或损失权重。

## 当前轮裁决

Scale-PINN 只进入**训练课程/残差监督设计候选**，不进入默认 inference graph。任何下一轮实现必须先过未来扰动因果、两次本构调用、独立力/加速度 RMS 和端到端速度门。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[entities/index]]
- [[index]]
