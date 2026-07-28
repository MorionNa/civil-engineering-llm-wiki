---
title: "Functional Scaling Laws 结果：WSD 优势与 LLM loss 轨迹预测"
created: 2026-07-28
updated: 2026-07-28
type: paper-analysis
tags: [scaling-law, large-language-model, learning-rate-schedule]
sources: [raw/papers/li2025-functional-scaling-laws.pdf]
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
