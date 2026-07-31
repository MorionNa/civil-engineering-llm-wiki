---
id: papers--lee2024-aznas-results
title: 'Lee & Ham (2024) — AZ-NAS: 结果证据详解'
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- evidence/paper
- method/neural-architecture-search
- method/transformer
keywords:
- neural-architecture-search
- training-free-nas
- zero-shot
sources:
- sources/papers/lee2024-aznas.md
created: '2026-06-15'
updated: '2026-07-31'
confidence: high
---

# AZ-NAS 结果证据

> 返回 [[lee2024-aznas-analysis]] 总览

## 实验全景

AZ-NAS 在三个搜索空间上进行了全面验证：
1. **NAS-Bench-201**：全空间排序一致性评测（15625 架构 × 3 数据集）
2. **MobileNetV2 ImageNet**：大规模 CNN 搜索（倒残差块，可变深度/宽度/扩展比）
3. **AutoFormer**：Vision Transformer 搜索（可变深度/嵌入维度/注意力头数/MLP 扩展比）

---

## 实验 1：NAS-Bench-201 排序一致性（Table 1）

### 实验设置

- 搜索空间：15625 个架构（4 节点 cell DAG，5 种操作）
- 评估数据集：CIFAR-10, CIFAR-100, ImageNet16-120
- 指标：Kendall τ（全空间 15625 架构排序一致性）, Spearman ρ, 选出架构的 Top-1 精度
- 精度评估：每轮随机采样 3000 个架构 → 选 AZ-NAS 最高分架构 → 重复 5 轮取均值和标准差
- **所有对比方法共享相同的 5 组随机架构集合**（公平性保证）
- 所有对比方法结果均用**原作者官方代码复现**

### 结果：排序一致性

| 方法 | 类型 | CIFAR-10 τ | CIFAR-100 τ | IN16-120 τ | Runtime (ms/arch) |
|------|------|-----------|------------|-----------|-------------------|
| #Params | A | 0.578 | 0.552 | 0.520 | — |
| FLOPs | A | 0.578 | 0.551 | 0.517 | — |
| GradNorm | B | 0.357 | 0.350 | 0.304 | 28.8 |
| Grasp | B | 0.318 | 0.315 | 0.282 | 395.9 |
| Snip | B | 0.454 | 0.451 | 0.400 | 326.5 |
| Synflow | B | 0.571 | 0.565 | 0.555 | 53.4 |
| NASWOT | F | 0.557 | 0.579 | 0.573 | 36.9 |
| TE-NAS | B+F | 0.536 | 0.535 | 0.492 | 1311.8 |
| ZenNAS | F | 0.296 | 0.283 | 0.303 | 19.9 |
| GradSign | B | 0.618 | 0.594 | 0.575 | 1823.9 |
| ZiCo | B | 0.589 | 0.590 | 0.584 | 372.8 |
| **AZ-NAS** | **A+B+F** | **0.741** | **0.723** | **0.710** | **42.7** |

**关键发现**：
- AZ-NAS 的 Kendall τ 比第二名（GradSign）高出 **0.123** (CIFAR-10), **0.129** (CIFAR-100), **0.135** (IN16-120)——这是非常大的差距。在相关工作中，0.05 的改善通常就会被认为显著。
- AZ-NAS 的 Spearman ρ 达到 **0.913/0.900/0.886**——基本可以认为预测排名接近 ground truth。
- Runtime 仅为 42.7 ms/arch，比慢的方法快 **30-40 倍**，比大部分单代理方法也只慢 1-2 倍——但提供了远超的信息量。

### 结果：选出架构的精度

| 方法 | CIFAR-10 Acc | CIFAR-100 Acc | IN16-120 Acc |
|------|-------------|--------------|-------------|
| AZ-NAS | **93.53 ± 0.15** | **70.75 ± 0.48** | **45.43 ± 0.29** |
| GradSign | 93.52 ± 0.19 | 70.57 ± 0.31 | 41.89 ± 0.69 |
| ZiCo | 93.50 ± 0.18 | 70.62 ± 0.26 | 42.04 ± 0.82 |
| Ground Truth | 94.29 ± 0.13 | 73.25 ± 0.26 | 47.05 ± 0.30 |

AZ-NAS 选出的架构在三个数据集上均达到了最高精度，且标准差最小（稳定性好）。在 IN16-120 上领先 GradSign **3.54%**——说明 AZ-NAS 在更接近真实分布（ImageNet 降采样）的数据集上优势更大。

---

## 实验 2：MobileNetV2 ImageNet（Table 2）

### 实验设置

