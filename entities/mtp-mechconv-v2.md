---
id: entity--mtp-mechconv-v2
title: MTP-MechConv v2
type: entity
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-07-31'
updated: '2026-07-31'
confidence: low
legacy_tags:
- neural-operator
- message-passing
- structural-dynamics
- equation-of-motion
- spatial-partitioning
- hard-constraints
- hysteresis
legacy_sources:
- raw/papers/10_1016_j_cma_2024_117441.pdf
- raw/papers/10_1016_j_cma_2025_118476.pdf
- raw/papers/10_1016_j_cma_2024_117116.pdf
- raw/papers/arxiv_2202_03376.pdf
- raw/papers/10_1007_s10444_023_10065_9.pdf
---

# MTP-MechConv v2

## 定义
MTP-MechConv v2 是面向非线性结构动力响应的多层时间并行图物理算子草案。MTP 表示 multi-level temporal-parallel：时间上一次输出整段轨迹，空间上结合细图矩阵 MechConv、halo 子图和稀疏粗层通信。

## 模块
- 稳定因果时间算子与高频 residual；
- 矩阵边权细图 MechConv；
- 子结构粗图上下文；
- 可插拔 linear/bilinear/Bouc-Wen 本构；
- \(a=M^{-1}(F-Cv-f_\mathrm{int})\) 硬平衡层；
- direct-only 正式推理与可选失败保险分离。

## 状态
当前是等待反方 grill 和实验门槛冻结的候选，不是已证明的最终架构。任何“任意规模”“严格物理”“快于 Newmark”结论必须通过 [[mtp-mechconv-v2-evidence]] 中的独立测试。

## 关联
- [[mtp-mechconv-v2-evidence]]
- [[message-passing-reach-contract]]
- [[multilevel-fbpinn]]
- [[mp-pde]]

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.
