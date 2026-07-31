---
id: papers--xie2021-segformer-method
title: SegFormer 方法机制展开
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computer-vision
- evidence/paper
- method/transformer
keywords:
- efficient-self-attention
- hierarchical-transformer
- mix-ffn
- mlp-decoder
- semantic-segmentation
- vision-transformer
sources:
- sources/papers/xie2021-segformer.md
created: '2026-06-11'
updated: '2026-07-31'
confidence: high
methods:
- mit-encoder
- mix-ffn
- mlp-decoder
- efficient-self-attention
- hierarchical-transformer
- overlap-patch-merging
- sequence-reduction
---

# SegFormer 方法机制

> 父页面：[[xie2021-segformer-analysis]]

## 整体架构

```
Input (H×W×3)
    │
    ▼ Overlap Patch Embedding (K=7, S=4, P=3)
Stage 1: H/4 × W/4 × C₁ (Transformer Block ×L₁)
    │ Overlap Patch Merging (K=3, S=2, P=1)
Stage 2: H/8 × W/8 × C₂ (Transformer Block ×L₂)
    │ Overlap Patch Merging
Stage 3: H/16 × W/16 × C₃ (Transformer Block ×L₃)
    │ Overlap Patch Merging
Stage 4: H/32 × W/32 × C₄ (Transformer Block ×L₄)
    │
    ├─→ F₁ ────→ MLP (unify) → Upsample ──┐
    ├─→ F₂ ────→ MLP (unify) → Upsample ──┤
    ├─→ F₃ ────→ MLP (unify) → Upsample ──→ Concat → MLP → MLP → Pred (H/4×W/4×N_cls)
    └─→ F₄ ────→ MLP (unify) → Upsample ──┘
```

**All-MLP Decoder**：4 个 MLP Linear + Upsample + Concat，**零卷积**。

## 一、Hierarchical Transformer Encoder (MiT)

### MiT 系列配置

| 参数 | B0 | B1 | B2 | B3 | B4 | B5 |
|------|----|----|----|----|----|----|
| Params | 3.7M | 14.0M | 25.4M | 45.2M | 62.6M | 82.0M |
| Top-1 | 70.5 | 78.7 | 81.6 | 83.1 | 83.6 | 83.8 |
| Stage1 [C₁, L₁] | [32, 2] | [64, 2] | [64, 3] | [64, 3] | [64, 3] | [64, 3] |
| Stage2 [C₂, L₂] | [64, 2] | [128, 2] | [128, 3] | [128, 3] | [128, 8] | [128, 6] |
| Stage3 [C₃, L₃] | [160, 2] | [320, 2] | [320, 6] | [320, 18] | [320, 27] | [320, 40] |
| Stage4 [C₄, L₄] | [256, 2] | [512, 2] | [512, 3] | [512, 3] | [512, 3] | [512, 3] |

设计原则同 ResNet：通道数随深度递增，Stage 3 承担大部分计算。

### Overlap Patch Merging

```
ViT (non-overlap): K=16, S=16, P=0 → 16×16→1×1 vector，patch 间不连续
SegFormer:        K=7, S=4, P=3 → 重叠 patch，保留局部连续性
                  K=3, S=2, P=1 → 后续 stage 的下采样
```

**关键**：重叠使相邻 patch 共享信息，对 dense prediction 至关重要。

### Efficient Self-Attention

标准 self-attention 复杂度 O(N²)，N=H×W 在高分辨率输入下不可接受。

**Sequence Reduction**：

```
K = Reshape(N/R, C·R)(K)    # 将 N×C 的 K reshape 为 N/R × (C·R)
K = Linear(C·R, C)(K̂)        # 降维回 C
→ 复杂度从 O(N²) 降至 O(N²/R)
```

各 stage 的 reduction ratio：**R = [64, 16, 4, 1]**（Stage 1-4）。Stage 4 不 reduction（R=1），保留全分辨率 attention。

### Mix-FFN（替代位置编码）⭐⭐⭐

这是 SegFormer 最优雅的设计。

```
标准 ViT FFN:   x = MLP(GELU(MLP(x)))
SegFormer FFN:  x_out = MLP(GELU(Conv3×3(MLP(x_in)))) + x_in
                              ↑
                    3×3 depthwise conv 在 FFN 中间
```

