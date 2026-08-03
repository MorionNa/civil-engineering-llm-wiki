---
id: paper--gu2022-s4-results
title: Gu et al. (2022) S4 — 结果
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/gu2022-s4
created: '2026-08-01'
updated: '2026-08-01'
confidence: low
legacy_tags:
- sequence-modeling
- long-horizon-rollout
- parallel-computing
legacy_sources:
- raw/papers/arxiv_2111_00396v3.pdf
evidence_scope: local workspace source record pending canonical verification
---

# S4 结果证据

## 长序列

论文在 Long Range Arena 的 1K–16K 序列上报告全部任务当时最优，并完成其他方法未解决的 Path-X。该证据说明结构化 SSM 能学习长依赖，但任务主要是分类/序列建模，不是结构动力方程。^[raw/papers/arxiv_2111_00396v3.pdf]

## 效率

论文报告相对先前 LSSL 最多约 30× 加速和约 400× 内存降低；生成时切换递推视图，相对所用 Transformer 基线约 60×。这些数字依赖论文硬件、batch 和实现，不能直接作为 Newmark/RK4 对照。

## 迁移判定

S4 支持 V19 使用并行因果边历史头，但不能证明 4096 个真实结构频点求解的显存。项目自己的 V19 正式结果显示速度可达 39.55×，而峰值显存比 RK4 高 18.35×，见 [[mtp-mechconv-v2-v18-v19-negative-knowledge]]。

## 关联页面

- [[gu2022-s4-analysis]]
- [[gu2022-s4-critical]]
- [[structured-state-space-s4]]
