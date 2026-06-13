---
title: "NAS-BERT"
created: 2026-06-13
updated: 2026-06-13
type: entity
tags: [neural-architecture-search, transformer, pruning-based-nas]
sources: [raw/papers/xu2021_nas_bert.md]
---

# NAS-BERT

NAS-BERT 是面向 BERT 模型压缩的神经架构搜索方法，通过 Block-Wise NAS + Progressive Shrinking 策略，自动搜索出 5M-60M 参数的任务无关轻量 BERT 变体。

## 关键信息
- **类型**: model
- **提出**: Jin Xu et al. (华为诺亚方舟实验室), 2021
- **发表**: KDD 2021
- **核心贡献**: 将 BERT 压缩建模为 NAS 问题，Block-wise 搜索 + Progressive Shrinking 训练，生成多尺度通用轻量模型

## 架构要点

- **Block-Wise NAS**: 逐块搜索，每层独立选择最优的 hidden size、FFN size、head 数等组合
- **Progressive Shrinking**: 从大超网逐步收缩到目标配置，避免直接训练小模型的精度损失
- **Task-Agnostic**: 搜索时使用 masked LM 目标，搜索结果不依赖下游任务
- **搜索空间**: 每层 hidden dim (128-768)、intermediate dim (512-3072)、attention heads (2-12)

## 关键结果

- NAS-BERT-5M 精度 88.9% (GLUE avg)，远超同等规模的 DistilBERT
- 5M-60M 参数范围内提供平滑的精度-效率 trade-off
- 搜索一次后得到的架构可直接用于多种下游任务、无需重新搜索

## 关联页面
- [[xu2021-nas-bert-analysis]] — 完整论文分析
