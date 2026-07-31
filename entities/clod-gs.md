---
id: entities--clod-gs
title: CLOD-GS
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/remote-sensing
- entity/model
keywords:
- 3d-gaussian-splatting
- bhattacharyya-distance
- clod-gs
- domain/remote-sensing
- entity/model
- lod-hierarchy
- multi-lod
sources:
- raw/papers/amapcvlab2026-abotearth.pdf
created: '2026-06-22'
updated: '2026-07-31'
confidence: medium
---

# CLOD-GS (Continuous Level-of-Detail via 3D Gaussian Splatting)

> **开发者**: AMAP CV Lab, Alibaba Group
> **论文**: Cheng et al. (2025) "CLOD-GS: Continuous Level-of-Detail via 3D Gaussian Splatting" (ICLR 2025, arXiv:2510.09997)
> **类型**: 3DGS 连续 LOD 方法

## 概述

CLOD-GS 提供 3DGS 场景的连续 LOD 层级管理能力。ABot-Earth 0.5 依赖此技术实现从行星级俯瞰到街道细节的无缝 LOD 过渡。

## 在 ABot-Earth 中的应用

| 用途 | 描述 |
|------|------|
| **ABot-3DGS 重建阶段** | 层次化 block 架构中管理城市场景复杂度 |
| **ABot-Earth 渲染阶段** | 支持 6 级 LOD (zoom 14-19) 的视口依赖 tile 调度 |

## LOD 生成策略

- **高精度级 (zoom 17-19)**: 模型原生生成
- **低精度级 (zoom 14-16)**: Bhattacharyya 距离引导的高斯统计裁剪

## 开源状态

🔴 **闭源**。

## 关联页面
- `[[entities/abot-3dgs]]` — ABot-3DGS 重建引擎
- `[[entities/3d-gaussian-splatting]]` — 3DGS 技术概述

## Evidence By Source

### `raw/papers/amapcvlab2026-abotearth.pdf`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/amapcvlab2026-abotearth.pdf]
