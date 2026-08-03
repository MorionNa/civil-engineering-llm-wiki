---
id: paper--tesan2025-under-reaching-method
title: Tesan et al. (2025) — 消息传播物理下界方法
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
- physics-simulation
- pde
- message-passing
- spatial-partitioning
legacy_sources:
- raw/papers/10_1016_j_cma_2025_118476.pdf
- raw/papers/extracted/10_1016_j_cma_2025_118476_extracted.txt
evidence_scope: local workspace source record pending canonical verification
---

# Under-reaching 的物理下界

## 双曲系统
对二维方格波动方程，CFL 要求物理波在一步内不越过离散格式可通信的范围。迁移到逐邻边消息后，论文要求

\[
M\Delta x>\sqrt{2}c\Delta t,\qquad
M>\left\lceil\sqrt{2}\frac{c\Delta t}{\Delta x}\right\rceil .
\]

这里 \(M\) 是每个时间步的消息迭代数。核心不是照抄 \(\sqrt2\)，而是“图消息覆盖距离 ≥ 一步物理影响距离”。

## 抛物与椭圆系统
在局部消息图、方形均匀域的设定下，论文假设单次推理需要全域信息，给出

\[
M=\frac{L}{\Delta x},
\]

即从一侧边界传播到另一侧的跳数。它是研究所用处理器的下界，不是所有神经算子的普适复杂度定理。

## 受控实验
处理器每次迭代共享参数，使改变 \(M\) 不改变可训练参数量。作者对多个随机种子测量多步 RRMSE，并比较理论阈值前后误差、稳定性和扩大几何外推。

## 对 halo 的解释
若细层 MechConv 有 \(B\) 个块，则核心节点的精确子图推理至少需要 \(B\) 跳 halo；若每块内部重复消息，则按实际 receptive field 计算。粗层路径可补全远距离上下文，但不能伪装成局部矩阵作用的逐边等价。

## 关联页面
- [[tesan2025-under-reaching-analysis]]
- [[message-passing-reach-contract]]
- [[multilevel-fbpinn]]

^[sources/papers/tesan2025-under-reaching]
