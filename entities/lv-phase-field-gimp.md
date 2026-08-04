---
type: entity
title: explicit phase-field generalized interpolation material point method
authors:
- Chi Lv
- Xiao-Ping Zhou
year: 2025
venue: Computers and Structures
tags:
- domain/computational-mechanics
- entity/model
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
failure_modes:
- large-deformation
- fracture
- contact-mechanics
- numerical-methods
datasets: []
reproducibility: medium
code_url: []
dataset_url: []
id: entity--lv-phase-field-gimp
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
- numerical-methods
- impact
- large-deformation
- Computers and Structures
sources:
- sources/papers/lv2025-phase-field-gimp-fracture.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# explicit phase-field generalized interpolation material point method

^[sources/papers/lv2025-phase-field-gimp-fracture.md]

## 定义

**Explicit phase field generalized interpolation material point method（EPF-GIMPM）** 是 Chi Lv 与 Xiao-Ping Zhou 在 2025 年论文中提出的动态断裂数值算法。它把显式速率相关 phase-field fracture 与 Generalized Interpolation Material Point Method（GIMP）结合，并在材料点之间加入接触预测–修正和 Coulomb friction。论文原题为 *Explicit phase field generalized interpolation material point method for dynamic fracture problems*。

对应论文总览、方法和结果分别见 [[lv2025-phase-field-gimp-fracture-analysis]]、[[lv2025-phase-field-gimp-fracture-method]] 和 [[lv2025-phase-field-gimp-fracture-results]]。

## 核心机制

1. **显式 phase field**：用张拉/压缩能量分解、`g_c(c)=(1-c)^2`、历史场 `H` 和人工黏性 `η` 更新弥散裂纹；`c` 施加单调增长和 `0≤c≤1` 约束。
2. **GIMP 插值**：在材料点特征域上平均背景网格形函数，使权函数达到 `C^1` 连续，降低材料点跨 cell 时的梯度不连续噪声。
3. **显式 MPM 时间步**：质量、动量、应力和 phase field 从粒子映射到背景节点，节点更新后再映射回粒子并重置背景网格；时间步满足位移场与相场共同给出的 CFL 条件。
4. **MUSL/double mapping**：更新粒子动量后再次投影到网格并重算节点速度，以改善论文所述的能量守恒性质。
5. **接触与摩擦**：多个物体在同一节点有贡献时，先用各物体 trial velocity 预测，再基于质心速度和接触法向修正法向/切向速度，并用 Coulomb 上限限制摩擦力；法向和摩擦力满足作用–反作用。

## 证据范围

论文用预裂方板拉伸和剪切研究人工黏性、长度尺度、网格密度和材料点数；用 Kalthoff-Winkler 试验比较裂纹方向；用双环碰撞展示接触面起裂和摩擦；用三维板展示动态裂纹分叉。作者报告这些算例的路径、曲线或能量与参考结果吻合较好，但没有给出公开代码 URL 或独立数据集。

## 边界与复现

EPF-GIMPM 的验证范围主要是弹性材料动态断裂和所示物体碰撞。人工黏性、相场长度尺度和网格会影响响应；显式积分受 CFL 时间步限制。接触推导首先针对两个物体，弹塑性和更复杂多体场景被列为未来方向。代码声明可向通讯作者合理请求，`code_url: []`，`dataset_url: []`，因此实体复现等级为 medium。

## 关联

方法机制详见 [[lv2025-phase-field-gimp-fracture-method]]；结果证据见 [[lv2025-phase-field-gimp-fracture-results]]；失败边界和可迁移知识见 [[lv2025-phase-field-gimp-fracture-critical]]。
