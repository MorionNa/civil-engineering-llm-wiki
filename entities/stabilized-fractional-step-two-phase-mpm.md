---
id: entity--stabilized-fractional-step-two-phase-mpm
title: 稳定化增量分步双相双点 MPM
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/computational-mechanics
- entity/model
- evidence/paper
keywords:
- double-point-mpm
- hydromechanical-coupling
- incremental-fractional-step
- spgp
- tpic-pressure
sources:
- sources/papers/juel2026-stabilized-fractional-step-mpm.md
created: '2026-08-01'
updated: '2026-08-01'
confidence: high
---

# 稳定化增量分步双相双点 MPM

## 定义

该方法是 Juel 等提出的饱和固–液两相大变形求解框架。固相和液相分别由材料点追踪，网格上通过增量分步压力离散、半隐式阻力、[[concepts/stabilized-pressure-gradient-projection]] 和 [[concepts/tpic-pressure-mapping]] 完成稳定耦合。^[sources/papers/juel2026-stabilized-fractional-step-mpm.md]

## 关键组成

- 固液双点离散与相分离；
- APIC 速度映射和 TPIC 压力映射；
- 速度预测–压力泊松–速度校正；
- SPGP 压力梯度投影稳定化；
- 改进孔隙率/渗透率映射；
- 核修正、自由面罚约束和可选粒子重排；
- Taichi GPU、稀疏网格、矩阵自由 CG。

## 适用边界

已验证饱和、等温、超弹性固相下的固结、自由液面、低渗透和相分离。尚未验证非饱和、热耦合、塑性损伤或真实滑坡全尺度问题。

## 项目角色

可作为含水地质灾害与局部土–水耦合的高可信数值基线，也可为局部 MPM 与结构模型耦合提供两相模块；不能直接视为建筑结构倒塌求解器。

## 关联页面

- [[papers/juel2026-stabilized-fractional-step-mpm-analysis]]
- [[papers/juel2026-stabilized-fractional-step-mpm-method]]
- [[papers/juel2026-stabilized-fractional-step-mpm-results]]
- [[papers/juel2026-stabilized-fractional-step-mpm-critical]]
