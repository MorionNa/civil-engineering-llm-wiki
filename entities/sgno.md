---
id: entities--sgno
title: Spectral Generator Neural Operator (SGNO)
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- entity/model
- method/neural-operator
keywords:
- ai4s
- domain/ai4s
- entity/model
- fourier-operator
- method/neural-operator
- neural-operator
- time-marching
sources:
- raw/papers/2602.18801v2.pdf
created: '2026-07-23'
updated: '2026-07-31'
confidence: high
---

# SGNO

## 定义

Spectral Generator Neural Operator 是一种面向长时 PDE 自回归预测的谱生成神经算子。其核心思想是将单步预测器设计为具有谱演化结构的更新，而不是完全黑箱映射。

## 核心机制

- 非正谱生成元控制 Fourier 模态增益；
- correction pathway 学习残余动力学；
- ETD-inspired 更新分离传播和修正。

## 关联

- [[li2026-sgno-analysis]]
- [[node-onet]]
- [[pgt]]
- [[seisgpt]]

## Evidence By Source

### `raw/papers/2602.18801v2.pdf`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/2602.18801v2.pdf]
