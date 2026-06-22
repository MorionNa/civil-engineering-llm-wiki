---
title: "ABot-Earth"
created: 2026-06-22
updated: 2026-06-22
type: entity
tags: [3d-gaussian-splatting, generative-3d-earth, digital-earth, satellite-imagery, urban-modeling, multi-lod, abot-earth]
sources: [raw/papers/amapcvlab2026-abotearth.pdf]
confidence: high
---

# ABot-Earth

> **开发者**: AMAP CV Lab, Alibaba Group（高德地图 CV Lab）
> **版本**: 0.5
> **类型**: 生成式 3D 地球模型（Generative 3D Earth Model）
> **官网**: http://abot-earth.amap.com/

## 概述

ABot-Earth 是一个**原生 3D Gaussian Splatting (3DGS) 生成框架**，能够从卫星图像直接合成无缝的大规模 3D 城市场景。当前版本 (0.5) 已覆盖 190+ 国家的 300+ 城市,生成速率 <10 分钟/km²。

## 核心能力

| 能力 | 描述 |
|------|------|
| **卫星条件生成** | 仅需卫星图像作为输入，无需采集角度/多视图重叠 |
| **3DGS 原生生成** | 直接在非结构化高斯原语上训练/推理，无需 mesh 中间表示 |
| **原生多 LOD** | 6 级 LOD (zoom 14-19)，高精度级由模型直接生成 |
| **行星级覆盖** | 190+ 国家,非洲 68.5%（vs Google Earth 3.7%） |
| **Web 实时渲染** | 集成云镜 (YunJing) 渲染引擎,万亿级原语实时交互 |

## 架构

```
卫星图像 → 地理配准预处理 → 压缩编码 → 潜在扩散生成 → 多 LOD 解码 → 3DGS 原语 → 云镜渲染
```

## 关键组件

- **ABot-3DGS**: 训练数据重建引擎 → `[[entities/abot-3dgs]]`
- **FromOrbit2Ground**: 卫星→3DGS 模块 → `[[entities/from-orbit-to-ground]]`
- **CLOD-GS**: 连续 LOD for 3DGS → `[[entities/clod-gs]]`
- **YunJing (云镜)**: Web 端 3DGS 渲染引擎

## 性能

| 指标 | 数值 |
|------|------|
| FID | 16.1 |
| 生成速率 | <10 min/km² |
| 覆盖城市 | 300+ |
| 覆盖国家 | 190+ |
| 输出规模 | 3.2 万亿高斯原语 |

## 开源状态

🔴 **闭源**。仅提供展示页面，核心算法代码、训练数据、预训练权重均未公开。

## 关联论文
- `[[amapcvlab2026-abotearth-analysis]]` — ABot-Earth 0.5 技术报告分析
