---
id: papers--wang2024-nas-pinn-critical
title: Wang & Zhong (2024) — NAS-PINN critical analysis
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
- method/graph-neural-network
- method/neural-architecture-search
- method/pinn
keywords:
- future-work
- limitation
- neural-architecture-search
- pinn
sources:
- sources/papers/wang2024-nas-pinn.md
created: '2026-07-30'
updated: '2026-07-31'
confidence: high
---

# Critical Analysis

## Limitations

- 架构搜索针对单个 PDE，跨问题泛化能力未验证；
- 搜索过程仍产生额外计算成本；
- 搜索空间决定可能发现的结构范围；
- 数据 availability 仅说明可请求获取。

## Transfer to structural PINN

NAS-PINN 对你的非线性结构动力 PINN 研究具有直接启发：

1. 不应固定 MLP 深度和宽度；
2. 可以联合搜索物理约束网络结构；
3. 可以将结构拓扑、自由度图编码加入 NAS 搜索空间。

## Future opportunities

- NAS + RL loss weighting；
- NAS + adaptive sampling；
- graph neural architecture search for structural dynamics PINN。

## Related

- [[wang2024-nas-pinn-analysis]]
- [[kolzhetsov2026-rl-adaptive-loss-control-analysis]]
- [[rathore2024-pinn-loss-landscape-analysis]]

## Evidence By Source

### `sources/papers/wang2024-nas-pinn.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/wang2024-nas-pinn-source.md`

^[sources/papers/wang2024-nas-pinn.md]
