---
id: paper--tesan2025-under-reaching-results
title: Tesan et al. (2025) — Under-reaching 实验结果
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/tesan2025-under-reaching
created: '2026-07-31'
updated: '2026-07-31'
confidence: low
legacy_tags:
- pde
- message-passing
- long-horizon-rollout
- limitation
legacy_sources:
- raw/papers/10_1016_j_cma_2025_118476.pdf
- raw/papers/extracted/10_1016_j_cma_2025_118476_extracted.txt
evidence_scope: local workspace source record pending canonical verification
---

# 结果与阈值证据

## 阈值

| 问题 | 理论下界示例 | 观察 |
|---|---:|---|
| 波动低/高分辨率 | 4 / 8 | 阈值以下不能稳定滚动，跨过后误差饱和 |
| 热扩散不同域长 | 10 / 20 | 达到全域覆盖后收益很小 |
| Poisson 不同分辨率 | 10 / 20 | 阈值前欠拟合，阈值后趋稳 |
| 弹塑性增量成形 | 15 | 15 跳优于 2/4 跳，过深略退化 |

## 计算与稳定性
消息成本随 \(M\) 近似线性增加。多个算例在下界附近达到最佳区间，继续增加迭代可能产生 over-smoothing，因此最优设计不是“越深越好”。

## 外推
双曲波的局部传播允许模型从 1×1 域外推到更长几何，只要每步消息仍领先波前。抛物/椭圆问题在新域超出原消息覆盖范围时失败，即使载荷形式更简单。

## 对任意规模声明的约束
仅在固定小图上做高 R² 不能证明任意规模。必须让图直径、分区、halo 和粗层路径同时变化，并检查核心节点与全图推理等价性。

## 关联页面
- [[tesan2025-under-reaching-analysis]]
- [[tesan2025-under-reaching-critical]]
- [[message-passing-reach-contract]]

^[sources/papers/tesan2025-under-reaching]
