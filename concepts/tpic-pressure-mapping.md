---
id: concept--tpic-pressure-mapping
title: TPIC 压力映射 — 一阶 Taylor 粒子网格传递
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- free-surface
- pressure-mapping
- taylor-particle-in-cell
- tpic
sources:
- sources/papers/juel2026-stabilized-fractional-step-mpm.md
created: '2026-08-01'
updated: '2026-08-01'
confidence: high
---

# TPIC 压力映射

## 定义

TPIC 压力映射使用材料点压力及其压力梯度的一阶 Taylor 展开，把标量压力从材料点传到网格。Juel 等将原用于速度的 Taylor Particle-in-Cell 思想首次用于 MPM 压力映射。^[sources/papers/juel2026-stabilized-fractional-step-mpm.md]

## 作用

标准 PIC 在自由液面附近只做零阶平均，容易把零压界面推向外侧。TPIC 对压力线性外推，使网格压力的零点更接近真实界面，并把映射压力用作自由面 Dirichlet 值的近似，从而缓解材料点跨网格时的压力尖峰。

## 与其他映射比较

- PIC：成本低，但自由面位置偏移明显；
- TPIC：一阶、成本适中，本文默认；
- 二阶 Taylor：界面同样准确，但额外成本没有明显必要。

## 边界

该方法仍是固定于压力迭代之外的近似，不等同于把 ghost-fluid 界面条件直接写入求解器。效果依赖可用的压力梯度、核修正和自由面节点识别。

## 关联页面

- [[concepts/stabilized-pressure-gradient-projection]]
- [[entities/stabilized-fractional-step-two-phase-mpm]]
- [[papers/juel2026-stabilized-fractional-step-mpm-method]]
- [[papers/juel2026-stabilized-fractional-step-mpm-critical]]
