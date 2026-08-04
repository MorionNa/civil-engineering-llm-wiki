---
type: entity
title: implicit gradient-enhanced microplane damage material model
authors:
- Osvaldo Andres Oropeza-Navarro
- Ahmad Chihadeh
- Jakob Platen
- Michael Kaliske
year: 2024
venue: Computers and Structures
tags:
- domain/computational-mechanics
- entity/model
methods:
- microplane
- gradient-enhanced
- damage-mechanics
- coupled-methods
results:
- damage-mechanics
- coupled-methods
- fracture
failure_modes:
- damage-mechanics
- numerical-methods
- large-deformation
datasets: []
reproducibility: medium
code_url: []
dataset_url: []
id: entity--oropeza-microplane-damage
status: active
project: civil-engineering-llm-wiki
keywords:
- microplane
- gradient-enhanced
- damage-mechanics
- material-point-method
- finite-element-method
- coupled-methods
- large-deformation
- fracture
- numerical-methods
- Computers and Structures
sources:
- sources/papers/oropeza-navarro2024-microplane-damage.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# implicit gradient-enhanced microplane damage material model

^[sources/papers/oropeza-navarro2024-microplane-damage.md]

## 定义

这是 Oropeza-Navarro 等人在 2024 年论文中用于有限变形纤维增强混凝土的材料模型：以微平面描述基体与纤维方向各向异性，以隐式梯度增强的非局部等效应变正则化软化损伤，并嵌入耦合隐式 MPM-FEM。论文说明其损伤构式基于 Platen et al. 的非局部微平面工作（PDF pp. 1–2）。

## 核心机制

- 用 21 个单位球面微平面积分方向，将有限变形应变投影到体积、偏量和纤维方向分量。
- 以每个微平面的局部等效应变最大值作为体材料局部变量 \(\eta\)。
- 用改进 Helmholtz 方程求非局部变量 \(\bar\eta\)，并把它映射回各微平面。
- 通过历史变量 \(\gamma_{mic}=\max(\gamma_0,\bar\eta_{mic})\) 驱动基体损伤 \(d_{mic}\)。
- 损伤削弱基体能量和应力；论文的设定不包含纤维失效贡献。
- 在 MPM-FEM 界面，通过 nonlocal bond element 传递非局部等效应变，而不仅是机械位移。

方法中的双场残量、交叉切线和 bond 刚度见 [[oropeza-navarro2024-microplane-damage-method]]。

## 证据与适用范围

论文用缺口拉伸、纤维增强悬臂和 L 形混凝土试件进行数值验证；报告 nonlocal bond 在选定配置下改善局部化并得到接近 FEM/MPM/实验的力–位移或损伤结果，详见 [[oropeza-navarro2024-microplane-damage-results]]。

## 边界与限制

论文明确不考虑纤维脆性失效；纯机械 bond 在部分界面配置中会导致非物理局部化；材料点移动会造成卸载–再加载积分位置差异；E–F 段还报告了由最大基体损伤与纤维对齐引起的刚度跳变振荡。

论文未披露代码或数据 URL，且没有完整输入文件、penalty 标定规则和系统敏感性分析。因此该实体的复现等级为 medium，而不是 high。

## 相关页面

- 论文总览：[[oropeza-navarro2024-microplane-damage-analysis]]
- 结果证据：[[oropeza-navarro2024-microplane-damage-results]]
- 批判性边界：[[oropeza-navarro2024-microplane-damage-critical]]
