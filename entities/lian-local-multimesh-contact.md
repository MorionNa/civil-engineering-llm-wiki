---
type: entity
title: local multi-mesh contact coupling method
authors:
- Y.P. Lian
- X. Zhang
- Y. Liu
year: 2011
venue: Computer Methods in Applied Mechanics and Engineering
tags:
- domain/computational-mechanics
- entity/model
methods:
- hybrid-node contact
- background-grid momentum correction
- Coulomb friction
- central difference integration
results:
- plate impact
- sphere rolling
- thick-plate perforation
- fluid-structure interaction
failure_modes:
- mesh-ratio mismatch
- interface oscillation
- background-grid penetration
- early contact
datasets: []
reproducibility: medium
code_url: []
dataset_url: []
id: entity--lian-local-multimesh-contact
status: active
project: civil-engineering-llm-wiki
keywords:
- coupled-methods
- contact-mechanics
- material-point-method
- finite-element-method
- large-deformation
- friction
- hybrid-node contact
- background-grid momentum correction
- Coulomb friction
- central difference integration
- plate impact
- sphere rolling
- thick-plate perforation
- fluid-structure interaction
- mesh-ratio mismatch
- interface oscillation
- background-grid penetration
- early contact
- Computer Methods in Applied Mechanics and Engineering
sources:
- sources/papers/lian2011-mpm-fem-coupling.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# local multi-mesh contact coupling method

^[sources/papers/lian2011-mpm-fem-coupling.md]

## 定义

这是 Lian、Zhang 和 Liu 在 2011 年论文中用于耦合 FEM 体与 MPM 体的局部多网格接触方法。它把小变形物体用 FEM 表示，把极端变形物体用 MPM 表示，再借助 MPM 的规则背景网格处理两者的接触动量交换，而不要求两侧网格共节点。

论文原始实现称为 coupled finite element–material point（CFEMP）方法，并将 8 节点六面体单元加入三维显式 MPM3D 代码。详见 [[lian2011-mpm-fem-coupling-analysis]]。

## 核心机制

1. MPM 粒子和 FEM 接触表面节点分别把质量、半步动量映射到同一个背景网格点。
2. 对同一网格点的两侧计算分体速度；相对速度沿 FEM 外法向满足接触判据时，标记该点发生接触。
3. 对参与该网格点的 FEM 表面节点标记为 hybrid nodes，使其在接触阶段像粒子一样参与背景网格动量方程。
4. FEM 表面法向由相关单元面法向求和；MPM 表面法向由粒子质量梯度近似。
5. 通过不可穿透条件求法向接触力；通过无滑移条件求 stick 切向力，再用 `μ f_n` 的 Coulomb 上限得到 slip 力。
6. 因为 MPM 每个时间步末会丢弃变形网格，算法在应力更新前先用法向力第一项修正 MPM 网格动量和 FEM hybrid-node 速度，随后才完成主体内力和接触力更新。

方法的详细公式和 11 步实现顺序见 [[lian2011-mpm-fem-coupling-method]]。

## 证据与适用范围

论文用对称/非对称板撞击、斜板球滚动、厚板穿孔和水柱-弹性障碍物流固耦合进行验证。板撞击和滚动与解析解比较，穿孔与实验比较，水柱问题与 PFEM 等已有数值结果比较；具体数字见 [[lian2011-mpm-fem-coupling-results]]。

该方法适合两侧变形尺度明显不同、且需要接触传力的显式动力学问题。它的优势依赖于 FEM 与 MPM 网格尺度匹配和共同临界时间步长；论文的尺寸比敏感性分析报告，过大的 FEM 单元/MPM 网格尺寸比会引起界面振荡，并可能产生穿透。

## 边界与未披露项

- 论文围绕规则背景网格、8 节点六面体单元和中心差分实现，未证明任意单元类型、任意高阶形函数或隐式积分下的同样表现。
- 穿孔算例忽略摩擦；水柱算例没有可用实验结果。
- 文本未提供 MPM3D 公共代码 URL、输入文件或独立数据集，因此实体的复现等级为 medium，而非 high。
