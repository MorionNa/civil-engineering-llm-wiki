---
id: papers--lee2026-skyfall-gs-results
title: Skyfall-GS 结果：感知质量、几何消融、用户研究与多块扩展
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computer-vision
- domain/remote-sensing
- evidence/paper
keywords:
- 3d-gaussian-splatting
- 3d-reconstruction
- 3d-scene-generation
- embodied-ai
- multi-view-rendering
- satellite-imagery
- urban-modeling
sources:
- sources/papers/lee2026-skyfall-gs.md
created: '2026-07-16'
updated: '2026-07-31'
confidence: high
---

# Skyfall-GS 实验结果

## 1. 数据集与评估设置

### DFC2019 / Jacksonville

- WorldView-3 RGB，多时相卫星影像，约 35 cm/pixel；
- 4 个标准 AOI：JAX_004、068、214、260；训练图数量分别为 9、17、21、15；
- 参考视图由 Google Earth Studio (GES) 在 17° elevation 渲染；
- 对比：Sat-NeRF、EOGS、CoR-GS、Mip-Splatting。

### GoogleEarth / New York City

- 4 个场景：004、010、219、336；
- 每个场景用 GES 在 80° elevation 渲染 60 张输入图，模拟卫星条件；
- 对比：CityDreamer、GaussianCity、CoR-GS、Mip-Splatting；
- 参考视频在 45° elevation 评估。

### 指标解释

- **主指标：** FIDCLIP、CMMD，衡量生成分布的感知接近程度；
- **辅指标：** PSNR、SSIM、LPIPS；
- 作者明确指出：不可见立面由生成模型补全，不可能逐像素匹配真实世界；DFC2019 与 GES 还存在系统光照/色彩差异，因此像素指标只能作辅助。

## 2. DFC2019 平均结果

| 方法 | FIDCLIP ↓ | CMMD ↓ | PSNR ↑ | SSIM ↑ | LPIPS ↓ |
|---|---:|---:|---:|---:|---:|
| Sat-NeRF | 86.52 | 4.788 | 10.08 | 0.268 | 0.862 |
| EOGS | 87.67 | 5.291 | 7.26 | 0.168 | 0.958 |
| CoR-GS | 84.95 | 5.692 | 11.55 | **0.351** | 0.947 |
| Mip-Splatting | 86.72 | 5.404 | 11.91 | 0.319 | 0.819 |
| **Skyfall-GS** | **27.03** | **2.110** | **12.41** | 0.322 | **0.790** |

关键结论：

- 相对次优 CoR-GS，FIDCLIP 从 84.95 降到 27.03，下降约 **68.2%**；
- 相对次优 Sat-NeRF，CMMD 从 4.788 降到 2.110，下降约 **55.9%**；
- CoR-GS 的 SSIM 更高，但其图像明显更平滑、模糊，说明 SSIM 会对 blur 产生虚高；
- Skyfall-GS 在四个 AOI 的 FIDCLIP 和 CMMD 均大幅领先，优势不是由单一场景贡献。

## 3. GoogleEarth 平均结果

| 方法 | FIDCLIP ↓ | CMMD ↓ | PSNR ↑ | SSIM ↑ | LPIPS ↓ |
|---|---:|---:|---:|---:|---:|
| CityDreamer | 36.66 | 4.200 | 12.58 | 0.267 | 0.558 |
| GaussianCity | 28.76 | 2.915 | 13.41 | 0.291 | 0.540 |
| CoR-GS | 26.35 | 3.758 | 13.35 | 0.299 | 0.412 |
| Mip-Splatting | 16.09 | 2.086 | 14.13 | **0.302** | **0.379** |
| **Skyfall-GS** | **10.29** | **1.959** | **14.42** | **0.302** | 0.393 |

- FIDCLIP 相对 Mip-Splatting 下降约 **36.0%**；
- CMMD 仅小幅优于 Mip-Splatting（约 6.1%），LPIPS 则略差；
- NYC_219 是低层住宅、立面较少，Mip-Splatting 的 FIDCLIP/CMMD 略优，说明生成补全面对“较平坦、可见结构占比高”的场景收益有限；
- 在高层和立面显著的 004/010/336 场景，Skyfall-GS 优势更明显。

## 4. 用户研究

每个数据集有 44 名参与者，分别判断几何准确性、空间对齐和总体感知质量。

| 数据集 | 几何准确性 | 空间对齐 | 总体感知质量 |
|---|---:|---:|---:|
| DFC2019 | 90.3% | 92.0% | 93.8% |
| GoogleEarth | 79.0% | 79.0% | 81.8% |

结果证明感知指标提升与人类偏好一致，但问题设置是“选择最好结果”，不是绝对真实性评分；高胜率不能证明合成立面与真实立面逐项一致。

## 5. Stage 1 消融：重建质量

| Appearance | Opacity Reg. | Depth Sup. | FIDCLIP ↓ | CMMD ↓ | DSM MAE (m) ↓ | DSM RMSE (m) ↓ |
|---|---|---|---:|---:|---:|---:|
| ✗ | ✗ | ✗ | Failed | Failed | Failed | Failed |
| ✓ | ✗ | ✗ | 41.90 | 2.450 | 3.542 | 5.218 |
| ✓ | ✓ | ✗ | 39.95 | 2.395 | 2.980 | 4.527 |
| ✓ | ✓ | ✓ | **38.01** | **2.307** | **2.250** | **3.483** |

