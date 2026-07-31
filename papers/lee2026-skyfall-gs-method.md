---
id: papers--lee2026-skyfall-gs-method
title: Skyfall-GS 方法：卫星 3DGS 重建 + 课程式扩散 IDU
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/computer-vision
- domain/remote-sensing
- evidence/paper
keywords:
- 3d-gaussian-splatting
- 3d-reconstruction
- diffusion-models
- multi-view-rendering
- photogrammetry
- reconstruction-based-generation
- satellite-conditioned-generation
- satellite-imagery
sources:
- sources/papers/lee2026-skyfall-gs.md
created: '2026-07-16'
updated: '2026-07-31'
confidence: high
---

# Skyfall-GS 方法机制

## 1. 总体管线

Skyfall-GS 把问题拆成“先重建可信骨架，再生成缺失细节”两阶段：

```text
Stage 1 — Reconstruction
RPC 卫星相机 → 透视相机近似 + SfM 稀疏点
多时相卫星图 → appearance-aware 3DGS
              + opacity regularization
              + pseudo-camera depth supervision

Stage 2 — Synthesis
当前 3DGS → 课程式采样相机（高空→低空）→ render
render → FlowEdit + FLUX.1-dev → 每视图 Ns 个 refined samples
refined samples + 原始卫星图 → 更新同一个 3DGS
重复 Ne 个 episode → 融合并导出标准 3DGS/PLY
```

## 2. 3DGS 基础目标

每个高斯包含中心 $\mu_i$、协方差 $\Sigma_i$、不透明度 $\alpha_i$ 和视角相关颜色。投影协方差为：

$$
\Sigma_i' = J W \Sigma_i W^T J^T.
$$

颜色重建损失沿用标准 3DGS：

$$
\mathcal{L}_{color}=\lambda_{D-SSIM}\,DSSIM(\hat C,C)
+(1-\lambda_{D-SSIM})|\hat C-C|_1.
$$

## 3. RPC 到透视相机近似

卫星影像通常使用 Rational Polynomial Camera (RPC) 模型，不能直接套用标准 3DGS 透视相机。作者调用 SatelliteSfM：

1. 用严格 RPC 生成密集 3D–2D 对应；
2. 通过 DLT 求投影矩阵 $P$；
3. 分解 $P=K[R|t]$ 得到内外参；
4. 生成 SfM 稀疏点作为高斯初始化。

其依据是卫星高度 $Z$ 远大于地表深度变化 $\Delta Z$，满足弱透视近似。补充材料报告：相对 RPC 的最大前向投影误差平均约 0.126 pixel，三角化点差异通常 <5 cm，Bundle Adjustment 中位重投影误差约 0.864 pixel。

## 4. 多时相外观建模

多日期卫星图具有光照、季节、阴影和瞬态物体差异。作者借鉴 WildGaussians，为每张图设置 embedding $e_j$，为每个高斯设置 embedding $g_i$，再由轻量 MLP 预测仿射颜色参数：

$$
(\beta,\gamma)=f(e_j,g_i,\bar c_i),\qquad
\tilde c_i(r)=\gamma\cdot\hat c_i(r)+\beta.
$$

- per-image embedding：32 维，学习率 0.001；
- per-Gaussian embedding：24 维，学习率 0.005；
- MLP：2 个 128-neuron hidden layers，ReLU，学习率 0.0005；
- SH 只保留 0/1 阶，避免把时相变化错误解释为高阶视角效应。

推理时选择固定 $e^*$，把颜色变换烘焙到普通 3DGS 中，再丢弃 embeddings 和 MLP，从而兼容标准实时渲染器。

## 5. 不透明度熵正则

卫星视差不足会产生大量低不透明度 floaters。作者使用二元熵：

$$
\mathcal L_{op}=-\sum_i[\alpha_i\log\alpha_i+(1-\alpha_i)\log(1-\alpha_i)].
$$

它把 $\alpha_i$ 推向 0 或 1，使无效低透明高斯更容易在 densification/pruning 中删除。实现上还将 scaling learning rate 从 0.005 降到 0.001，并删除最大协方差 >20 的高斯，减少俯视条件下的细长椭球伪影。

## 6. 伪相机深度监督

仅在原始卫星相机上优化，无法约束低空视角的悬浮几何。作者周期性采样靠近地面的伪相机：

1. 从当前 3DGS 渲染 RGB $I_{RGB}$ 和 alpha-blended depth $\hat D_{GS}$；
2. 用 MoGe 从 RGB 估计尺度不变单目深度 $\hat D_{est}$；
3. 用 Pearson 相关系数监督相对深度结构：

$$
\mathcal L_{depth}=1-|PCorr(\hat D_{GS},\hat D_{est})|.
$$

