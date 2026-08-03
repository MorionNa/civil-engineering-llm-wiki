---
id: entity--fbpinn
title: Finite Basis Physics-Informed Neural Network (FBPINN)
type: entity
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-07-31'
updated: '2026-07-31'
confidence: low
legacy_tags:
- physics-informed
- pinn
- spatial-partitioning
- spectral-bias
- parallel-computing
legacy_sources:
- raw/papers/10_1007_s10444_023_10065_9.pdf
- raw/papers/10_1016_j_cma_2024_117116.pdf
---

# FBPINN

## 定义
FBPINN 用重叠子域上的局部神经网络和光滑窗函数构成全局 PINN 解；局部输入归一化缓解高频谱偏差，重叠区负责邻域通信。

## 演化
单层 FBPINN 适合局部化；[[multilevel-fbpinn]] 增加粗层，修复大量子域时的全局通信退化。

## 对图结构的边界
坐标窗求和不能直接等同于矩阵边 MechConv 或滞回状态拼接。图迁移应以核心节点单写出、halo 上下文和粗层通信为主，并验证全图等价。

## 关联
- [[moseley2023-fbpinn-analysis]]
- [[dolean2024-multilevel-fbpinn-analysis]]
- [[message-passing-reach-contract]]

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.
