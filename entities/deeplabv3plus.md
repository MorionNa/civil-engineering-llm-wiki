---
title: "DeepLabv3+"
created: 2026-06-13
updated: 2026-06-13
type: entity
tags: [semantic-segmentation, atrous-convolution, depthwise-separable-convolution]
sources: [raw/papers/deepLabv3plus.pdf]
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
