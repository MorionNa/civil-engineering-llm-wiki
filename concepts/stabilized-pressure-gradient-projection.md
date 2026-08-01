---
id: concept--stabilized-pressure-gradient-projection
title: SPGP — 稳定化压力梯度投影
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- inf-sup
- pressure-gradient-projection
- pressure-stabilization
- spgp
sources:
- sources/papers/juel2026-stabilized-fractional-step-mpm.md
created: '2026-08-01'
updated: '2026-08-01'
confidence: high
---

# SPGP：稳定化压力梯度投影

## 定义

SPGP 通过惩罚压力梯度与其 $L^2$ 投影之间的差异，稳定等阶速度–压力插值下的压力泊松方程。Juel 等首次将 Codina 的 FEM SPGP 方法适配到 MPM。^[sources/papers/juel2026-stabilized-fractional-step-mpm.md]

## 机制

投影量在每个时间步末计算，并在下一步滞后进入压力系统。它针对的是 inf-sup 条件不足产生的棋盘压力，而不是通过人为降低液体体积模量来换取稳定。

## 证据

在固结问题中，误差在 $\tau_{stab}\approx2\Delta t$ 最小；复杂溃坝在约 $1.33\Delta t$ 以上保持稳定。SPGP 投影仅占三维算例总耗时 1.70%。

## 边界

过强稳定化会平滑压力曲率；推荐参数不是普适常数。SPGP 也不能修复错误自由面、核边界误差、孔隙率跳变或严重材料点聚集。

## 关联页面

- [[entities/stabilized-fractional-step-two-phase-mpm]]
- [[concepts/tpic-pressure-mapping]]
- [[papers/juel2026-stabilized-fractional-step-mpm-method]]
- [[papers/juel2026-stabilized-fractional-step-mpm-results]]
