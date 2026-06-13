---
title: "NAS-BERT 实验结果：GLUE · SQuAD · Ablation · Multi-Size 验证"
created: 2026-06-13
updated: 2026-06-13
type: paper-analysis
tags: [bert-compression, glu-e, squad, model-compression, neural-architecture-search]
sources: [raw/papers/xu2021_nas_bert.md]
confidence: high
---

# NAS-BERT 实验结果

> 父页面：[[xu2021-nas-bert-analysis]]

## 1. vs 手设计 BERT Baseline（Table 2）

NAS-BERT vs 同参数量的标准 Transformer 架构，在两个 setting 下评估：
- **PF**：纯预训练 + fine-tuning（无蒸馏）
- **KD**：两阶段知识蒸馏（预训练 + fine-tuning 均蒸馏）

### 60M 级别

| Setting | MNLI | QQP | QNLI | CoLA | SST-2 | STS-B | RTE | MRPC | AVG |
|---------|------|-----|------|------|-------|-------|-----|------|-----|
| BERT60+PF | 82.6 | 90.3 | 89.4 | 52.6 | 92.1 | 88.3 | 75.6 | 89.2 | 82.5 |
| NAS-BERT60+PF | 83.0 | 90.9 | 90.8 | 53.8 | 92.3 | 88.7 | 76.7 | 88.9 | **83.2** |
| BERT60+KD | 83.2 | 90.5 | 90.2 | 56.3 | 91.8 | 88.8 | 78.5 | 88.5 | 83.5 |
| NAS-BERT60+KD | 84.1 | 91.0 | 91.3 | 58.1 | 92.1 | 89.4 | 79.2 | 88.5 | **84.2** |

→ NAS-BERT60 在 PF 和 KD 设置下均优于手设计 BERT60。CoLA 尤其显著（+1.2~+1.8）。

### 30M / 10M / 5M 级别（AVG only）

| Model Size | BERT+PF | NAS-BERT+PF | BERT+KD | NAS-BERT+KD | Advantage |
|------------|---------|-------------|---------|-------------|-----------|
| 60M | 82.5 | 83.2 | 83.5 | **84.2** | +0.7 |
| 30M | 79.2 | **80.0** | 79.7 | **80.3** | +0.6 |
| 10M | 74.0 | **75.2** | 74.6 | **75.5** | +0.9 |
| 5M | 68.4 | **72.3** | 68.5 | **72.7** | +4.2 |

→ **模型越小，NAS-BERT 优势越大**。5M 级别 NAS-BERT 在 PF 下领先 BERT5 高达 +3.9%（72.3 vs 68.4）。说明手工设计的 Transformer 架构在极低参数量下严重欠拟合，而 NAS 搜索到的 SepConv 混合架构保持更好的表达能力。

### BERT baseline 配置

| Baseline | Layers L | Hidden H | Heads A |
|----------|----------|----------|---------|
| BERT60 | 10 | 512 | 8 |
| BERT30 | 6 | 512 | 8 |
| BERT10 | 6 | 256 | 4 |
| BERT5 | 6 | 128 | 2 |

## 2. vs 已有 BERT 压缩方法（Table 3）

### GLUE Dev Set（60M 级别，two-stage KD）

| Model | Params | MNLI | QQP | QNLI | CoLA | SST-2 | STS-B | RTE | MRPC | AVG |
|-------|--------|------|-----|------|------|-------|-------|-----|------|-----|
| Teacher (BERT-base) | 110M | 85.2 | 91.0 | 91.3 | 61.0 | 92.9 | 90.3 | 76.0 | 87.7 | 84.4 |
| DistilBERT | 66M | 82.2 | 88.5 | 89.2 | 51.3 | 91.3 | 86.9 | 59.9 | 87.5 | 79.6 |
| MiniLM | 66M | 84.0 | 91.0 | 91.0 | 49.2 | 92.0 | — | 71.5 | 88.4 | — |
| BERT-of-Theseus | 66M | 82.3 | 89.6 | 89.5 | 51.1 | 91.5 | 88.7 | 68.2 | — | — |
| PD-BERT | 66M | 82.5 | 90.7 | 89.4 | — | 91.1 | — | 66.7 | 84.9 | — |
| DynaBERT* | 60M | 84.2 | 91.2 | 91.5 | 56.8 | 92.7 | 89.2 | 72.2 | 84.1 | 82.7 |
| **NAS-BERT** | **60M** | **84.1** | **91.0** | **91.3** | **58.1** | **92.1** | **89.4** | **79.2** | **88.5** | **84.2** |
| NAS-BERT* | 60M | 84.8 | 91.2 | 91.9 | 58.7 | 93.1 | 89.9 | 79.8 | 88.9 | **84.8** |

> * 表示使用数据增强（同 DynaBERT/TinyBERT）

→ NAS-BERT 在没有数据增强的情况下已超越几乎所有 prior work（84.2 AVG，60M）。加数据增强达 84.8。**RTE 上 79.2 远超同类（DistilBERT 59.9, DynaBERT 72.2），CoLA 上 58.1 仅次于 teacher 61.0。**

### GLUE Test Set

