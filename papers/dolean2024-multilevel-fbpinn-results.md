---
id: paper--dolean2024-multilevel-fbpinn-results
title: Dolean et al. (2024) — 多层 FBPINN 结果
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
- spectral-bias
- multi-scale-context
legacy_sources:
- raw/papers/10_1016_j_cma_2024_117116.pdf
- raw/papers/extracted/10_1016_j_cma_2024_117116_extracted.txt
evidence_scope: local workspace source record pending canonical verification
---

# 结果与缩放证据

## 消融
- 增大重叠通常提高精度，但增加重复计算。
- 增大子域网络容量提高精度。
- 在简单 Laplace 问题上，单层 FBPINN 随子域数增加反而退化；多层模型因粗层全局通信保持更好精度。

## 强/弱缩放
强缩放固定问题复杂度并增加层数/子域/容量；弱缩放同步增加解频率复杂度和模型容量。多层 FBPINN 在多尺度 Laplace 和 Helmholtz 上总体保持比标准 PINN 更好的误差与训练成本。

## 高频对照
标准 PINN 和 SA-PINN 在部分高波数算例不能准确建模；Fourier 输入 PINN 可达到与多层 FBPINN 相近的精度，但训练时间约高一个数量级。高波数 Helmholtz 仍会先收敛到错误低频解，显示多层结构没有消除全部非凸优化困难。

## 扩展性边界
论文所有训练均在单 GPU 上。作者只证明模型容量意义的强/弱缩放，没有证明多 GPU wall-clock 线性缩放；10,000+ 子域仍是未来工作。

## 关联页面
- [[dolean2024-multilevel-fbpinn-analysis]]
- [[dolean2024-multilevel-fbpinn-critical]]
- [[multilevel-fbpinn]]

^[sources/papers/dolean2024-multilevel-fbpinn]
