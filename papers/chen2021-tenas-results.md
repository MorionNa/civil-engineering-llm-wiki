---
id: papers--chen2021-tenas-results
title: TE-NAS 实验结果：NAS-Bench-201 / DARTS / ImageNet
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/llm
- evidence/paper
- method/neural-architecture-search
keywords:
- cifar10-darts
- imagenet-mobile
- nas-bench-201
- training-free-nas
sources:
- sources/papers/chen2021-tenas.md
created: '2026-06-12'
updated: '2026-07-31'
confidence: high
---

# TE-NAS 实验结果

> 父页面：[[chen2021-tenas-analysis]]

## NAS-Bench-201（15,625 架构，可查表验证）

| 方法 | CIFAR-10 | CIFAR-100 | ImageNet-16-120 | 搜索时间 (GPU sec) | 类型 |
|------|----------|-----------|-----------------|-------------------|------|
| ResNet | 93.97 | 70.86 | 43.63 | — | 人工 |
| RSPS | 87.66±1.69 | 58.33±4.34 | 31.14±3.88 | 8007 | 随机 |
| ENAS | 54.30 | 15.61 | 16.32 | 13315 | RL |
| DARTS (1st) | 54.30 | 15.61 | 16.32 | 10890 | 梯度 |
| DARTS (2nd) | 54.30 | 15.61 | 16.32 | 29902 | 梯度 |
| GDAS | 93.61±0.09 | 70.70±0.30 | 41.84±0.90 | 28926 | 梯度 |
| NASWOT | 91.78±1.45 | 67.05±2.89 | 37.07±6.39 | **4.8** | training-free |
| **TE-NAS** | **93.9±0.47** | **71.24±0.56** | **42.38±0.46** | 1558 | training-free |
| Optimal | 94.37 | 73.51 | 47.31 | — | — |

**关键发现**：TE-NAS 在三个数据集上均达到最高精度，搜索时间比 DARTS 少 5-19 倍。NASWOT 虽然更快（仅 4.8 秒），但精度低 2.12% 且方差大。

## DARTS 搜索空间（CIFAR-10）

| 方法 | Test Error (%) | Params (M) | 搜索成本 (GPU-days) | 类型 |
|------|---------------|------------|-------------------|------|
| NASNet-A | 2.65 | 3.3 | 2000 | RL |
| AmoebaNet-A | 3.34±0.06 | 3.2 | 3150 | 进化 |
| ENAS | 2.89 | 4.6 | 0.5 | RL |
| DARTS (2nd) | 2.76±0.09 | 3.3 | 1.0 | 梯度 |
| GDAS | 2.82 | 2.5 | 0.17 | 梯度 |
| PC-DARTS | 2.57±0.07 | 3.6 | 0.1 | 梯度 |
| P-DARTS | 2.50 | 3.4 | 0.3 | 梯度 |
| **TE-NAS** | **2.63±0.064** | 3.8 | **0.05** | training-free |

**关键发现**：TE-NAS 以 0.05 GPU-day 的极小成本（单卡 1080Ti 仅 1.2 小时），达到与顶级梯度方法（P-DARTS 2.50%, PC-DARTS 2.57%）可比的精度。搜索成本创 CIFAR-10 DARTS 空间新低。

## ImageNet（mobile setting, ≤600M FLOPs）

| 方法 | Top-1 Error (%) | Top-5 Error (%) | Params (M) | 搜索成本 (GPU-days) | 类型 |
|------|----------------|-----------------|------------|-------------------|------|
| NASNet-A | 26.0 | 8.4 | 5.3 | 2000 | RL |
| AmoebaNet-C | 24.3 | 7.6 | 6.4 | 3150 | 进化 |
| MnasNet-92 | 25.2 | 8.0 | 4.4 | — | RL |
| DARTS (2nd) | 26.7 | 8.7 | 4.7 | 4.0 | 梯度 |
| GDAS | 26.0 | 8.5 | 5.3 | 0.21 | 梯度 |
| P-DARTS (CIFAR-10) | 24.4 | 7.4 | 4.9 | 0.3 | 梯度 |
| P-DARTS (CIFAR-100) | 24.7 | 7.5 | 5.1 | 0.3 | 梯度 |
| PC-DARTS | 24.2 | 7.3 | 5.3 | 0.1 | 梯度 |
| **TE-NAS** | **24.5** | **7.5** | 5.4 | **0.17 (4 GPU 小时)** | training-free |

**关键发现**：TE-NAS 在 ImageNet 上仅用 4 GPU 小时（单 1080Ti）达到 competitive 精度。对比 RL 方法（NASNet-A 2000 GPU-days），节省了**12,000 倍**搜索成本。

## 算子偏好分析

TE-NAS 揭示了一个关键洞察——**κN 和 ˆRN 对不同算子有截然不同的偏好**：

| 算子 | κN 选择比例 | ˆRN 选择比例 |
|------|------------|-------------|
| skip-connect | 27.9% | 13.3% |
| conv 1×1 | 19.2% | 30.6% |
| conv 3×3 | 30.6% | 31.1% |
| avg pool 3×3 | 10.3% | 13.9% |
| none (zero) | 13.5% | 9.1% |

- κN 偏好 skip-connect（梯度流好）
- ˆRN 偏好 conv1×1（非线性多）
- conv3×3 两者都偏好（综合最优）

这解释了为什么 TE-NAS 需要同时考虑两个指标——单用 κN 会选太多 skip-connect（如 DARTS 崩塌问题），单用 ˆRN 可能选太多卷积（训练困难）。

## 关联页面

- [[chen2021-tenas-analysis]] — 全维度总览
- [[chen2021-tenas-method]] — 方法展开
- [[chen2021-tenas-critical]] — 贡献·局限·可迁移·机会

## Evidence By Source

### `sources/papers/chen2021-tenas.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/TE-NAS_chen2021_ICLR.pdf`

^[sources/papers/chen2021-tenas.md]
