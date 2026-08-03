---
id: comparison--cycle15_v27_cdno-d-evidence-20260803
title: Cycle 15：V27-CDNO-D Teacher-Compiled MechConv 证据卡
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 15：V27-CDNO-D Teacher-Compiled MechConv 证据卡

## 证据来源

- 当前最佳父模型：`outputs/remote_temporal_parallel_dynamicprojection75_selected_full_v2_20260731cm/selected_model.pt`。
- V21 顺序因果本构/硬 MechConv：物理 oracle 在 50DOF/1501 步上达到约 `0.9999` 的响应 R²，但顺序 rollout 不能直接作为快速部署模型。
- CDNO-D 本地 oracle：linear、bilinear、Bouc–Wen 均通过短轨迹因果隐式 BDF1/BDF2 收敛与残差检查；训练池 teacher 曾达到平均有效 force residual 约 `1.90e-9`，student 短前缀表达性 smoke 的损失下降 `74.48%`。
- 上一轮远程尝试没有开始训练，原因是配置把 teacher 数据文件 hash 当成 checkpoint hash；这属于流程失败，不是模型科学结果，仍必须重新通过本轮门。

## 文献迁移边界

离散多步 PINN 研究支持把已知离散动力学/本构结构直接嵌入学习流程，通常比让网络同时学习整个 RHS 更有利于稳定与精度：[Multistep and continuous PINN methods](https://www.pnnl.gov/publications/multistep-and-continuous-physics-informed-neural-network-methods-learning)。Nature Scientific Reports 的路径依赖材料工作把“未来输入不影响历史”和“不同时间离散得到一致状态”作为 surrogate 的独立要求：[Self-consistent recurrent neural network for path dependent deformation](https://www.nature.com/articles/s41598-026-49661-2)。这些证据支持 CDNO-D 的因果 teacher 与离散一致性门，但不能证明本项目的硬 EOM、可替换本构、非零 halo 或速度目标。

## 与 V25/V26 的差异

V25/V26 是父轨迹上的 post-hoc residual-to-correction；V26 真实留出 force RMS 从 `0.166289` 恶化到 `1.040846`，设计矩阵秩为 `3`、条件数约 `6.86e15`。V27 不学习一个病态残差读出，而是把物理一致的完整状态/力轨迹作为 teacher target，部署仍只用原有一次 forward 和 hard EOM。

## 现阶段裁决

V27 仅获得“允许无训练预检”的资格，未获得远程训练授权。必须重新验证 teacher provenance、student 表达性、真实高频/留出风险、跨本构和非零 halo；任何缺失都保持 V25 父模型为生产基线。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