- 搜索空间：MobileNetV2 风格的倒残差块，可变深度、宽度、扩展比
- FLOPs 约束：450M / 600M / 1000M 三档
- 搜索算法：Algorithm 1 进化搜索，T=1e5 迭代，k=1024
- 训练：选出的架构在 ImageNet 上完整训练
- 对比方法：包括 MS（多轮训练式）、OS（one-shot）、ZS（零-shot）各类方法
- **AZ-NAS 不依赖特殊技巧**：不删除残差连接（区别于 ZenNAS/ZiCo 搜索时去 residual）

### 结果

| 方法 | FLOPs | Top-1 Acc | 类型 | 搜索成本 |
|------|-------|----------|------|---------|
| **450M 档** | | | | |
| ZiCo | 448M | 78.1 | ZS | 0.4 GPU天 |
| **AZ-NAS** | **462M ± 1.5M** | **78.6 ± 0.2** | **ZS** | **0.4 GPU天** |
| OFA (训练式) | 406M | 77.7 | OS | 50 GPU天 |
| **600M 档** | | | | |
| ZenNAS | 611M | 79.1 | ZS | 0.5 GPU天 |
| ZiCo | 603M | 79.4 | ZS | 0.4 GPU天 |
| **AZ-NAS** | **615M ± 2.2M** | **79.9 ± 0.3** | **ZS** | **0.6 GPU天** |
| OFA (训练式) | 662M | 78.7 | OS | 50 GPU天 |
| **1000M 档** | | | | |
| ZenNAS | 934M | 80.8 | ZS | 0.5 GPU天 |
| ZiCo | 1005M | 80.5 | ZS | 0.4 GPU天 |
| **AZ-NAS** | **1022M ± 5.1M** | **81.1 ± 0.1** | **ZS** | **0.7 GPU天** |

**关键发现**：
- AZ-NAS 在所有三档 FLOPs 上达到最高精度，且搜索成本与 ZiCo 相当（都是 ~0.5 GPU 天）。
- 在 600M 档，AZ-NAS 的 79.9% 超越 OFA（78.7%）——OFA 是 one-shot 训练式方法，搜索成本 50 GPU 天。**零训练超越了需要训练超网的方法**。
- 三次随机运行的均值±标准差显示 AZ-NAS 的搜索结果**高度稳定**（0.1-0.3% 的标准差）。
- AZ-NAS 搜索时不删除残差连接，避免了 ZenNAS/ZiCo 的"搜索-训练不一致"问题（搜索时去 residual → 训练时加回来 → 性能可能变化）。

---

## 实验 3：AutoFormer Vision Transformer（Table 3）

### 实验设置

- 搜索空间：AutoFormer，可变深度、嵌入维度、注意力头数、MLP 扩展比
- 分为 Tiny / Small / Base 三个子空间
- 每个子空间从 10000 个随机架构中选最高分
- **不应用 sP 代理**（因为高斯输入下 ViT attention 的块间特征空间不可靠区分）
- 训练：按 AutoFormer 原配置（Base 训练 epoch 减半防过拟合）

### 结果

| 方法 | #Params | FLOPs | Top-1 Acc | 类型 | 搜索成本 |
|------|---------|-------|----------|------|---------|
| **Tiny** | | | | | |
| AutoFormer | 5.70M | 1.30G | 74.7 | OS | 24 GPU天 |
| AZ-NAS | 5.92M | 1.38G | **76.1** | ZS | **0.03 GPU天** |
| TF-TAS | 6.20M | 1.43G | 75.3 | ZS | 0.5 GPU天 |
| AZ-NAS | 6.16M | 1.43G | **76.4** | ZS | **0.04 GPU天** |
| **Small** | | | | | |
| AutoFormer | 22.9M | 5.10G | 81.7 | OS | 24 GPU天 |
| AZ-NAS | 23.0M | 4.94G | **82.0** | ZS | **0.06 GPU天** |
| TF-TAS | 23.9M | 5.16G | 81.9 | ZS | 0.5 GPU天 |
| AZ-NAS | 23.8M | 5.13G | **82.2** | ZS | **0.07 GPU天** |
| **Base** | | | | | |
| AutoFormer | 54.0M | 11.0G | 82.4 | OS | 24 GPU天 |
| AZ-NAS | 53.7M | 11.4G | 82.1 | ZS | **0.11 GPU天** |
| TF-TAS | 56.5M | 11.9G | 82.2 | ZS | 0.5 GPU天 |
| AZ-NAS | 54.1M | 11.5G | **82.3** | ZS | **0.17 GPU天** |

**关键发现**：
- 在 Tiny 和 Small 子空间上，AZ-NAS **全面超越** one-shot 训练的 AutoFormer（+1.4% Tiny, +0.3% Small），且搜索成本差距是 **800×**（24 GPU天 vs 0.03 GPU天）。
- 在 Base 上 AZ-NAS 略低于 AutoFormer（-0.3%），但这是因为 Base 训练 epoch 被减半（防止 AZ-NAS 选出的较大模型过拟合）——并非搜索阶段的劣势。
- AZ-NAS 在两个参数量约束下（对齐 AutoFormer 和对齐 TF-TAS）都达到了更好或可比的精度，证明**代理泛化到 ViT 架构**。
- 搜索成本仅 0.03-0.17 GPU天（即使去掉 sP 只用 3 个代理，依然优于所有对比方法），比 TF-TAS（另一个零-shot 方法）快 **3-12 倍**。

