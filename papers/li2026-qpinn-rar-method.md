---
id: paper--li2026-qpinn-rar-method
title: "Li et al. (2026) — QPINN-RAR 方法机制"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/paper
keywords:
- residual-based-adaptive-refinement
- quantum-circuit
sources:
- sources/papers/li2026-qpinn-rar.md
created: '2026-08-06'
updated: '2026-08-06'
confidence: high
evidence_scope: full-text
---

# 方法机制

## 数据流

初始采样 → QPINN训练 → 候选点残差计算 → 选择高残差点 → 加入训练集 → 继续优化。

## RAR机制

候选点按照 PDE residual 排序，选取高残差区域增加collocation points。

## QPINN结构

经典输入通过参数化量子线路编码到高维Hilbert空间，并结合神经网络和物理损失训练。

## 损失函数

损失包含初值条件、边界条件和物理方程残差。

## 关联页面

- [[papers/li2026-qpinn-rar-analysis]]
- [[papers/li2026-qpinn-rar-results]]
- [[papers/li2026-qpinn-rar-critical]]
- [[entities/qpinn-rar]]
