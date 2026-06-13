---
title: "AutoFormer"
created: 2026-06-13
updated: 2026-06-13
type: entity
tags: [neural-architecture-search, vision-transformer, weight-sharing-nas, one-shot-nas]
sources: [raw/papers/chen2021_autoformer.md]
---

# AutoFormer

AutoFormer 是首个专为 Vision Transformer (ViT) 设计的神经架构搜索方法，通过 Weight Entanglement 实现 one-shot supernet 训练，配合进化搜索自动发现高效 ViT 架构。

## 关键信息
- **类型**: model
- **提出**: Minghao Chen et al. (清华大学), 2021
- **发表**: ICCV 2021
- **核心贡献**: 首个 ViT 专用 NAS，Weight Entanglement 训练 one-shot supernet，自动搜索出的 AutoFormer 超越手工 ViT 和 CNN

## 架构要点

- **Weight Entanglement**: 不同深度的子网络共享 Core-Layer、ID-Layer 结构，梯度回传不分深度，实现 supernet 中所有子网的参数共享训练
- **设计空间**: embedding 维度、QKV 维度、头数、MLP ratio、深度等
- **One-Shot NAS**: 训练一次 Supernet，然后用进化搜索从中采样子架构评估
- **搜索目标**: 可在参数量/FLOPs 约束下搜索，支持多硬件延迟约束

## 关键结果

- AutoFormer-Tiny (5.7M) 在 ImageNet 上 74.7% Top-1 精度，超越 MobileViT
- 搜索成本: 24 GPU days（supernet 训练）+ 少量搜索时间
- 多个搜索架构在 ImageNet 分类、COCO 检测、ADE20K 分割上表现优异

## 关联页面
- [[chen2021-autoformer-analysis]] — 完整论文分析
