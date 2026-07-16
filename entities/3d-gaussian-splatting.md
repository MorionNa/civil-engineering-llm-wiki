---
title: "3D Gaussian Splatting (3DGS)"
created: 2026-06-22
updated: 2026-07-16
type: entity
tags: [3d-gaussian-splatting, 3dgs, gaussian-primitives, differentiable-rendering, 3d-reconstruction, novel-view-synthesis]
sources: [raw/papers/amapcvlab2026-abotearth.pdf, raw/papers/lee2026-skyfall-gs.pdf]
confidence: high
---

# 3D Gaussian Splatting (3DGS)

> **原始论文**: Kerbl et al. (2023) "3D Gaussian Splatting for Real-time Radiance Field Rendering" (ACM TOG, SIGGRAPH 2023)
> **核心思想**: 用 3D 高斯原语集合显式表示场景，通过可微光栅化实现高质量实时渲染

## 概述

3DGS 是一种显式场景表示方法，将场景建模为**数百万个各向异性 3D 高斯分布**（椭球体）。每个高斯由以下参数定义：
- **位置** (mean): 3D 坐标
- **协方差矩阵**: 控制椭球体的形状和方向
- **球谐系数** (SH): 控制 view-dependent 颜色/外观

## 为什么 3DGS 适合户外场景？

| 特性 | 3DGS | Mesh/NeRF |
|------|------|-----------|
| 非流形拓扑 | ✅ 天然支持（高斯集合是离散的） | ❌ Mesh 需要连通性 |
| 植被/水面 | ✅ 半透明高斯混合 | ⚠️ 困难 |
| 建筑立面 | ✅ 显式几何 | ✅（需足够分辨率） |
| 渲染速度 | ✅ 实时 (100+ FPS) | ❌ NeRF 慢 |
| 可编辑性 | ✅ 可独立操作单个高斯 | ⚠️ Mesh 好，NeRF 难 |
| 存储 | 🔴 大（百万级原语） | 🟢 Mesh 小 |

## 在 ABot-Earth 中的应用

ABot-Earth 0.5 是第一篇**直接在 3DGS 原生空间中做生成**的工作：
1. 训练数据由 ABot-3DGS 重建引擎产生（真实世界城市 3DGS 场景）
2. 生成模型学习将 3DGS 场景压缩到潜在空间
3. 扩散模型在潜在空间中生成新场景
4. 解码器直接输出 3DGS 原语（而非 mesh 或 NeRF）

## 在 Skyfall-GS 中的应用

`[[skyfall-gs]]` 不训练一个前向 3DGS 生成器，而是把 3DGS 作为**跨视角共识容器**：

1. 先用多视角、多时相卫星影像拟合地点特异的初始 3DGS；
2. 用 appearance embedding、opacity entropy regularization 与 MoGe 伪深度提高初始几何稳定性；
3. 将当前 3DGS 从高空到低空逐步渲染，交给 FlowEdit/FLUX.1 修复；
4. 把多个 2D 修复样本重新监督同一组高斯，使独立生成结果通过共享 3D 表示形成折中；
5. 训练后把外观参数烘焙并融合为标准 PLY，供实时查看器使用。

这说明 3DGS 除了是渲染表示，还可以作为“**重建观测 + 生成先验**”之间的优化接口。详见 `[[lee2026-skyfall-gs-analysis]]` 与 `[[skyfall-gs-vs-abot-earth]]`。

## 相关技术

- **CLOD-GS**: 连续 LOD 3DGS 管理 → `[[entities/clod-gs]]`
- **Bhattacharyya 距离裁剪**: 用于高斯简化/多 LOD 的解析方法
- **OGC 3D Tiles**: 3DGS 的 Web 标准化分发格式
- **Iterative Dataset Update**: 用逐轮渲染—编辑—重训练提高不可见区域质量

## 关联页面
- `[[entities/abot-earth]]` — ABot-Earth 生成系统
- `[[entities/abot-3dgs]]` — ABot-3DGS 重建引擎
- `[[amapcvlab2026-abotearth-analysis]]` — ABot-Earth 论文分析
- `[[skyfall-gs]]` — 逐场景卫星 3DGS + 扩散精修框架
- `[[lee2026-skyfall-gs-method]]` — Skyfall-GS 的 3DGS 优化机制
