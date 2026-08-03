---
id: paper--list2025-unrolled-training-method
title: List et al. (2025) — 展开训练方法
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
- sequence-modeling
- time-marching
- autoregressive-rollout
- physics-simulation
legacy_sources:
- raw/papers/10_1016_j_cma_2024_117441.pdf
- raw/papers/extracted/10_1016_j_cma_2024_117441_extracted.txt
evidence_scope: local workspace source record pending canonical verification
---

# 展开训练：ONE、NOG 与 WIG

## 统一时间步
论文把一步模拟写成 \(u_{t+1}=g_\theta(u_t)\)。Prediction 中 \(g_\theta=f_\theta\)；correction 中 \(g_\theta\) 同时含数值求解器 \(S\) 与学习修正。两类任务使用相同网络族，避免把架构差异误判为训练差异。

## 三种梯度路径

| 变体 | 前向输入 | 时间梯度 | 主要作用 |
|---|---|---|---|
| ONE | 真值状态 | 一步 | 最便宜，但部署分布偏移最大 |
| NOG | 闭环预测状态 | 截断 | 暴露模型自身状态分布 |
| WIG | 闭环预测状态 | 全展开 | 同时利用状态分布与长程梯度 |

NOG 仍在每个展开位置对参数求梯度，只切断状态对前序状态的链式梯度；因此它不等同于完全停止学习。WIG 的 correction 需要数值求解器对输入状态可微。

## 训练稳定性
长展开对学习率和课程敏感。作者建议从较短展开开始逐步增加长度，并随梯度反馈幅值调整学习率。NOG 的前向成本随展开长度增长，但跨时间反向路径可被截断；WIG 必须保留完整链。

## 对本项目的迁移边界
[[unrolled-training]] 适合诊断自回归模型；整段时间并行模型没有逐步回灌同一种部署偏移。对后者可迁移的是“训练输入应覆盖部署状态分布”和“比较相同参数量”，而不是强制引入时间步求解器。

## 关联页面
- [[list2025-unrolled-training-analysis]]
- [[list2025-unrolled-training-results]]
- [[mp-pde]]

^[sources/papers/list2025-unrolled-training]
