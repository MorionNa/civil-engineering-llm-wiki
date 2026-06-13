---
title: "PSPNet"
created: 2026-06-13
updated: 2026-06-13
type: entity
tags: [semantic-segmentation, pyramid-pooling, scene-parsing]
sources: [raw/papers/10_1145_3731195_abstract.txt]
---

# PSPNet

Pyramid Scene Parsing Network (PSPNet) 引入 **Pyramid Pooling Module**，通过四级不同尺度的池化操作聚合全局和局部上下文信息，配合带辅助损失的深度监督 ResNet，在 ImageNet 2016 场景解析挑战赛中夺冠。

## 关键信息
- **类型**: model
- **提出**: Zhao, Shi, Qi, Wang & Jia (CUHK / SenseTime), 2017
- **发表**: CVPR 2017
- **核心贡献**: Pyramid Pooling Module 实现多尺度上下文聚合，解决场景解析中的类混淆和不可见类问题

## 关联页面
- [[zhao2017-pspnet-analysis]] — 论文完整分析
