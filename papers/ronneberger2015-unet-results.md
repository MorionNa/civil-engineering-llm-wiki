---
title: "U-Net 实验结果展开"
created: 2026-06-11
updated: 2026-06-11
type: paper-analysis
tags: [semantic-segmentation, small-dataset, biomedical-imaging]
sources: [raw/papers/ronneberger2015-unet.md]
confidence: high
---

# U-Net 实验结果

## 实验 1：ISBI EM Segmentation Challenge (2012)

**任务**：电子显微镜下的果蝇神经毡神经元膜分割。30 张 512×512 训练图。

**指标**：Warping Error（越低越好）、Rand Error、Pixel Error

| 排名 | 方法 | Warping Err | Rand Err | Pixel Err |
|:--:|------|:--:|:--:|:--:|
| human | — | 0.000005 | 0.0021 | 0.0010 |
| **1** | **U-Net** | **0.000353** | 0.0382 | 0.0611 |
| 2 | DIVE-SCI | 0.000355 | 0.0305 | 0.0584 |
| 3 | IDSIA (sliding-window CNN) | 0.000420 | 0.0504 | 0.0613 |

**关键**：U-Net 无需任何 pre/post-processing，7 个旋转版本平均。sliding-window CNN（Ciresan et al.）最好的结果需要 78 种不同后处理方案。

## 实验 2：ISBI Cell Tracking Challenge — PhC-U373

**任务**：相差显微镜下的胶质母细胞瘤细胞分割。35 张部分标注训练图。

| 方法 | IOU |
|------|:--:|
| **U-Net (2015)** | **92.03%** |
| Second-best 2015 | 83% |
| KTH-SE (2014) | 79.53% |

## 实验 3：ISBI Cell Tracking Challenge — DIC-HeLa

**任务**：微分干涉显微镜下的 HeLa 细胞分割。20 张部分标注训练图。

| 方法 | IOU |
|------|:--:|
| **U-Net (2015)** | **77.56%** |
| Second-best 2015 | 46% |
| KTH-SE (2014) | 46.07% |

**碾压级优势**：+31.6pp over second place。20 张训练图 + 弹性变形 = 比当时所有方法都好。

## 关键结论

- **训练样本量不是瓶颈**——30 张图 + 弹性变形 = SOTA。这对标注成本极高的结构图纸是个重要信号。
- **无后处理**：U-Net 的 raw output 直接可用，不像 sliding-window 需要复杂的后处理（78 种方案）才能达到类似精度。
- **跨模态泛化**：同一架构在 EM（电子显微镜）和相差/DIC（光学显微镜）上均最优——暗示对扫描图纸这类"非自然图像"同样适用。

## 关联页面
- [[ronneberger2015-unet-analysis]] — 全维度概述
- [[ronneberger2015-unet-method]] — 方法机制
- [[ronneberger2015-unet-critical]] — 贡献 + Negative + 可迁移
