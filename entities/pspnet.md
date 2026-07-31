---
id: entities--pspnet
title: PSPNet
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computer-vision
- entity/model
keywords:
- domain/computer-vision
- entity/model
- pyramid-pooling
- scene-parsing
- semantic-segmentation
sources:
- raw/papers/10_1145_3731195_abstract.txt
created: '2026-06-13'
updated: '2026-07-31'
confidence: medium
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

## Evidence By Source

### `raw/papers/10_1145_3731195_abstract.txt`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/10_1145_3731195_abstract.txt]

## Related Indexes

- [[entities/index]]
