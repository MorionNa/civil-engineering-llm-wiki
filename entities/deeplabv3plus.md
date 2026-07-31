---
id: entities--deeplabv3plus
title: DeepLabv3+
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computer-vision
- entity/model
keywords:
- atrous-convolution
- depthwise-separable-convolution
- domain/computer-vision
- entity/model
- semantic-segmentation
sources:
- raw/papers/deepLabv3plus.pdf
created: '2026-06-13'
updated: '2026-07-31'
confidence: medium
---

# DeepLabv3+

DeepLabv3+ 是 DeepLab 系列的巅峰之作，采用 **ASPP encoder**（atrous spatial pyramid pooling）与 **simple decoder** 组合，引入 atrous separable convolution 实现速度与精度平衡，在 PASCAL VOC 2012 上达到 89.0% mIoU。

## 关键信息
- **类型**: model
- **提出**: Chen, Zhu, Papandreou, Schroff & Adam (Google), 2018
- **发表**: ECCV 2018
- **核心贡献**: Encoder-decoder + ASPP + atrous separable convolution，VOC 2012 SOTA 且计算高效

## 关联页面
- [[chen2018-deeplabv3plus-analysis]] — 论文完整分析

## Evidence By Source

### `raw/papers/deepLabv3plus.pdf`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/deepLabv3plus.pdf]

## Related Indexes

- [[entities/index]]
