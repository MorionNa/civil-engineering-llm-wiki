---
id: entity--incompressible-crack-mpm
title: 不可压缩裂纹 MPM — 体积保持损伤–碎屑转换模型
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- entity/model
- evidence/paper
keywords:
- continuum-damage-mechanics
- drucker-prager-debris
- fracture
- incompressible-crack
- mpm
sources:
- sources/papers/liu2025-incompressible-crack-mpm.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
---

# 不可压缩裂纹 MPM

## 定义

不可压缩裂纹 MPM 是 Liu 等提出的动态断裂框架。它在局部连续损伤模型中保留部分损伤的拉伸应力软化，并在损伤超过阈值后把粒子转换为体积保持的 Drucker–Prager 摩擦碎屑。^[sources/papers/liu2025-incompressible-crack-mpm.md]

## 核心组成

- 体积相关 Weibull 主失效应力；
- 最大主有效应力驱动的局部损伤；
- 拉伸主应力软化、压缩应力保留；
- [[concepts/compression-aware-damage-transition]]；
- [[concepts/volume-preserving-debris-plasticity]]；
- 额外体积变形梯度追踪真实体积历史；
- MLS-MPM 粒子–网格传递与自动碎片接触。

## 适用范围

论文展示了脆性/半脆性图形学对象的压缩、拉伸、复杂几何和碎屑反复挤压。它特别针对传统应力软化在压缩下难以形成裂纹、以及碎屑 return mapping 导致体积增长的问题。

## 局限

该模型仍是局部损伤，裂纹厚度受网格分辨率影响；完全损伤粒子被统一视为摩擦碎屑，没有显式大块碎片、黏聚残余或钢筋桥联。论文也未进行工程材料定量标定和网格收敛验证。

## 项目角色

可作为局部 MPM 结构倒塌中的压碎–碎屑状态转换候选模块，与 [[mpm-lite]] 和 [[unified-sparse-mpm]] 在计算层面互补，但组合后的精度、稳定性和性能尚未验证。

## 关联页面

- [[papers/liu2025-incompressible-crack-mpm-analysis]]
- [[papers/liu2025-incompressible-crack-mpm-method]]
- [[papers/liu2025-incompressible-crack-mpm-results]]
- [[papers/liu2025-incompressible-crack-mpm-critical]]
