---
id: papers--chen2018-deeplabv3plus-method
title: DeepLabv3+ 方法机制展开
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computer-vision
- evidence/paper
keywords:
- aspp
- atrous-convolution
- atrous-separable-convolution
- depthwise-separable-convolution
- encoder-decoder
- semantic-segmentation
- xception
sources:
- sources/papers/chen2018-deeplabv3plus.md
created: '2026-06-11'
updated: '2026-07-31'
confidence: high
methods:
- aspp
- atrous-separable-convolution
- encoder-decoder
- output-stride
- depthwise-separable-convolution
- aligned-xception
- bilinear-upsample
---

# DeepLabv3+ 方法机制

> 父页面：[[chen2018-deeplabv3plus-analysis]]

## 整体架构

```
Input Image (H×W×3)
       │
       ▼
CNN Backbone (ResNet-101 / Modified Xception)
       │
       ├──────────────────────────────────────┐
       │                                      │
       ▼                                      ▼
  Low-Level Features                     ASPP Module
  (Conv2, stride=4)                      (atrous rates: 1,6,12,18
       │                                 + Image-level pooling)
       │                                      │
       │                                      ▼
       │                              Encoder Output
       │                              (stride=16, 256 channels)
       │                                      │
       │                              Bilinear Upsample ×4
       │                              (to stride=4)
       │                                      │
       ▼                                      ▼
  1×1 Conv ─────────────────────→  Concat
  (reduce to 48 channels)
                                        │
                                        ▼
                                   3×3 Conv ×2
                                   (256 filters)
                                        │
                                        ▼
                                   Bilinear Upsample ×4
                                        │
                                        ▼
                                   Final Prediction
                                   (H×W×num_classes)
```

## 一、Atrous Convolution（空洞卷积）

### 公式

$$y[i] = \sum_k x[i + r \cdot k] \cdot w[k]$$

其中 $r$ 为 atrous rate（膨胀率），控制采样步长。r=1 即标准卷积。

### 核心作用：输出 stride 控制

| 任务 | 原始输出 stride | Atrous 调整 |
|------|---------------|-----------|
| ImageNet 分类 | 32 | r=1（标准 conv） |
| 语义分割 | 16 | 最后 1 个 block：stride 改 r=2 |
| 密集预测 | 8 | 最后 2 个 block：r=2, r=4 |

**关键 insight**：在 ResNet-101 中，输出 stride=8 需要膨胀 9 层（3 个残差块 × 3 层）；输出 stride=4 需要膨胀 78 层 → GPU 显存爆炸。

## 二、Depthwise Separable Convolution

```
标准 Conv3×3:    输入 (H×W×C_in) → filters (3×3×C_in) → 输出 (H×W×C_out)
                 计算量: H×W×C_in×C_out×3×3

分解为:
  Depthwise:     输入 (H×W×C_in) → filters (3×3×1 per channel) → 输出 (H×W×C_in)
                 计算量: H×W×C_in×3×3

  Pointwise:     输入 (H×W×C_in) → 1×1 conv → 输出 (H×W×C_out)
                 计算量: H×W×C_in×C_out

总计算量比例: (C_out + 9) / (9 × C_out) ≈ 1/C_out (当 C_out 较大)
```

### Atrous Separable Convolution = Atrous + Depthwise Separable

在 depthwise 步骤中使用 atrous convolution（rate > 1），pointwise 不变。这是本文的核心加速技术。

## 三、Encoder：DeepLabv3 + ASPP

### ASPP 结构

```
Encoder Feature Map (stride=16)
    │
    ├── 1×1 Conv ──────────────────────────┐
    ├── 3×3 Conv, rate=6 ──────────────────┤
    ├── 3×3 Conv, rate=12 ─────────────────┤
    ├── 3×3 Conv, rate=18 ─────────────────┤
    └── Image-level Pooling → 1×1 Conv → Upsample ─┘
                                              │
                                         Concat → 1×1 Conv → Encoder Output
                                         (256 channels)
```

用不同 atrous rate 的并行卷积分支在多个尺度上探测特征，类似 PPM 但用卷积替代池化。

## 四、Decoder：简洁设计

### 设计选择（来自 ablation）

| 设计要素 | 搜索空间 | 最优值 | 关键发现 |
|---------|---------|--------|---------|
| 低层特征通道降维 | [8, 16, 32, 48, 64] | **48** | 太少信息不足，太多压过 encoder 特征 |
| 低层特征来源 | Conv2 / Conv2+Conv3 | **Conv2 only** | U-Net 式多层 skip 无额外收益 |
| Decoder 卷积 | 1个/2个/3个 [3×3] | **2× [3×3, 256]** | 1太少 3过度 |
| 卷积核大小 | 1×1 vs 3×3 | **3×3** | 3×3 显著优于 1×1 |

### 完整 Decoder 流程

1. Encoder output（stride=16, 256ch）→ Bilinear Upsample ×4 → stride=4
2. Low-level features（Conv2, stride=4, 256/512ch）→ 1×1 Conv → 48 channels
3. Concat (encoder upsampled + reduced low-level) → stride=4, 304ch
4. 2× [3×3 Conv, 256] + BN + ReLU
5. Bilinear Upsample ×4 → 原始分辨率 → Prediction

## 五、Modified Aligned Xception

基于 MSRA 的 Aligned Xception 修改：

| 修改 | 目的 |
|------|------|
| Entry flow 不修改 | 保持速度和显存 |
| Max Pooling → Depthwise Separable Conv (stride=2) | 支持 atrous，任意分辨率 |
| 每个 3×3 depthwise conv 后加 BN + ReLU | MobileNet 风格，精度 +0.75% Top-1 |

**Middle flow 重复 16 次**（原版 8 次），更深。

## 六、训练策略

| 参数 | 值 |
|------|-----|
| LR schedule | Poly: base=0.007, power=0.9 |
| Crop size | 513 × 513 |
| Batch norm | Fine-tune (train OS=16) / Frozen (train OS=8) |
| 数据增强 | Random scale + random left-right flip |
| 训练方式 | End-to-end（不分阶段预训练各组件）|

### 推理策略

```
train OS: 训练时的输出 stride
eval OS:  测试时的输出 stride（可以不同！）

策略叠加（精度递增，计算量递增）：
  eval OS=16 → +Decoder → eval OS=8 → Multi-Scale → Left-Right Flip
  77.21%  →   78.85%   →   79.35%   →   80.43%    →    80.57%
```

## 与 PSPNet / U-Net 的关键对比

| 维度 | DeepLabv3+ | PSPNet | U-Net |
|------|-----------|--------|-------|
| 多尺度上下文 | ASPP (atrous conv) | PPM (pyramid pooling) | 隐式（encoder 深度） |
| 边界恢复 | Simple Decoder (Conv2) | 无（bilinear upsample） | Skip connections |
| 输出 stride | 可调（16/8） | 固定 1/8 | 原生分辨率 |
| 加速 | Atrous separable conv | 无 | 无 |
| VOC mIoU | **89.0%** | 85.4% | — |

→ [[zhao2017-pspnet-method]] | [[ronneberger2015-unet-method]]

## 关联页面
- [[chen2018-deeplabv3plus-analysis]] — 总览
- [[zhao2017-pspnet-method]] — PPM vs ASPP
- [[ronneberger2015-unet-method]] — U-Net skip connections

## Evidence By Source

### `sources/papers/chen2018-deeplabv3plus.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/deepLabv3plus.pdf`

^[sources/papers/chen2018-deeplabv3plus.md]
