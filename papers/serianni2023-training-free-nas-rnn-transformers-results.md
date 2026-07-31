---
id: papers--serianni2023-training-free-nas-rnn-transformers-results
title: 'Serianni & Kalita (2023) — Results: Training-free NAS for RNNs and Transformers'
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- evidence/paper
- method/neural-architecture-search
- method/transformer
keywords:
- flexibert
- kendall-tau
- nas-bench-nlp
- rnn
- spearman-rho
- training-free-nas
- transformer
sources:
- sources/papers/serianni2023-training-free-nas-rnn-transformers.md
created: '2026-06-14'
updated: '2026-07-31'
confidence: high
parent:
- - serianni2023-training-free-nas-rnn-transformers-analysis
---

# Results: Training-free NAS for RNNs and Transformers

## 1. RNN: NAS-Bench-NLP 实验结果

### 1.1 整体表现

在 NAS-Bench-NLP 的 8,795 个 RNN 架构上评估了所有训练-free 指标（排除了训练未完成或指标无法计算的架构）。

| 指标 | Kendall τ | Spearman ρ | 备注 |
|------|-----------|------------|------|
| **Hidden Covariance (ours)** | **0.37** | **0.53** | 第 1+2 层分别计算 |
| Jacobian Covariance | 0.28 | 0.42 | 现有最佳 CNN 指标 |
| Synaptic Saliency | ~0.15 | ~0.22 | |
| Activation Distance | ~0.05 | ~0.08 | |
| Synaptic Diversity | ~0.10 | ~0.15 | 原为 ViT 设计 |

### 1.2 关键发现

1. **所有 CNN 专用指标在 RNN 上失效**：最高 τ 仅 0.28（Jacobian Covariance），远低于其在 CNN 上的表现（τ ≈ 0.5–0.7）
2. **Hidden Covariance 的绝对优势**：τ = 0.37，比第二名高出 32%（相对提升）。该结果验证了 "RNN 隐藏状态是最富含架构质量信息的中间表示"这一假设
3. **按层分离计算优于全层求和**：对第 1 层和第 2 层分别计算 Hidden Covariance 并组合（取平均相对排名），效果优于所有层统一求和
4. **Hidden Covariance 在 RNN 低层最有效**：RNN 的前几层隐藏状态信息最丰富，高层隐藏状态趋于收敛

### 1.3 消融分析

- **初始化权重**：10 个不同随机种子下，Hidden Covariance 的方差很小，能稳定区分不同架构（好架构的分数持续高于差架构）
- **输入 minibatch**：10 个不同 minibatch 下，所有指标的方差极小 → 训练-free 指标捕捉的是架构内在属性而非输入依赖信号
- **参数量无相关性**：NAS-Bench-NLP 中参数数量与测试 loss 无相关性（与 Transformer 形成鲜明对比）

---

## 2. BERT: FlexiBERT Benchmark 实验结果

### 2.1 整体表现

在自建 BERT NAS Benchmark 的 500 个架构上评估。

| 指标 | Kendall τ (归一化) | Kendall τ (未归一化) | 备注 |
|------|--------------------|--------------------|------|
| **Attention Confidence** | **0.27** | **0.49** | 最佳指标 |
| Attention Importance | ~0.10 | ~0.35 | |
| Softmax Confidence | ~0.05 | ~0.30 | |
| Jacobian Covariance | ~0.05 | ~0.25 | 几乎无预测力 |
| Synaptic Saliency | ~0.00 | ~0.20 | |
| **参数量** | **0.44** | **0.44** | **最强 predictor！** |

### 2.2 关键发现

1. **参数量碾压一切**：τ = 0.44，远超所有归一化后的训练-free 指标。这是本文最颠覆性的结果——在一个设计良好的 Transformer 搜索空间里，你不需要任何复杂的训练-free 指标，"数参数"就是最好的 proxy

2. **归一化前指标的高 τ 是假象**：未归一化的 Attention Confidence (τ = 0.49) 看似好，但将指标值对参数量作图发现两者高度相关——**指标实际上在"偷看"参数量**。归一化后 τ 骤降至 0.27

3. **归一化后的困境**：去除参数量信号后，所有训练-free 指标几乎无剩余预测力。残差 τ ≈ 0.0–0.27，说明现有指标无法捕捉超越参数量的架构质量信号

4. **注意力机制指标 > 通用指标**：Attention Confidence 在归一化后仍保持微弱的正相关（τ = 0.27），暗示注意力结构信息确实包含一些独立于参数量的信号——但信号太弱，远不足以驱动可靠的搜索

### 2.3 消融分析

- **初始化权重**：BERT 指标对不同初始化种子的方差极小（< RNN 上的方差），模型的初始化鲁棒性更好
- **输入 minibatch**：类似 RNN，输入数据选择几乎不影响指标值
- **未归一化全指标矩阵**（附录 Figure 11）：所有指标在未归一化时都显示正相关，其中 Attention Confidence 最强——但都追踪的是参数量信号

---

## 3. 跨架构对比：为什么 RNN 和 Transformer 表现差异巨大

| 维度 | RNN (NAS-Bench-NLP) | Transformer (FlexiBERT) |
|------|---------------------|------------------------|
| 搜索空间拓扑 | Cell-based DAG | 线性堆叠 |
| 架构变体核心 | 操作 + 连接方式 | 层数 + 宽度 + 操作类型 |
| 参数量与性能 | **无相关** | **强相关** (τ = 0.44) |
| 最佳训练-free 指标 | Hidden Covariance (τ = 0.37) | Attention Confidence (τ = 0.27) |
| 训练-free 是否有效？ | 部分有效（有一定预测力） | 几乎无效（不如数参数） |

### 3.1 根因分析

- **Cell-based DAG 的拓扑丰富性**：NAS-Bench-NLP 中不同架构的差异主要来自 RNN cell 内部的连接方式（有向无环图），拓扑结构的变化对性能影响大，而参数量变化小
- **线性堆叠的维度单调性**：FlexiBERT 中架构变体主要来自层数、宽度、操作类型——这些变化几乎总是伴随着参数量的同向变化，导致参数量成为信息瓶颈
- **结论**：搜索空间的结构决定了训练-free 指标的天花板

---

## 4. 相关性与显著性

| 比较 | τ 值范围 | 解释 |
|------|---------|------|
| Hidden Covariance vs 随机 | 0.37 | 弱中等正相关，足以提供有用信号但不足以独立搜索 |
| Attention Confidence vs 随机 | 0.27 | 弱正相关，勉强显著 |
| 参数量 vs GLUE | 0.44 | 中等正相关，足够驱动简单搜索 |
| CNN 训练-free (NAS-Bench-201) | 0.5–0.7 | 参考值——RNN/Transformer 远低于 CNN |

---

## 关联页面

- [[serianni2023-training-free-nas-rnn-transformers-analysis]] — 论文分析总览
- [[serianni2023-training-free-nas-rnn-transformers-method]] — 方法细节
- [[serianni2023-training-free-nas-rnn-transformers-critical]] — 批判性分析
- [[entities/training-free-nas-transformers]] — 实体页
- [[entities/nasbench201]] — NAS-Bench-201（CNN 训练-free 参考基线）

## Evidence By Source

### `sources/papers/serianni2023-training-free-nas-rnn-transformers.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/training_free_nas2023.pdf`

^[sources/papers/serianni2023-training-free-nas-rnn-transformers.md]
