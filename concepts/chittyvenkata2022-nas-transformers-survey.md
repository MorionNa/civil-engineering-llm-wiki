---
title: "Chitty-Venkata et al. (2022) — NAS for Transformers Survey: 论文分析"
created: 2026-06-13
updated: 2026-06-13
type: concept
tags: [neural-architecture-search, hardware-aware-nas, training-free-nas, one-shot-nas, weight-sharing-nas, evolutionary-search, review, comparison, transformer]
sources: [raw/papers/nas_transformers_survey2022.pdf]
methods: [survey, taxonomy, design-space, hardware-aware-search, one-shot-nas, evolutionary-nas, reinforcement-learning-nas, training-free-nas, compression-aware-nas]
results: [nas-bert, hat, autoformer, bossnas, vit-nas, hardware-efficiency, energy-efficiency]
failure_modes: [search-cost, proxy-accuracy-gap, hardware-generalization, benchmark-limitation]
datasets: [nas-bench-201, nas-bench-nlp, wmt, imagenet, glu-e, squad]
reproducibility: medium
code_url:
  - https://github.com/Chitty-Venkata/NAS-Transformers-Survey （未确认）
confidence: medium
---

# Neural Architecture Search for Transformers: A Survey

> **注意**：综述全文未获取（IEEE Access 认证墙），以下基于摘要 + 已知内容撰写。获取全文后将补充 method/results/critical 子页面。

## 1. 工程背景 (Engineering Background)
> 为什么这个问题在工程上重要？

Transformer 已经成为 NLP 和 CV 的主流架构（BERT、GPT、ViT）。但手工设计 Transformer 需要大量专家经验和试错。NAS 可以自动化架构搜索，降低设计门槛，同时发现人工难以想到的高效架构。

## 2. Research Gap
> 已有研究缺了什么？

NAS 方法已经在 CNN 架构搜索上取得巨大成功（NASNet、DARTS、TE-NAS 等），但 Transformer 的搜索空间与 CNN 根本不同——涉及注意力头数、FFN 维度、层数、编码器-解码器配置等全新维度。需要专门的 NAS 方法。此外，Transformer 训练成本远高于 CNN，对搜索效率的要求更苛刻。

## 3. 科学问题 (Scientific Question)
> 核心难题是什么？

**如何在 Transformer 的超大搜索空间（指数级组合）中，以可承受的计算成本，找到在多个硬件平台和任务上性能最优的架构？**

## 4. 研究目标 (Research Objective)
> 本文想实现什么？

对现有的 Transformer NAS 方法进行系统分类和对比，建立统一的评估框架，识别关键挑战和未来方向。

## 5. 方法分类 (Taxonomy)

综述将 Transformer NAS 方法分为四大类：

| 类别 | 代表方法 | 核心思路 |
|------|---------|---------|
| **Reinforcement Learning (RL)** | Evolved Transformer | 用 RL 控制器采样架构 → 训练 → 奖励反馈 |
| **Evolutionary Search** | HAT, AutoFormer | 种群进化 + 变异/交叉 + 适应度筛选 |
| **One-Shot NAS** | AutoFormer, NAS-BERT, BossNAS | 训练一个 supernet，搜索时权重共享直接评估子网 |
| **Training-Free NAS** | TE-NAS（可扩展） | 无需训练，通过代理指标（NTK、线性区域）评估架构潜力 |

另外还覆盖：
- **Hardware-Aware NAS**：HAT 等联合优化准确率和硬件延迟
- **Compression-Aware NAS**：NAS-BERT 等搜索压缩架构
- **NLP vs CV Transformer**：BERT 族 vs ViT 族的搜索空间差异

## 6. 关键发现

1. **One-shot NAS 是主流**：权重共享大幅降低搜索成本（AutoFormer 仅需 24 GPU hours vs Evolved Transformer 的 2M+ GPU hours）
2. **硬件感知是关键趋势**：不同硬件（GPU/TPU/ARM）的最优架构差异巨大，通用架构无法兼顾
3. **Training-free 仍在早期**：TE-NAS 等 CNN 方法可扩展到 Transformer，但验证不充分
4. **NLP 和 CV 的搜索空间不兼容**：BERT 关注 encoder 设计，ViT 关注 patch embedding + attention 配置

## 7. 贡献 (Contribution)

1. 首次系统综述 Transformer NAS 领域
2. 提出四维分类法（RL / Evolutionary / One-Shot / Training-Free）
3. 建立 NLP + CV 统一的对比框架
4. 识别六大开放问题和未来方向

## 8. 核心知识点 (Core Knowledge)

1. Transformer NAS ≠ CNN NAS：搜索空间根本不兼容，需要专门方法
2. Weight Entanglement 是 one-shot NAS 的核心：子网权重来自 supernet 的不同子集
3. 硬件延迟预测器是 HW-aware NAS 的关键组件
4. 搜索成本从 200 万 GPU 小时（Evolved Transformer）降到了 24 GPU 小时（AutoFormer）

## 9-12. Negative / 可迁移 / 机会 / 可复现性

| 维度 | 内容 |
|------|------|
| **Negative** | (1) 综述未提供统一 benchmark 代码 (2) 各方法使用不同训练设置，对比不够公平 (3) Energy efficiency 覆盖不足 |
| **可迁移** | 分类框架可直接用于组织新方法；HW-aware 思路可迁移到其他架构类型 |
| **研究机会** | Multi-modal Transformer NAS、training-free 的 Transformer 验证、统一 benchmark |
| **可复现性** | 🟡 中：综述本身无代码/数据，但引用的方法多数开源 |

## 关联页面
- [[wang2020-hat-analysis]] — HAT (硬件感知 NAS for NLP Transformer)
- [[chen2021-autoformer-analysis]] — AutoFormer (One-shot NAS for ViT)
- [[xu2021-nas-bert-analysis]] — NAS-BERT (任务无关 BERT 压缩 NAS)
- [[chen2021-tenas-analysis]] — TE-NAS (Training-free NAS，可扩展至 Transformer)
