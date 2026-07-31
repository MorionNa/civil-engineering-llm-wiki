---
id: papers--sun2019-hrnetv2-results
title: HRNetV2 实验结果展开
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computer-vision
- evidence/paper
keywords:
- benchmark
- high-resolution-representation
- hrnet
- semantic-segmentation
sources:
- sources/papers/sun2019-hrnetv2.md
created: '2026-06-11'
updated: '2026-07-31'
confidence: high
results:
- cityscapes-81.6
- pascal-context-54.0
- lip-sota
- aflw-sota
- 300w-sota
- coco-detection
datasets:
- cityscapes
- pascal-context
- lip
- aflw
- cofw
- 300w
- wflw
- coco
---

# HRNetV2 实验结果

> 父页面：[[sun2019-hrnetv2-analysis]]

## 实验一：Cityscapes 语义分割

### Val Set — 效率对比

| Method | Backbone | #Param | GFLOPs | mIoU (%) |
|--------|----------|--------|--------|---------|
| UNet++ | ResNet-101 | 59.5M | 748.5 | 75.5 |
| DeepLabv3 | Dilated-ResNet-101 | 58.0M | 1778.7 | 78.5 |
| DeepLabv3+ | Dilated-Xception-71 | 43.5M | 1444.6 | 79.6 |
| PSPNet | Dilated-ResNet-101 | 65.9M | 2017.6 | 79.7 |
| **HRNetV2-W40** | — | **45.2M** | **493.2** | **80.2** |
| **HRNetV2-W48** | — | **65.9M** | **747.3** | **81.1** |

**关键发现**：HRNetV2-W40 参数量与 DeepLabv3+ 相近，计算量仅 1/3，mIoU 高 0.6%。HRNetV2-W48 与 PSPNet 参数量相同，计算量仅 37%，mIoU 高 1.4%。

### Test Set

| Method | mIoU | iIoU cla. | IoU cat. | iIoU cat. |
|--------|------|-----------|---------|-----------|
| PSPNet | 78.4 | 56.7 | 90.6 | 78.6 |
| PSANet | 80.1 | — | — | — |
| DenseASPP | 80.6 | 59.1 | 90.9 | 78.1 |
| **HRNetV2-W48 (train)** | **80.4** | **59.2** | **91.5** | **80.8** |
| **HRNetV2-W48 (train+val)** | **81.6** | **61.8** | **92.1** | **82.2** |

仅 train set 训练即 80.4%，train+val 达 81.6%（全面超越所有对比方法）。

## 实验二：PASCAL Context 语义分割

| Method | Backbone | mIoU (59类) |
|--------|----------|------------|
| FCN-8s | VGG-16 | 35.1* |
| DeepLab-v2 | Dilated-ResNet-101 | 45.7* |
| RefineNet | ResNet-152 | 47.3* |
| PSPNet | Dilated-ResNet-101 | 47.8 |
| UNet++ | ResNet-101 | 47.7 |
| EncNet | Dilated-ResNet-101 | 52.6 |
| **HRNetV2-W48** | — | **54.0** |

*60 类评测

## 实验三：LIP 人体解析

HRNetV2 在 LIP 数据集上达到 SOTA，无需额外信息（姿态/边缘）。具体数值见论文 Table 6-8。

## 实验四：面部关键点检测

### AFLW (NME ↓)

| Method | NME |
|--------|-----|
| SAN | 1.91 |
| LAB (w/ boundary) | 1.85 |
| **HRNetV2-W18** | **1.57** |

### COFW (NME ↓, occlusion)

| Method | NME |
|--------|-----|
| DAC-CSR | 4.72 |
| LAB (w/ boundary) | 3.82 |
| **HRNetV2-W18** | **3.45** |

### 300W (full set, NME ↓)

| Method | Common | Challenging | Full |
|--------|--------|------------|------|
| LAB | 2.98 | 5.19 | 3.49 |
| **HRNetV2-W18** | **2.87** | **5.15** | **3.32** |

### WFLW (NME ↓)

HRNetV2-W18 在 WFLW 上同样最佳（论文 Table 11）。

**关键发现**：轻量 W18 模型在四个面部关键点数据集上均为 SOTA，验证了高分辨率表示对空间精度任务的普适优势。

## 实验五：COCO 目标检测（HRNetV2p）

| Backbone | Method | AP | AP₅₀ | AP₇₅ | AP_S | AP_M | AP_L |
|----------|--------|----|----|----|----|----|----|
| ResNet-101 | FPN | 38.5 | 59.4 | 41.9 | 21.4 | 42.1 | 50.6 |
| **HRNetV2p-W32** | Faster R-CNN | **39.4** | **60.4** | **43.0** | **22.3** | **42.8** | **51.7** |
| **HRNetV2p-W48** | Faster R-CNN | **40.5** | **61.4** | **44.2** | **23.0** | **43.8** | **53.3** |

**小物体 (AP_S) 提升尤为显著**：HRNetV2p-W32 比 ResNet-101-FPN 高 0.9 AP_S，W48 高 1.6 AP_S。

### Mask R-CNN 分割（COCO）

| Backbone | AP_bbox | AP_mask |
|----------|---------|---------|
| ResNet-101-FPN | 39.8 | 36.1 |
| **HRNetV2p-W32** | **41.0** | **37.0** |
| **HRNetV2p-W48** | **42.1** | **38.0** |

## 实验六：HRNetV1 vs HRNetV2 消融

| 任务 | 模型 | HRNetV1 | HRNetV1h | HRNetV2 |
|------|------|---------|----------|---------|
| Cityscapes (mIoU) | W18 | 76.9 | 77.4 | **79.0** |
| Cityscapes | W48 | 80.6 | 80.7 | **81.1** |
| PASCAL Context | W18 | 45.7 | 46.3 | **50.5** |
| PASCAL Context | W48 | 52.9 | 53.2 | **54.0** |
| COCO (AP) | W32 LS=1 | 37.4 | 37.8 | **39.4** |
| COCO (AP) | W32 LS=2 | 39.0 | 39.2 | **40.5** |

**HRNetV1h** = HRNetV1 + 1×1 conv 增大输出维度（不聚合低分辨率）。

**结论**：聚合低分辨率表示（V2）才是关键，仅增大输出维度（V1h）提升微小。小模型收益更显著（PASCAL Context W18: +4.8%）。

## 关联页面
- [[sun2019-hrnetv2-analysis]] — 总览
- [[zhao2017-pspnet-results]] — Cityscapes 对比
- [[chen2018-deeplabv3plus-results]] — Cityscapes/VOC 对比

## Evidence By Source

### `sources/papers/sun2019-hrnetv2.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/arxiv_1904.04514.pdf`

^[sources/papers/sun2019-hrnetv2.md]
