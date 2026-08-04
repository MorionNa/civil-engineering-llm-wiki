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
id: paper--lv2025-phase-field-gimp-fracture-analysis
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
# Explicit phase field generalized interpolation material point method for dynamic fracture problems

^[sources/papers/lv2025-phase-field-gimp-fracture.md]

> 论文概览：Chi Lv 与 Xiao-Ping Zhou 在 2025 年 *Computers and Structures* 310, 107685 中提出 EPF-GIMPM，将显式速率相关 phase-field fracture、GIMP、MUSL 和带 Coulomb 摩擦的粒子接触算法组合起来，用于大变形、碰撞与动态裂纹问题。

DOI：<https://doi.org/10.1016/j.compstruc.2025.107685>

原始证据：`raw/papers/1-s2.0-S0045794925000434-main.pdf`；本次使用的预提取文本为 `tmp/pdfs/1-s2.0-S0045794925000434-main.txt`。

相关页面：[[lv2025-phase-field-gimp-fracture-method]] · [[lv2025-phase-field-gimp-fracture-results]] · [[lv2025-phase-field-gimp-fracture-critical]] · [[entities/lv-phase-field-gimp]]

## 1. 工程背景

> **⚙️ 非线性类型：** 材料/本构非线性**（核心非线性来自张拉能量的 phase-field degradation、历史变量导致的不可逆断裂和接触状态切换；基体材料在算例中按弹性材料处理，因此不是 PDE 算子非线性，也不是“线性弹性下仅动力响应非线性”的分类）。大变形和碰撞会放大离散误差，但论文的物理失效机制仍是损伤/断裂退化。

动态裂纹的起裂、传播、分叉和多体碰撞对工程设计重要，但实验耗时且受试样差异影响。传统 PF-FEM 在大变形时可能出现网格畸变，需要细化或删除网格；传统 MPM 又会在材料点跨越背景单元时产生数值噪声（§1）。

## 2. Research Gap

已有 phase-field fracture 与 FEM、MPM 或 total-Lagrangian MPM 的工作，尚未同时解决本文聚焦的三件事：显式 phase-field 演化、大变形下的 cell-crossing noise，以及复杂多体接触/碰撞中的摩擦传递。作者因此在 Updated Lagrangian MPM 框架内引入 GIMP，并把粒子接触和 Coulomb friction 纳入同一计算流程（§1）。

## 3. 科学问题

如何不用每个时间步求解隐式全局耦合刚度方程，就稳定推进位移场和 phase field；如何让材料点跨越背景网格时保持足够平滑的形函数；以及如何在多物体共享节点贡献时判定接触、施加法向/切向修正并满足动量守恒，是本文的核心问题。

## 4. 研究目标

1. 构造显式速率相关 phase-field fracture 与 GIMP 的 EPF-GIMP 方法。
2. 用 forward-difference 时间积分和 lumped viscous matrix 更新位移与 phase field。
3. 用 MUSL/double mapping 改善能量守恒，用 GIMP 形函数减弱 cell-crossing noise。
4. 加入粒子到粒子接触和 Coulomb friction，验证拉伸、剪切、Kalthoff-Winkler、环碰撞和三维裂纹分叉。

## 5. 方法机制

裂纹由 `c(x)` 的弥散 phase field 表示，`c=0` 为无裂纹、`c=1` 为完全断裂；张拉弹性能由 `g_c(c)=(1-c)^2` 退化，历史场 `H=max(φ_e^+)` 保证断裂不可逆。显式相场方程包含断裂能、梯度正则化和人工黏性 `η`。

位移场和 phase field 都用 GIMP 形函数从材料点映射到背景网格；节点方程推进后，再把结果映射回材料点并重置网格。MUSL 把更新后的粒子动量重新投影到网格以更新节点速度。方法机制、离散方程和 Algorithm 1 见 [[lv2025-phase-field-gimp-fracture-method]]。

## 6. 结果证据

方板拉伸中，不同人工黏性给出相同裂纹路径，但 `η` 增大时裂纹演化速度降低；减小长度尺度会提高峰值力并推迟峰值时刻。2×2 与 4×4 材料点/单元的裂纹演化一致，力–时间峰值与参考模型相符。

Kalthoff-Winkler 算例在约 14.6 μs 起裂并分叉，左右裂纹相对竖直方向偏转 67.5°，接近实验约 70° 的方向。两种环碰撞速度下，裂纹均从接触面起裂，且与既有 phase-field MPM 结果吻合。三维板的裂纹约在 17 μs 起裂、约 80 μs 到达边界，路径与 Borden 等人的结果一致。完整参数和图表证据见 [[lv2025-phase-field-gimp-fracture-results]]。

