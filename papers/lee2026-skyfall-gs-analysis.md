---
title: "Lee et al. (2026) — Skyfall-GS：从卫星影像合成可自由飞行的沉浸式 3D 城市"
created: 2026-07-16
updated: 2026-07-16
type: paper-analysis
tags: [3d-gaussian-splatting, 3dgs, satellite-imagery, remote-sensing, 3d-scene-generation, 3d-reconstruction, photogrammetry, urban-modeling, multi-view-rendering, diffusion-models, satellite-conditioned-generation, reconstruction-based-generation, embodied-ai, uav-navigation]
sources: [raw/papers/lee2026-skyfall-gs.pdf, raw/papers/lee2026-skyfall-gs-extracted.md]
methods: [appearance-conditioned-3dgs, opacity-entropy-regularization, pseudo-camera-depth-supervision, curriculum-idu, flowedit, multi-sample-diffusion]
results: [fidclip, cmmd, user-study, real-time-rendering, multi-block-scalability]
failure_modes: [off-nadir-dependence, diffusion-hallucination, per-scene-optimization, heuristic-camera-blind-spots, city-scale-memory]
datasets: [dfc-2019, googleearth]
reproducibility: high
code_url:
  - https://github.com/jayin92/Skyfall-GS
dataset_url:
  - https://huggingface.co/datasets/jayinnn/Skyfall-GS-datasets
  - https://huggingface.co/datasets/jayinnn/Skyfall-GS-eval
  - https://huggingface.co/jayinnn/Skyfall-GS-ply
confidence: high
---

# Skyfall-GS: Synthesizing Immersive 3D Urban Scenes from Satellite Imagery

> **作者：** Jie-Ying Lee, Yi-Ruei Liu, Shr-Ruei Tsai, Wei-Cheng Chang, Chung-Ho Wu, Jiewen Chan, Zhenjun Zhao, Chieh Hubert Lin, Yu-Lun Liu  
> **发表状态：** ECCV 2026；arXiv:2510.15869（首次公开于 2025-10-17）  
> **一句话定位：** 先用多视角、多时相倾斜卫星影像重建“可信但粗糙”的 3DGS，再用开放域扩散模型按“高空→低空”的课程式视角逐轮修复渲染结果，使被遮挡立面逐步写回同一个可实时浏览的 3D 场景。

## 1. 工程背景 (Engineering Background)

城市级数字孪生、无人机导航、机器人仿真和沉浸式内容需要同时满足：大范围覆盖、真实地理布局、近距离立面细节、任意视角一致性和实时渲染。传统倾斜摄影/LiDAR 能提供真实 3D，但采集与更新昂贵；只用互联网照片又面临相机配准、时相变化和动态物体噪声。卫星影像覆盖广、自动采集且具有地理参照，因此是更可扩展的入口。→ `[[lee2026-skyfall-gs-method]]`

## 2. Research Gap

直接把 Sat-NeRF、EOGS 或普通 3DGS 用于卫星影像，只能可靠恢复屋顶和俯视可见区域；由于视差有限、立面长期遮挡，低空渲染会出现 floaters、纹理拖影和几何融化。另一类 CityDreamer/GaussianCity 等城市生成方法依赖语义图、建筑高度场或特定域训练集，几何通常过度简化，也难保持输入地点的真实纹理与空间对应。

核心空白不是“能否从卫星图生成一张街景图”，而是：**能否在没有街景、LiDAR 或领域专用 3D 训练数据的情况下，把卫星观测约束与开放域生成先验融合到同一个可自由飞行、跨视角一致的显式 3D 场景中。**

## 3. 科学问题 (Scientific Question)

在卫星视角对建筑立面约束极弱的条件下，如何利用 2D 扩散模型补充不可见信息，同时避免生成结果偏离卫星影像确定的真实布局，并使不同视角的独立 2D 修复最终收敛为一个几何一致的 3D 表示？

