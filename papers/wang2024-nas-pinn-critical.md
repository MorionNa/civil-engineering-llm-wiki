---
title: "Wang & Zhong (2024) — NAS-PINN critical analysis"
created: 2026-07-30
updated: 2026-07-30
type: paper-analysis
tags: [pinn, neural-architecture-search, limitation, future-work]
sources: [raw/papers/wang2024-nas-pinn-source.md]
confidence: high
---

# Critical Analysis

## Limitations

- 架构搜索针对单个 PDE，跨问题泛化能力未验证；
- 搜索过程仍产生额外计算成本；
- 搜索空间决定可能发现的结构范围；
- 数据 availability 仅说明可请求获取。fileciteturn23file0L573-L579

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
