---
type: paper-analysis
title: A coupled implicit MPM-FEM approach for brittle fracture and fragmentation
authors:
- Ahmad Chihadeh
- William Coombs
- Michael Kaliske
year: 2023
venue: Computers and Structures
tags:
- domain/computational-mechanics
- evidence/paper
methods:
- material-point-method
- finite-element-method
- coupled-methods
- numerical-methods
- contact-mechanics
- brittle-fracture
- large-deformation
results:
- fracture
- dynamic-fracture
- impact
- coupled-methods
failure_modes:
- large-deformation
- fracture
- contact-mechanics
- numerical-methods
datasets: []
reproducibility: medium
code_url: []
dataset_url: []
id: paper--chihadeh2023-implicit-mpm-fem-fracture-results
status: active
project: civil-engineering-llm-wiki
keywords:
- computational-mechanics
- material-point-method
- finite-element-method
- coupled-methods
- large-deformation
- fracture
- brittle-fracture
- dynamic-fracture
- contact-mechanics
- impact
- numerical-methods
- reproducibility
- Computers and Structures
sources:
- sources/papers/chihadeh2023-implicit-mpm-fem-fracture.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# Results — coupled implicit MPM-FEM for brittle fracture and fragmentation

^[sources/papers/chihadeh2023-implicit-mpm-fem-fracture.md]

论文：*A coupled implicit MPM-FEM approach for brittle fracture and fragmentation*；Ahmad Chihadeh、William Coombs、Michael Kaliske；2023；*Computers and Structures* 288, 107143。DOI：<https://doi.org/10.1016/j.compstruc.2023.107143>。

导航：[[chihadeh2023-implicit-mpm-fem-fracture-analysis]] · [[chihadeh2023-implicit-mpm-fem-fracture-method]] · [[chihadeh2023-implicit-mpm-fem-fracture-critical]] · [[entities/chihadeh-implicit-mpm-fem]]

本页只记录预提取文本中明确报告的实验/数值设置、图表现象和数量；“验证”或“吻合”均指论文与其给出的对照之间的表述，不代表本页重新运行了代码。

## 1. 结果总览

| 结果组 | 正文/图表证据 | 报告的观察 |
|---|---|---|
| 动力悬臂梁 | Fig. 2–3，第 3–6 页 | MPM、FEM、MP–FE 的梁端位移相同 |
| 应力波界面 | Fig. 12–18，第 10–13 页 | 粗 FE 需要 intermediate bonds；网格细化后趋于解析传播关系 |
| MPM–FEM 接触 | Fig. 7–9，第 7–8 页 | 移动块在三个时刻与框架边界碰撞并反弹 |
| L 形板 | Fig. 19–22，第 12–14 页 | 裂纹图样与文献实验/数值结果相符，FE 侵蚀区转为材料点 |
| 动力裂纹分叉 | Fig. 23–25，第 14–16 页 | 初始缺口裂纹先直线传播，随后分成两支 |
| 三维冲击板 | Fig. 26–29，第 15–17 页 | 冲击器穿透板材，裂纹阶段前后速度/加速度发生对应变化 |

## 2. 悬臂梁：nodal bond element 实现

模型是 `1 × 5 cm` 悬臂梁，左端固定，梁端施加 `8 N` 三角形载荷，载荷函数节点为 `{(0,0),(0.1,1),(0.2,0)}`。

材料参数为 Young's modulus `10^4 N/cm²`、Poisson's ratio `0.2`；MPM 和 FEM 单元尺寸均为 `0.1 × 0.1 cm`，每单元使用 `2 × 2` 个材料点。

Fig. 2 展示分别用 MPM、FEM 和耦合 MP–FE 离散的梁，Fig. 3 给出梁端位移。

论文报告三种方法的梁端位移相同，并以此说明 nodal bond elements 的实现能够正确传递界面位移。

## 3. 应力波：网格尺度与 intermediate bond