这个问题包含三个耦合难点：
1. **观测退化：** 多时相光照、阴影、瞬态物体和有限视差会污染初始 3DGS；
2. **生成漂移：** 2D 扩散模型能补细节，却可能改变建筑结构或在不同视角产生矛盾；
3. **难度递增：** 高空视角较可靠，越接近地面，遮挡与幻觉风险越大，不能一次性同等优化。

## 4. 研究目标 (Research Objective)

构建一种仅以多视角卫星影像为输入的混合重建—生成框架：保留真实城市的几何布局和场景语义，逐步补全立面等不可见区域，并输出可在标准 3DGS 渲染器中实时浏览的城市街区场景。

## 5. 方法机制 (Method & Mechanism)

→ 详见 `[[lee2026-skyfall-gs-method]]`

Skyfall-GS 采用两阶段管线：

```text
多视角/多时相卫星影像
  → SatelliteSfM 相机近似 + 初始点云
  → Stage 1：外观建模 + 不透明度正则 + 伪相机深度监督的 3DGS 重建
  → Stage 2：高空到低空课程式采样
  → 当前 3DGS 渲染 → FlowEdit/FLUX.1 修复 → 多样本伪真值
  → 75% 修复视图 + 25% 原始卫星视图继续训练 3DGS
  → 5 个 episode 后得到可自由飞行的融合 3DGS
```

关键机制不是单次“扩散增强”，而是 **render–edit–update 的 Iterative Dataset Update (IDU)**：每轮把当前 3D 场景渲染为新视角，扩散模型修复后再作为伪监督写回 3DGS；视角高度逐轮下降，先解决较容易的区域，再进入立面和低空视角。

## 6. 结果证据 (Result & Evidence)

→ 详见 `[[lee2026-skyfall-gs-results]]`

- **DFC2019 平均：** FIDCLIP 27.03、CMMD 2.110，显著优于 Sat-NeRF、EOGS、CoR-GS 和 Mip-Splatting；相对次优 FIDCLIP 下降约 68%。
- **GoogleEarth 平均：** FIDCLIP 10.29、CMMD 1.959、PSNR 14.42；除 LPIPS 略逊于 Mip-Splatting 外，整体最优。
- **用户研究：** DFC2019 三项偏好率约 90–94%，GoogleEarth 约 79–82%。
- **消融：** 外观建模保证多时相收敛；不透明度正则和伪深度监督将 DSM MAE 从 3.542 m 降至 2.250 m；课程式 IDU 明显优于随机采样；每视图 2 个扩散样本取得最佳质量—成本折中。
- **效率与规模：** 单块完整训练约 6 h 45 min（RTX A6000 48GB）；两个相邻 AOI 合并为约 1 km × 512 m 场景，约 9 h、350 万高斯、峰值约 46GB；融合模型可在消费级设备实时渲染。

## 7. 贡献 (Contribution)

1. **重建约束下的开放域生成：** 不是从语义图自由生成城市，而是让扩散先验补充卫星重建的缺失区域，保留地点特异性。
2. **面向卫星影像的稳健 3DGS 初始化：** 将多时相外观嵌入、不透明度熵正则和伪相机尺度不变深度监督组合成可用的初始场景。
3. **课程式 IDU：** 将视角难度显式排序为高空→低空，使伪监督随 3D 场景质量共同演化。
4. **多扩散样本的 3D 共识：** 不直接相信单条 2D 去噪轨迹，而让多个样本通过 3DGS 优化形成跨视角折中。
5. **完整开源链路：** 代码、训练/评估数据、融合 PLY 和运行脚本均公开，并支持自定义卫星或 COLMAP 数据。

## 8. 核心知识点 (Core Knowledge)

- **生成模型最适合补“观测缺失”，不应替代观测约束。** 原始卫星图在每轮训练中仍占 25%，用于防止伪真值逐轮漂移。
- **视角可靠性可以转化为课程。** 从高置信度视角启动，再逐步引入低置信度视角，比随机混合所有难度更稳定。
- **多时相变化应尽量进入外观隐变量，而不是污染几何。** per-image/per-Gaussian embedding 将阴影和瞬态变化吸收到外观分支。
- **2D 生成的一致性可通过共享 3D 表示间接约束。** 多样本、多视角共同优化同一组高斯，相当于寻找生成分布的 3D 共识。

