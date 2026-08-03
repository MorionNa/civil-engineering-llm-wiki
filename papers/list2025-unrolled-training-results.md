---
id: paper--list2025-unrolled-training-results
title: List et al. (2025) — 展开训练结果
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
- long-horizon-rollout
- autoregressive-rollout
- physics-simulation
legacy_sources:
- raw/papers/10_1016_j_cma_2024_117441.pdf
- raw/papers/extracted/10_1016_j_cma_2024_117441_extracted.txt
evidence_scope: local workspace source record pending canonical verification
---

# 结果与量化证据

## 准确率
- Correction：NOG 相对 ONE 平均降低 33% 误差；WIG 相对 ONE 平均改善 92%。
- Prediction：误差大致比对应 correction 高一个数量级；NOG 改善约 41%，WIG 在此基础上再改善约 30%。
- 网络规模通常主导准确率，因此架构比较必须固定参数量。

## 参数缩放
Correction 网络的推理误差随参数量经验上约按 \(n^{-1/3}\) 收敛；prediction 略差但相近。作者据此判断，单纯扩大网络不是与数值离散竞争的高效路线。

## 成本
以 1M 参数 KS 图模型为例，correction 训练约为 ONE 34 min、NOG 84 min、WIG 87 min；KOLM correction 的 NOG 10 h、WIG 16 h。三种训练方式部署时调用签名相同，但 correction 推理仍含数值求解器。

## 结论强度
跨多个系统、卷积/图架构和大量随机种子的一致趋势支持“闭环状态暴露有效”。但结果不支持“纯预测已优于 correction”或“网络规模扩展优于数值法”。

## 关联页面
- [[list2025-unrolled-training-analysis]]
- [[list2025-unrolled-training-critical]]
- [[unrolled-training]]

^[sources/papers/list2025-unrolled-training]
