---
id: papers--so2021-primer-results
title: 'So et al. (2021) — Primer: 关键实验与结果'
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- evidence/paper
- method/transformer
keywords:
- c4
- efficient-inference
- lm1b
- one-shot-nas
- scaling-law
- transformer
sources:
- sources/papers/so2021-primer.md
created: '2026-06-14'
updated: '2026-07-31'
confidence: high
datasets:
- lm1b
- c4
- pg19
- glue
- squad
- superglue
---

# Primer 关键实验与结果

> 父页面：[[so2021-primer-analysis]]
> 四个实验递进验证：搜索任务 → Scaling Law → T5 大尺度 → One-shot downstream

## 实验 1：搜索任务对比 (LM1B, 35M)

### Setup
- 任务：LM1B 自回归语言建模，序列 64，batch 4096 tokens
- 模型：~35M 参数，训练 24h
- 对比基线：Vanilla Transformer, Transf.+GELU, Transf.++, Primer, Primer-EZ
- 三个平台：T2T/TPUv2, T2T/V100, T5/TPUv2

### 结果

| Model | T2T TPUv2 PPLX | Speedup | T2T V100 PPLX | Speedup | T5 TPUv2 PPLX | Speedup |
|-------|----------------|---------|---------------|---------|---------------|---------|
| Vanilla Transformer | 35.44 | 1.00× | 37.19 | 1.00× | 23.30 | 1.00× |
| Transformer+GELU | 35.00 | 1.23× | 37.11 | 1.05× | 23.39 | 0.97× |
| Transformer++ | 34.87 | 1.37× | 36.23 | 1.54× | 23.04 | 1.33× |
| **Primer** | **33.77** | **2.12×** | **35.06** | **2.13×** | **22.71** | **1.72×** |
| **Primer-EZ** | **33.53** | **2.34×** | **35.16** | **2.03×** | **22.62** | **1.75×** |

> Speedup = 达到 Vanilla Transformer 最终质量所需计算量的倒数。PPLX 因 codebase tokenization 不同不可跨行比较。

### 关键发现
- Primer 在所有设置中加速 1.7× 以上
- Primer-EZ 和完整 Primer 性能接近，验证了 Squared ReLU + MDHA 贡献了大部分增益
- Transformer+GELU 在 T5 上竟不如 Vanilla（speedup 0.97×），说明 GELU 的增益不是普适的

## 实验 2：Scaling Law 分析

### Setup
- 参数扫描：L∈{6,9,12} × d_model∈{384,512,1024} × p∈{4,8,12} = 27 个配置
- 参数范围：23M ~ 385M
- 每个配置训练不同 compute budgets，画 l-c 双对数图

### 核心结果
- 所有模型遵循 l = a·c^(-k) 幂律
- **四条线平行**（斜率 k 相同），Primer 的线在整个 compute 范围内向下平移
- **平移量 log(b^k)**：Primer vs Vanilla 在整个 compute-range 上保持恒定计算节省比例 b
- 导出 compute savings 幂律：l = a₁(1-1/b)^k · s^(-k)

| Architecture | 相对垂直偏移 | 推算 constant compute savings factor b |
|-------------|-------------|--------------------------------------|
| Vanilla Transformer | 基准 | 1.00× |
| Transformer+GELU | 中等 | ~1.15× |
| Transformer++ | 较小 | ~1.35× |
| Primer | 最大 | ~1.5-2.0× |

### 推理效率
- 前向传播时间 vs 质量：Primer 在多数质量目标上 Pareto 最优
- 训练步时与推理时间相关系数 0.97

## 实验 3：T5 大尺度训练 (C4, 537M)

### Setup
- 完全复制 Raffel et al. (2020) T5 配置
- d_model=1024, d_ff=8192, L=24, 537M 参数
- Batch ~1M tokens, 64 TPUv3 chips, 1M steps

### 结果

| Model | Steps to 13.25 PPLX | TPUv3 Hours | Steps to 12.69 PPLX | TPUv3 Hours | Final PPLX (1M steps) |
|-------|---------------------|-------------|---------------------|-------------|----------------------|
| Original T5 | 1M | 15.7K | - | - | 13.25 |
| T5++ | 251K | 4.6K | 1M | 16.5K | 12.69 |
| **Primer** | **207K** | **3.8K** | **480K** | **8.3K** | **12.35** |

**Primer 加速比**：
- vs Original T5: **4.2×**（同等质量用不到 1/4 计算）
- vs T5++: **2.0×**（同等质量用 1/2 计算）

