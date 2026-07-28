---
title: "Functional Scaling Laws 批判分析：贡献、限制与迁移机会"
created: 2026-07-28
updated: 2026-07-28
type: paper-analysis
tags: [scaling-law, limitation, future-work, transfer-learning]
sources: [raw/papers/li2025-functional-scaling-laws.pdf]
confidence: high
---

# Functional Scaling Laws Critical

## 主要贡献

1. 从最终 loss scaling law 扩展到完整训练轨迹。
2. 提出 intrinsic time 描述不同学习率计划下的有效训练进度。
3. 用 forgetting kernel 解释学习率衰减和噪声遗忘。

## Negative Knowledge

- 理论对象是 power-law kernel regression，而非完整 Transformer 非凸训练。
- 主要结论是渐近缩放关系，有限规模下常数项可能影响实际效果。
- LLM 验证规模为 0.1B–1B，不能直接证明超大模型规律。
- 未公开代码和数据，未报告完整计算资源。

## 可迁移方向

- 将轨迹级 surrogate 用于 PINN、神经算子和结构响应模型训练调度。
- 分析物理损失、多任务损失的学习与遗忘时间尺度。
- 设计 warmup/stable/decay 式物理模型训练策略。

## 关联页面

- [[li2025-functional-scaling-laws-analysis]]
- [[functional-scaling-law]]
