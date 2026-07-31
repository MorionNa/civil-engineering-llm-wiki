---
id: entities--segformer
title: SegFormer
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computer-vision
- entity/model
- method/transformer
keywords:
- domain/computer-vision
- entity/model
- hierarchical-transformer
- method/transformer
- semantic-segmentation
- vision-transformer
sources:
- raw/papers/segformer.pdf
created: '2026-06-13'
updated: '2026-07-31'
confidence: medium
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

## Evidence By Source

### `raw/papers/segformer.pdf`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/segformer.pdf]

## Related Indexes

- [[entities/index]]
