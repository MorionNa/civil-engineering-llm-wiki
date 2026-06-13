---
title: "PSPNet 方法机制展开"
created: 2026-06-11
updated: 2026-06-11
type: paper-analysis
tags: [semantic-segmentation, pyramid-pooling, multi-scale-context, fully-convolutional, deep-supervision, auxiliary-loss]
sources: [raw/papers/1612.01105v2.pdf]
methods: [pyramid-pooling-module, auxiliary-loss, dilated-convolution, bilinear-upsample, poly-lr-schedule, dimension-reduction]
confidence: high
---

# PSPNet 方法机制

> 父页面：[[zhao2017-pspnet-analysis]]

## 整体架构

```
Input Image → ResNet Backbone (dilated) → Feature Map (1/8 size)
                                              │
                    ┌─────────────────────────┼─────────────────────────┐
                    │                         │                         │
              Pyramid Pooling Module      Auxiliary Loss           Master Loss
              (4-scale pooling)           (at res4b22)             (final output)
                    │
              Concat + Conv → Final Prediction
```

## Pyramid Pooling Module (PPM)

### 设计动机

CNN 的经验感受野远小于理论感受野（Zhou et al.），高层特征实际上只覆盖图像的局部区域。Global average pooling 提供全局上下文但丢失空间关系。PPM 的解决方案：**在不同尺度上对特征图做子区域池化，保留粗粒度空间结构的同时聚合全局信息**。

### 四级金字塔结构

| Level | Bin Size | 覆盖范围 | 含义 |
|-------|----------|---------|------|
| Red (coarsest) | 1×1 | 全图 | 全局场景类别 |
| Orange | 2×2 | 半图 | 上下/左右区域 |
| Blue | 3×3 | 1/3 图 | 中间粒度 |
| Green | 6×6 | 1/6 图 | 细粒度子区域 |

### 每级处理流程

```
Feature Map (H×W×C)
    ↓ Pooling (bin_size × bin_size)
Pooled Feature (bin_size × bin_size × C)
    ↓ 1×1 Conv (reduce channels to C/N, N=bin_size)
Reduced Feature (bin_size × bin_size × C/N)
    ↓ Bilinear Upsample (to H×W)
Upsampled Feature (H×W × C/N)
```

4 个 level 的 upsampled feature 与原特征图 **concat** → 最终特征。

### 设计要点

- **池化类型**：Average Pooling > Max Pooling（实验验证，average 在所有设置下都更好）
- **维度缩减**：1×1 conv 将通道数降至 1/N（N=pyramid level），保持全局特征的权重不过大
- **可调整性**：pyramid levels 数量和 bin sizes 可根据特征图尺寸修改

**参数量/计算量**：相比原始 dilated FCN 增加很小，end-to-end 联合优化。

## Deeply Supervised Loss

### 动机

深层 ResNet 的优化困难：后层主要学习残差，梯度传播路径长。传统解：ResNet 的 skip connection。本文方案：在中层加辅助监督信号，将优化问题分解。

### 实现

```
ResNet101 Architecture:
  conv1 → res2 → res3 → res4a...res4b21 → [res4b22] → res4b23... → res5 → ...
                                              │                    │
                                        Auxiliary Loss        Master Loss
                                        (α = 0.4)              (α = 1.0)
```

辅助分类器加在 **res4b22 残差块之后**（第 4 阶段末尾）。

### 与 Relay Backpropagation 的区别

- **Relay BP** [32]：阻塞辅助 loss 的反向传播，不让它影响浅层
- **本文**：两个 loss 都反向传播通过所有层。辅助 loss 帮助优化过程，主 loss 承担主要责任

辅助 loss 权重 α：实验搜索 0.3/0.4/0.6/0.9，**α=0.4 最优**（ResNet50 on ADE20K）。测试时丢弃辅助分支。

## 训练细节

| 参数 | 值 | 说明 |
|------|-----|------|
| LR policy | Poly: base=0.01, power=0.9 | `lr = base × (1 - iter/max_iter)^power` |
| Momentum | 0.9 | |
| Weight decay | 0.0001 | |
| Iterations | ADE20K: 150K, VOC: 30K, Cityscapes: 90K | |
| Batch size | 16 | Multi-GPU BN via OpenMPI (修改 Caffe) |
| Crop size | 适当大的 crop size 提升性能 | |
| Data augmentation | 随机镜像 + 随机缩放 (0.5-2×) | |
| | + 旋转 (-10°~10°) + 高斯模糊 | ADE20K 和 VOC 额外使用 |

### 多尺度测试 (Multi-Scale Testing)

测试时使用多个输入尺度，结果取平均。**对最终性能有显著贡献**（ADE20K 上 +1.13 Mean IoU），但单尺度推理会掉分——这是实际部署需注意的 trade-off。

## 与 U-Net 的对比

| 维度 | PSPNet | U-Net |
|------|--------|-------|
| 上下文策略 | 全局金字塔池化 | Skip connections（局部特征融合） |
| 上采样 | Bilinear interpolation | Transposed convolution |
| 全局信息 | 显式 PPM | 隐式（通过 encoder 深度） |
| 设计哲学 | "先看全局再看局部" | "细节和语义逐层融合" |

→ [[ronneberger2015-unet-method]]

## 关联页面
- [[zhao2017-pspnet-analysis]] — 总览
- [[ronneberger2015-unet-method]] — U-Net 方法对比
