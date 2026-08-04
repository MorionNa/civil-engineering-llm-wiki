---
type: entity
title: MPM beam particle with frictional contact
authors:
- Jingu Kang
- Michael A. Homel
- Eric B. Herbold
year: 2022
venue: International Journal for Numerical Methods in Engineering
doi: 10.1002/nme.6886
tags:
- domain/computational-mechanics
- entity/model
methods:
- CPDI2
- beam-particle
- multi-velocity-field-contact
- Coulomb-friction
- Euler-Bernoulli
- Timoshenko
results:
- analytical-validation
- finite-element-comparison
- dynamic-contact
- fiber-mixing
failure_modes:
- contact-gap
- grid-resolution-dependence
- no-angular-momentum-contact
- small-strain-beam-constitutive-assumption
datasets:
- paper-defined-numerical-benchmarks
reproducibility: medium
code_url: []
dataset_url: []
id: entity--kang-beam-particle
status: active
project: civil-engineering-llm-wiki
keywords:
- material-point-method
- beam-elements
- contact-mechanics
- friction
- large-deformation
- coupled-methods
- CPDI2
- beam-particle
- multi-velocity-field-contact
- Coulomb-friction
- Euler-Bernoulli
- Timoshenko
- analytical-validation
- finite-element-comparison
- dynamic-contact
- fiber-mixing
- contact-gap
- grid-resolution-dependence
- no-angular-momentum-contact
- small-strain-beam-constitutive-assumption
- paper-defined-numerical-benchmarks
- International Journal for Numerical Methods in Engineering
sources:
- sources/papers/kang2022-beam-contact-mpm.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# MPM beam particle with frictional contact

^[sources/papers/kang2022-beam-contact-mpm.md]

## 定义

该算法是 Kang、Homel 和 Herbold 在 2022 年论文中提出的 MPM 梁离散：用一个含两个端节点的 reduced-order beam particle 表示一段直梁，并把端节点的平移/转动自由度、梁截面刚度和质量惯性传递到背景网格。完整论文总览见 [[kang2022-beam-contact-mpm-analysis]]，逐步机制见 [[kang2022-beam-contact-mpm-method]]。

## 核心机制

- 两个端节点各有 3 个平移和 3 个转动 DOF；端点位置表示轴向变形，端点转角表示曲率/弯曲。
- 梁粒子质心保存平移速度、角速度、局部正交基、lumped mass 和惯性张量。
- 质量/线动量按两端六面体网格形函数的平均映射到背景网格：`S_gb = 0.5 S_g(x_I) + 0.5 S_g(x_J)`。
- 背景网格增加角速度和角加速度场；梁粒子的角动量以惯性加权方式映射，网格力矩更新后再回写端部转角。
- 内力和内力矩通过 Euler–Bernoulli 或 Timoshenko 梁切线刚度矩阵计算，截面面积、二次矩、极惯性矩和剪切系数进入结构响应。
- 梁边缘布置 spatial nodes 表示截面空间范围；它们把梁的试探速度映射到共享网格，参与 multi-velocity-field 接触。
- 接触法向来自不同材料速度场的质量梯度；法向力防止穿透，切向力按 Coulomb 摩擦系数截断。

## 证据与适用场景

论文通过纯弯曲悬臂梁、空间六边形框架、动力梁、45° 曲梁和厚梁振动与解析/FEM/既有实验或数值结果对照，并用纤维堆积、框架落球和两类纤维混合展示大转动摩擦接触。结果汇总见 [[kang2022-beam-contact-mpm-results]]。

适用对象包括梁、框架、纤维和其他以细长构件为主的多体结构；论文还提出它可用于纤维—CPDI2 基体复合材料、纤维分散和制造过程混合。它不是通用的高应变实体材料模型，也不是已经验证的滚动接触求解器。

## 边界与失败模式

1. 接触力只使用平动速度，没有把 angular-momentum field 纳入接触冲量；滚动圆柱会滑动而非正确滚动。
2. 多速度场接触可能产生 gap；背景网格过粗会影响接触位置，网格小于梁直径时又可能在梁内部接触。
3. 梁粒子采用大位移/大转动、小应变的梁本构，初始长度、面积和惯性张量保持常数；论文仅指出非线性材料可通过扩展切线刚度实现。
4. 论文没有给出公开代码 URL 或数据仓库 URL；数据可得性声明是大部分结果在文中、附加数据可向通讯作者合理请求。

## 关系与迁移

该算法连接了 [[kang2022-beam-contact-mpm-method]] 的结构更新和多速度场接触，也与 [[kang2022-beam-contact-mpm-critical]] 中讨论的角动量、gap、自适应网格和非线性材料问题直接相关。可迁移的设计模式是：在粒子—网格框架中并行传递平动与转动状态，并用空间代理节点让非体积对象参与统一接触。
