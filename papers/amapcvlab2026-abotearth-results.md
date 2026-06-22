---
title: "ABot-Earth 0.5 — 实验结果与证据"
created: 2026-06-22
updated: 2026-06-22
type: paper-analysis
tags: [3d-gaussian-splatting, 3d-scene-generation, fid, kid, urban-modeling, digital-earth]
sources: [raw/papers/amapcvlab2026-abotearth.pdf]
confidence: high
---

# ABot-Earth 0.5 — 实验结果与证据

> 主页面：`[[amapcvlab2026-abotearth-analysis]]`

## 生成保真度 (Generative Fidelity)

### 定量对比 (Tab. 2)

| Method | FID ↓ | KID ↓ |
|--------|-------|-------|
| CityDreamer (CVPR 2024) | 97.3 | 0.096 |
| GaussianCity (CVPR 2025) | 86.9 | 0.090 |
| EarthCrafter (AAAI 2026) | 69.5 | 0.061 |
| **ABot-Earth 0.5 (Ours)** | **16.1** | **0.006** |

> ⚠️ 注意：FID/KID 数值不可直接比较——各方法的 GT 图像集和视点采样不同（论文脚注说明）。但 ABot-Earth 的 GT 来自**真实高复杂度 3DGS 重建的渲染图**，建模难度显著高于合成数据集。

**关键结论**: ABot-Earth 在更难的评估条件下取得了 4倍以上的 FID 改善（69.5 → 16.1）。

---

## 系统级对比 (System-level Applicability)

### vs Google Earth & Marble (Tab. 3, Fig. 7)

| 维度 | Google Earth | Marble | ABot-Earth 0.5 |
|------|-------------|--------|-----------------|
| **范式** | 重建 (Reconstruction) | 生成 (Generation) | 生成 (Generation) |
| **空间覆盖** | 稀疏（仅扫描区域） | N/A | **无限** |
| **开放性** | API only | Open Platform | **Open Platform** |

### 大陆级 3D 覆盖率对比 (Fig. 7b)

| 大洲 | Google Earth | ABot-Earth 0.5 |
|------|-------------|-----------------|
| 非洲 | 3.7% | **68.5%** |
| 亚洲 | 8.5% | **91.5%** |
| 欧洲 | 81.4% | **88.4%** |
| 北美洲 | 17.4% | **56.5%** |
| 南美洲 | 25.0% | **91.7%** |
| 大洋洲 | 14.3% | **57.1%** |

**关键发现**: ABot-Earth 在发展中国家和不发达地区的覆盖优势极为显著（非洲 3.7% → 68.5%），解决了 Google Earth 的"3D 数字鸿沟"。

### 用户评测视觉质量 (Fig. 7a Radar)

| 指标 | Google Earth | ABot-Earth 0.5 |
|------|-------------|-----------------|
| 几何精度 | **3.84** (更高) | 2.84 |
| 纹理保真度 | **3.79** (更高) | 3.30 |
| 美学评分 | 3.15 | **3.91** (更高) |

**分析**: 
- Google Earth 几何和纹理占优——预期结果（多年优化 + "Manhattan-world" 强先验 + 人工后处理）
- ABot-Earth 美学占优——用户更看重光照和色彩和谐而非微观精度的整体感受
- 作者类比：这相当于"手工建模 vs 第一代生成模型 (LRM/CLAY)" 的质量差距

---

## 定性结果

### 区域对比 (Fig. 6)

| 区域 | Google Earth | ABot-Earth |
|------|-------------|------------|
| 新西兰 | 3D 重建 ✓ | 生成 ✓ (质量可比) |
| 日本 | 3D 重建 ✓ | 生成 ✓ (质量可比) |
| 爱尔兰 | **无 3D 数据** (仅 2D) | **生成完整 3D** ✓ |

爱尔兰案例证明：在 Google Earth 没有扫描数据的区域，ABot-Earth 仍能生成可信 3D。

### 地标融合 (Fig. 8)

成功将 COLMAP 重建的地标模型融入生成环境：
- 埃菲尔铁塔
- 罗马斗兽场
- 美国国会大厦
- 凯旋门

保持精细建筑细节，与周围生成环境有效融合。

---

## 效率指标

| 指标 | 数值 |
|------|------|
| 单 km² 生成时间 | < 10 分钟 |
| 单 tile 推理时间 | ~25 分钟 (1000 GPU) |
| 全量产周期 | < 10 天 (300+ 批次) |
| 总输出原语 | 3.2 万亿 |
| 总推理块数 | 32 万 |
| 覆盖城市 | 300+ |
| 覆盖国家 | 190+ |

---

## 消融与局限性证据

- **FID 对比非公平**（论文承认）：不同方法的 GT 集和视点采样不同
- **Google Earth 几何/纹理仍更好**（论文承认）：ABot-Earth 是"第一代生成模型"水平
- **无 closed-loop UAV 仿真定量结果**：只声称适合，未提供实验证据
- **地标融合是手动管道**：COLMAP + MVS 重建 + 手动 compositing

## 关联页面
- `[[amapcvlab2026-abotearth-analysis]]` — 论文总览
- `[[amapcvlab2026-abotearth-critical]]` — 贡献+Negative+可迁移+研究机会
