---
id: concept--separable-mpm-boundary-via-fem
title: "FEM 显式几何驱动的可分离 MPM 边界"
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
keywords:
- irregular-mpm-boundary
- separable-boundary
- prescribed-fem-motion
sources:
- sources/papers/li2022-bfemp.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
---

# FEM 显式几何驱动的可分离 MPM 边界

## Definition

当 FEM 域全部节点位移被规定时，FEM 网格可作为具有显式边界几何、可移动、可分离并可设置摩擦的 MPM 运动学边界。MPM 粒子通过障碍接触与该边界交互，而不是通过在背景网格节点上直接锁定速度。^[sources/papers/li2022-bfemp.md]

## Advantages

- 边界几何可比 MPM 网格更精细；
- 分离时不产生由网格锁定导致的数值黏附；
- 支持曲线、曲面及非规则运动边界；
- 摩擦参数直接作用于粒子–边界接触。

## Contrast with Grid-Based Boundary Conditions

传统 level-set 或网格速度约束在有限网格分辨率下具有涂抹效应，可能造成边界穿透或分离黏连。显式 FEM 边界把几何查询与 MPM 背景网格分离。

## Limitations

- FEM 边界需要初始正间隙；
- 接触针对粒子中心，未完整考虑粒子有限支持；
- 复杂边界与大量粒子会增加接触查询；
- 该机制不是切割算法，薄边界两侧的粒子仍可能通过 MPM 核相互通信。

## Relations

- implemented by [[entities/bfemp]];
- uses [[concepts/particle-simplex-barrier-coupling]];
- relevant to irregular-boundary MPM and moving-tool simulations.
