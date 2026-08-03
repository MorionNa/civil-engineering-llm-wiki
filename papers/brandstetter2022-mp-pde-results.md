---
id: paper--brandstetter2022-mp-pde-results
title: Brandstetter et al. (2022) — MP-PDE 结果
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/brandstetter2022-mp-pde
created: '2026-07-31'
updated: '2026-07-31'
confidence: low
legacy_tags:
- message-passing
- long-horizon-rollout
- pde
- limitation
legacy_sources:
- raw/papers/arxiv_2202_03376.pdf
- raw/papers/extracted/arxiv_2202_03376_extracted.txt
evidence_scope: local workspace source record pending canonical verification
---

# 结果证据

## 稳定性
在 1000 步长滚动中，pushforward 比无 pushforward 和高斯噪声训练有更高生存率；不切断前序梯度的变体也不占优。Temporal bundling + pushforward 还显著改善了 FNO 自回归基线。

## 方程与分辨率
在 Burgers/KdV/KS 混合参数族中，显式 PDE 参数使 MP-PDE 在未见参数组合上优于不含参数的消融。模型还测试了周期、Dirichlet、Neumann 边界和不规则网格。

## 报告速度
论文表 1 的 250 步任务中，MP-PDE 在 RTX 2080 Ti 上约 0.08–0.09 s；相应 WENO 实现约 1.7–4.8 s。表 2 对未优化 CPU 伪谱实现也显示优势。

## 速度证据边界
正文脚注明确说明后续加入的优化数值求解器可快多个数量级。因此这些数字只能证明该实现对照，不能证明 MP-PDE 普遍快于优化数值法。公平基准必须同硬件、同精度、含数据搬运和预热，并比较批量与单样本。

## 关联页面
- [[brandstetter2022-mp-pde-analysis]]
- [[brandstetter2022-mp-pde-critical]]
- [[mp-pde]]

^[sources/papers/brandstetter2022-mp-pde]
