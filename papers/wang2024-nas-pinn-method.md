---
title: "Wang & Zhong (2024) — NAS-PINN method"
created: 2026-07-30
updated: 2026-07-30
type: paper-analysis
tags: [pinn, neural-architecture-search, differentiable-nas, bi-level-optimization]
sources: [raw/papers/wang2024-nas-pinn-source.md]
confidence: high
---

# Method

## Architecture search

NAS-PINN 将 PINN 网络设计转化为连续优化问题。传统 NAS 的离散架构组合被 DARTS 风格连续松弛替代。论文指出，DARTS 的核心思想是将离散选择转化为可梯度优化的连续权重。fileciteturn23file0L77-L86

## Mask mechanism

由于不同神经元数量对应不同张量尺寸，论文通过 padding 与 zero-one mask 保持统一计算形式，使不同宽度网络可以在同一搜索空间优化。fileciteturn23file0L177-L181

## Bi-level optimization

- 内层：优化网络权重 θ
- 外层：优化架构参数 α

最终根据 α 解码得到离散网络结构。fileciteturn23file0L246-L250

## Search targets

搜索变量包括：

- hidden layer 数量
- 每层 neuron 数量
- residual/identity connection

方法流程见论文 Fig.3。fileciteturn23file0L227-L260
