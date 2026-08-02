---
id: paper--liu2025-incompressible-crack-mpm-method
title: "Liu et al. (2025) — 体积保持 MPM 不可压缩裂纹模型方法机制"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- damage-evolution
- drucker-prager
- mls-mpm
- state-transition
- volume-gradient
sources:
- sources/papers/liu2025-incompressible-crack-mpm.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
evidence_scope: full-text
---

# 方法机制

## 总体数据流

```text
粒子应力与变形状态
  → Weibull 主失效应力
  → 最大主有效应力驱动局部损伤
  → 仅软化拉伸主应力
  → 损伤超过阈值：根据体积状态重置 F
  → 切换为体积保持 Drucker–Prager 碎屑相
  → MLS-MPM P2G / 网格更新 / G2P
```

该流程在粒子属性更新阶段完成，不显式构造裂纹面。^[sources/papers/liu2025-incompressible-crack-mpm.md]

## MPM 与基础本构

作者采用 MLS-MPM 内力离散和 Neo-Hookean 弹性。粒子携带位置、速度、体积、应力和弹塑性变形梯度；P2G 后在背景网格处理应力与碰撞，再由 G2P 更新粒子。

## 随机失效强度

为减弱规则网格对裂纹模式的控制，每个粒子的主失效应力按体积相关 Weibull 分布采样。论文实验中 Weibull 模数设为 4，使微观缺陷随机性进入裂纹萌生位置。

## 局部损伤演化

[[concepts/compression-aware-damage-transition]] 使用最大主有效应力作为标量驱动力。有效应力张量在主空间分解为拉伸部分和压缩部分；损伤变量按局部线性软化更新，但只缩放拉伸主应力，压缩主应力保留。

## 完全损伤状态转换

当损伤变量超过阈值 $\xi$，粒子进入完全损伤集合。若当前体积处于膨胀状态，不额外压缩；若处于压缩状态，则通过体积保留参数 $\eta$ 重置弹性变形梯度的体积分量。该转换决定碎裂脆性、残余体积和能量释放。

## 碎屑塑性

[[concepts/volume-preserving-debris-plasticity]] 采用 Drucker–Prager 屈服面。为了保持塑性流动中的体积，作者使用非关联流动方向，只校正偏应力。摩擦角控制碎屑从近无黏流体到摩擦颗粒材料的行为。

## 额外体积变形梯度

传统做法依据弹性变形梯度判断膨胀/压缩，但弹性部分会被 return mapping 重置，可能误判并产生体积增长。作者额外累计体积变形梯度 $F^V$，其行列式代表相对初始构形的真实体积比，并独立于塑性修正。

## 输入与输出

输入包括初始粒子/网格、弹性参数、断裂能、Weibull 强度、完全损伤阈值、体积保留参数、摩擦角和边界条件。输出包括粒子位置、速度、损伤、碎屑状态、应力、弹性变形与真实体积历史。

## 假设与失效边界

- 损伤为局部模型，裂纹带宽仍受网格影响；
- 完全损伤后统一转为无黏聚 Drucker–Prager 碎屑，未表示块体碎片内部刚度；
- 没有显式裂纹面和位移跳跃，因此裂纹几何是粒子分离的结果；
- 主要面向视觉仿真，未进行工程材料反演标定；
- 论文未报告严格能量守恒、裂纹面能量和网格收敛。

## 关联页面

- [[liu2025-incompressible-crack-mpm-analysis]]
- [[liu2025-incompressible-crack-mpm-results]]
- [[liu2025-incompressible-crack-mpm-critical]]
- [[entities/incompressible-crack-mpm]]
