---
id: papers--li2025-functional-scaling-laws-results
title: Functional Scaling Laws 结果：WSD 优势与 LLM loss 轨迹预测
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/llm
- evidence/paper
keywords:
- large-language-model
- learning-rate-schedule
- scaling-law
sources:
- sources/papers/li2025-functional-scaling-laws.md
created: '2026-07-28'
updated: '2026-07-31'
confidence: high
---

# Functional Scaling Laws 结果

## 1. SGD 轨迹验证

FSL 能够准确拟合不同 learning rate schedule 下的 SGD risk trajectory，包括 cosine、WSD-like 和 cyclic schedule。

## 2. Scaling law 结论

论文推导得到：

- WSD scaling efficiency 最优；
- exponential decay 次之；
- constant learning rate 最差。

## 3. LLM 实验

在 0.1B–1B 参数规模 LLM 上：

- 使用 8-1-1 schedule 的 loss 曲线拟合 FSL；
- 用拟合结果预测 cosine 和 WSD 曲线；
- FSL-optimal LRS 呈 WSD-like 形态，并取得更低最终 loss。

## 4. 核心观察

训练曲线本身包含学习率计划、模型容量和噪声遗忘的信息，可以作为设计训练策略的 surrogate model。

## 关联页面

- [[li2025-functional-scaling-laws-analysis]]
- [[li2025-functional-scaling-laws-method]]
- [[li2025-functional-scaling-laws-critical]]

## Evidence By Source

### `sources/papers/li2025-functional-scaling-laws.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/li2025-functional-scaling-laws.pdf`

^[sources/papers/li2025-functional-scaling-laws.md]
