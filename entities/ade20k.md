---
title: "ADE20K"
created: 2026-06-13
updated: 2026-06-13
type: entity
tags: [dataset, benchmark, semantic-segmentation, scene-parsing]
sources: []
confidence: high
---

# ADE20K

Zhou et al. (IJCV 2019) 发布的场景解析基准数据集。包含 20K 训练图像、2K 验证图像，标注 150 个语义类别，是语义分割领域最广泛使用的评测基准之一。

## 关键信息

- **类型**: dataset / benchmark
- **作者**: Bolei Zhou, Hang Zhao, Xavier Puig, Sanja Fidler, Adela Barriuso, Antonio Torralba (MIT / Toronto)
- **发表**: IJCV 2019
- **规模**: 20,210 训练 / 2,000 验证，150 个类别
- **核心贡献/角色**: 大规模、细粒度场景解析 benchmark，被 PSPNet、DeepLabv3+、HRNet、SegFormer 等主流方法采用

## 数据集特点

- 覆盖室内外多样化场景（卧室、街道、厨房、办公室、自然景观等）
- 150 个语义类别（物体 + 材料 + 场景成分）
- 提供实例级标注和部分全景分割标注
- 标注密度高，平均每张图 ~19 个物体实例

## 常用评测模型

- **PSPNet** (Zhao et al., CVPR 2017) — 金字塔池化模块
- **DeepLabv3+** (Chen et al., ECCV 2018) — 空洞卷积 + 编解码结构
- **HRNet / HRNetV2** (Sun et al., TPAMI 2020) — 高分辨率表征
- **SegFormer** (Xie et al., NeurIPS 2021) — Transformer 分割

## 关联页面

- [[zhao2017-pspnet-analysis]] — PSPNet 论文分析
- [[chen2018-deeplabv3plus-analysis]] — DeepLabv3+ 论文分析
- [[sun2019-hrnetv2-analysis]] — HRNetV2 论文分析
