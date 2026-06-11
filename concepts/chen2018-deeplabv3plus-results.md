---
title: "DeepLabv3+ 实验结果展开"
created: 2026-06-11
updated: 2026-06-11
type: concept
tags: [semantic-segmentation, encoder-decoder, atrous-convolution, sota]
sources: [raw/papers/deepLabv3plus.pdf]
results: [pascal-voc-89.0, cityscapes-82.1, trimap-boundary, coco-pretraining, jft-pretraining]
datasets: [pascal-voc-2012, cityscapes, ms-coco, imagenet, jft-300m]
confidence: high
---

# DeepLabv3+ 实验结果

> 父页面：[[chen2018-deeplabv3plus-analysis]]

## 实验一：Decoder 设计选择（VOC 2012 val, ResNet-101）

### 1×1 降维通道数

| 通道数 | 8 | 16 | 32 | **48** | 64 |
|--------|----|----|----|----|----|
| mIoU (%) | 77.61 | 77.92 | 78.16 | **78.21** | 77.94 |

**48 最优** — 太少信息不足，太多压过 encoder 特征（encoder 仅 256ch）。

### Decoder 卷积结构

| Low-level 特征 | 3×3 Conv 结构 | mIoU (%) |
|---------------|---------------|---------|
| Conv2 | [3×3, 256] | 78.21 |
| Conv2 | **[3×3, 256] ×2** | **78.85** |
| Conv2 | [3×3, 256] ×3 | 78.02 |
| Conv2 | [3×3, 128] | 77.25 |
| Conv2 | [1×1, 256] | 78.07 |
| Conv2+Conv3 | [3×3, 256] | 78.61 |

**关键发现**：
- 2 个 3×3 conv 最优（1 个太少，3 个过度）
- **类似 U-Net 的多层 skip connection (Conv2+Conv3) 无额外收益**（78.61 < 78.85）
- 1×1 conv 显著不如 3×3

## 实验二：ResNet-101 推理策略（VOC 2012 val）

| train OS | eval OS | Decoder | MS | Flip | mIoU (%) | Multiply-Adds |
|----------|---------|---------|----|------|----------|-------------|
| 16 | 16 | | | | 77.21 | 81.02B |
| 16 | 16 | ✓ | | | **78.85** | 101.28B |
| 16 | 16 | ✓ | ✓ | | 80.09 | 898.69B |
| 16 | 16 | ✓ | ✓ | ✓ | 80.22 | 1797.23B |
| 16 | 8 | ✓ | | | 79.35 | 297.92B |
| 16 | 8 | ✓ | ✓ | ✓ | **80.57** | 5247.07B |
| 32 | 32 | ✓ | | | 77.37 | 74.20B |
| 32 | 16 | ✓ | | | 77.80 | 101.28B |

**Decoder 增益**：+1.64%（eval OS=16）/ +0.84%（eval OS=8），仅增加 ~20B Multiply-Adds。

**train OS=32**：推理快（74B），但始终比 OS=16 低 1-1.5%。

## 实验三：Xception Backbone（VOC 2012 val）

| 配置 | mIoU (%) | Multiply-Adds |
|------|----------|-------------|
| Xception baseline (无 decoder) | 79.17 | 68.00B |
| + Decoder | **79.93** | 89.76B |
| + Decoder + MS + Flip | **81.38** | 790.12B |
| + Atrous Separable Conv (SC) | 79.79 | **54.17B** (−41%) |
| + SC + MS + Flip | 81.21 | 928.81B |
| + COCO pretrain | 82.20 | 54.17B |
| + COCO + JFT pretrain | **84.22** | 928.81B |
| + COCO + JFT + eval OS=8 + MS + Flip | **84.56** | 3055.35B |

**Atrous Separable Conv 效果**：Multiply-Adds 降 33-41%，mIoU 持平。

**预训练递进**：Xception → +Decoder (+0.76%) → +SC (持平, −41% 计算) → +COCO (+2.01%) → +JFT (+2.02%)。

## 实验四：PASCAL VOC 2012 Test Set（SOTA 对比）

| Method | mIoU (%) |
|--------|---------|
| Deep Layer Cascade | 82.7 |
| Large Kernel Matters | 83.6 |
| RefineNet | 84.2 |
| PSPNet | 85.4 |
| DeepLabv3 | 85.7 |
| DeepLabv3-JFT | 86.9 |
| DIS | 86.8 |
| **DeepLabv3+ (Xception)** | **87.8** |
| **DeepLabv3+ (Xception-JFT)** | **89.0** |

**无 JFT 即超 DeepLabv3-JFT**（87.8 > 86.9）。有 JFT 达到 89.0%。

## 实验五：Cityscapes

### Val Set Ablation

| Backbone | Decoder | ASPP | Image-Level | mIoU (%) |
|----------|---------|------|-------------|---------|
| X-65 | | ✓ | ✓ | 77.33 |
| X-65 | ✓ | ✓ | ✓ | 78.79 |
| X-65 | ✓ | ✓ | | **79.14** |
| X-71 | ✓ | ✓ | | **79.55** |

**意外发现**：Image-level feature 在 Cityscapes 上有害（79.14 > 78.79），与 VOC 相反。

### Test Set SOTA

| Method | mIoU (%) |
|--------|---------|
| ResNet-38 | 80.6 |
| PSPNet | 81.2 |
| Mapillary | 82.0 |
| DeepLabv3 | 81.3 |
| **DeepLabv3+** | **82.1** |

## 实验六：边界 Trimap 分析

在 "void" 标签周围膨胀不同宽度的 trimap band，计算 band 内像素的 mIoU：

| Trimap Width | ResNet-101 (BU) | ResNet-101 (Decoder) | Xception (BU) | Xception (Decoder) |
|-------------|----------------|---------------------|--------------|-------------------|
| 最窄 (~1px) | baseline | **+4.8%** | baseline | **+5.4%** |
| 中等 | baseline | +2~3% | baseline | +3~4% |
| 宽 | baseline | +1% | baseline | +1% |

**Decoder 在紧邻边界处提升最大**，验证了 "恢复锐利边界" 的设计目标。

## 失败案例

论文展示三类典型失败：
1. **Sofa vs Chair**：外观相似类别混淆
2. **严重遮挡**：被遮挡物体分割不完整
3. **罕见视角**：从未见过的物体角度

## 关联页面
- [[chen2018-deeplabv3plus-analysis]] — 总览
- [[zhao2017-pspnet-results]] — PSPNet 结果对比
- [[ronneberger2015-unet-results]] — U-Net 挑战赛结果
