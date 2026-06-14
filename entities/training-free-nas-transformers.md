---
title: "Training-free NAS for Transformers"
created: 2026-06-14
updated: 2026-06-14
type: entity
tags: [training-free-nas, transformer, rnn, nas-method, benchmark]
sources: [raw/papers/training_free_nas2023.pdf]
confidence: high
---

# Training-free NAS for RNNs and Transformers

> Serianni & Kalita (2023) — 首个系统性将训练零成本 NAS 范式拓展到 RNN 和 BERT Transformer 的工作，同时揭示了 Transformer 搜索空间制约训练-free 方法有效性的根本问题。

## 关键信息

| 项目 | 内容 |
|------|------|
| **全称** | Training-free Neural Architecture Search for RNNs and Transformers |
| **类型** | NAS methodology + Benchmark |
| **作者** | Aaron Serianni (Princeton), Jugal Kalita (UCCS) |
| **发表** | arXiv:2306.00288, 2023 (preprint) |
| **代码** | https://github.com/aaronserianni/training-free-nas |
| **许可证** | Apache 2.0 (code), CC BY 4.0 (benchmark data) |

## 核心贡献

### 1. Hidden Covariance — RNN 训练-free 指标
- 基于 RNN 隐藏状态协方差矩阵的 KL 散度
- NAS-Bench-NLP 上 Kendall τ = 0.37，超越所有现有通用指标
- 核心直觉：隐藏状态越多样化 → 区分输入的能力越强 → 训练效果越好

### 2. 注意力剪枝 → NAS 指标迁移
- 将 Voita et al. (2019)、Michel et al. (2019)、Behnke & Heafield (2020) 的注意力头剪枝分数改造为全网络 NAS 指标
- Attention Confidence / Softmax Confidence / Attention Importance

### 3. BERT NAS Benchmark
- FlexiBERT 搜索空间 + ELECTRA 预训练 + GLUE 评估
- 500 架构，~25 TPU-days
- 首个公开的 BERT 架构 NAS benchmark

### 4. 搜索空间的"参数量陷阱"发现
- Transformer 线性堆叠搜索空间中，参数量是性能的最佳预测器（τ = 0.44）
- 归一化后的训练-free 指标几乎无额外预测力
- 结论：训练-free NAS 必须与搜索空间协同设计

## 关键结果

| 场景 | 最佳指标 | Kendall τ |
|------|---------|-----------|
| RNN (NAS-Bench-NLP) | Hidden Covariance | 0.37 |
| BERT (FlexiBERT) | Attention Confidence (归一化) | 0.27 |
| BERT (FlexiBERT) | **参数量** (baseline) | **0.44** |

## 局限性

- BERT Benchmark 仅 500 架构，统计力有限
- 仅评估 encoder-only Transformer
- 仅英文数据集
- Hidden Covariance 的 τ = 0.37 尚未达到可独立驱动搜索的水平
- 未在 cell-based Transformer 搜索空间（如 Evolved Transformer/Primer）上验证

## 关联页面

- [[serianni2023-training-free-nas-rnn-transformers-analysis]] — 论文分析（12 维度）
- [[serianni2023-training-free-nas-rnn-transformers-method]] — 方法细节
- [[serianni2023-training-free-nas-rnn-transformers-results]] — 实验结果
- [[serianni2023-training-free-nas-rnn-transformers-critical]] — 批判性分析
- [[chen2021-tenas-analysis]] — TE-NAS（CNN 训练-free NAS，NTK + 线性区域）
- [[so2021-primer-analysis]] — Primer（cell-based Transformer 搜索空间，本文建议的未来方向）
- [[entities/nasbench201]] — NAS-Bench-201
- [[entities/te-nas]] — TE-NAS 实体
