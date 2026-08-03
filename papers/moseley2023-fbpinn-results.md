---
id: paper--moseley2023-fbpinn-results
title: Moseley et al. (2023) — FBPINN 结果
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/moseley2023-fbpinn
created: '2026-07-31'
updated: '2026-07-31'
confidence: low
legacy_tags:
- physics-informed
- pinn
- spectral-bias
- multi-scale-context
- limitation
legacy_sources:
- raw/papers/10_1007_s10444_023_10065_9.pdf
- raw/papers/extracted/10_1007_s10444_023_10065_9_extracted.txt
evidence_scope: local workspace source record pending canonical verification
---

# 结果证据

## 一维频率实验
- \(\omega=1\)：5 个子域的 FBPINN 与小 PINN 精度和数据效率相近。
- \(\omega=15\)：30 个子域、每个 2 层×16 单元，共 9630 参数；相比 5 层×128 的最佳 PINN，以少多个数量级的前向 FLOPs 达到更高精度。
- \(\omega=1+15\) 混频：深 PINN 可表示周期但误差约比 FBPINN 高两个数量级，且收敛更不稳定。

## 其他算例
二维高频问题使用 15×15=225 子域；时空波动方程使用 3×3×4=36 子域并采用 time-marching 调度。接口恰好落在解不连续处会增加困难，移动分区边界后改善。

## 成本事实
论文的波动方程上，PINN/单线程 FBPINN 单 GPU 训练约 10 h，而有限差分单 CPU 约 1 min。作者将多线程和训练解族视为未来达到竞争力的条件，不把当前结果描述为已经更快。

## 扩展性主张
局部网络固定时，理论计算随子域数线性增加，且仅重叠邻域需通信；但没有多 GPU 强缩放曲线，前向 FLOPs 也未包含梯度、通信和调度的全部成本。

## 关联页面
- [[moseley2023-fbpinn-analysis]]
- [[moseley2023-fbpinn-critical]]
- [[fbpinn]]

^[sources/papers/moseley2023-fbpinn]
