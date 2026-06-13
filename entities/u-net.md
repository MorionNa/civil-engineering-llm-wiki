---
title: "U-Net"
created: 2026-06-13
updated: 2026-06-13
type: entity
tags: [semantic-segmentation, encoder-decoder, skip-connections, biomedical-imaging]
sources: [raw/papers/ronneberger2015-unet.md]
---

# U-Net

U-Net 是一种对称的 encoder-decoder 卷积架构，通过 skip connections 将编码器特征直接传递到解码器，实现了**小样本下的精确语义分割**。最初为生物医学图像分割设计，现已成为语义分割领域的基础范式。

## 关键信息
- **类型**: model
- **提出**: Ronneberger, Fischer & Brox (University of Freiburg), 2015
- **发表**: MICCAI 2015
- **核心贡献**: Skip connections + 对称 encoder-decoder，开创小样本语义分割范式，仅需少量标注图像即可训练

## 关联页面
- [[ronneberger2015-unet-analysis]] — 论文完整分析
