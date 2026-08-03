---
id: paper--list2025-unrolled-training-critical
title: List et al. (2025) — 展开训练批判与迁移边界
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/list2025-unrolled-training
created: '2026-07-31'
updated: '2026-07-31'
confidence: low
legacy_tags:
- future-work
- limitation
- autoregressive-rollout
- physics-simulation
legacy_sources:
- raw/papers/10_1016_j_cma_2024_117441.pdf
- raw/papers/extracted/10_1016_j_cma_2024_117441_extracted.txt
evidence_scope: local workspace source record pending canonical verification
---

# 批判性分析

## 贡献
论文用受控实验把状态分布偏移和长程梯度分开，并说明不可微传统代码仍可参与训练期展开。大规模多种子实验比单一 PDE 的演示更能支持训练规律。

## Negative Knowledge
1. Correction 的高精度不能计入纯 E2E 模型成绩；其推理耗时由数值求解器主导。
2. Prediction 比 correction 差约一个数量级，说明纯网络的“方便”不能替代物理或数值先验。
3. \(n^{-1/3}\) 参数缩放提示盲目加宽成本高。
4. 研究对象主要是流体混沌系统；没有矩阵边权、滞回本构、阻尼或 halo stitching。
5. 自回归展开结论不自动适用于一次输出整段轨迹的时间并行算子。

## 对 MechConv-PINN 的可检验迁移
- 若模型是自回归：比较 ONE、2-step NOG、2-step WIG，保持参数和数据不变。
- 若模型是整段时间并行：比较教师真值、加入预测扰动的教师数据和轨迹级频谱监督；不引入部署时求解器。
- 主报告把 direct、optional refinement、solver correction 三类结果完全分栏。

## 不应照搬
不应因为 NOG correction 很强就把 Newmark 放入正式推理；这会改变用户要求的端到端问题。也不应在没有闭环分布偏移证据时付出长展开训练成本。

## 关联页面
- [[list2025-unrolled-training-analysis]]
- [[unrolled-training]]
- [[mp-pde]]

^[sources/papers/list2025-unrolled-training]