| Model | Params | MNLI | QQP | QNLI | CoLA | SST-2 | STS-B | RTE | MRPC | AVG |
|-------|--------|------|-----|------|------|-------|-------|-----|------|-----|
| Teacher | 110M | 84.8 | 89.0 | 91.7 | 57.1 | 94.1 | 88.0 | 71.0 | 84.1 | 82.5 |
| TinyBERT* | 66M | 84.6 | 89.1 | 90.4 | 51.1 | 93.1 | 83.7 | 70.0 | 82.6 | 80.6 |
| NAS-BERT | 60M | 83.5 | 88.9 | 90.9 | 48.4 | 92.9 | 86.1 | 73.7 | 84.5 | 81.1 |
| NAS-BERT* | 60M | 84.1 | 88.8 | 91.2 | 50.5 | 92.6 | 86.9 | 72.7 | 86.4 | **81.7** |

→ NAS-BERT* 在 60M/66M 级别 test set 上达到 SOTA（81.7 AVG）。

## 3. 极小模型对比（Table 4）

NAS-BERT5 (5M) vs AdaBERT (6-10M) — 均不使用复杂蒸馏和数据增强：

| Setting | QNLI / Params | MRPC / Params | RTE / Params |
|---------|--------------|---------------|--------------|
| AdaBERT | 82.0 / 7.9M | 77.2 / 7.5M | 56.7 / 8.6M |
| NAS-BERT5 | **83.9 / 5.0M** | **80.0 / 5.0M** | **67.0 / 5.0M** |

→ NAS-BERT5 以**更小**的参数量全面超越 AdaBERT，RTE 上领先 +10.3%（绝对差）。

## 4. SQuAD 结果（Table 8）

| Model | Params | v1.1 EM | v1.1 F1 | v2.0 EM | v2.0 F1 |
|-------|--------|---------|---------|---------|---------|
| Teacher | 110M | 81.8 | 88.9 | 74.5 | 77.9 |
| DistilBERT | 66M | 79.1 | 86.9 | — | — |
| TinyBERT | 66M | 79.7 | 87.5 | 69.9 | 73.4 |
| MiniLM† | 66M | — | — | — | 76.4 |
| NAS-BERT | 60M | 80.5 | 88.0 | 73.2 | 76.3 |
| NAS-BERT† | 60M | **81.2** | **88.4** | **73.9** | **77.1** |

> † 表示用更大 batch (2048) 和更多 steps (200k) 训练以公平对比 MiniLM

→ NAS-BERT† 在 v1.1 F1=88.4, v2.0 F1=77.1，均达到 60M 级别 SOTA。

## 5. Ablation Studies

### Progressive Shrinking 效果（Table 5）

| Setting | AVG |
|---------|-----|
| w/o PS | 83.1 |
| w/ PS | **84.2** |

→ PS 带来 +1.1% AVG 提升。无 PS 搜索时间 50 小时，有 PS 仅需 5 分钟（评估时间）。

**Loss 曲线分析**（Fig. 3）：无 PS 的 supernet 收敛极慢，大量劣质架构分摊了训练资源。PS 将资源集中给有潜力架构 → 更快收敛 + 更准确评估。

### Pruning Architectures vs Pruning Operations（Table 6）

| Approach | AVG |
|----------|-----|
| PS-arch (prune architectures) | **84.2** |
| PS-op (prune operations/nodes) | 82.8 |

→ 剪枝完整架构路径优于剪枝单个操作节点，因为操作间的组合效果无法从单操作性能推断。

### 两阶段蒸馏 Ablation（Table 7）

| Setting | PD | FD | BERT60 AVG | NAS-BERT60 AVG |
|---------|----|----|-----------|---------------|
| Full KD | ✓ | ✓ | 83.5 | **84.2** |
| Pre-training only | ✓ | | 82.9 | **83.5** |
| Fine-tuning only | | ✓ | 82.6 | **83.1** |

→ (1) NAS-BERT 在所有蒸馏设置下均优于 BERT baseline；(2) 两阶段蒸馏均有增益；(3) **仅预训练蒸馏时（完全 task-agnostic），NAS-BERT60 仍达 83.5 AVG**，已超越 Table 3 中所有 prior work。

## 6. 多尺寸架构输出（Table 10）

NAS-BERT 可输出 5M–60M 以 5M 为间隔的 12 种架构，部分示例：

| Size | 操作序列（简化） |
|------|-----------------|
| 60M | E512→S3-512→M512→M512→S7-512→F512→...→F512 (24层) |
| 30M | E256→S3-512→M512→S5-512→S7-512→F512→...→S5-512 (21层) |
| 10M | E128→S3-384→S5-384→M384→S3-384→...→S3-384 (24层) |
| 5M | E64→S3-192→S7-192→M192→S7-192→...→S3-192 (13层) |

→ 大模型多用 MHA+FFN+少量 SepConv，小模型以 SepConv 为主。SepConv 在小尺寸下保持表达能力的关键操作。

## 关联页面

- [[xu2021-nas-bert-analysis]] — 全维度总览
- [[xu2021-nas-bert-method]] — 方法机制
- [[xu2021-nas-bert-critical]] — 贡献·局限·可迁移·机会