**为什么有效**：3×3 conv 的 zero-padding 操作天然泄露了像素在特征图上的位置信息（Islam et al. 2020 证明 CNN 的 padding 隐式编码了位置）。同时，卷积分辨率随输入自适——测试任意分辨率都不需要插值 PE。

**实验验证**：
| 测试分辨率 | PE (ViT) | Mix-FFN (SegFormer) |
|-----------|---------|-------------------|
| 768×768 (训练分辨率) | 77.3% | **80.5%** |
| 1024×2048 (不同分辨率) | 74.0% (−3.3%) | **79.8%** (−0.7%) |

Mix-FFN 不仅精度更高，而且对测试分辨率变化**极鲁棒**。

### Transformer Block 完整结构

```
Input x
  │
  ├─→ Efficient Multi-Head Self-Attention
  │     (with Sequence Reduction on K, V)
  │
  └─→ Mix-FFN
        MLP → GELU → 3×3 Depthwise Conv → MLP → + x (residual)
```

## 二、Lightweight All-MLP Decoder

### 设计公式

```
F̂_i = Linear(C_i, C)(F_i)              # Step 1: 统一通道到 C
F̂_i = Upsample(H/4 × W/4)(F̂_i)         # Step 2: 上采样到 1/4 分辨率
F = Linear(4C, C)(Concat(F̂_1,...,F̂_4)) # Step 3: Concat + MLP 融合
M = Linear(C, N_cls)(F)                # Step 4: 预测
```

### 为什么 MLP Decoder 有效？

→ ERF 分析（图 3）：

| | DeepLabv3+ | SegFormer |
|---|---|---|
| Stage-1 ERF | 极小（~7×7） | 局部注意力（类似 conv） |
| Stage-4 ERF | 仍然局部（~50×50） | **高度非局部（覆盖全图）** |
| Decoder Head ERF | 与 Stage-4 相似 | **非局部 + 增强的局部注意力** |

**核心 insight**：Transformer 的深层自然具有全局感受野，CNN 需要 ASPP/PPM 强行扩大。因此：
- CNN + MLP decoder = 失败（ERF 不够大）
- Transformer + MLP decoder = 成功（天然大 ERF 补偿了 decoder 的简单性）
- MLP decoder 融合低层局部注意力 + 高层非局部注意力 → **互补表示**

### 实验：CNN vs Transformer + MLP Decoder

| Encoder | Feature | mIoU (ADE20K) |
|---------|---------|-------------|
| ResNet50 | S1-4 | 34.7 |
| ResNet101 | S1-4 | 38.7 |
| ResNeXt101 | S1-4 | 39.8 |
| MiT-B2 | S4 only | 43.1 |
| **MiT-B2** | **S1-4** | **45.4** |

**结论**：(1) MLP decoder 在 CNN 上无效；(2) Transformer 必须融合所有 stage（仅 Stage-4 不够）。

## 三、与前四篇架构的本质对比

| | U-Net | PSPNet | DeepLabv3+ | HRNet | **SegFormer** |
|---|---|---|---|---|---|
| 基础算子 | Conv | Conv | Conv | Conv | **Self-Attention** |
| 感受野 | 局部 | PPM 扩大 | ASPP 扩大 | 多分辨率融合 | **天然大 ERF** |
| 上下文模块 | skip | PPM | ASPP | 隐式 | **不需要** |
| Decoder | 重 | 无 | 轻 | 无 | **极简 MLP** |
| 位置信息 | 隐式 | 隐式 | 隐式 | 隐式 | **Mix-FFN** |
| 测试分辨率敏感 | 否 | 否 | 否 | 否 | **自适应** |

## 关联页面
- [[xie2021-segformer-analysis]] — 总览
- [[chen2018-deeplabv3plus-method]] — ASPP decoder vs MLP decoder
- [[sun2019-hrnetv2-method]] — 全分辨率保持 vs Transformer 大 ERF

## Evidence By Source

### `sources/papers/xie2021-segformer.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/segformer.pdf`

^[sources/papers/xie2021-segformer.md]
