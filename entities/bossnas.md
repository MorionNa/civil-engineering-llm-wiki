---
title: "BossNAS"
created: 2026-06-14
updated: 2026-06-14
type: entity
tags: [nas-method, neural-architecture-search, self-supervised, hybrid-cnn-transformer, ensemble-bootstrapping, block-wise-nas, weight-sharing, hybra]
sources: [raw/papers/bossnas2021_iclr.pdf]
confidence: high
---

# BossNAS

Li et al. 在 ICLR 2021 提出的无监督块级神经架构搜索方法。通过 Ensemble Bootstrapping 自监督训练和种群中心评估，在不使用标签或教师模型的情况下实现高精度架构排序，并在自定义 HyTra 混合 CNN-Transformer 搜索空间中搜出超越 EfficientNet 的架构。

## 关键信息

- **全称**: Block-wisely Self-supervised Neural Architecture Search
- **类型**: NAS method
- **作者**: Changlin Li (Monash), Tao Tang (SYSU), Guangrun Wang (DarkMatter/Oxford), Jiefeng Peng, Bing Wang (Alibaba), Xiaodan Liang (SYSU), Xiaojun Chang (RMIT)
- **发表**: ICLR 2021
- **代码**: https://github.com/changlinli/BossNAS

## 核心组件

### 1. Ensemble Bootstrapping（训练）

双 Siamese 超级网络（在线网络 + EMA 网络）受 BYOL 启发。在线网络的每条路径学习预测 EMA 网络中**所有采样路径的概率集成**——为共享权重提供共同优化目标，解决超级网络自监督训练的不稳定性。

### 2. 向种群中心搜索（评估）

以整个块级搜索空间的预测集成为评价目标，计算每个候选架构与集成中心的 L2 距离作为无监督评分。可在块大小 ≤256 时遍历搜索。

### 3. HyTra 搜索空间

Fabric-like 混合 CNN-Transformer 搜索空间。候选块包括 ResConv（3×3 卷积残差瓶颈）和 ResAtt（带隐式深度可分离卷积位置编码的多头自注意力）。支持灵活下采样位置，总架构数 ≈ 2.8×10⁶。

## 关键结果

| 搜索空间 | 数据集 | 模型 | 性能 | 评分精度 (Spearman ρ) |
|----------|--------|------|------|----------------------|
| HyTra | ImageNet | BossNet-T1↑ | 82.5% Top-1 | - |
| MBConv | ImageNet | BossNet-M2 | 77.4% Top-1 | 0.78 |
| NATS-Bench SS | CIFAR-100 | - | 70.86% | 0.76 |

- 超越 EfficientNet-B2 2.4%（同推理时间）
- 超越 MnasNet 评分精度同时加速 28.8×（10 GPU-days vs 288 TPU-days）
- 超越有监督块级 NAS (DNA) 评分精度（τ=0.65 vs 0.62）

## 关联页面

- [[li2021-bossnas-analysis]] — 完整论文分析（12 维度）
- [[li2021-bossnas-method]] — Ensemble Bootstrapping 与 HyTra 搜索空间详解
- [[li2021-bossnas-results]] — ImageNet / CIFAR / 消融实验结果
- [[li2021-bossnas-critical]] — 批判性分析：贡献、局限、可迁移洞见

## 相关方法/实体

- [[nasbench201]] — NAS-Bench-201 benchmark（同领域 NAS 评测标准）
- [[chen2021-autoformer-analysis]] — AutoFormer（搜索纯 ViT 架构，有监督权重共享）
- [[chen2021-tenas-analysis]] — TE-NAS（训练无关 NAS，NTK + 线性区域数）