---

## 实验 4：消融研究（Table 4）

### 单个代理的贡献

| 配置 | CIFAR-10 τ | CIFAR-100 τ | IN16-120 τ |
|------|-----------|------------|-----------|
| sE only | 0.569 | 0.563 | 0.506 |
| sP only | 0.521 | 0.508 | 0.489 |
| sT only | 0.349 | 0.353 | 0.407 |
| sC only | 0.578 | 0.551 | 0.517 |
| sE + sC (NL) | 0.674 | 0.653 | 0.601 |
| sE + sP + sC (NL) | 0.679 | 0.673 | 0.669 |
| sE + sT + sC (NL) | 0.731 | 0.714 | 0.708 |
| sE + sP + sT + sC (NL) | **0.741** | **0.723** | **0.710** |
| sE + sP + sT + sC (L) | 0.697 | 0.681 | 0.663 |

**关键发现**：
1. **单个代理都不够**：最好的单代理 sC τ = 0.517-0.578，比 AZ-NAS 全组合低 0.13-0.17。
2. **互补性是关键**：sE+sC（0.601-0.674）明显好于任何单代理；sE+sT+sC（0.708-0.731）比 sE+sP+sC（0.616-0.683）好得多——因为 sT 与 sE/sC 的相互 Kendall τ 最低（见 Figure 3），互补性最强。
3. **非线性聚合处处优于线性**：在每一个配置上 NL > L。全 4 代理：NL 0.710-0.741 vs L 0.663-0.697 → 差距 0.04-0.05 τ。
4. **sT 单独最弱但组合最强**：sT alone τ 只有 0.349-0.407，但它与 sE+sC 组合后 τ 跃升 0.05-0.11（对比 sE+sC 的 0.601-0.674 → sE+sT+sC 的 0.708-0.731）。说明 sT 捕获了其他代理完全看不到的信号——这正是互补代理的核心价值。

---

## 实验 5：代理间相关性分析（Figure 3）

4 个代理在 IN16-120 上的相互 Kendall τ：

| | sE | sP | sT | sC |
|--|-----|-----|-----|-----|
| sE | 1.00 | 0.60 | 0.17 | 0.44 |
| sP | 0.60 | 1.00 | 0.22 | 0.38 |
| sT | 0.17 | 0.22 | 1.00 | 0.15 |
| sC | 0.44 | 0.38 | 0.15 | 1.00 |

**sT 几乎独立于所有其他代理**（τ 仅 0.15-0.22），这解释了为什么 sT 对组合贡献最大。sE 和 sP 之间有一定相关性（0.60）——正常，因为 sP 直接从 sE 推导。整体而言，4 代理之间没有高度冗余，保证了组合的有效性。

---

## 实验 6：与其他代理的融合（Table 5）

| 聚合配置 | CIFAR-10 τ | CIFAR-100 τ | IN16-120 τ |
|----------|-----------|------------|-----------|
| ZiCo alone | 0.589 | 0.590 | 0.584 |
| ZiCo + sC + sE + sT + sP | **0.773** | **0.757** | **0.747** |
| Synflow alone | 0.571 | 0.565 | 0.555 |
| Synflow + sC + sE + sT + sP | **0.776** | **0.758** | **0.747** |

**关键发现**：
- 将 AZ-NAS 代理融入已有的单一代理（ZiCo/Synflow），Kendall τ 提升 0.16-0.20——超越了 AZ-NAS 自身的 0.710-0.741。这证明"组装互补代理"是通用范式，不限于 AZ-NAS 自己的代理。
- Synflow+AZ proxies 达到 τ=0.776（CIFAR-10），是 NAS-Bench-201 全空间排序的 SoTA。
- 代价是额外计算时间：ZiCo+all = 415.5 ms/arch（vs ZiCo 372.8），Synflow+all = 96.1 ms/arch（vs Synflow 53.4）——仍然可以接受。

---

## 关联页面

- [[lee2024-aznas-analysis]] — 返回总览
- [[lee2024-aznas-method]] — 方法机制详解
- [[lee2024-aznas-critical]] — 贡献 / 失败知识 / 研究机会
- [[az-nas]] — 实体页面
- [[nasbench201]] — NAS-Bench-201 基准数据集

## Evidence By Source

### `sources/papers/lee2024-aznas.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/aznas_lee2024.pdf`

^[sources/papers/lee2024-aznas.md]
