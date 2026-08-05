---
id: entity--qpinn-rar
title: QPINN-RAR — Residual adaptive quantum physics-informed neural network
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- entity/model
- evidence/paper
keywords:
- quantum-pinn
- rar
- adaptive-sampling
sources:
- sources/papers/li2026-qpinn-rar.md
created: '2026-08-06'
updated: '2026-08-06'
confidence: high
---

# QPINN-RAR

## 定义

QPINN-RAR 是将 residual-based adaptive refinement 引入 quantum physics-informed neural network 的方法，用于求解偏微分方程。

## 核心机制

初始采样训练后，在候选点计算 PDE residual，将高残差区域加入训练集，再继续优化。QPINN 使用参数化量子线路进行特征映射，并通过物理损失约束方程、边界和初值条件。

## 证据边界

论文验证对象为 Burgers 方程、扩散方程和三维热方程。尚未验证工程结构动力学等复杂场景。

## 关联页面

- [[papers/li2026-qpinn-rar-analysis]]
- [[papers/li2026-qpinn-rar-method]]
- [[papers/li2026-qpinn-rar-results]]
- [[papers/li2026-qpinn-rar-critical]]
