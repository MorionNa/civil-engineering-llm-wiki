---
title: "FromOrbit2Ground"
created: 2026-06-22
updated: 2026-06-22
type: entity
tags: [3d-gaussian-splatting, satellite-imagery, cross-view-fusion, 3d-reconstruction, from-orbit-to-ground]
sources: [raw/papers/amapcvlab2026-abotearth.pdf]
confidence: medium
---

# FromOrbit2Ground

> **开发者**: AMAP CV Lab, Alibaba Group
> **论文**: Yu et al. (2026) "From Orbit to Ground: Generative City Photogrammetry from Extreme Off-Nadir Satellite Images" (arXiv:2512.07527)
> **类型**: 卫星图像→3DGS 转换模块

## 概述

FromOrbit2Ground 是 ABot-3DGS 的卫星专用子模块，解决从极低俯角 (off-nadir) 卫星图像到地面级 3D 渲染的**极端视角间隙**问题。

## 双阶段管线

| 阶段 | 方法 | 输出 |
|------|------|------|
| **1. Z-Monotonic SDF** | 从稀疏俯视图恢复水密城市几何 | 水密 SDF 几何 |
| **2. 扩散恢复网络** | 合成高保真立面纹理 | 完整 3DGS 场景 |

## 关键价值

卫星图像是 ABot-Earth 训练数据管线的三级数据源之一（卫星/航拍/地面），FromOrbit2Ground 使卫星图像也能直接转化为 3DGS 重建，显著扩展地理覆盖面。

## 开源状态

🔴 **闭源**。

## 关联页面
- `[[entities/abot-3dgs]]` — ABot-3DGS 重建引擎
- `[[entities/abot-earth]]` — ABot-Earth 生成系统
