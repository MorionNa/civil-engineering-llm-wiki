---
id: papers--ronneberger2015-unet-method
title: U-Net 方法机制展开
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- evidence/paper
keywords:
- data-augmentation
- encoder-decoder
- overlap-tile
- skip-connections
sources:
- sources/papers/ronneberger2015-unet.md
created: '2026-06-11'
updated: '2026-07-31'
confidence: high
---

# U-Net 方法机制

## 架构总览

```
Contracting Path (Encoder)          Expanding Path (Decoder)
   输入 572×572                          ↓
   ↓                                   388×388
  3×3 conv ×2, ReLU                    ↑ up-conv 2×2 + concat + 3×3 conv ×2
   ↓ 64ch                               ↓ 64ch
  2×2 max-pool                          ↓
   ↓ 64ch                               ↓
  3×3 conv ×2                          up-conv + concat + 3×3 conv ×2
   ↓ 128ch                              ↓
  2×2 max-pool                          ↓
   ...                                  ...
   ↓ 512ch                              ↓
  2×2 max-pool                          ↓
   ↓                                   ↓
  3×3 conv ×2, ReLU → 1024ch (bottleneck)
```

**对称性**：每个 contracting level 的 feature map 通过 skip connection 拼接到同分辨率 expanding level。

## 三大核心技术

### ① Overlap-Tile（任意大图无缝分割）

**问题**：GPU 显存放不下完整 A0 扫描图（~10000×7000px）。

**方案**（Fig 2）：
- 输入 tile（蓝色区）> 输出 tile（黄色区）——多出的边框提供 context
- 边界的缺失 context 用**镜像填充**补全
- 只取 valid 部分拼接 → 无缝

**关键约束**：输入 tile 尺寸必须使得每个 max-pool 层的输入为偶数（否则 up-conv 尺寸不对齐）。

**对结构图纸的意义**：A0 图纸 → tiling 推理 → 直接输出整张 mask，无需后处理接缝。

### ② 弹性变形数据增强

**核心 insight**：生物组织/扫描图纸中，最常见的变异不是旋转缩放，而是**局部变形**（组织拉伸、图纸褶皱）。

**实现**：
1. 在 3×3 粗糙网格上采样随机位移向量（高斯 σ=10px）
2. 双三次插值生成每像素位移 → 平滑变形场
3. 同时变形原图和 mask（保证对齐）

**效果**：30 张训练图 → 有效训练样本 ≈ 无限。这是 U-Net 在小样本上碾压其他方法的根本原因。

### ③ 加权交叉熵 Loss

**问题**：接触的同类物体（细胞、紧邻的梁）边界像素容易被网络当成同一物体。

**方案**（Eq 2）：
```
w(x) = w_c(x) + w₀ · exp(-(d₁(x)+d₂(x))² / 2σ²)
```
- `w_c`：类频率平衡权重
- `d₁`, `d₂`：到最近/次近物体边界的距离
- `w₀=10, σ≈5px`：边界附近权重大 → 强制网络关注分离边界

**对结构图纸的意义**：相邻的平行梁线、梁与柱的贴合边界——都需要高权重防止粘连。

## 训练细节

| 参数 | 值 |
|------|-----|
| Optimizer | SGD + momentum 0.99 |
| Batch size | 1（大 tile > 大 batch） |
| 初始化 | Gaussian σ=√(2/N)，N=输入通道数×kernel² |
| 输入 | 单通道灰度，tile 尺寸需配合 max-pool 偶数列 |
| 硬件 | NVidia Titan 6GB，训练 10h |
| 框架 | Caffe |

## 关联页面
- [[ronneberger2015-unet-analysis]] — 全维度概述
- [[ronneberger2015-unet-results]] — 实验结果
- [[ronneberger2015-unet-critical]] — 贡献 + Negative + 可迁移

## Evidence By Source

### `sources/papers/ronneberger2015-unet.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/ronneberger2015-unet.md`, `raw/papers/10_1007_978-3-319-24574-4_28.pdf`

^[sources/papers/ronneberger2015-unet.md]
