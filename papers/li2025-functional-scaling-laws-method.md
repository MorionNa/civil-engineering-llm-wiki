---
id: papers--li2025-functional-scaling-laws-method
title: Functional Scaling Laws 方法：内禀时间、SDE 与遗忘核卷积
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- evidence/paper
keywords:
- intrinsic-time
- kernel-regression
- learning-rate-schedule
- scaling-law
- stochastic-gradient-descent
sources:
- sources/papers/li2025-functional-scaling-laws.md
created: '2026-07-28'
updated: '2026-07-31'
confidence: high
---

# Functional Scaling Laws 方法机制

## 1. Power-Law Kernel Regression

作者选择 PLK regression 作为可解析的大模型 scaling law 代理。模型由任务难度 $s$、容量指数 $\beta$、模型规模 $M$ 和标签噪声 $\sigma$ 控制。

## 2. SGD 到随机微分方程

离散 SGD 被连续化为 Ito 型 SDE。学习率计划同时影响漂移项和扩散项。

## 3. 内禀时间 (Intrinsic Time)

作者指出，当学习率变化时，iteration count 不能真实表示训练进度，因此定义：

$$t=\int_0^\tau \phi(r)dr$$

在内禀时间中，确定性优化过程与学习率引起的随机噪声效应被解耦。

## 4. Functional Scaling Law

FSL 将 loss 分解为：

- irreducible error：标签噪声导致的不可消除误差；
- approximation error：有限模型容量误差 $M^{-s\beta}$；
- signal learning：无噪声梯度下降学习速度；
- noise accumulation：学习率计划控制的噪声注入与遗忘。

核心结构为 Volterra 型积分：

$$\int_0^tK(t-z)[e(z)+\sigma^2]\gamma(z)dz$$

其中 $K$ 为 forgetting kernel。

## 5. 学习率计划分析

论文统一分析：

- constant LRS；
- exponential decay；
- warmup-stable-decay (WSD)。

并推导数据受限和计算受限下的最优缩放关系。

## 关联页面

- [[li2025-functional-scaling-laws-analysis]]
- [[li2025-functional-scaling-laws-results]]
- [[li2025-functional-scaling-laws-critical]]
- [[functional-scaling-law]]

## Evidence By Source

### `sources/papers/li2025-functional-scaling-laws.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/li2025-functional-scaling-laws.pdf`

^[sources/papers/li2025-functional-scaling-laws.md]