- **Appearance modeling 是收敛前提**：没有它，多时相卫星影像无法稳定拟合；
- opacity regularization 主要清除 floaters；
- pseudo-depth 对屋顶、道路等弱纹理平面最有效；
- 相对只使用 appearance，完整配置将 MAE 降低约 **36.5%**、RMSE 降低约 **33.2%**。

## 6. Stage 2 消融：扩散样本与课程

### 每视图扩散样本数

| $N_s$ | FIDCLIP ↓ | CMMD ↓ | 时间 (h) |
|---:|---:|---:|---:|
| 1 | 34.11 | 3.189 | 3.44 |
| **2** | **28.35** | 2.875 | 6.37 |
| 3 | 28.64 | 2.769 | 7.19 |
| 5 | 29.17 | **2.677** | 9.80 |

$N_s=2$ 相对单样本将 FIDCLIP 降低约 16.9%，但时间增加约 85%；继续增加样本主要改善 CMMD，视觉收益和 FIDCLIP 不再提升。

### 组件消融

| 变体 | FIDCLIP ↓ | CMMD ↓ | 结论 |
|---|---:|---:|---|
| 完整方法 | **28.35** | **2.875** | 最佳综合配置 |
| 无课程，随机采样 | 33.79 | 3.361 | 遮挡区域几何更不连贯 |
| context-free prompt | 30.78 | 2.981 | 仅细节小幅退化，提示词鲁棒 |
| 用 SDEdit 替代 FlowEdit | 64.74 | 4.138 | 严重退化，结构保持不足 |

课程式视角使 FIDCLIP 相对随机采样改善约 16.1%，说明“难度顺序”不是可有可无的训练技巧，而是卫星→地面跨视角优化的核心稳定器。

## 7. 渐进式覆盖

Episode-vs-Coverage 分析显示，累计可见表面覆盖率从 Episode 1 的约 0.50 提升到 Episode 5 的约 0.75。下降相机仰角确实逐步暴露立面高斯。

但该指标以最终 3DGS 为“总表面”代理，无法统计从未生成的真空洞。因此 0.75 不能解释为覆盖了真实场景 75%，只能说明最终模型中的点有更大比例被课程相机访问。

## 8. 训练成本与渲染效率

### 单块 JAX_214

- Stage 1 重建：约 1 h 35 min；
- Stage 2 合成：约 5 h 10 min；
- 总计：约 **6 h 45 min**，单张 RTX A6000 48GB；
- 每个 IDU episode 约 1 h：FlowEdit 修复约 30 min，3DGS 更新约 32 min；
- 初始渲染约 4 s，可忽略。

### 显存与模型规模

- 合成阶段峰值显存约 46GB；
- 最终训练内存约 28.04GB；
- 高斯数量约 1.65M → 2.1M，增加约 27%，主要补充垂直立面。

### 交互渲染

- 论文正文报告：MacBook Pro M4 Pro，1920×1080 可达约 60 FPS；
- 补充材料报告：NVIDIA T4 约 11 FPS，MacBook Air M2 约 40 FPS；
- 训练很重，但融合后的标准 3DGS 推理轻量，适合实时浏览。

## 9. 多块扩展

将相邻 JAX_214 与 JAX_260 合并：

| 指标 | 数值 |
|---|---:|
| 空间范围 | 约 1 km × 512 m |
| look-at grid | 6×3 |
| episodes | 5 |
| 总训练时间 | 约 9 h |
| 高斯数量 | 约 3.5M |
| 峰值显存 | 约 46GB |

高速公路和跨块建筑没有明显拼缝，证明统一优化可以避免 tile 后拼接断裂。但这里只验证两个相邻块，尚不能证明城市级内存、训练时间和长距离坐标误差会近似线性扩展。

## 10. 复杂结构与随机性

- 城堡、教堂、桥梁等非 Manhattan 几何可被合理合成，表明方法不只适用于盒状建筑；
- 不同 appearance embeddings 能让车辆等瞬态物体出现/消失，而静态建筑几何保持稳定；
- 不同扩散随机种子下，建筑轮廓保持，但招牌文字会变化（如 “Outeil”/“CUTAN”），直接证明高频外观是生成的，而非从卫星影像真实恢复。

## 结论性判断

Skyfall-GS 的强项不是像素级复原，而是把低空视角从“不可浏览的卫星重建”提升为“视觉可信、几何大体一致、可实时漫游的 3D 场景”。对仿真或数字孪生应用，应把它理解为**地理布局受观测约束的合成环境**，不能把生成立面当作测绘级真值。

## 关联页面

- `[[lee2026-skyfall-gs-analysis]]`
- `[[lee2026-skyfall-gs-method]]`
- `[[lee2026-skyfall-gs-critical]]`
- `[[skyfall-gs-vs-abot-earth]]`

## Evidence By Source

### `sources/papers/lee2026-skyfall-gs.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/lee2026-skyfall-gs.pdf`, `raw/papers/lee2026-skyfall-gs-extracted.md`

^[sources/papers/lee2026-skyfall-gs.md]
