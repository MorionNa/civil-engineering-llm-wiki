---
id: paper--tesan2025-under-reaching-critical
title: Tesan et al. (2025) — Under-reaching 批判与结构动力迁移
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
- limitation
- future-work
- message-passing
- physics-simulation
legacy_sources:
- raw/papers/10_1016_j_cma_2025_118476.pdf
- raw/papers/extracted/10_1016_j_cma_2025_118476_extracted.txt
evidence_scope: local workspace source record pending canonical verification
---

# 批判性分析

## 贡献
最重要的贡献不是某个固定层数，而是可证伪的 reach contract：根据物理传播与图几何预先判定某个 GNN 是否必然欠感受野。

## Negative Knowledge
1. 方形均匀网格公式不能原样套到不规则结构图。
2. 抛物/椭圆“每步全域可见”是局部单尺度处理器假设；粗网格、谱算子和低秩全局通道可能改变路径长度。
3. 论文没有矩阵边权 MechConv、阻尼、Bouc-Wen 状态或动力平衡硬层。
4. 增量成形是准静态，不能证明高频结构动力收敛。
5. 更多消息可能 over-smoothing，且 \(O(M)\) 成本会破坏大图速度目标。

## 对本项目的判定规则
- 细层 halo 深度必须覆盖真实 MechConv receptive field，核心输出与全图输出最大绝对差小于数值容差。
- 大图全局效应通过显式粗层或边界摘要传递；粗层应做消融，不能把全图密集 attention 当作“可扩展”。
- 对 50/500/5000 DOF 分别测 wall time、显存和误差，报告随图直径的斜率。
- 高频集合按真实模态频带定义，不能用训练标签筛选。

## 不应照搬
不应把 \(M=L/\Delta x\) 直接变成上千层 MechConv；更合理的是细层满足局部传播下界，粗层承担跨分区通信，并用等价与误差试验证明两者分工。

## 关联页面
- [[tesan2025-under-reaching-analysis]]
- [[message-passing-reach-contract]]
- [[multilevel-fbpinn]]

^[sources/papers/tesan2025-under-reaching]
