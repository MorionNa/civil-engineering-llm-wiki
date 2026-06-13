---
title: "HAT (Hardware-Aware Transformer)"
created: 2026-06-13
updated: 2026-06-13
type: entity
tags: [hardware-aware-nas, transformer, evolutionary-search, latency-prediction]
sources: [raw/papers/wang2020_hat.md]
---

# HAT (Hardware-Aware Transformer)

HAT 是首个面向 NLP Transformer 的硬件感知神经架构搜索（Hardware-Aware NAS）方法，通过 SuperTransformer + 延迟预测器 + 进化搜索，自动设计硬件最优 Transformer 架构。

## 关键信息
- **类型**: model
- **提出**: Hanrui Wang et al. (MIT), 2020
- **发表**: ACL 2020
- **核心贡献**: 首个 Hardware-Aware NAS for NLP Transformer，SuperTransformer 权重共享 + 硬件延迟预测器，搜索出远快于基线且精度不降的 Transformer

## 架构要点

- **SuperTransformer**: 训练一个包含所有候选架构的超网，通过权重共享实现 Amortized 搜索
- **设计空间**: 包含 self-attention 头数、FFN 中间维度、层数、embedding 维度等维度
- **延迟预测器（Latency Predictor）**: 训练一个轻量模型预测任意子架构在目标硬件上的延迟，无需逐一实测
- **进化搜索**: 在延迟约束下，进化算法在 SuperTransformer 子空间中搜索 Pareto 最优架构

## 关键结果

- 搜索到的 HAT 模型在多个硬件平台（Raspberry Pi、Intel Xeon、NVIDIA GPU）上比标准 Transformer 快 2-3×
- 精度优于或持平于同等延迟下的人工设计架构
- SuperTransformer 训练一次后可为任意硬件延迟约束快速搜索专用模型

## 关联页面
- [[wang2020-hat-analysis]] — 完整论文分析
- [[wang2020-hat-method]] — 方法机制