相关系数不要求两个深度图具有相同绝对尺度，适合单目伪深度。补充设置：每 10 次迭代采样 24 个 1024² 视图，仰角 80°→45°、半径 300→250。

## 7. Stage 1 总损失与配置

$$
\mathcal L_{sat}=\mathcal L_{color}
+\lambda_{op}\mathcal L_{op}
+\lambda_{depth}\mathcal L_{depth}.
$$

| 参数 | 论文配置 |
|---|---:|
| 总迭代 | 30,000 |
| densification | 1,000–21,000 |
| $\lambda_{D-SSIM}$ | 0.2 |
| $\lambda_{op}$ | 10 |
| $\lambda_{depth}$ | 0.5 |
| scaling learning rate | 0.001 |
| covariance prune threshold | 20 |

GoogleEarth 数据的输入视图更密，作者关闭 opacity regularization。

## 8. 课程式 Iterative Dataset Update

普通 IDU 从训练视角或简单轨道随机采样。Skyfall-GS 的关键观察是：初始 3DGS 在高仰角仍可用，仰角越低退化越严重。因此设定 $N_e$ 个 episode，让 elevation 随 episode 逐步下降。

每轮执行：

```text
cam_views    = OrbitViews(look_at_points, radius_i, elevation_i, Nv)
render_views = Render(G_{i-1}, cam_views)
refine_views = FlowEdit(render_views, source_prompt, target_prompt, Ns)
G_i          = Train(G_{i-1}, refine_views + original_satellite_views)
```

DFC2019 的主要配置：

| 参数 | 数值 |
|---|---:|
| episodes $N_e$ | 5 |
| 每 episode 迭代 | 10,000 |
| look-at points $N_p$ | 9（3×3，宽 512） |
| 每点相机 $N_v$ | 6 |
| 每视图扩散样本 $N_s$ | 2 |
| elevation | 85°→45° |
| radius | 300→250 |
| 训练采样 | 75% refined + 25% original |
| densification 截止 | 每轮 9,000 |

## 9. FlowEdit 修复

作者用 FlowEdit + FLUX.1-dev 做 prompt-to-prompt 编辑，而不是自由 inpainting：输入仍包含卫星重建中可见的斜视立面约束，编辑目标是去除模糊、扭曲和浮点伪影，同时保留结构。

- FlowEdit：$n_{min}=4$, $n_{max}=10$；
- source prompt：描述“卫星城市图像 + distortion/blurring/warping artifacts”；
- target prompt：要求“sharp buildings、smooth edges、natural lighting、well-defined textures”。

提示词消融显示对措辞不敏感；真正关键的是 FlowEdit 的结构保持能力。用 SDEdit 替换后质量显著下降。

## 10. 多扩散样本为何有效

对每个视角独立扩散，单个样本可能沿着不一致的 2D 去噪轨迹走向局部幻觉。Skyfall-GS 为同一视图生成 $N_s$ 个候选，不选择其中一张，而是在 3DGS photometric loss 中共同训练。共享 3D 表示迫使模型寻找多个候选和多个视角之间的共识：

- $N_s=1$：细节尖锐但跨视角噪声较大；
- $N_s=2$：质量—成本最佳；
- $N_s=5$：CMMD 略好，但训练时间增至 9.8 h，收益有限。

## 11. IDU 优化目标

每个 episode 使用：

$$
\mathcal L_{IDU}(G_{i-1},\tilde C_i)
=\mathcal L_{color}+\lambda_{depth}\mathcal L_{depth}.
$$

IDU 阶段关闭 opacity regularization，让半透明结构保留可变不透明度；同时继续用伪深度约束几何。原始卫星图保留 25% replay，是防止扩散伪标签逐轮吞噬真实观测的关键设计。

## 12. 训练产物与融合

外观 embeddings 在训练后被烘焙到静态颜色；官方代码要求将训练输出进一步通过 `create_fused_ply.py` 融合，得到可供 Mip-Splatting Viewer 或 SuperSplat 使用的独立 PLY。不要直接把训练目录中的 raw PLY 当作最终模型。

## 关联页面

- `[[lee2026-skyfall-gs-analysis]]` — 总览
- `[[lee2026-skyfall-gs-results]]` — 定量与消融
- `[[lee2026-skyfall-gs-critical]]` — 失败边界与研究机会
- `[[3d-gaussian-splatting]]` — 基础表示

## Evidence By Source

### `sources/papers/lee2026-skyfall-gs.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/lee2026-skyfall-gs.pdf`, `raw/papers/lee2026-skyfall-gs-extracted.md`

^[sources/papers/lee2026-skyfall-gs.md]
