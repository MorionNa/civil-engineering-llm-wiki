---
title: "HRNet 方法机制展开"
created: 2026-06-11
updated: 2026-06-11
type: concept
tags: [semantic-segmentation, high-resolution-representation, multi-resolution-fusion, parallel-convolutions, hrnet]
sources: [raw/papers/arxiv_1904.04514.pdf]
methods: [hrnet, multi-resolution-parallel, repeated-fusion, hrnetv2, multi-resolution-block, multi-resolution-group-convolution, multi-resolution-convolution]
confidence: high
---

# HRNet 方法机制

> 父页面：[[sun2019-hrnetv2-analysis]]

## 一、整体架构

```
Input (H×W×3)
    │
    ▼
Stem: 2× strided 3×3 Conv → 1/4 resolution
    │
    ▼
Stage 1: 4× Bottleneck (width=64) → 1×3×3 Conv (reduce to C)
    │                         1× resolution, C channels
    ▼
┌─────────────────────────────────────────────────────┐
│ Stage 2: 1× Multi-Resolution Block                  │
│   Branch 1: 1× res, C channels                      │
│   Branch 2: 1/2× res, 2C channels                   │
│   Repeated fusion across branches                   │
├─────────────────────────────────────────────────────┤
│ Stage 3: 4× Multi-Resolution Blocks                 │
│   + Branch 3: 1/4× res, 4C channels                 │
├─────────────────────────────────────────────────────┤
│ Stage 4: 3× Multi-Resolution Blocks                 │
│   + Branch 4: 1/8× res, 8C channels                 │
└─────────────────────────────────────────────────────┘
    │
    ▼
HRNetV2 Aggregation:
  1×   branch ──────────────────────────────┐
  1/2× branch ──→ bilinear upsample ×2 ────→ Concat → 1×1 Conv → Prediction
  1/4× branch ──→ bilinear upsample ×4 ────→        (15C dim)
  1/8× branch ──→ bilinear upsample ×8 ────→
```

**宽度配置**：C ∈ {18, 30, 40, 48}（W18/W30/W40/W48），对应不同模型大小。

## 二、Multi-Resolution Block

每个 block 由两部分组成：

### (a) Multi-Resolution Group Convolution

```
标准 Group Conv: 输入 channels → 分成 G 组 → 每组独立 conv
Multi-Res 版本: 输入 channels → 按分辨率分组成多个分支 → 每个分支在自己的分辨率上做 conv
```

每个分支 = 4 个 residual unit，每个 unit = 2× 3×3 conv。**分支之间不交换信息**（信息交换在下一步）。

### (b) Multi-Resolution Convolution（核心创新）

**类比**：标准卷积 = 输入 channels 全集 → 输出 channels 全集，本质是"全连接"式的多对多映射。

Multi-resolution convolution 把这种全连接映射推广到多分辨率：

```
输入:  R1 (1×,  C ch)    R2 (1/2×, 2C ch)    R3 (1/4×, 4C ch)
        │  │  │            │  │  │              │  │  │
        ▼  ▼  ▼            ▼  ▼  ▼              ▼  ▼  ▼
      对每个输入分辨率 x，变换到每个输出分辨率 y：
      
      变换类型:
      - 同分辨率: 普通 3×3 conv
      - 降分辨率: strided 3×3 conv (stride=2)
      - 升分辨率: bilinear upsample + 1×1 conv
    
      每个输出分辨率 = Σ(所有输入分辨率经相应变换)
      
输出: R1' (1×,  C ch)   R2' (1/2×, 2C ch)   R3' (1/4×, 4C ch)
```

**关键特性**：信息在所有分辨率之间双向流动，每次融合后每个分辨率都包含了其他分辨率的信息。

### 各 Stage 配置

| Stage | Blocks | 分辨率数 | 通道数 (W48) |
|-------|--------|---------|-------------|
| 1 | 4× Bottleneck | 1 | [48] |
| 2 | 1× MRB | 2 | [48, 96] |
| 3 | 4× MRB | 3 | [48, 96, 192] |
| 4 | 3× MRB | 4 | [48, 96, 192, 384] |

## 三、HRNetV1 vs HRNetV2 vs HRNetV2p

### HRNetV1（原始，Sun et al. CVPR 2019）

```
4 分辨率分支输出
    │
    仅取最高分辨率分支 → 1×1 Conv → Output
```

**问题**：低分辨率分支的丰富语义信息被丢弃。

### HRNetV2（本文）

```
4 分辨率分支输出
    │
    所有低分辨率分支 → bilinear upsample → concat → 1×1 Conv → 15C-dim → Output
```

**参数开销极小**：仅增加几个 upsample + concat 操作。

### HRNetV2p（检测用）

```
HRNetV2 输出（高分辨率）
    │
    avg pooling 逐级下采样 → 多级特征金字塔（类似 FPN）
    │
    → Faster R-CNN / Mask R-CNN / Cascade R-CNN
```

## 四、与前三篇架构的哲学对比

```
U-Net:        High → Low → High     (先降后升，skip连接保细节)
PSPNet:       Low (1/8×) + PPM      (低分辨率 + 全局池化)
DeepLabv3+:   Low (1/16×) + Decoder (低分辨率 + 轻量恢复)
HRNet:        High ═══════ High     (全程保持高分，低分并行增强)
              Low ─→ 反复融合 ─→
```

**核心差异**：
| | U-Net/DeepLabv3+ | PSPNet | HRNet |
|---|---|---|---|
| 分辨率策略 | 先降后升 | 保持中低分辨率 | **全程保持高分** |
| 上下文获取 | skip/decoder | 显式 PPM | **隐式多分辨率融合** |
| 计算效率 | 中（decoder开销） | 低（大特征图+模块） | **高（无decoder，并行高效）** |
| 空间精度 | 恢复有损 | 16× up 粗糙 | **原生高分辨率** |

## 五、ImageNet 预训练

附录给出了 HRNet 的分类预训练配置（用于初始化 backbone）：

- Classification head：4 分辨率→ bottleneck→ 逐步 downsample+add→ 2048-dim→ classifier
- 训练：100 epochs, batch 256, lr=0.1 (×0.1 at 30/60/90), SGD
- 结果：HRNet-W18 23.1% Top-1 vs ResNet-38 24.6%（参数少 25%）

**HRNet 分类性能 comparable or better than ResNet**，因此可直接替换 ResNet backbone。

## 关联页面
- [[sun2019-hrnetv2-analysis]] — 总览
- [[ronneberger2015-unet-method]] — U-Net 架构对比
- [[zhao2017-pspnet-method]] — PPM 对比
- [[chen2018-deeplabv3plus-method]] — ASPP + Decoder 对比
