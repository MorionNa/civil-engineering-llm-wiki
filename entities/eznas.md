---
id: entities--eznas
title: EZNAS
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/llm
- entity/dataset
- method/neural-architecture-search
- method/transformer
keywords:
- domain/llm
- entity/dataset
- evolutionary-search
- genetic-programming
- method/neural-architecture-search
- method/transformer
- neural-architecture-search
- training-free-nas
- zero-cost-proxy
sources:
- raw/papers/eznas_akhauri2022.pdf
created: '2026-06-15'
updated: '2026-07-31'
confidence: high
---

# EZNAS

EZNAS（Evolutionarily Generated Zero-Cost Neural Architecture Scoring Metric）是一种**基于遗传编程**自动发现零成本神经架构评分指标的方法。与手工设计的指标（如 synflow、NASWOT、TE-NAS）不同，EZNAS 通过进化表达式树来自动合成可解释、可泛化的架构评分程序。

## 关键信息

| 项目 | 内容 |
|------|------|
| **全称** | Evolutionarily Generated Zero-Cost Neural Architecture Scoring Metric |
| **类型** | NAS method / Zero-Cost Proxy Discovery |
| **作者** | Yash Akhauri (Cornell), J. Pablo Muñoz, Nilesh Jain, Ravi Iyer (Intel Labs) |
| **发表** | NeurIPS 2022 (arXiv:2209.07413) |
| **代码** | https://github.com/EzNAS/EZNAS |
| **核心贡献** | 首个自动化发现零成本 NAS 评分指标的框架；发现跨搜索空间泛化的 SoTA 指标 EZNAS-A |

## 核心机制

### 1. 表达式树程序表示

ZC-NASM 被表示为表达式树：终端节点 = 网络统计量（22 种），内部节点 = 数学运算（34 种），根节点 = 评分输出。树结构保证无冗余计算，使进化时间可控。

### 2. 网络统计量采集

对每个 ReLU-Conv2D-BatchNorm2D (RCB) 实例，用三种输入（数据 D、噪声 N、扰动 P）做一次前向/反向传播，采集 22 个张量（权重、激活、梯度）。

### 3. 进化搜索 + 抗过拟合评估

DEAP 框架，每代 50 个体，进化 15 代。适应度 = 在 4 个随机搜索空间上的**最低** Kendall τ → 强制程序跨空间泛化。

### 4. 发现的指标：EZNAS-A

仅在 NDS-DARTS CIFAR-10 上进化发现。本质是一种**非线性加权参数计数**——使用 T3GN（噪声权重梯度）作为输入，得分随通道数单调递增，对不同 kernel size 有非对称偏好。

## 关键结果

| Benchmark | 数据集 | 最佳指标 | EZNAS-A | 次优方法 | 次优值 |
|-----------|--------|----------|:--:|------|:--:|
| NAS-Bench-201 | CIFAR-10 | Kendall τ | **0.65** | NASWOT | 0.57 |
| NAS-Bench-201 | CIFAR-100 | Kendall τ | **0.65** | NASWOT | 0.61 |
| NAS-Bench-201 | ImageNet-16-120 | Kendall τ | **0.61** | NASWOT | 0.55 |
| NDS CIFAR-10 | DARTS | Kendall τ | **0.56** | FLOPs | 0.51 |
| NDS CIFAR-10 | Amoeba | Kendall τ | **0.45** | NASWOT | 0.22 |
| NATS-Bench SSS | CIFAR-10 | Spearman ρ | **0.89** | NASWOT | 0.45 |
| NDS ImageNet | DARTS | Spearman ρ | **0.70** | — | — |

- **进化搜索碳足迹**：358.6g CO₂e（vs 一次 NAS 搜索 4.49kg）
- **搜索加速**：端到端 NAS 效率提升 >100×

## 与相关方法的关系

### vs [[te-nas]] (Chen et al., ICLR 2021)

TE-NAS 是**手工设计**的零成本代理（NTK 条件数 + 线性区域数），在 NAS-Bench-201 上 Kendall τ ≈ 0.5-0.7。EZNAS 的进化发现范式与之互补——

- TE-NAS 的指标源自深度学习理论（NTK），是**理论驱动**的
- EZNAS 的指标源自数据驱动的进化搜索，是**经验驱动**的
- 两者殊途同归：都证明初始化统计量蕴含架构质量信号
- EZNAS-A 在泛化性上更强（跨 NDS 空间），但 TE-NAS 的双指标分析给出了可训练性/表达能力的理论解耦

### vs NAGO (Ru et al., 2020)

NAGO 使用神经架构生成优化进行 NAS，属于训练式方法。EZNAS 与之正交——EZNAS 生成的零成本代理**可以替代** NAGO 中昂贵的训练评估步骤，加速任意训练式 NAS 方法。

### vs AZ-NAS（零成本代理方法类）

AZ-NAS 泛指自动化零成本 NAS 方法。EZNAS 是目前该类别中最系统的工作——首个用遗传编程端到端自动合成代理程序的方法。后续工作的改进方向包括：引入连接编码、多输入比较操作、动态超参数优化。

### vs [[training-free-nas-transformers]]

Serianni & Kalita (2023) 将训练-free NAS 拓展到 RNN 和 Transformer，发现了"参数量陷阱"。EZNAS 的进化框架可以直接迁移到 Transformer 搜索空间——只需重新设计统计量采集（attention 层的 Q/K/V 权重和注意力矩阵）和操作集（如添加注意力专用的操作）。

## 局限性

- Top 10% 最佳架构无法有效区分（ZC-NASM 共性局限）
- 连接拓扑信息完全丢失（所有层的 mean 聚合）
- 仅支持 RCB/CBR 固定结构，不适用于 Transformer、RNN
- 操作空间无可调标量超参数
- batch size=1 时方差大，增大 batch 线性增加内存

## 关联页面

- [[akhauri2022-eznas-analysis]] — 完整论文分析（12 维度）
- [[akhauri2022-eznas-method]] — 遗传编程框架与表达式树详解
- [[akhauri2022-eznas-results]] — 完整实验结果与相关性数据
- [[akhauri2022-eznas-critical]] — 批判性分析：贡献、局限、可迁移、未来方向
- [[nasbench201]] — NAS-Bench-201 基准数据集
- [[te-nas]] — TE-NAS 实体（手工设计的零成本代理）
- [[training-free-nas-transformers]] — 训练-free NAS 到 Transformer 的拓展（可通过 EZNAS 框架进一步自动化）

## Evidence By Source

### `raw/papers/eznas_akhauri2022.pdf`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/eznas_akhauri2022.pdf]
