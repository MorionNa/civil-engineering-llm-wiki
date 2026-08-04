---
type: paper-analysis
title: Explicit phase field generalized interpolation material point method for dynamic
  fracture problems
authors:
- Chi Lv
- Xiao-Ping Zhou
year: 2025
venue: Computers and Structures
tags:
- domain/computational-mechanics
- evidence/paper
methods:
- phase-field
- material-point-method
- generalized-interpolation
- contact-mechanics
- friction
- numerical-methods
results:
- dynamic-fracture
- brittle-fracture
- fracture
- impact
- numerical-methods
failure_modes:
- large-deformation
- fracture
- contact-mechanics
- numerical-methods
datasets: []
reproducibility: medium
code_url: []
dataset_url: []
id: paper--lv2025-phase-field-gimp-fracture-results
status: active
project: civil-engineering-llm-wiki
keywords:
- computational-mechanics
- material-point-method
- generalized-interpolation
- phase-field
- fracture
- brittle-fracture
- dynamic-fracture
- contact-mechanics
- friction
- large-deformation
- impact
- numerical-methods
- reproducibility
- Computers and Structures
sources:
- sources/papers/lv2025-phase-field-gimp-fracture.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# Results — EPF-GIMP dynamic fracture benchmarks

^[sources/papers/lv2025-phase-field-gimp-fracture.md]

论文：*Explicit phase field generalized interpolation material point method for dynamic fracture problems*；Chi Lv、Xiao-Ping Zhou；2025；*Computers and Structures* 310, 107685。DOI：<https://doi.org/10.1016/j.compstruc.2025.107685>。

证据范围：正文 §5、Tables 1–4、Figures 6–20，以及结论。以下只记录文本明确给出的算例设置、图表观察和比较结论；图中未在预提取文本中列出的数值不补写。

相关页面：[[lv2025-phase-field-gimp-fracture-analysis]] · [[lv2025-phase-field-gimp-fracture-method]] · [[lv2025-phase-field-gimp-fracture-critical]] · [[entities/lv-phase-field-gimp]]

## 1. 结果总览

| 算例 | 主要证据 | 文本明确报告的结果 |
|---|---|---|
| 预裂方板拉伸/剪切 | Figs. 7–11、Table 1 | 裂纹路径、黏性/长度尺度/粒子数/网格影响、力–时间曲线与参考结果比较 |
| Kalthoff-Winkler | Figs. 12–13、Table 2 | 起裂时间、裂纹分叉角与实验角度比较 |
| 双环碰撞 | Figs. 14–16、Table 3 | 两种初速度下接触起裂、后续裂纹路径与既有 phase-field MPM 比较 |
| 三维裂纹分叉 | Figs. 17–20、Table 4 | 起裂/到边界时间、裂纹路径和弹性/耗散能与参考结果比较 |

论文没有报告统一的误差百分比、运行时间、内存或加速比表；“good agreement”均按图形/曲线或路径比较理解。

## 2. 预裂方板：拉伸

### 2.1 设置

方板长宽均为 100 mm、厚度 1 mm，中央水平预裂纹长 50 mm。材料点数为 160,400，背景 cell 数为 40,200，每 cell 通常 4 个材料点；背景网格尺寸 `h=0.5 mm`，相场正则化长度 `l_c=2Δh=1 mm`。计算取 `ζ=1`、`Δt=7.9×10^-8 s`。顶部和底部沿竖直方向施加恒速 `v_0=10 mm/s`（§5.1、Fig. 6）。

Table 1 给出的材料/黏性参数为 `E=208.0 GPa`、`ν=0.3`、`ρ=7000.0 kg/m^3`、`G_c=2.7×10^3 J/m^2`、`η=1.0×10^-6 kNs/mm^2`。

### 2.2 黏性参数

Fig. 7 同时展示三种人工黏性下的 phase-field contour。文本明确结论是：三组解具有相同裂纹路径；随着 `η` 增大，裂纹演化速度降低。提供文本没有列出 Fig. 7 三个黏性试验的全部数值，因此不推断其具体组合。

### 2.3 长度尺度

Fig. 8(a) 比较不同 `l_c` 对顶部总竖向响应的影响。当 `l_c=2Δh=1 mm` 时，force–time 曲线与 model C [42] 的结果一致。减小 `l_c` 会提高峰值力，并使达到峰值的时间变长。

### 2.4 材料点密度

论文比较每 cell `2×2` 与 `4×4` 材料点。两者裂纹演化一致；相应 force–time 曲线的峰值力与到峰值时间均与 model C [42] 的结果一致，且两种材料点密度之间的峰值与时间也一致（Fig. 8(b)）。

## 3. 预裂方板：剪切

剪切算例沿用拉伸算例的主要材料和几何参数。顶部、底部沿水平方向连续施加 `v_0=10 mm/s`，上下边缘在竖直方向完全约束。Fig. 9 给出不同时间的损伤场 contour，终止时间标为 `t_f=9×10^-3 s`。

Fig. 10 的顶部总水平响应与 phase-field method [42] 的 load–time 曲线吻合较好；该图将总水平反力按 `16 kN/mm` 归一化、时间按 `t_f=9.0×10^-3 s` 归一化。Fig. 11 比较不同网格尺寸：网格变粗时，峰值载荷和达到峰值的时间都增加；论文将其归因于粗网格带来的数值不准确。

