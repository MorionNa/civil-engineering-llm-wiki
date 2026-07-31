---
id: entities--hrnet
title: HRNet
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computer-vision
- entity/model
keywords:
- domain/computer-vision
- entity/model
- high-resolution-representation
- multi-resolution-fusion
- semantic-segmentation
sources:
- raw/papers/arxiv_1904.04514.pdf
created: '2026-06-13'
updated: '2026-07-31'
confidence: medium
---

# HRNet

HRNet (High-Resolution Network) 全程保持高分辨率表示，通过并行的多分辨率卷积分支与反复的多尺度融合，避免传统 encoder-decoder 架构中的分辨率损失，在 Cityscapes 语义分割上达到 81.6% mIoU。

## 关键信息
- **类型**: model
- **提出**: Sun, Xiao, Liu, Wang et al. (Microsoft Research / USTC), 2019
- **发表**: CVPR 2019 (oral); PAMI 2021 (journal extension)
- **核心贡献**: 全程高分辨率并行卷积 + 多分辨率反复融合，空间精度显著优于先降后升的架构

## 关联页面
- [[sun2019-hrnetv2-analysis]] — HRNetV2 论文完整分析

## Evidence By Source

### `raw/papers/arxiv_1904.04514.pdf`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/arxiv_1904.04514.pdf]

## Related Indexes

- [[entities/index]]