二维矩形杆尺寸为 `150 × 50 mm`，左端施加幅值 `σ₀ = 50 MPa` 的动力载荷；材料 `E = 40 GPa`、Poisson's ratio `0`、密度 `2400 kg/m³`，时间步为 `0.5 μs`。

三个界面模拟都初始激活 `600` 个 MPM 单元，每单元 `3 × 3` 个材料点，总材料点数为 `5400`；MPM 背景网格尺寸保持 `1.25 × 5 mm`。

### 3.1 相同单元尺寸

MPM 计算网格与 FE 单元尺寸相同时，仅放置 nodal bond elements，Fig. 13 显示应力波平滑通过界面。

### 3.2 粗 FE、无中间连接

FE 单元尺寸增大为 `1.25 × 16.7 mm`，Fig. 14 显示应力波到达只有 nodal bond 的界面后不能正确传播，波形发生失真。

### 3.3 粗 FE、加入中间连接

在相同粗 FE 设置中加入 intermediate bond elements，Fig. 15 显示应力波恢复为与相同尺寸情形相同的正确传播方式。

论文据此明确指出：当 FE 单元大于 MPM 背景网格单元时，需要 intermediate bond elements。

### 3.4 与纯 FEM 的比较

Fig. 16 比较了第一种和第三种耦合结果与仅 FEM 结果。论文报告拉伸和压缩下的结果“very good agreement”，并据此说明在提供足够 bond elements 时能正确传播应力波。

## 4. 应力波：收敛行为

固定右端的冲击杆用于考察总反力随单元尺寸变化的行为。入射应力幅值为 `50 MPa`，依据波传播理论，固定边界处传递应力幅值应为 `100 MPa`，即 `σ_T = 2σ_I`。

论文研究了边长为 `1/40、1/80、1/120、1/160、1/200 m` 的五组方形网格；MPM 与 FEM 使用相同网格细化，并分别考察每单元 `2 × 2` 与 `3 × 3` 材料点。

Fig. 18 以归一化应力 `σ_I/σ_T` 对 `1/element size` 绘制收敛行为。

报告的趋势是：单元尺寸减小时结果收敛；与单元尺寸相比，材料点数量对结果几乎没有影响。

## 5. MPM–FEM 接触基准

接触基准是三维方形框架和位于其中的 `1 m` 立方 FEM 小块。框架外尺寸 `11 m`、厚度 `1 m`、深度 `3 m`，外角固定；小块中心初始位置为 `(5.5, 1.5, 9.5)` m，初速度为 `(v_x,v_y,v_z)=(-10,0,-10) m/s`。

时间步为 `0.001 s`，Newmark 参数 `β=0.5、γ=0.5`；材料 `E=10 GPa`、Poisson's ratio `0.2`。

Fig. 8 给出接触基准，Fig. 9 给出移动块 x 方向位移和速度。

当块在 `t=0.4 s` 到达框架左边缘时，接近和相向运动条件满足，接触 bond 激活；随后块在 `t=0.8 s` 撞击下边缘，在 `t=1.2 s` 撞击右边缘。

论文特别说明：`t=0 s` 时块靠近上边缘、距离条件满足，但块正在远离材料点，因此相向运动条件不满足，接触 bond 没有激活。

结果中块发生反射，位移和速度曲线体现了这些接触事件；该算例使用无摩擦设置 `C_t=0`。

## 6. L 形板：准静态脆性断裂与转换

L 形试件底部固定，施加准静态位移；MPM 计算网格尺寸为 `2.5 × 2.5 mm`，FE 网格为非均匀网格。

材料参数为 `E=25850 MPa`、Poisson's ratio `0.18`；距边缘 `30 mm` 的节点施加 `25 mm` 位移，分成 `1000` 个加载增量；临界能量释放率 `G_c=0.035 N/mm`。

Fig. 19 给出几何和边界，Fig. 20 给出竖向总反力，Fig. 21–22 给出裂纹发展和 FE 到材料点的转换。

