---
id: papers--li2021-bossnas-results
title: BossNAS 实验结果：ImageNet / CIFAR / 迁移学习
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- evidence/paper
- method/neural-architecture-search
keywords:
- benchmark
- cifar
- imagenet
- neural-architecture-search
sources:
- sources/papers/li2021-bossnas.md
created: '2026-06-14'
updated: '2026-07-31'
confidence: high
---

# BossNAS: 完整实验结果

> 回主分析页：[[li2021-bossnas-analysis]]

---

## 1. HyTra 搜索空间 — ImageNet 分类

### 1.1 手工设计的 HyTra 变体（验证搜索空间质量）

| 模型 | 类型 | MAdds | 推理时间 | Top-1 (%) |
|------|------|-------|----------|-----------|
| ResNet50 (原版) | Conv-Only | 4.1B | 100ms | 77.7 |
| R50-T (HyTra) | Conv-Only | 4.1B | 104ms | 78.2 |
| ViT-B/16 (原版) | Att-Only | 17.6B | 158ms | 77.9 |
| ViT-T/16 (HyTra) | Att-Only | 3.2B | 96ms | 76.5 |
| BoT50 (原版) | Hybrid | 4.0B | 120ms | 78.3 |
| BoT50-T (HyTra) | Hybrid | 3.9B | 103ms | **79.5** |
| Random-T | Hybrid | 3.7B | 84ms | 76.7 |

HyTra 手工设计模型的显著提升（BoT50-T 比 BoT50 高 1.2%，同时 1.17× 更快）验证了 ResConv/ResAtt 构建块设计的优越性。

### 1.2 BossNet-T 系列：搜索模型对比

| 模型 | MAdds | 推理时间 | Top-1 (%) | Top-5 (%) |
|------|-------|----------|-----------|-----------|
| EfficientNet-B1 | 0.7B | 131ms | 79.1 | 94.4 |
| DeiT-S | 10.1B | 84ms | 79.8 | - |
| DNA-T [37] (有监督块级NAS) | 3.9B | 121ms | 80.3 | 95.0 |
| UnNAS-T [41] (无监督NAS) | 3.7B | 104ms | 79.8 | 94.6 |
| **BossNet-T0** (w/o SE) | 3.4B | 101ms | **80.5** | 95.0 |
| **BossNet-T0** (w/ SE) | 3.4B | 115ms | **80.8** | 95.2 |
| BoTNet50 + SE | 4.0B | 149ms | 79.6 | 94.6 |
| BossNet-T0↑ (288×288) | 5.7B | 147ms | **81.6** | 95.6 |
| SENet101 | 7.8B | 218ms | 81.4 | 95.7 |
| EfficientNet-B2 | 1.0B | 143ms | 80.1 | 94.9 |
| DeiT-B | 17.6B | 152ms | 81.8 | - |
| BoTNet-S1-59 | 7.3B | 184ms | 81.7 | 95.8 |
| T2T-ViT-19 | 8.9B | 158ms | 81.9 | - |
| TNT-S | 5.2B | 468ms | 81.3 | 95.6 |
| **BossNet-T1** | 7.9B | 156ms | **82.2** | 95.8 |
| **BossNet-T1↑** (256×256) | 10.5B | 165ms | **82.5** | 96.0 |

**关键观察**：
- BossNet-T0 超越 DNA-T（有监督块级 NAS 对应方法）0.5%，验证了无监督方案成功避免了教师偏见
- BossNet-T1↑ 超越 EfficientNet-B2 **2.4%**，同推理时间
- ↑ 表示直接测试更大输入分辨率（无微调）—— 展现了 HyTra 架构的多分辨率泛化能力

### 1.3 架构可视化分析

| 模型 | ResConv 块数 | ResAtt 块数 | Top-1 |
|------|-------------|-------------|-------|
| DNA-T (有监督蒸馏) | 13 | 3 | 80.3% |
| BossNet-T0 (无监督) | 8 | 8 | 80.8% |

DNA-T 明显偏向 ResConv（教师 ResNet-50 为纯卷积），验证了**Phenomenon I（候选偏好）**。BossNAS 无教师偏见，搜出的模型 ResConv/ResAtt 数量均衡且性能更优。

---

## 2. MBConv 搜索空间 — ImageNet 分类

### 2.1 搜索模型性能

