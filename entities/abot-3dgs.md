---
id: entities--abot-3dgs
title: ABot-3DGS
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/remote-sensing
- entity/dataset
keywords:
- 3d-gaussian-splatting
- 3d-reconstruction
- abot-3dgs
- cross-view-fusion
- domain/remote-sensing
- entity/dataset
- photogrammetry
sources:
- raw/papers/amapcvlab2026-abotearth.pdf
created: '2026-06-22'
updated: '2026-07-31'
confidence: high
---

# ABot-3DGS

> **开发者**: AMAP CV Lab, Alibaba Group
> **类型**: 城市级 3DGS 重建引擎
> **角色**: ABot-Earth 的训练数据生产管线

## 概述

ABot-3DGS 是 ABot-Earth 生态中的重建引擎，负责将多源真实世界图像（卫星/航拍/地面）转化为城市级 photorealistic 3DGS 场景，作为下游生成模型的训练数据。

## 核心能力

1. **可扩展架构**：层次化分块 + 连续 LOD + 多策略点云简化 + GPU 集群并行
2. **几何与细节优化**：深度估计 + 多视图几何一致性 + 原生全分辨率训练
3. **场景鲁棒性**：语义感知优化（不同类别差异化策略）+ 多层外观变化建模（光照/天气/季节分离）
4. **跨视角质量增强**：跨视图匹配 + 粗定位 + 精细配准，航拍广度 + 地面细度融合

## 数据输入

| 层级 | 数据源 | 关键数据集 |
|------|--------|-----------|
| 卫星 | 多立体卫星图像 (off-nadir) | DFC 2019 |
| 航拍 | 高分辨率倾斜航拍 | UrbanScene3D, Mill-19 |
| 地面 | 街景视频/低空无人机 | UC-GS |

## 子模块

- **FromOrbit2Ground**: 卫星图像→3DGS 转换 → `[[entities/from-orbit-to-ground]]`
- **CLOD-GS**: 连续 LOD 3DGS 管理 → `[[entities/clod-gs]]`

## 与 ABot-Earth 的关系

```
ABot-3DGS  →  训练数据 (3DGS GT)  →  ABot-Earth 0.5 生成模型
```

ABot-3DGS 提供高质量的真实世界 3DGS 重建作为 ground truth，ABot-Earth 生成模型学习从卫星图像到这些重建的映射。

## 开源状态

🔴 **闭源**。

## 关联页面
- `[[entities/abot-earth]]` — ABot-Earth 生成系统
- `[[amapcvlab2026-abotearth-method]]` — 数据管线详细展开

## Evidence By Source

### `raw/papers/amapcvlab2026-abotearth.pdf`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/amapcvlab2026-abotearth.pdf]