## 4. Kalthoff-Winkler 动态断裂

### 4.1 设置

板尺寸为 `200 mm×100 mm`，初始裂纹长 50 mm。顶部速度在 `10^-6 s` 内从 0 线性/渐进达到 `v_y=16.5 m/s`，此后保持恒定。模型有 320,800 个材料点、80,400 个背景 cell；材料点间距 `Δx=2.5×10^-4 m`，背景网格 `Δh=5×10^-4 m`，`l_c=2Δh=1×10^-3 m`，`ζ=0.5`，`Δt=2.824×10^-8 s`（§5.2、Table 2、Fig. 12）。

Table 2 给出 `E=190.0 GPa`、`ν=0.3`、`ρ=8000.0 kg/m^3`、`G_c=2.213×10^4 J/m^2`、`η=1.0×10^-8 kNs/mm^2`。

### 4.2 裂纹证据

Fig. 13 的 displacement field 和 phase-field contour 显示：在 `t=14.6 μs` 左右，裂纹从初始裂纹尖端起裂并随时间分叉。左右裂纹相对竖直方向的偏转角均为 `67.5°`，与实验中约 `70°` 的角度接近。论文将该结果用于验证动态脆性断裂路径。

## 5. 双环碰撞与摩擦接触

### 5.1 设置

算例采用平面应力，环厚 2 mm；外半径 40 mm、内半径 30 mm、初始间距 `D=2h=1 mm`；背景网格 `h=0.5 mm`，材料点总数 70,364，摩擦系数 `μ=0.65`。两环材料参数相同（Table 3）：`E=190.0 GPa`、`ν=0.3`、`ρ=8000.0 kg/m^3`、`G_c=6×10^3 J/m^2`、`η=1.0×10^-9 kNs/mm^2`（§5.3、Fig. 14）。

### 5.2 初速度 `10 m/s`

Case (1) 取 `v_0=10 m/s`、`Δt=1×10^-8 s`。两个环首先在接触面因碰撞产生新裂纹，随后裂纹向各自环的另一侧完全传播（Fig. 15，时间标为 75、95、200、400 μs）。作者报告该裂纹演化与 Kakouris 等人的 phase-field MPM 结果吻合较好，用于支持 EPF-GIMP 接触算法的准确性。

### 5.3 初速度 `20 m/s`

Case (2) 取 `v_0=20 m/s`、`Δt=2×10^-8 s`。初次冲击仍在接触面起裂；速度增加后，每个环的上部和下部同时出现两条新裂纹，随后在每个环的右上/左上和右下/左下区域出现更多裂纹。Fig. 16 给出从 `t=0`、30、45、60 μs 的完整演化路径。作者同样报告其结果与 Kakouris 等人结果吻合较好。

## 6. 三维动态裂纹分叉

### 6.1 设置

模型是 `100 mm×40 mm`、厚度 5 mm 的板，中央裂纹长 50 mm；顶部和底部施加连续拉应力 `σ=1 MPa`。网格为 `0.25 mm×0.25 mm×0.25 mm` 立方 cell，每个 cell 一个材料点，总材料点数 1,280,000；`l_c=2Δh=5×10^-4 m`，`ζ=0.5`，`Δt=2.824×10^-8 s`，总计算时间 80 μs（§5.4、Fig. 17、Table 4）。

Table 4 给出 `E=32.0 GPa`、`ν=0.2`、`ρ=2450.0 kg/m^3`、`G_c=3.0` 和 `η=1.0×10^-11`；预提取文本的表格单位排版不完整，后两项的单位按原文表头未能完全确认，因此不补充解释。

### 6.2 裂纹路径与能量

Fig. 18 显示新裂纹约在 `17 μs` 从初始裂纹尖端起裂，传播至约 `80 μs` 到达边界。Fig. 19 将最终裂纹路径与 Borden 等人的 phase-field 结果比较，作者报告两者吻合良好。

Fig. 20 比较不同网格尺寸下板的弹性应变能和耗散/断裂能，并与 Borden 等人结果对照。总体上两类能量曲线较为一致；网格尺寸增大时，弹性应变能和耗散能均增大，但论文仍认为收敛性令人满意。

## 7. 证据边界

- 文本给出的是曲线、contour、裂纹路径和与参考工作的图形比较，没有给出统一的相对误差、峰值误差、运行时或内存数字。
- 算例使用预裂纹；论文说明为形成初始裂纹，会沿裂纹中心线移除背景网格中的材料点，不能将这些结果理解为完全无预设缺陷的起裂测试。
- 论文声明代码可向通讯作者合理请求，但提供文本没有代码 URL、数据 URL、输入文件或独立数据集。

方法流程的解释见 [[lv2025-phase-field-gimp-fracture-method]]；关于参数敏感性、显式稳定步和外推边界的批判性整理见 [[lv2025-phase-field-gimp-fracture-critical]]。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[lv2025-phase-field-gimp-fracture-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | 无公开代码 |
| **数据集** | 无外部数据集 URL（或使用论文内/合成数据） |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
