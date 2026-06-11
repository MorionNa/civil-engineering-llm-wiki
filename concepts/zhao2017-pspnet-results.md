---
title: "PSPNet 实验结果展开"
created: 2026-06-11
updated: 2026-06-11
type: concept
tags: [semantic-segmentation, scene-parsing, pyramid-pooling, sota, multi-scale-testing]
sources: [raw/papers/1612.01105v2.pdf]
results: [ade20k-champion, pascal-voc-85.4-mIoU, cityscapes-80.2]
datasets: [ade20k, pascal-voc-2012, cityscapes]
confidence: high
---

# PSPNet 实验结果

> 父页面：[[zhao2017-pspnet-analysis]]

## 实验一：ADE20K (ImageNet Scene Parsing Challenge 2016)

### 数据集

150 类（object + stuff），1038 场景标签。20K train / 2K val / 3K test。被论文认为是**最具挑战性**的场景解析数据集。

### PPM Ablation

| 配置 | Mean IoU (%) | Pixel Acc. (%) |
|------|-------------|----------------|
| ResNet50 Baseline (dilated FCN) | 37.23 | 78.01 |
| + B1 + MAX (global max pool) | 39.94 | 79.46 |
| + B1 + AVE (global avg pool) | 40.07 | 79.52 |
| + B1236 + MAX (4-level max) | 40.18 | 79.45 |
| + B1236 + AVE (4-level avg) | 41.07 | 79.97 |
| + B1236 + MAX + DR | 40.87 | 79.61 |
| + **B1236 + AVE + DR (PSPNet)** | **41.68** | **80.04** |

**结论**：Average > Max；4-level > 1-level；Dimension Reduction 有利。

### Auxiliary Loss Ablation

| Loss Weight α | Mean IoU (%) | Pixel Acc. (%) |
|--------------|-------------|----------------|
| 无 AL | 35.82 | 77.07 |
| α=0.3 | 37.01 | 77.87 |
| **α=0.4** | **37.23** | **78.01** |
| α=0.6 | 37.09 | 77.84 |
| α=0.9 | 36.99 | 77.87 |

**α=0.4 最优**，基线提升 +1.41 IoU。

### Backbone Depth

| Backbone | Mean IoU (%) | Pixel Acc. (%) |
|----------|-------------|----------------|
| ResNet50 | 41.68 | 80.04 |
| ResNet101 | 41.96 | 80.64 |
| ResNet152 | 42.62 | 80.80 |
| ResNet269 | 43.81 | 80.88 |
| ResNet269 + MS | **44.94** | **81.69** |

(IoU+Acc)/2 均值：从 60.86 (50) → 62.35 (269)，+1.49 绝对提升。

### 组件累积分解

| 配置 | Mean IoU → | Pixel Acc. → |
|------|-----------|-------------|
| ResNet50 Baseline | 34.28 | 76.35 |
| + Data Augmentation | 35.82 (+1.54) | 77.07 (+0.72) |
| + Auxiliary Loss | 37.23 (+1.41) | 78.01 (+0.94) |
| + PSP Module | 41.68 (+4.45) | 80.04 (+2.03) |
| → ResNet269 | 43.81 (+2.13) | 80.88 (+0.84) |
| + Multi-Scale Testing | 44.94 (+1.13) | 81.69 (+0.81) |

**最大单次提升来自 PPM**（+4.45 IoU），远超数据增强和辅助 loss 之和。

### Challenge 排名

| Rank | Team | Final Score (%) |
|------|------|----------------|
| **1** | **PSPNet (Ours)** | **57.21** |
| 2 | Adelaide | 56.74 |
| — | (PSPNet single model) | (55.38) |
| 3 | 360+MCG-ICT-CAS SP | 55.56 |
| 4 | SegModel | 54.65 |
| — | DilatedNet | 45.67 |
| — | FCN | 44.80 |

**单模型已超过其他团队的多模型集成**。

## 实验二：PASCAL VOC 2012

### 数据集

20 类 + 背景，10,582 train / 1,449 val / 1,456 test（增强标注）。

### 结果

| 配置 | mIoU (%) |
|------|---------|
| PSPNet (ResNet101, 仅 VOC) | **82.6** |
| PSPNet (+ MS-COCO pretrain) | **85.4** |
| DeepLab-CRF (ResNet101) | ~77 |
| CRF-RNN | 72.0 |
| DeconvNet | 72.5 |
| DPN | 74.1 |

**仅 VOC 训练的 PSPNet 已超过使用 MS-COCO 预训练的 DeepLab-CRF**。MS-COCO 预训练后 85.4%，20 类中 19 类最高。

**关键点**：未使用 CRF 后处理（DeepLab 用了），推理更快。

## 实验三：Cityscapes

### 数据集

5,000 张精细标注的城市街道图像，来自 50 个城市。

### 结果

**80.2% mIoU**，1st place。论文的 Table 仅有宣称，详细 per-class 结果见 Cityscapes benchmark 网站。

## 可视化分析

论文展示了三类典型 FCN 错误在 PSPNet 下的修正：
- **船→车**（行 1）：PSPNet 利用"船在河上"的场景上下文正确分类
- **building/skyscraper 混淆**（行 2）：PPM 的全局类别线索消除歧义
- **枕头漏检**（行 3）：子区域池化捕捉小物体

## 关联页面
- [[zhao2017-pspnet-analysis]] — 总览
- [[ronneberger2015-unet-results]] — U-Net 结果对比（ISBI 挑战赛）
