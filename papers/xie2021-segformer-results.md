---
id: papers--xie2021-segformer-results
title: SegFormer 实验结果展开
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computer-vision
- evidence/paper
- method/transformer
keywords:
- benchmark
- semantic-segmentation
- vision-transformer
sources:
- sources/papers/xie2021-segformer.md
created: '2026-06-11'
updated: '2026-07-31'
confidence: high
results:
- ade20k-51.8
- cityscapes-84.0
- cityscapes-83.1-test
- coco-stuff-46.7
- zero-shot-robustness
datasets:
- ade20k
- cityscapes
- coco-stuff
- cityscapes-c
- mapillary-vistas
---

# SegFormer 实验结果

> 父页面：[[xie2021-segformer-analysis]]

## 实验一：ADE20K

### 效率对比（Table 2 上半部分 — 实时）

| Method | Encoder | Params ↓ | Flops ↓ | FPS ↑ | mIoU ↑ |
|--------|---------|----------|--------|-------|--------|
| FCN | MobileNetV2 | 9.8M | 39.6G | 64.4 | 19.7 |
| PSPNet | MobileNetV2 | 13.7M | 52.9G | 57.7 | 29.6 |
| DeepLabV3+ | MobileNetV2 | 15.4M | 69.4G | 43.1 | 34.0 |
| **SegFormer-B0** | MiT-B0 | **3.8M** | **8.4G** | **50.5** | **37.4** |

B0 参数仅 DeepLabV3+ 的 1/4，计算量 1/8，但 mIoU 高 3.4%。

### 精度对比（Table 2 下半部分 — 非实时）

| Method | Encoder | Params ↓ | Flops ↓ | FPS ↑ | mIoU ↑ |
|--------|---------|----------|--------|-------|--------|
| FCN | ResNet-101 | 68.6M | 275.7G | 14.8 | 41.4 |
| DeepLabV3+ | ResNet-101 | 62.7M | 255.1G | 14.1 | 44.1 |
| OCRNet | HRNet-W48 | 70.5M | 164.8G | 17.0 | 45.6 |
| SETR | ViT-Large | 318.3M | — | 5.4 | 50.2 |
| **SegFormer-B4** | MiT-B4 | **64.1M** | **95.7G** | **15.4** | **51.1** |
| **SegFormer-B5** | MiT-B5 | 84.7M | 183.3G | 9.8 | **51.8** |

B4: 50.3% (论文正文) / 51.1% (附录 Table 2)，**5× 小于 SETR 且高 2.2%**。B5: 51.8% SOTA。

## 实验二：Cityscapes

### Val Set

| Method | Params | Flops | FPS | mIoU |
|--------|--------|-------|-----|------|
| ICNet | — | — | 30.3 | 67.7 |
| DeepLabV3+ (MBv2) | 15.4M | 555.4G | 8.4 | 75.2 |
| **SegFormer-B0** (short=1024) | 3.8M | 125.5G | **15.2** | **76.2** |
| **SegFormer-B0** (short=512) | 3.8M | 17.7G | **47.6** | **71.9** |
| DeepLabV3+ (R101) | 62.7M | 2032.3G | 1.2 | 80.9 |
| OCRNet (HRNet-W48) | 70.5M | 1296.8G | 4.2 | 81.1 |
| SETR (ViT-Large) | 318.3M | — | 0.5 | 82.2 |
| **SegFormer-B4** | 64.1M | 1240.6G | 3.0 | **83.8** |
| **SegFormer-B5** | 84.7M | 1447.6G | 2.5 | **84.0** |

B5 84.0%，超 SETR 1.8% 且快 5×、小 4×。

### Test Set

| Method | Encoder | Extra Data | mIoU |
|--------|---------|-----------|------|
| PSPNet | ResNet-101 | IM-1K | 78.4 |
| CCNet | ResNet-101 | IM-1K | 81.9 |
| SETR | ViT | IM-22K | 81.0 |
| SETR | ViT | IM-22K + Coarse | 81.6 |
| **SegFormer-B5** | MiT-B5 | **IM-1K** | **82.2** |
| **SegFormer-B5** | MiT-B5 | IM-1K + Mapillary | **83.1** |

仅 ImageNet-1K 即超 SETR 的 ImageNet-22K + coarse 配置。

## 实验三：COCO-Stuff（172 类全量）

| Method | Encoder | Params | mIoU |
|--------|---------|--------|------|
| DeepLabV3+ | ResNet50 | 43.7M | 38.4 |
| OCRNet | HRNet-W48 | 70.5M | 42.3 |
| SETR | ViT | 305.7M | 45.8 |
| **SegFormer-B5** | MiT-B5 | **84.7M** | **46.7** |

## 实验四：Cityscapes-C 零样本鲁棒性

B5 在 16 种干扰上的 mIoU 对比（选摘）：

| 干扰类型 | DeepLabV3+ (X71) | **SegFormer-B5** | 相对提升 |
|---------|-----------------|------------------|---------|
| Clean | 78.6 | **82.4** | — |
| Gaussian Noise | 19.4 | **72.8** | **+275%** |
| Shot Noise | 41.2 | **82.8** (est.) | +101% |
| Impulse Noise | 14.9 | **57.8** | +288% |
| Snow | 18.8 | **40.7** | +116% |
| Fog | 64.1 | **78.5** | +22% |

**结论**：SegFormer 的鲁棒性远超 CNN，对安全关键应用意义重大。

## 实验五：Ablation Studies

### (a) MLP Decoder 维度 C

| C | Flops ↓ | Params ↓ | mIoU ↑ |
|---|---------|----------|--------|
| 256 | 25.7G | 24.7M | 44.9 |
| 512 | 39.8G | 25.8M | 45.0 |
| **768** | **62.4G** | **27.5M** | **45.4** |
| 1024 | 93.6G | 29.6M | 45.2 |
| 2048 | 304.4G | 43.4M | 45.6 |

C=768 最佳性价比。后续实验固定 C=768。

### (b) Mix-FFN vs PE（跨分辨率）

| 测试分辨率 | PE | Mix-FFN |
|-----------|-----|---------|
| 768×768 (训练) | 77.3 | **80.5** |
| 1024×2048 | 74.0 (−3.3) | **79.8** (−0.7) |

**关键**：Mix-FFN 不仅精度高，分辨率敏感性极低（−0.7% vs −3.3%）。

### (c) CNN vs Transformer + MLP Decoder

| Encoder | Feature | mIoU |
|---------|---------|------|
| ResNet50 | S1-4 | 34.7 |
| ResNet101 | S1-4 | 38.7 |
| ResNeXt101 | S1-4 | 39.8 |
| MiT-B2 | S4 only | 43.1 |
| **MiT-B2** | **S1-4** | **45.4** |

CNN+MLP decoder 完全失败。Transformer 必须用所有 stage。

## 关联页面
- [[xie2021-segformer-analysis]] — 总览
- [[chen2018-deeplabv3plus-results]] — DeepLabv3+ 结果对比
- [[sun2019-hrnetv2-results]] — HRNet 结果对比

## Evidence By Source

### `sources/papers/xie2021-segformer.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/segformer.pdf`

^[sources/papers/xie2021-segformer.md]
