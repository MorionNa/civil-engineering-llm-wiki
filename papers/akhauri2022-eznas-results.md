---
id: papers--akhauri2022-eznas-results
title: EZNAS 结果证据 — 跨搜索空间评分-精度相关性
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/llm
- evidence/paper
- method/neural-architecture-search
keywords:
- kendall-tau
- nas-bench-201
- nats-bench
- nds
- spearman-rho
- training-free-nas
- zero-cost-proxy
sources:
- sources/papers/akhauri2022-eznas.md
created: '2026-06-15'
updated: '2026-07-31'
confidence: high
parent: akhauri2022-eznas-analysis
---

# EZNAS 实验结果详解

> EZNAS-A 仅在 NDS-DARTS CIFAR-10 上进化发现，却在三大 benchmark 的所有数据集和搜索空间上取得 SoTA 评分-精度相关性。

## 6.1 NAS-Bench-201 结果

NAS-Bench-201 含 15,625 个架构 × 3 数据集。**全量评估**（非采样）。

### Kendall τ 排名相关系数

| 方法 | CIFAR-10 | CIFAR-100 | ImageNet-16-120 |
|------|:--:|:--:|:--:|
| **EZNAS-A** | **0.65** | **0.65** | **0.61** |
| NASWOT | 0.57 | 0.61 | 0.55 |
| AngleNAS | 0.57 | 0.60 | 0.54 |
| FLOPs | 0.56 | 0.54 | 0.50 |
| Params | 0.56 | 0.54 | 0.50 |

> EZNAS-A 在所有三个数据集上均取得最高 Kendall τ，比第二名 NASWOT 高出 0.06-0.08。

### Spearman ρ 排名次序相关系数

| 方法 | CIFAR-10 | CIFAR-100 | ImageNet-16-120 |
|------|:--:|:--:|:--:|
| **EZNAS-A** | **0.83** | **0.82** | **0.78** |
| synflow | 0.74 | 0.76 | 0.75 |
| jacob_cov | 0.73 | 0.71 | 0.71 |
| FLOPs | 0.75 | 0.72 | 0.69 |
| Params | 0.75 | 0.72 | 0.69 |
| grad_norm | 0.58 | 0.64 | 0.58 |
| snip | 0.58 | 0.63 | 0.58 |
| grasp | 0.48 | 0.54 | 0.56 |
| fisher | 0.36 | 0.39 | 0.33 |

> EZNAS-A 的 Spearman ρ 全面超越 FLOPs/Params 0.08-0.09，超越 synflow 0.03-0.09。

## 6.2 NDS CIFAR-10 结果

NDS 包含 5 个设计空间（DARTS / Amoeba / ENAS / PNAS / NASNet），每个约 5,000 架构。**全量评估**。

### Kendall τ — EZNAS-A vs 已有方法

| 方法 | DARTS | Amoeba | ENAS | PNAS | NASNet |
|------|:--:|:--:|:--:|:--:|:--:|
| **EZNAS-A** | **0.56** | **0.45** | **0.52** | **0.51** | **0.44** |
| NASWOT | 0.47 | 0.22 | 0.37 | 0.38 | 0.30 |
| FLOPs | 0.51 | 0.26 | 0.47 | 0.34 | 0.20 |
| Params | 0.50 | 0.26 | 0.47 | 0.32 | 0.21 |
| grad_norm | 0.28 | -0.10 | -0.02 | -0.01 | -0.08 |
| synflow | 0.37 | -0.06 | 0.02 | 0.03 | -0.03 |

> **关键发现**：synflow 在 NAS-Bench-201 上表现良好，但在 NDS 上几乎完全失效（Amoeba τ=-0.06, NASNet τ=-0.03）。EZNAS-A 在所有 5 个空间上始终保持正相关且最高。

### NDS ImageNet — Spearman ρ

| 方法 | DARTS | Amoeba | PNAS | ENAS | NASNet |
|------|:--:|:--:|:--:|:--:|:--:|
| **EZNAS-A** | **0.70** | **0.58** | 0.43 | 0.43 | 0.31 |

> ImageNet 评估采样 40 个架构 × 5 seeds。EZNAS-A 在 DARTS 和 Amoeba 空间上远超其他方法。

## 6.3 NATS-Bench 结果

NATS-Bench 包含 TSS（与 NB-201 相同）和 SSS（不同尺寸变体）两个搜索空间。

### NATS-Bench SSS — Spearman ρ

| 方法 | CIFAR-10 | CIFAR-100 | ImageNet-16-120 |
|------|:--:|:--:|:--:|
| **EZNAS-A** | **0.89** | **0.74** | **0.81** |
| NASWOT | 0.45 | 0.18 | 0.41 |

> **最显著的结果**：在 NATS-Bench SSS 上，EZNAS-A 的 Spearman ρ 是 NASWOT 的 **2-4 倍**（CIFAR-100 上 0.74 vs 0.18），凸显了跨空间泛化的价值。

## 6.4 NAS 搜索集成

将 EZNAS-A 与 Aging Evolution (AE) 搜索算法集成，在 NAS-Bench-201 CIFAR-10 上测试搜索效率。

**10 次重复实验**：EZNAS-A 驱动的 AE 搜索在同等采样数下始终找到比 synflow 更高精度的架构，且接近"oracle"（真实精度引导）的搜索效率。

## 6.5 结果解读

### 为什么 EZNAS-A 能跨空间泛化？

1. **EZNAS-A 本质是"加权参数计数"**——利用 T3GN（噪声权重梯度）作为输入，生成的得分与激活/权重尺寸有强但不简单的非线性关系。参数容量是跨搜索空间最稳健的架构质量信号。
2. **FLOPs/Params 是它的下界近似**：纯 FLOPs/Params 对所有架构一视同仁（只算数量），EZNAS-A 能区分同等参数下不同 kernel 配置的效率差异。
3. **synflow 等指标过于依赖特定搜索空间的统计特性**（如梯度流的假设）——换一个算子分布就失效。

### 为什么 NDS 比 NAS-Bench-201 更难？

NAS-Bench-201 仅 5 种操作（none/skip/conv1×1/conv3×3/avgpool），架构变体相对同质。NDS 包含真实 NAS 发现的高性能 cell → 架构多样性更大 → 评分难度更高。

### batch size 效应

EZNAS-A 的评分-精度相关性随 batch size 增大而**单调提升**（CIFAR-10 PNAS 上从 batch=1 的 τ≈0.35 到 batch=16 的 τ≈0.50）。batch=1 时方差显著，需多 seed 均值。

## 关联页面

- [[akhauri2022-eznas-analysis]] — 论文分析总览
- [[akhauri2022-eznas-method]] — 遗传编程方法详解
- [[akhauri2022-eznas-critical]] — 批判性分析
- [[eznas]] — EZNAS 实体
- [[nasbench201]] — NAS-Bench-201 基准

## Evidence By Source

### `sources/papers/akhauri2022-eznas.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/eznas_akhauri2022.pdf`

^[sources/papers/akhauri2022-eznas.md]
