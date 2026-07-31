---
id: entities--autoformer
title: AutoFormer
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- entity/model
- method/neural-architecture-search
- method/transformer
keywords:
- entity/model
- method/neural-architecture-search
- method/transformer
- neural-architecture-search
- one-shot-nas
- vision-transformer
- weight-sharing-nas
sources:
- raw/papers/chen2021_autoformer.md
created: '2026-06-13'
updated: '2026-07-31'
confidence: medium
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

## Evidence By Source

### `raw/papers/chen2021_autoformer.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/chen2021_autoformer.md]

## Related Indexes

- [[entities/index]]
