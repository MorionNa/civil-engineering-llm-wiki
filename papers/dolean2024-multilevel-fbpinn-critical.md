---
id: paper--dolean2024-multilevel-fbpinn-critical
title: Dolean et al. (2024) — 多层 FBPINN 批判与图结构迁移
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/dolean2024-multilevel-fbpinn
created: '2026-07-31'
updated: '2026-07-31'
confidence: low
legacy_tags:
- limitation
- future-work
- spatial-partitioning
- spectral-bias
legacy_sources:
- raw/papers/10_1016_j_cma_2024_117116.pdf
- raw/papers/extracted/10_1016_j_cma_2024_117116_extracted.txt
evidence_scope: local workspace source record pending canonical verification
---

# 批判性分析

## 贡献
粗层改善大子域数下通信的证据扎实，并且作者区分了模型强/弱缩放。局部归一化、重叠组合和粗空间三者的职责清楚。

## Negative Knowledge
1. 多层 FBPINN 是坐标网络的加和，不自动保持结构图矩阵边作用。
2. 规则矩形、均匀复杂度和线性 PDE 不能代表任意拓扑/非线性本构。
3. 单 GPU 结果不能声称硬件可扩展。
4. 粗层可能平滑掉局部高频；必须保留细层直通路径。
5. 高波数 Helmholtz 仍难优化，说明粗层不是高频万能药。
6. 作者报告传统线性求解器通常仍更快。

## 对 MTP-MechConv v2 的硬约束
- 粗层只生成上下文或低频修正，不替代细层矩阵力计算。
- pooling/prolongation 必须对分区置换不敏感，并保持核心节点的局部平衡路径。
- 同一模型在不同分区、halo 宽度和粗图构造下做等价检查。
- 加入粗层后，高频 R² 不得低于无粗层基线超过 0.01，且大图误差/延迟必须改善。

## 不应照搬
不能直接在结构图上对不同子图输出做无约束求和；位移、速度、内力和本构状态具有不同拼接语义。核心节点单归属、halo 只作上下文，通常比平均所有重叠状态更安全。

## 关联页面
- [[dolean2024-multilevel-fbpinn-analysis]]
- [[multilevel-fbpinn]]
- [[message-passing-reach-contract]]

^[sources/papers/dolean2024-multilevel-fbpinn]
