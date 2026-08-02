---
id: entity--mpm-lite
title: MPM Lite — 求解阶段无粒子积分的材料点法
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- entity/model
- evidence/paper
keywords:
- apic
- fem-style-integration
- linear-kernel
- material-point-method
- mpm-lite
sources:
- sources/papers/feng2026-mpm-lite.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
---

# MPM Lite

## 定义

MPM Lite 是 Feng 等提出的混合拉格朗日–欧拉连续体仿真方法。粒子仅携带运动状态与材料历史，质量、动量、体积和 Kirchhoff 应力先重采样到固定单元中心；力组装与显式/隐式时间积分完全在网格上执行，因此求解阶段复杂度不再随每单元粒子数增长。^[sources/papers/feng2026-mpm-lite.md]

## 关键组成

- 线性核粒子—单元中心—节点两跳传递；
- 广延量 $V\tau$ 的应力传递，避免直接平均变形梯度；
- [[concepts/particle-independent-grid-integration]]；
- [[concepts/rotation-free-stretch-reconstruction]]；
- 六面体 FEM 式增量势隐式求解；
- 显式、APIC 和退化 FLIP/PIC 模式；
- 多材料、塑性、流体、断裂与现成求解器接口。

## 已验证能力

论文展示了超弹性、von Mises 塑性、Drucker–Prager 砂、Cam-Clay 断裂、雪、砂水耦合、金属与 Herschel–Bulkley 黏塑性材料；在高 PPC 隐式场景中最高报告 15.9 倍加速。

## 适用边界

当前旋转无关伸长重构依赖各向同性；单点六面体积分对弯曲主导、薄结构和强子单元应力变化可能偏软；完整流程中的粒子平流、重采样和本构更新仍随粒子数增长。

## 项目角色

MPM Lite 可作为大变形、断裂与碎片阶段的高效局部 MPM 候选基线。迁移到钢筋混凝土倒塌前，需要补充各向异性/损伤本构、薄构件积分、接触验证以及与梁壳或 AEM 的守恒耦合。

## 关联页面

- [[papers/feng2026-mpm-lite-analysis]]
- [[papers/feng2026-mpm-lite-method]]
- [[papers/feng2026-mpm-lite-results]]
- [[papers/feng2026-mpm-lite-critical]]
