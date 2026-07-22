---
title: "Spectral Generator Neural Operator (SGNO)"
created: 2026-07-23
updated: 2026-07-23
type: entity
tags: [neural-operator, fourier-operator, time-marching, ai4s]
sources: [raw/papers/2602.18801v2.pdf]
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
