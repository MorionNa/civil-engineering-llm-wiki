---
id: papers--amapcvlab2026-abotearth-method
title: ABot-Earth 0.5 — 方法机制展开
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/remote-sensing
- evidence/paper
keywords:
- 3d-gaussian-splatting
- bhattacharyya-distance
- compression-generation
- cross-view-fusion
- multi-lod
- multi-view-rendering
- satellite-conditioned-generation
- spatial-partitioning
- tile-based-rendering
- vlm-quality-assessment
sources:
- sources/papers/amapcvlab2026-abotearth.md
created: '2026-06-22'
updated: '2026-07-31'
confidence: high
---

# ABot-Earth 0.5 — 方法机制展开

> 主页面：`[[amapcvlab2026-abotearth-analysis]]`

## 总体架构

ABot-Earth 0.5 是一个**重建驱动 + 原生 3DGS 生成**的两阶段框架：

```
阶段 1: 数据管线 (Data Pipeline)
  多源图像 → ABot-3DGS 重建 → 空间分块 → 多视角渲染 → 质量评估 → 训练 Tile

阶段 2: 生成模型 (Generation)
  训练 Tile → 压缩编码 → 卫星图像条件 → 潜在扩散生成 → 多 LOD 解码 → 3DGS 原语
```

---

## 数据管线 (Data Pipeline)

### 数据采集：三层互补

| 层级 | 数据源 | 覆盖 | 关键数据集 |
|------|--------|------|-----------|
| **卫星 (Satellite)** | 多立体卫星图像（多 off-nadir 角） | 行星级 | DFC 2019 |
| **航拍 (Aerial)** | 高分辨率倾斜航拍 + LiDAR/网格先验 | 城区 | UrbanScene3D, Mill-19 |
| **地面 (Urban)** | 街景视频、无人机、低空影像 | 细粒度 | UC-GS |

三层数据各自包含**专有采集 + 公开数据集**（Table 1），经统一坐标变换和元数据标准化后进入 ABot-3DGS。

### ABot-3DGS 重建引擎

四大核心能力：

1. **可扩展架构**：层次化分块、连续 LOD 层级、多策略点云简化、GPU 集群并行
2. **几何与细节优化**：深度估计 + 多视图几何一致性，原生全分辨率训练保留纹理
3. **场景鲁棒性**：语义感知优化（不同语义类别差异化策略），多层外观变化建模分离光照/天气/季节
4. **跨视角质量增强**：跨视图匹配 + 粗定位 + 精细配准，航拍贡献广度 + 地面贡献细度

卫星→3DGS 的专项模块为 **FromOrbit2Ground**：
- Z-Monotonic SDF 恢复水密城市几何
- 扩散恢复网络合成高保真立面纹理

### 训练 Tile 生成

- **空间分块**: 200 m × 200 m 滑动窗口，相邻 tile 重叠提供边界上下文
- **多视角渲染**: 虚拟相机阵列分布多个高度层，覆盖 nadir→oblique，多方位角
- **条件输入**: 从同一场景渲染模拟卫星视图图像

### 多粒度质量评估

| 级别 | 评估内容 | 方法 |
|------|---------|------|
| **Tile 级** | PSNR/SSIM/LPIPS + 几何精度 + VLM 感知分 + 空间完整度 | 四维评估，不合格重做或剔除 |
| **View 级** | 低累积不透明度过滤 + VLM 评分纹理/伪影/感知质量 | 仅保留双过滤器通过的视图 |
| **Dataset 级** | 空间多样性平衡 + 语义去重 | 分层采样 + 嵌入空间聚类去重 |

---

## 生成模型 (Method)

### 3.1 Native 3DGS 生成框架

**核心挑战**: 物体级生成方法（TRELLIS, Hunyuan3D, Seed3D）为 mesh 设计，而真实户外环境有复杂的非流形拓扑（植被、水面、建筑立面）——3DGS 更适合但 3DGS 是非结构化高斯原语集合。

**方案**: Compression-Generation 范式
1. 从高质量真实 3DGS 场景（每个包含百万级非结构化高斯原语）学习紧凑潜在空间
2. 直接在 native 3DGS 格式中生成新场景
3. 不使用 mesh 中间表示

### 3.2 原生多 LOD 解码

**核心挑战**: 行星级数字地球需要从全局 10000m→街道 10m 的无缝 LOD 过渡。

**方案**: 模型原生输出 6 级 LOD（zoom 14-19）

| LOD 级别 | 生成方式 | 精度 |
|----------|---------|------|
| Zoom 17-19 (高) | 模型原生输出 | 高 |
| Zoom 14-16 (低) | Bhattacharyya 距离引导统计裁剪 | 中 |

**Bhattacharyya 距离裁剪方案**:
- 在高斯参数上解析计算 Bhattacharyya 距离（衡量两个高斯分布的相似度）
- 高效——可在 CPU 上与 GPU 推理并行，显著减少端到端延迟
- 利用异构计算资源（CPU + GPU 并行）

### 3.3 卫星条件编码

输入卫星图像通过地理配准提供条件信号：
- 记录每个 tile 的地理边界框
- 统一 GSD（地面采样距离）重采样
- Web Mercator (EPSG:3857) 高纬度失真处理：先拼接→等向重采样→统一有效 GSD

## 生产管线

### 推理调度
- 全球按 tile 分区并行推理（Fig. 4a）
- 单 tile ~25 分钟（1000 GPU 集群）
- 300+ 批次并发，<10 天完成全部生产
- 动态队列 + 负载均衡 + 检查点恢复 + 自动重试

### 可视化部署管线 (EarthScape)

产出 **3.2 万亿高斯原语**，32 万推理块 → 三大支柱：

**I. 地理对齐 (ENU 坐标)**
- 仿射变换恢复到 EPSG:3857
- ENU (East-North-Up) 局部切平面坐标系统一表示
- 所有高斯位置/四元数/缩放统一变换

**II. LOD 数据重组**
- 6 级 LOD (zoom 14-19)，按标准地图 tile 层级 (zoom/x/y) 重组
- 高精度级 (17-19) 由模型原生生成
- 低精度级 (14-16) 通过 Bhattacharyya 距离从 zoom-17 裁剪
- 双层空间索引：OGC 3D Tiles 标准 (`tileset.json`) + 隐式地图 tile 路径

**III. 云镜 (YunJing) 渲染引擎**
- 视口依赖的 tile 调度和流式加载
- 近距离加载高精度 tile，远距离加载粗粒度 tile
- 平滑淡入淡出过渡
- 最终实现万亿级 3DGS 实时交互渲染

## 关联页面
- `[[amapcvlab2026-abotearth-analysis]]` — 论文总览
- `[[entities/abot-earth]]` — ABot-Earth 系统概述
- `[[entities/abot-3dgs]]` — ABot-3DGS 重建引擎
- `[[entities/3d-gaussian-splatting]]` — 3DGS 技术概述

## Evidence By Source

### `sources/papers/amapcvlab2026-abotearth.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/amapcvlab2026-abotearth.pdf`

^[sources/papers/amapcvlab2026-abotearth.md]
