---
id: paper--dolean2024-multilevel-fbpinn-method
title: Dolean et al. (2024) — 多层 FBPINN 方法
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
- physics-informed
- pinn
- spatial-partitioning
- multi-scale-context
- hard-constraints
legacy_sources:
- raw/papers/10_1016_j_cma_2024_117116.pdf
- raw/papers/extracted/10_1016_j_cma_2024_117116_extracted.txt
evidence_scope: local workspace source record pending canonical verification
---

# 多层解表示

## 层级结构
第 \(l\) 层使用 \(J^{(l)}\) 个重叠子域。论文默认指数层级 \(J^{(l)}=2^{d(l-1)}\)，因此少量层即可覆盖从全局到细尺度的频率范围；每个子域网络输入独立归一化到 \([-1,1]\)。

## 组合
各局部输出乘光滑窗函数，再在同层子域和不同层之间求和。重叠窗构成连续的全局表示，硬边界约束算子可直接作用在组合结果上，无需额外接口损失。

## 粗层作用
单层方法的信息只通过重叠区传播，子域增多时收敛恶化。最粗层通常含全局子域，提供直接远距离路径；细层负责局部复杂度。论文没有声称默认指数层级对所有几何最优。

## 复杂度主张
若每个采样点只落入平均 \(C\) 个子域，单局部网络求值成本为 \(\tilde S\)，则解评估可写为 \(O(NC\tilde S)\)，不直接依赖全部子域数。但跨层重叠会增加通信常数。

## 图结构迁移
对 [[message-passing-reach-contract]]，可把层级改写为：
1. 细图保持矩阵边 MechConv；
2. 子结构 pooling 生成粗节点；
3. 粗边聚合跨区耦合；
4. prolongation 把全局上下文送回核心节点；
5. halo 只为细层精确感受野服务。

## 关联页面
- [[dolean2024-multilevel-fbpinn-analysis]]
- [[dolean2024-multilevel-fbpinn-results]]
- [[multilevel-fbpinn]]

^[sources/papers/dolean2024-multilevel-fbpinn]