### 关键发现
- 加速比随训练进行而增长（Figure 10）：越训练越节省
- 原因是 Primer 的渐进收敛更快，且两曲线渐近性质不同

## 实验 4：One-shot Downstream (类 GPT-3 XL, 1.9B)

### Setup
- 1.9B 参数 Transformer (d_model=2048, d_ff=12288, L=24) vs Primer
- 512 TPUv4 chips, ~72K hours (~1M steps)
- Proprietary pretraining 数据
- 27 个下游任务（QA + Multi-Choice），one-shot 评估

### 核心结果：相同计算量

| 指标 | Transformer 24K hrs | Primer 24K hrs (1/3×) | Transformer 72K hrs | Primer 72K hrs |
|------|---------------------|----------------------|---------------------|----------------|
| Pretrain PPLX | 15.3 | **14.3** | 14.3 | **13.5** |
| QA Average | 30.9 | **34.6** | 34.5 | **36.8** |
| Multi-Choice Avg | 53.1 | **55.0** | 54.7 | **56.2** |

**Primer with 1/3 compute ≈ Transformer with full compute**：
- 优于 Transformer 5 tasks
- 差于 Transformer 1 task
- 持平 21 tasks

### QA 详细（部分代表性任务）

| Task | Transf. Full | Primer 1/3 | Primer Full |
|------|-------------|-----------|-------------|
| TriviaQA | 26.8 | 27.5 | 32.2 |
| SQuADv2 | 65.4 | 64.2 | 67.8 |
| LAMBADA | 55.2 | 54.5 | 56.8 |

### Multi-Choice 详细（部分）

| Task | Transf. Full | Primer 1/3 | Primer Full |
|------|-------------|-----------|-------------|
| HellaSwag | 59.5 | 60.2 | 63.3 |
| PIQA | 72.6 | 73.7 | 75.0 |
| ARC (Challenge) | 34.4 | 35.6 | 37.4 |

## 实验 5：消融与迁移

### 消融分析（Insertion + Ablation, T2T + T5）

| Modification | Insertion (T2T) | Insertion (T5) | Ablation (T2T) | Ablation (T5) |
|-------------|-----------------|----------------|----------------|---------------|
| Squared ReLU | **+++** | **+++** | **---** | **---** |
| MDHA | **+++** | **+++** | **---** | **---** |
| 12× Projection | ++ | + | -- | - |
| Pre/Post Norm | + | - | - | O |
| Custom Norm | O | O | O | O |
| Shared QK | - | - | + | + |

> 符号：+++ 强正，+ 弱正，O 中性，- 弱负，--- 强负

### 跨模型家族

| Model | Params | Speedup @525K steps | Speedup @1M steps |
|-------|--------|---------------------|--------------------|
| Switch Transformer | 550M | baseline | baseline |
| Switch Primer (Primer-EZ) | 550M | **1.45×** | **1.56×** |
| Synthesizer | 145M | baseline | baseline |
| Synthesizer + Squared ReLU | 145M | **1.74×** | **1.96×** |

### Encoder-Decoder MLM (Appendix)

| Model | Pretrain Log PPLX | SGLUE | XSum | WebQ |
|-------|-------------------|-------|------|------|
| Vanilla Transformer | 1.838 | 70.97 | 17.78 | 23.02 |
| Transformer++ | 1.792 | 75.65 | 17.90 | 25.92 |
| Primer-EZ Decoder | 1.787 | 76.69 | 17.87 | 24.87 |

Primer-EZ Decoder 在 SGLUE 上略优，但整体不如 Transformer++。Decoder LM 改进入 encoder-decoder 需要更多研究。

## 能耗分析

| 阶段 | 计算量 | CO₂e |
|------|--------|------|
| 架构搜索 | 1145.8 TPUv2-days | 2.06 MTCO₂e |
| 大尺度 T5 实验 | 2062.5 TPUv3-days | 8.54 MTCO₂e |
| One-shot pretraining | 2×71.8K TPUv4-hours | 29.26 MTCO₂e |
| One-shot 节省 | Primer 3× compute reduction | 9.75 MTCO₂e saved |
| 搜索 return | One-shot 节省 / 搜索成本 | **4.7×** (CO₂) / **9.24×** (FLOPs) |

## Evidence By Source

### `sources/papers/so2021-primer.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/primer2021_efficient_transformers.pdf`

^[sources/papers/so2021-primer.md]

## Related Indexes

- [[papers/index]]