论文报告所得裂纹图样与文献 [38] 的实验结果以及文献 [15,29,41] 的数值模拟“good agreement”；竖向总反力曲线与文献 [41,42] 的其他数值结果可比。

仿真开始和结束时 FE 数量分别为 `28958` 和 `27449`；最终材料点数量为 `6036`，每个转换单元使用 `4` 个材料点。

图中可见，侵蚀 FE 被材料点替代，材料点与完整 FE 之间动态创建 bond elements；连续体单元表面还加入每单元一个 intermediate bond。

## 7. 动力裂纹分叉

预裂矩形板尺寸为 `100 × 40 mm²`，初始裂纹长度 `50 mm`；上下表面施加 `1 MPa` 均匀阶跃应力。

材料为密度 `2450 kg/m³`、`E=32 GPa`、Poisson's ratio `0.2`，`G_c=1 N/m`；时间步 `5 μs`，Newmark 参数 `β=0.25、γ=0.5`。

FE 网格和 MPM 背景网格单元尺寸均为 `0.25 × 0.25 mm`；MPM 覆盖预期裂纹发展的右半域。

Fig. 23 给出模型，Fig. 24 给出裂纹路径，Fig. 25 放大裂纹分叉处的连接。

报告的裂纹演化是：裂纹从初始缺口尖端开始，先沿直线传播；到达某点后分成两支，之后两支都传播到试件末端。

该结果与文献 [8,30,31] 中的模拟相似。初始和最终 FE 数量分别为 `63600` 和 `63106`；最终材料点数量为 `1976`，每个转换单元使用 `4` 个材料点；每个连续体单元使用一个 intermediate bond。

## 8. 三维板冲击

板尺寸为 `300 × 300 × 25 mm`，外边缘固定；冲击器为直径 `50 mm`、长度 `100 mm` 的圆柱体。利用对称性模拟板的四分之一。

板参数为 `ρ=2400 kg/m³、E=30 GPa、ν=0.2、G_c=0.01 N/mm`；冲击器参数为 `ρ=7850 kg/m³、E=200 GPa、ν=0.3`。

时间步为 `1 μs`，Newmark 参数 `β=0.5、γ=0.5`，冲击器竖直初速度为 `24 m/s`；MPM 计算网格覆盖整个运动域，尺寸与 FE 单元相同，为 `5 × 5 × 5 mm`。

Fig. 26 给出几何、边界和网格，Fig. 27 给出冲击器速度与加速度，Fig. 28 给出穿透后的板，Fig. 29 给出 bond elements 的形成。

论文报告冲击器穿透板材；冲击前保持恒速，撞击后出现与运动方向相反的加速度并减速，断裂阶段后速度重新趋于恒定、加速度趋近零。

每个连续体 FE 表面共创建 `16` 个 bond elements：`4` 个 nodal bond 和 `12` 个 intermediate bond。

初始和最终 FE 数量分别为 `4635` 和 `4240`；最终材料点数量为 `3160`，每个转换单元使用 `8` 个材料点。

## 9. 论文没有给出的结果量

以下不是缺失结果的推测，而是从正文结果段和结论段可直接确认的披露边界：

- 没有给出统一的数值误差表或每个算例的误差百分比。
- 没有报告总运行时间、MPM/FEM 分区带来的加速比或内存节省量。
- 没有给出 penalty 参数敏感性曲线。
- 接触算例没有摩擦结果；提供文本明确写 `C_t=0`。
- 论文在 Data availability 中写明：`No data was used for the research described in the article.`
- 所有算法在 in-house Fortran MP-FE code 中实现，但提供文本没有 code URL 或可下载输入文件。

结果对应的方法细节见 [[chihadeh2023-implicit-mpm-fem-fracture-method]]，关于这些结果可迁移范围的判断见 [[chihadeh2023-implicit-mpm-fem-fracture-critical]]。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[chihadeh2023-implicit-mpm-fem-fracture-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | 无公开代码 |
| **数据集** | 无外部数据集 URL（或使用论文内/合成数据） |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