## 9. Negative Knowledge

→ 详见 `[[lee2026-skyfall-gs-critical]]`

- 需要 off-nadir 倾斜卫星影像；纯正射/纯天顶影像无法提供立面外观约束。
- 输出是**几何受约束的合理合成**，不等于真实立面测量；补出的招牌文字可随随机种子变化。
- 方法仍是逐场景优化，不是即时前向生成；训练成本和显存需求较高。
- 固定轨迹可能遗漏复杂街谷或深遮挡区域；极低街景视角仍可能出现伪影。
- 评价不可完全依赖 PSNR/SSIM，因为不可见区域不存在一一对应的真实像素；但纯感知指标也可能奖励“好看但不真实”的内容。

## 10. 可迁移知识 (Transferable Knowledge)

| 可迁移机制 | 可迁移到其他任务的方式 |
|---|---|
| 可靠→困难的课程视角 | 先用低分辨率全图/高置信区域稳定结构，再逐步加入高分辨率局部与遮挡区域 |
| 原始观测 replay | 伪标签迭代训练时持续混入原始数据，抑制自训练漂移 |
| 多生成样本共识 | 对不确定区域生成多个候选，让共享物理/几何模型选择一致解释 |
| 外观—几何解耦 | 将时相、阴影、扫描质量等 nuisance factor 置于独立 embedding，不让其进入主体几何 |
| 相关系数深度损失 | 当伪深度只有相对尺度时，用 Pearson correlation 监督形状而非绝对尺度 |
| 重建+生成混合评价 | 同时报告几何、像素、分布感知指标和人工偏好，避免单指标误导 |

## 11. 研究机会 (Research Opportunity)

1. 用可见性、几何不确定度或“真空洞”检测替代固定相机轨迹，自动选择下一轮 IDU 视角。
2. 引入建筑轮廓、DSM、道路/地块、语义分割和多源 GIS 作为硬约束，降低立面幻觉。
3. 为生成区域输出不确定度或“观测/推断”标签，区分测得几何与合成外观。
4. 研究纯 nadir 输入下的立面补全，以及卫星—街景少量配对的弱监督扩展。
5. 结合分块训练、层次 LOD 和分布式高斯优化，把 1 km 级验证扩展到城区/城市级。
6. 面向灾后城市数字孪生，将多时相变化显式分解为静态结构、灾损变化和瞬态物体。
7. 与 `[[abot-earth]]` 的前向生成范式结合：用快速生成提供初始化，再以 Skyfall-GS 的 IDU 做地点特异化精修。→ `[[skyfall-gs-vs-abot-earth]]`

## 12. 可复现性 (Reproducibility)

| 项目 | 说明 |
|---|---|
| **等级** | 🟢 高 |
| **官方代码** | https://github.com/jayin92/Skyfall-GS（Apache-2.0） |
| **数据集** | JAX/NYC 训练数据、评估数据与融合 PLY 已公开于 Hugging Face |
| **关键依赖** | Mip-Splatting、WildGaussians、FlowEdit、MoGe、SatelliteSfM、FLUX.1-dev |
| **硬件门槛** | 论文主实验使用单张 RTX A6000 48GB；扩散模型与 densification 使峰值显存约 46GB |
| **复现注意** | 论文补充材料称 IDU 图像为 2048²，而公开 README 示例参数 `--idu_render_size 1024`；应按代码版本和显存核对配置 |

## 关联页面

- `[[skyfall-gs]]` — 方法实体页
- `[[3d-gaussian-splatting]]` — 基础 3D 表示
- `[[amapcvlab2026-abotearth-analysis]]` — 同属卫星条件 3D 城市生成，但扩展尺度与范式不同
- `[[skyfall-gs-vs-abot-earth]]` — 两种路线的并排比较
