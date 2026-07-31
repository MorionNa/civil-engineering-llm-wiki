---
id: entities--cityscapes
title: Cityscapes
type: entity
status: draft
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/computer-vision
- entity/dataset
keywords:
- autonomous-driving
- benchmark
- dataset
- domain/civil-engineering
- domain/computer-vision
- entity/dataset
- semantic-segmentation
sources: []
created: '2026-06-13'
updated: '2026-07-31'
confidence: high
---

# Cityscapes

Cordts et al. (CVPR 2016) 提出的城市场景理解基准数据集。包含 5,000 张精细标注图像和 20,000 张粗标注图像，覆盖 19 个语义类别，是自动驾驶与语义分割领域的标准评测平台。

## 关键信息

- **类型**: dataset / benchmark
- **作者**: Marius Cordts, Mohamed Omran, Sebastian Ramos, et al. (Daimler AG, MPI, TU Darmstadt)
- **发表**: CVPR 2016
- **规模**: 5,000 fine + 20,000 coarse 标注，19 个类别（另有 29/30 类扩展标注）
- **核心贡献/角色**: 城市场景语义分割标准 benchmark，几乎所有主流分割方法必评测的数据集

## 数据集特点

- 采集自 50 个德国城市街景（春/夏/秋三季）
- 图像分辨率 1024×2048
- 19 类标准标注：road, sidewalk, building, car, pedestrian, bicycle, vegetation, sky, person, rider, truck, bus, train, motorcycle, wall, fence, pole, traffic sign, traffic light
- 提供实例级分割标注（8 类可移动物体）

## 常用评测模型

- **DeepLabv3+** — 空洞卷积 + 编解码结构
- **PSPNet** — 金字塔池化模块
- **HRNet / HRNetV2** — 高分辨率表征保持

## 关联页面

- [[chen2018-deeplabv3plus-analysis]] — DeepLabv3+ 论文分析
- [[sun2019-hrnetv2-analysis]] — HRNetV2 论文分析
- [[ade20k]] — ADE20K 场景解析 benchmark

## Verification Needed

- This historical page has no explicit source record. Recover and verify the original evidence before changing `status` from `draft`.
