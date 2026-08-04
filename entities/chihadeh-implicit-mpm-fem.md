---
type: entity
title: coupled implicit MPM-FEM approach for brittle fracture and fragmentation
authors:
- Ahmad Chihadeh
- William Coombs
- Michael Kaliske
year: 2023
venue: Computers and Structures
tags:
- domain/computational-mechanics
- entity/model
methods:
- material-point-method
- finite-element-method
- coupled-methods
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
id: entity--chihadeh-implicit-mpm-fem
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
- Computers and Structures
sources:
- sources/papers/chihadeh2023-implicit-mpm-fem-fracture.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# Algorithm entity: coupled implicit MPM-FEM approach for brittle fracture and fragmentation

^[sources/papers/chihadeh2023-implicit-mpm-fem-fracture.md]

来源论文：*A coupled implicit MPM-FEM approach for brittle fracture and fragmentation*（Ahmad Chihadeh、William Coombs、Michael Kaliske，2023，*Computers and Structures* 288: 107143）。DOI：<https://doi.org/10.1016/j.compstruc.2023.107143>。

关联页面：[[chihadeh2023-implicit-mpm-fem-fracture-analysis]] · [[chihadeh2023-implicit-mpm-fem-fracture-method]] · [[chihadeh2023-implicit-mpm-fem-fracture-results]] · [[chihadeh2023-implicit-mpm-fem-fracture-critical]]

## 1. 定义

这是 Chihadeh、Coombs 和 Kaliske 在 2023 年论文中提出并数值展示的算法组合：以隐式 MPM 和 FEM 为两个计算子域，用 bond elements 把 FE 与 MPM 激活背景单元在位移层面连接，并在同一个 monolithic 方程组中同时求解。

它不是单独的材料本构，也不是一个数据集；它是面向大变形、脆性断裂、碎片化和 MPM–FEM 接触的耦合求解框架。

## 2. 组成机制

- **隐式 MPM：** 采用 CPDI2 插值，把材料点数据映射到背景网格，进行隐式 Newmark + Newton–Raphson 求解，再映射回材料点并重置网格。
- **nodal bond：** 以 FE 节点和激活 MPM 单元同位置插值位移之差为 slip，通过用户定义的罚刚度抑制界面滑移。
- **intermediate bond：** 当 FE 单元比 MPM 网格粗时，在 FE 表面中间位置补充连接，以保持界面中部连通性。
- **contact bond：** 当 FE 节点进入激活 MPM 单元、满足距离条件且两体相向运动时激活；法向罚项防止穿透。
- **eigenfracture conversion：** 当 FE 的裂纹驱动能量达到 `G_c |C|`，单元从 intact 变为 eroded，并转换成材料点。

## 3. 论文中的证据

梁例子中，MPM、FEM 和 MP–FE 的梁端位移相同。应力波例子中，粗 FE 网格若没有 intermediate bonds 会失真，加入后可恢复传播；网格细化时归一化应力趋向解析关系。

接触例子验证了接近且相向运动时的 bond 激活。L 形板、动力裂纹分叉和三维冲击板例子展示了侵蚀 FE 转为材料点、裂纹传播/分叉和冲击穿透。

## 4. 适用范围与限制

论文的材料与断裂展示基于几何非线性、St. Venant–Kirchhoff 和 eigenfracture；不应直接当作对塑性、延性损伤或其他材料模型的验证。

接触算例取 `C_t=0`，因此实体只展示无摩擦接触。提供文本没有给出 penalty 具体数值、完整求解器容差、公开代码或数据；论文 Data availability 写明没有使用数据。

论文还建议 MPM 网格实际应比 FE 网格更细或至少不更粗，FE 更细的耦合没有被明确研究。

## 5. 可复现性状态

方法方程和主要算例参数较完整，但实现为 in-house Fortran MP-FE code，`code_url: []`；没有研究数据集，`dataset_url: []`。按知识库标准标为 `medium`，表示可据正文重建原型，不能直接下载复现。

方法展开：[[chihadeh2023-implicit-mpm-fem-fracture-method]]；批判性边界：[[chihadeh2023-implicit-mpm-fem-fracture-critical]]。
