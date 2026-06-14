---
title: "DARTSformer 实验结果：WMT'14 En-De / En-Fr · WMT'18 En-Cs · Ablation"
created: 2026-06-14
updated: 2026-06-14
type: paper-analysis
tags: [machine-translation, wmt14, bleu, neural-architecture-search, transformer]
sources: [raw/papers/memory_efficient_dnas2021.pdf]
confidence: high
---

# DARTSformer 实验结果

> 父页面：[[zhao2021-memory-efficient-dnas-analysis]]

## 1. 搜索配置对比 — WMT'14 En-De Test (Table 1)

| Model | Pooling | Search s | Params | BLEU |
|-------|---------|----------|--------|------|
| Transformer (base) | — | — | 61.1M | 27.7 |
| Evolved Transformer (ET) | — | — | 64.1M | 28.2 |
| Sampling (baseline) | max | 2 | 60.1M | 18.7 |
| Sampling (baseline) | avg | 2 | 61.6M | 16.8 |
| **DARTSformer** | **max** | **1** | **64.5M** | **27.9** |
| **DARTSformer** | **max** | **2** | **65.2M** | **28.4** |
| DARTSformer | avg | 1 | 66.0M | 28.3 |
| DARTSformer | avg | 2 | 63.4M | 28.3 |

**关键发现**：
- DARTSformer 在所有搜索配置下均优于标准 Transformer (+0.2~+0.7 BLEU)
- 最佳配置：max pooling + s=2 (search 2 consecutive layers)，BLEU 28.4
- **Sampling-based NAS 严重退化**（BLEU 16.8-18.7），倾向于大 kernel 卷积 → 重复生成
- DARTSformer 在 3/4 次实验中超越 Evolved Transformer（28.4 vs 28.2）

## 2. Split 数量消融 — WMT'14 En-De (Table 2)

| Pooling | Encoder split | Decoder split | BLEU |
|---------|--------------|---------------|------|
| max | 2 | 3 | **28.4** |
| max | 3 | 4 | 28.0 |
| max | 4 | 5 | 27.4 |
| avg | 2 | 3 | **28.3** |
| avg | 3 | 4 | 27.9 |
| avg | 4 | 5 | 27.1 |

**关键发现**：
- 最小 split (2/3) 性能最优，增大 split 单调退化
- 原因：(1) 搜索空间过大导致难以收敛 (2) 递归计算增加使训练/推理变慢
- max pooling 在 split 数增加时退化更快（28.4→27.4 vs 28.3→27.1）

## 3. 搜索成本对比 (Table 3)

| 方法 | 价格 | 参数更新步数 | 硬件 |
|------|------|------------|------|
| **DARTSformer** | **~$1,250** | **4.8×10⁵** | **8×V100** |
| Evolved Transformer (ET) | ~$150,000 | 4.2×10⁸ | 200 TPU v2 |

- DARTSformer 搜索成本约为 ET 的 **1/120**
- 参数更新步数少 **874 倍**
- 硬件需求从 200 TPU 降至 8 V100 — 学术可用
- 搜索时间约 40 小时（AWS p3dn.24xlarge）

## 4. 跨数据集泛化 — Base Model (Table 4a)

| Model | WMT'14 En-De | WMT'14 En-Fr | WMT'18 En-Cs |
|-------|-------------|-------------|-------------|
| Transformer (base) | 27.7 | 40.0 | 27.0 |
| Evolved Transformer | 28.2 | 40.6 | 27.6 |
| **DARTSformer** | **28.4** (+0.7) | **40.1** (+0.1) | **27.9** (+0.9) |

**关键发现**：
- 仅用 En-De 搜索的架构在所有数据集上均有效
- **En-Cs 上增益最大 (+0.9)**，尽管 En-Cs 不是搜索数据集 → 证明架构迁移能力
- En-Fr 上略逊于 ET (40.1 vs 40.6)，但 ET 可能直接在 En-Fr 上搜索/调优
- Base model 下 DARTSformer (65.2M) 达到原 big Transformer (28.4 BLEU, 210M) 的性能，**节省 69% 参数**

## 5. 跨数据集泛化 — Big Model (Table 4b)

| Model | WMT'14 En-De | WMT'14 En-Fr | WMT'18 En-Cs |
|-------|-------------|-------------|-------------|
| Transformer (big) | 29.1 | 41.2 | 28.1 |
| Evolved Transformer (big) | 29.3 | 41.3 | 28.2 |
| **DARTSformer (big)** | **29.8** (+0.7) | **41.3** (= ET) | **28.5** (+0.4) |

**关键发现**：
- Big model (e=512, d=1824) 下 DARTSformer 全面超越标准 Transformer 和 ET
- En-De 29.8 BLEU 是当时所有方法中的 SOTA
- Big model 训练配置：dropout 0.3，learning rate 1×10⁻³，gradient accumulation ×2

## 6. 多模型尺寸对比 — WMT'14 En-De (Fig. 5)

| Model Size | Transformer BLEU | DARTSformer BLEU | Δ BLEU |
|------------|-----------------|-------------------|--------|
| Small (~10M) | — | — | **+1.3** |
| Medium (~30M) | — | — | **+0.9** |
| Base (~65M) | 27.7 | 28.4 | **+0.7** |
| Big (~215M) | 29.1 | 29.8 | **+0.7** |

**关键发现**：
- DARTSformer 在所有模型尺寸上均优于 Transformer
- **模型越小，优势越大**（+1.3 BLEU @ small → +0.7 @ big）
- 大模型下两种架构性能趋近 —— 可能原因是过拟合效应在 large model 下变显著，数据增强有帮助
- 对资源受限场景（如移动端），DARTSformer 优势最显著

## 7. Search Hidden Size 影响 (Table 5)

所有搜索架构统一用 e=256, d=960 重训练：

| Search Setting | e | d (search) | Final BLEU |
|---------------|----|-----------|------------|
| Tiny | 128 | 120 | 24.2 ⚠️ |
| Small | 128 | 240 | 26.3 |
| Medium | 256 | 480 | 27.5 |
| **DARTSformer** | **256** | **960** | **28.4** |
| DARTS + Transformer | 320 | 320 | 27.7 |
| Transformer baseline | — | — | 27.7 |

**关键发现**：
- **搜索 hidden size 至关重要**：小 hidden size 搜索 + 大 hidden size 重训练 → 性能严重退化
- Tiny search (d=120) 重训练后甚至不如标准 Transformer (24.2 vs 27.7)
- DARTS + 标准 Transformer (d=320) 因内存限制无法使用更大 hidden size → 无性能增益 (27.7 = 27.7)
- DARTSformer 因内存高效可搜索 d=960 = target hidden size → 28.4 BLEU

## 8. 搜索结果的可视化

搜索到的最佳架构 (max pooling, s=2, 2/3 split) 如 Fig. 4 所示：

- **Encoder**：2 split，每层 FFN + Self Attn 配对
- **Decoder**：3 split，前两个 split 分别用 FFN+Self Attn 和 Cross Attn，第三个 split (fixed) 为 Cross Attn
- 架构呈现规律性：不同层的操作模式保持一致，说明 DARTS 找到了稳定的最优操作组合

## 关联页面

- [[zhao2021-memory-efficient-dnas-analysis]] — 全维度总览
- [[zhao2021-memory-efficient-dnas-method]] — 方法机制
- [[zhao2021-memory-efficient-dnas-critical]] — 贡献·局限·可迁移·机会
- [[memory-efficient-dnas]] — 实体页
- [[xu2021-nas-bert-results]] — NAS-BERT 的多尺寸压缩结果对比