| 模型 | MAdds | Top-1 (%) | 方法 |
|------|-------|-----------|------|
| FairNAS-A | 388M | 75.3 | 权重共享 |
| ProxylessNAS | 465M | 75.1 | 可微分 |
| SPOS | 472M | 74.8 | 单路径 one-shot |
| RLNAS | 473M | 75.6 | 无监督 NAS |
| **BossNet-M1** (w/o SE) | 475M | **76.2** | BossNAS |
| MobileNetV3 | 219M | 75.2 | 多试 NAS |
| MnasNet-A3 | 403M | 76.7 | 多试 NAS |
| EfficientNet-B0 | 399M | 76.3 | 多试 NAS |
| DNA-b | 406M | 77.5 | 有监督块级 NAS |
| **BossNet-M2** (w/ SE) | 403M | **77.4** | BossNAS |

BossNAS 在纯 CNN 空间也表现出色：BossNet-M2 超越 EfficientNet-B0 **1.1%**，接近 DNA-b。

### 2.2 架构评分精度（核心指标）

基于 23 个开源 MBConv 架构的真值排名 [37]：

| 方法 | 搜索成本 | Kendall τ | Spearman ρ | Pearson R |
|------|---------|-----------|------------|-----------|
| SPOS [22] | 8.5 Gds | -0.18 | -0.27 | -0.29 |
| DARTS [43] | 50 Gds | 0.08 | 0.14 | 0.06 |
| MnasNet [63] | 288 Tds | 0.61 | 0.77 | 0.78 |
| DNA (EffNet) [37] | 8.5 Gds | 0.62 | 0.77 | 0.83 |
| DNA (MBNet) [37] | 8.5 Gds | 0.23 | 0.27 | 0.37 |
| **BossNAS** | **10 Gds** | **0.65** | **0.78** | **0.85** |

- BossNAS τ=0.65 在所有方法中最高，超越 MnasNet（288 Tds）同时加速 28.8×
- DNA 使用 MobileNetV1 教师时 τ 暴跌至 0.23（**Phenomenon II：教师偏好**）
- BossNAS 无此问题：无教师 → 评分不受教师架构影响

---

## 3. NATS-Bench SS — CIFAR 实验

### 3.1 搜索模型性能

| 方法 | CIFAR-10 (%) | CIFAR-100 (%) | τ | ρ |
|------|-------------|---------------|-----|-----|
| FBNet v2 | 93.14 | 70.72 | - | - |
| TuNAS | 92.78 | 70.11 | - | - |
| CE [27] (predictor) | 90.55 | 70.78 | 0.43 | 0.60 |
| **BossNAS** | **93.29** | **70.86** | **0.59** | **0.76** |

BossNAS 在通道数搜索空间同样有效（使用 slimmable 权重共享）。

### 3.2 评分精度对比

| 数据集 | 方法 | Kendall τ | Spearman ρ | Pearson R |
|--------|------|-----------|------------|-----------|
| CIFAR-10 | CE [27] | 0.42 | 0.60 | 0.59 |
| CIFAR-10 | **BossNAS** | **0.53** | **0.73** | **0.72** |
| CIFAR-100 | CE [27] | 0.43 | 0.60 | 0.60 |
| CIFAR-100 | **BossNAS** | **0.59** | **0.76** | **0.79** |

BossNAS 在无任何标签、无真值架构性能的条件下，评分精度超越用真值训练的 CE predictor 达 0.16 τ。

---

## 4. 消融实验（MBConv + ImageNet）

### 4.1 训练方法消融

| 训练方法 | 评估方法 | τ | ρ | R |
|----------|---------|-----|-----|-----|
| 有监督蒸馏 (DNA) | 有监督蒸馏 | 0.62 | 0.77 | 0.83 |
| 有监督分类 | 有监督分类 | 0.46 | 0.65 | 0.71 |
| 无监督 bootstrapping (naive) | 无监督评估 | 0.12 | 0.15 | 0.28 |
| **无监督 EB** (Ensemble Boot.) | 有监督线性评估 | 0.55 | 0.73 | 0.79 |
| **无监督 EB** | **无监督评估** | **0.65** | **0.78** | **0.85** |

**关键发现**：
- Naive bootstrapping 彻底失败（τ=0.12）→ 概率集成不可或缺
- 无监督 EB + 无监督评估 超越 有监督线性评估（+0.10 τ）→ 种群中心评估优于线性分类头
- 无监督 EB + 无监督评估 超越 有监督蒸馏（+0.03 τ）→ 无监督可以反超有监督

### 4.2 收敛行为

评分精度在训练过程中快速上升，约第 12 epoch 收敛并保持稳定至 20 epoch。CIFAR 实验也在 20 epoch 收敛。证明方法稳定且易于优化。

---

*上接 [[li2021-bossnas-analysis]] | 方法细节 [[li2021-bossnas-method]] | 批判分析 [[li2021-bossnas-critical]]*

## Evidence By Source

### `sources/papers/li2021-bossnas.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/bossnas2021_iclr.pdf`

^[sources/papers/li2021-bossnas.md]
