---
title: "Skyfall-GS"
created: 2026-07-16
updated: 2026-07-16
type: entity
tags: [3d-gaussian-splatting, 3dgs, satellite-imagery, remote-sensing, 3d-scene-generation, 3d-reconstruction, diffusion-models, satellite-conditioned-generation, reconstruction-based-generation, embodied-ai, uav-navigation]
sources: [raw/papers/lee2026-skyfall-gs.pdf, raw/papers/lee2026-skyfall-gs-extracted.md]
confidence: high
---

# Skyfall-GS

> **类型：** 卫星条件的混合 3D 重建—生成框架  
> **输入：** 多视角、多时相、最好包含 off-nadir 的卫星影像  
> **输出：** 可自由飞行浏览、可实时渲染的城市街区 3D Gaussian Splatting  
> **论文：** ECCV 2026，arXiv:2510.15869  
> **代码：** https://github.com/jayin92/Skyfall-GS

## 定义

Skyfall-GS 先用卫星影像拟合地点特异的初始 3DGS，再用 FLUX.1-dev/FlowEdit 修复当前场景的退化渲染，并通过课程式 Iterative Dataset Update 把修复结果逐轮写回 3D。它的目标不是完全测量不可见立面，而是在卫星几何约束下合成视觉可信且跨视角相对一致的近地面外观。

## 核心结构

```text
卫星影像
  → SatelliteSfM 相机/点云
  → appearance-aware 3DGS
     + opacity entropy regularization
     + MoGe pseudo-depth correlation
  → curriculum camera: high elevation → low elevation
  → Render → FlowEdit/FLUX.1 → multi-sample refined views
  → IDU update (75% refined + 25% original)
  → fused standard 3DGS / PLY
```

## 关键组件

| 组件 | 作用 |
|---|---|
| per-image/per-Gaussian appearance embedding | 分离多时相光照、阴影和瞬态物体 |
| opacity entropy regularization | 将低透明 floaters 推向可删除状态 |
| pseudo-camera depth supervision | 用 MoGe 相对深度约束低空视角几何 |
| curriculum IDU | 从可靠高空视角逐步下降到遮挡立面 |
| FlowEdit + FLUX.1-dev | 在保持输入结构的前提下去模糊、补纹理 |
| multiple diffusion samples | 让共享 3DGS 对多个 2D 候选形成共识 |
| original-view replay | 防止多轮伪标签造成场景漂移 |

## 代表结果

- DFC2019：FIDCLIP 27.03、CMMD 2.110；
- GoogleEarth：FIDCLIP 10.29、CMMD 1.959；
- 用户偏好：DFC 约 90–94%，NYC 约 79–82%；
- 单块训练约 6 h 45 min（RTX A6000 48GB）；
- 两块联合约 1 km × 512 m、350 万高斯、约 9 h；
- 融合模型可在消费级设备实时渲染。

## 适用场景

- 无街景/无 LiDAR 条件下的城市视觉数字孪生；
- 无人机/机器人导航环境、游戏和影视虚拟城市；
- 需要真实地理布局但允许立面合理合成的仿真；
- 研究 satellite-to-ground、sparse-view 3DGS 和生成式补全。

## 不适用场景

- 测绘级立面恢复、构件尺寸量测和资产盘点；
- 需要真实文字、窗格数量或材料细节的取证任务；
- 只有纯 nadir 图像且要求地点特异立面；
- 大范围即时生成：Skyfall-GS 仍需逐场景迭代优化。

## 与 ABot-Earth 的区别

Skyfall-GS 是**逐场景、观测驱动的精修路线**：速度慢，但位置与输入场景绑定更强，目标覆盖低空自由飞行。ABot-Earth 是**训练后前向生成的行星级路线**：速度和范围更强，原生多 LOD，但目前闭源且主要面向航拍层级。详见 `[[skyfall-gs-vs-abot-earth]]`。

## 关联论文

- `[[lee2026-skyfall-gs-analysis]]` — 12 维总览
- `[[lee2026-skyfall-gs-method]]` — 方法与公式
- `[[lee2026-skyfall-gs-results]]` — 指标和消融
- `[[lee2026-skyfall-gs-critical]]` — 幻觉边界与研究机会

## 关联实体

- `[[3d-gaussian-splatting]]` — 显式场景表示
- `[[abot-earth]]` — 卫星条件 3D 地球生成路线
- `[[from-orbit-to-ground]]` — 卫星→地面 3DGS 相关模块
