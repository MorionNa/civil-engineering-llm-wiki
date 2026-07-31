---
id: papers--lepikhin2021-gshard-results
title: Lepikhin et al. (2020) — 结果证据展开
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/llm
- evidence/paper
- method/transformer
keywords:
- comparison
- llm-benchmark
- mixture-of-experts
- multilingual-data
- sparse-moe
- sublinear-scaling
sources:
- sources/papers/lepikhin2021-gshard.md
created: '2026-06-13'
updated: '2026-07-31'
confidence: high
results:
- sublinear-scaling
- superlinear-quality
- sample-efficiency
- constant-memory
- o1-compilation
- 600b-parameters
- multilingual-bleu
datasets:
- in-house-web-scale-mt-corpus
---

# Lepikhin et al. (2020) — 结果证据展开

> 返回概述 → [[lepikhin2021-gshard-analysis]]

---

## 实验设置

| 项目 | 详情 |
|------|------|
| 任务 | 多语言 NMT：100 languages → English |
| 训练数据 | Google 内部 Web 挖掘，25B 平行句对（过滤后 ~13B 用于 100→EN） |
| 数据分布 | 极度不均衡——高资源语言数十亿对，低资源语言数万对（幂律分布） |
| 评估指标 | BLEU（∆BLEU = 单多语言模型 vs. 单语基线差值） |
| 基线 | 100 个单语 Transformer 模型（各语言独立训练+调参） |
| 密集基线 | T(96L): 96 层密集 Transformer，GPipe 训练，2.3B 参数 |
| 硬件 | TPU v3（128 / 512 / 2048 cores） |

### 模型家族 (Table 1)

| ID | Model | Experts/Layer | Layers | TPU Cores | Params |
|----|-------|---------------|--------|-----------|--------|
| (6) | MoE(128E, 12L) | 128 | 12 | 128 | 12.5B |
| (5) | MoE(128E, 36L) | 128 | 36 | 128 | 37B |
| (4) | MoE(512E, 12L) | 512 | 12 | 512 | 50B |
| (3) | MoE(512E, 36L) | 512 | 36 | 512 | 150B |
| (2) | MoE(2048E, 12L) | 2048 | 12 | 2048 | 200B |
| (1) | MoE(2048E, 36L) | 2048 | 36 | 2048 | **600B** |
| * | T(96L) dense | — | 96 | 2048 | 2.3B |
| * | 100×Bilingual | — | — | — | ~0.4B each |

训练至每个模型看过 1T tokens，取此 checkpoint 评估——所有模型均未出现过拟合，继续训练 loss 仍在下降。

---

## 实验 1: 翻译质量 (Figure 6, Section 4.4)

### 整体 ∆BLEU 对比

| 模型 | Avg BLEU | ∆BLEU avg | vs. 单语基线 |
|------|----------|-----------|-------------|
| MoE(2048E, 36L) 600B | **44.3** | **+13.5** | 最强 |
| MoE(512E, 36L) 150B | 43.7 | +12.9 | |
| MoE(2048E, 12L) 200B | 41.3 | +10.5 | |
| MoE(512E, 12L) 50B | 40.0 | +9.2 | |
| MoE(128E, 36L) 37B | 39.0 | +8.2 | |
| MoE(128E, 12L) 12.5B | 36.7 | +5.9 | 最弱 MoE |
| T(96L) 2.3B dense | 36.9 | +6.1 | 密集基线 |
| 100×Bilingual baselines | 30.8 | — | |

### 发现 1: 深度带来一致的全面提升

在每组固定专家数下，12L→36L 带来了 **+2-3 BLEU 的近乎恒定加成**（最后一列 ∆BLEU 差异），高低资源语言均受益。

| 组 | 12L BLEU | 36L BLEU | ∆ |
|----|----------|----------|---|
| 128E | 36.7 | 39.0 | +2.3 |
| 512E | 40.0 | 43.7 | +3.7 |
| 2048E | 41.3 | 44.3 | +3.0 |

→ 深度 = 样本效率 + 泛化能力的可靠杠杆。

### 发现 2: 容量瓶颈在 128-512 专家之间

固定深度 12L：
- 128E → 512E（4x）：**+3.3 avg BLEU**（大跳跃）
- 512E → 2048E（4x）：**+1.3 avg BLEU**（边际递减）

→ 容量瓶颈在 ~128-512 专家区间。一旦越过，继续扩专家的收益递减。

### 发现 3: 专家增加特别惠及高资源语言