## 7. 贡献

- 把显式 rate-dependent phase field 与 GIMP-MPM 组合成一套用于动态断裂的更新流程。
- 用 GIMP 的 `C^1` 连续加权形函数降低材料点跨 cell 时的梯度不连续噪声。
- 将粒子接触预测–修正、Coulomb friction 和 Newton 第三定律约束并入多体碰撞断裂计算。
- 用四类数值例子覆盖拉伸/剪切、实验型动态断裂、二维碰撞和三维裂纹分叉，并讨论黏性、长度尺度和网格密度影响。

## 8. 核心知识点

1. Phase field 隐式表示裂纹路径，适合起裂和分叉，但显式速率项会把时间步稳定性与裂纹演化速度绑在一起。
2. GIMP 的粒子域平均形函数使权函数达到 `C^1` 连续，是缓解 MPM cell-crossing noise 的关键，不是单纯的后处理平滑。
3. 接触算法先由各物体独立解得到 trial velocity，再用质心速度、法向和 Coulomb 上限修正节点速度。
4. MUSL 的二次动量映射与 CFL 时间步共同决定显式更新的稳定性和能量行为。

## 9. Negative Knowledge

- `η` 没有直接物理意义，且论文显示增大它会降低裂纹演化速度；不能把某一黏性设置下的裂纹速度无条件当作材料真实速度。
- 长度尺度和网格密度会改变峰值力、峰值时刻以及能量曲线；粗网格下峰值力和到峰值时间上升，不能只凭一条裂纹路径宣称网格无关。
- 显式积分必须满足 CFL 条件，稳定性以较小时间增量为代价；论文没有给出与隐式方法的统一运行时间比较。
- 文本的主要验证对象是弹性材料中的动态断裂和物体碰撞；弹塑性、延性失效、热耦合和复杂本构不在本文验证范围内。
- 接触推导限制在两个物体，作者只说可向多物体扩展；不能把当前结果直接等同于任意数量碎片的接触验证。
- 论文报告的是裂纹路径、曲线和能量的图形/定性或近似一致，未提供统一误差表、收敛阶、公开输入文件或公开代码 URL。

## 10. 可迁移知识

- 对显式耦合场问题，可把每个场拆成“驱动力–几何阻力–黏性/质量矩阵”的局部更新，避免在每个时间步形成全局稀疏矩阵。
- 当粒子会跨越背景网格时，优先修正插值正则性和粒子域表示，再讨论材料模型；否则物理响应和离散噪声难以分离。
- 接触修正应同时使用接近/分离判据、法向投影和切向摩擦上限，并显式施加作用–反作用约束。
- 对相场或损伤变量，显式加入单调性与范围约束是防止数值更新产生“愈合”或超界状态的通用实现模式。

## 11. 研究机会

1. 系统标定 `η`、`l_c`、网格尺寸和材料点数，建立裂纹速度、峰值力和能量误差的联合收敛指标。
2. 将本文的接触算法扩展到多体碎片、摩擦敏感性和粘着–滑移转变，并用独立接触基准进行验证。
3. 在 phase-field MPM 中加入弹塑性或其他非线性本构，检验显式相场、GIMP 与材料失效之间的耦合稳定性。
4. 发布代码、输入文件和后处理脚本，形成可复现的二维/三维动态断裂基准。

以上为基于论文未覆盖部分提出的机会，不是已报告结果；贡献边界和迁移判断详见 [[lv2025-phase-field-gimp-fracture-critical]]。

## 12. 可复现性

本论文按本库分级为 **medium**。正文给出了能量泛函、强形式、离散方程、Algorithm 1、CFL 稳定条件，以及四类算例的相当一部分几何、材料、网格和时间步参数；但数据可用性声明仅为“所有代码可在向通讯作者合理请求后获得”，没有公开代码 URL，`code_url: []`，也没有外部数据集或 `dataset_url`。

仍无法从提供文本确认的关键复现项包括完整输入文件、实现语言/仓库、求解器封装、全部接触与边界参数、不同黏性/长度尺度图例的精确数值和自动化后处理。因而可重建方法原型和部分基准，但不能声称仅凭公开材料完成逐图独立复现。

复现入口应先按 [[lv2025-phase-field-gimp-fracture-method]] 重建显式更新，再按 [[lv2025-phase-field-gimp-fracture-results]] 的 Tables 1–4 与 Figures 7–20 对照。
