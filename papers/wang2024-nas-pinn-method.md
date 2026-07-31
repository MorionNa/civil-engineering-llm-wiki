---
id: papers--wang2024-nas-pinn-method
title: Wang & Zhong (2024) — NAS-PINN method
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/paper
- method/neural-architecture-search
- method/pinn
keywords:
- bi-level-optimization
- differentiable-nas
- neural-architecture-search
- pinn
sources:
- sources/papers/wang2024-nas-pinn.md
created: '2026-07-30'
updated: '2026-07-31'
confidence: high
---

# Method

## Architecture search

NAS-PINN 将 PINN 网络设计转化为连续优化问题。传统 NAS 的离散架构组合被 DARTS 风格连续松弛替代。论文指出，DARTS 的核心思想是将离散选择转化为可梯度优化的连续权重。

## Mask mechanism

由于不同神经元数量对应不同张量尺寸，论文通过 padding 与 zero-one mask 保持统一计算形式，使不同宽度网络可以在同一搜索空间优化。

## Bi-level optimization

- 内层：优化网络权重 θ
- 外层：优化架构参数 α

最终根据 α 解码得到离散网络结构。

## Search targets

搜索变量包括：

- hidden layer 数量
- 每层 neuron 数量
- residual/identity connection

方法流程见论文 Fig.3。

## Evidence By Source

### `sources/papers/wang2024-nas-pinn.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/wang2024-nas-pinn-source.md`

^[sources/papers/wang2024-nas-pinn.md]

## Related Indexes

- [[papers/index]]
- [[index]]