固定深度 12L 和 36L 下，增加专家数对高资源（左侧）语言的提升远大于低资源（右侧）。高资源语言急需额外容量（capacity bottleneck），低资源语言更多受益于参数共享（positive transfer）。

### 发现 4: 密集深模型在低资源语言的独特优势

T(96L) 密集模型在低资源语言上超越浅 MoE(128E, 12L)，差距随资源减少而扩大。**100% 参数共享最大化正向跨语言迁移**——代价是 235 core-years（vs MoE 的 6-22 core-years）。

---

## 实验 2: 训练效率 (Section 4.5)

### 样本效率：更深 → 更少 token 达到相同 loss (Table 2)

| 模型 | Billion tokens to cross-entropy |
|------|--------------------------------|
| | 0.7 | 0.6 | 0.5 |
| MoE(2048E, 36L) | **82** | **175** | **542** |
| MoE(2048E, 12L) | 176 | 484 | 1780 |
| MoE(512E, 36L) | 66 | 170 | 567 |
| MoE(512E, 12L) | 141 | 486 | — |
| MoE(128E, 36L) | 321 | 1074 | — |
| MoE(128E, 12L) | 995 | — | — |

→ 36L 模型需 2-3x 更少 token 达到相同 loss。**深度 = 样本效率。**

### 亚线性计算缩放 (Table 3)

| 模型 | Cores | Steps/sec | Batch | Core-years | Days | BLEU |
|------|-------|-----------|-------|------------|------|------|
| MoE(2048E, 36L) | 2048 | 0.72 | 4M | 22.4 | 4.0 | 44.3 |
| MoE(2048E, 12L) | 2048 | 2.15 | 4M | 7.5 | 1.4 | 41.3 |
| MoE(512E, 36L) | 512 | 1.05 | 1M | 15.5 | 11.0 | 43.7 |
| MoE(512E, 12L) | 512 | 3.28 | 1M | 4.9 | 3.5 | 40.0 |
| MoE(128E, 36L) | 128 | 0.67 | 1M | 6.1 | 17.3 | 39.0 |
| MoE(128E, 12L) | 128 | 2.16 | 1M | 1.9 | 5.4 | 36.7 |
| T(96L) dense | 2048 | — | 4M | **~235.5** | **~42** | 36.9 |

→ 600B MoE 仅需 22.4 core-years，密集 2.3B 需 235.5 core-years——**10x 效率差且密集质量更差**。模型 16x（37B→600B）→ 计算 3.6x（6→22 core-years）。

---

## 实验 3: 性能与显存 (Section 5)

### 显存缩放 (Figure 7)

| 特性 | 结论 |
|------|------|
| 同深度下专家数增加 | 权重显存 + 激活显存 **O(1)**（专家被分片） |
| 深度增加 | 权重和激活线性增长 |
| rematerialization | 36L: 28% 周期重计算; 60L: 34%; 12L/24L: 0% |

### 运行时缩放 (Figure 8)

从 128E 扩展到 2048E（16x），单步时间仅 **1.7x**。主要原因：
- Transformer 层（attention + FFN）：O(1)
- MoE FFN（专家计算）：O(1)
- 门控 Einsum + Cumsum：O(D) 但常数因子极小（<10% at 2048E）
- **AllToAll 通信：O(√D)**，16x→3.75x 耗时增长（占比 16%→36%）

### 通信微基准 (Figure 9, Table 4)

| 原语 | 复杂度 | 实测（16→2048 partitions） |
|------|--------|--------------------------|
| AllReduce | O(1) | ≈恒定 |
| AllToAll | O(√D) | D 128x → 时间 9x |
| AllGather | O(D) | — |
| CollectivePermute | O(1) | — |

---

## 汇总

```
翻译质量:  MoE(2048E,36L) 600B >> MoE(512E,36L) ≈ MoE(2048E,12L) > T(96L) > 单语基线
训练效率:  MoE(any) >> T(96L) dense (10x fewer core-years)
缩放特性:  模型 16x → 计算 3.6x, 显存 O(1), 编译 O(1)
关键杠杆:  深度 → 样本效率+泛化 | 专家数 → 高资源容量 | 共享参数 → 低资源迁移
```

---

## 关联

- [[lepikhin2021-gshard-analysis]] — 论文概述
- [[lepikhin2021-gshard-method]] — 方法机制展开
- [[lepikhin2021-gshard-critical]] — 贡献 / 知识点 / Negative / 可迁移 / 研究机会

## Evidence By Source

### `sources/papers/lepikhin2021-gshard.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/lepikhin2021_gshard.md`

^[sources/papers/lepikhin2021-gshard.md]
