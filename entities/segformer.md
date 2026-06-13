---
title: "SegFormer"
created: 2026-06-13
updated: 2026-06-13
type: entity
tags: [semantic-segmentation, vision-transformer, hierarchical-transformer]
sources: [raw/papers/segformer.pdf]
---

# SegFormer

SegFormer 将 **hierarchical Transformer encoder** 与轻量 **All-MLP decoder** 结合，无需位置编码（positional encoding），在 ADE20K 上达到 51.8% mIoU，同时保持推理效率，是 Transformer 语义分割的代表作。

## 关键信息
- **类型**: model
- **提出**: Xie, Wang, Yu, Anandkumar, Alvarez & Luo (NVIDIA), 2021
- **发表**: NeurIPS 2021
- **核心贡献**: Hierarchical Transformer + MLP decoder 的统一分割框架，ADE20K SOTA

## 关联页面
- [[xie2021-segformer-analysis]] — 论文完整分析
