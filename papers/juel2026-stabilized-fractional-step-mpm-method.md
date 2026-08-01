---
id: paper--juel2026-stabilized-fractional-step-mpm-method
title: "Juel et al. (2026) — 稳定化分步双相 MPM 方法机制"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
keywords:
- double-point
- matrix-free-cg
- pressure-poisson
- semi-implicit-drag
- spgp
- tpic-pressure
sources:
- sources/papers/juel2026-stabilized-fractional-step-mpm.md
created: '2026-08-01'
updated: '2026-08-01'
confidence: high
evidence_scope: full-text
---

# 方法机制

## 总体数据流

```text
固相材料点 + 液相材料点
  → P2G：质量、体积、APIC 速度、TPIC 压力、孔隙率、阻力
  → 速度预测：有效应力、黏性、重力、半隐式固液阻力
  → 压力泊松：增量压力 + SPGP + 自由面罚约束
  → 速度校正
  → G2P：速度、压力、压力梯度、变形梯度、孔隙率
  → 可选粒子重排
```

## 连续体与主变量

模型基于饱和固–液重叠连续体，分别满足动量守恒，并通过 Darcy 型阻力耦合。主变量为固相速度 $\mathbf v_s$、液相速度 $\mathbf v_l$ 和孔压 $p$。采用双点离散分别追踪两相，因此可守恒液体质量并表示相分离。^[sources/papers/juel2026-stabilized-fractional-step-mpm.md]

## 压力分步离散

参数 $\beta=0$ 表示非增量预测器忽略旧压力，$\beta=1$ 表示增量预测器显式保留旧压力。两者均随后求解压力增量并校正速度。统一阻力参数 $\boldsymbol\theta=[\theta_0,\theta_1,\theta_2]$ 覆盖显式、半隐式、隐式和多种 Crank–Nicolson 方案；论文默认 $[1,1,0]$ 半隐式阻力。

## SPGP 稳定化

[[concepts/stabilized-pressure-gradient-projection]] 将压力梯度与其 $L^2$ 投影之差加入压力泊松弱式，抑制等阶速度–压力插值导致的棋盘孔压。投影在上一时间步滞后使用，推荐 $\tau_{stab}=2\Delta t$。

## TPIC 压力映射与自由液面

[[concepts/tpic-pressure-mapping]] 用材料点压力及其梯度的一阶 Taylor 展开完成 P2G。自由面节点由液体材料点球的有符号距离识别，TPIC 外推压力作为零压界面的近似 Dirichlet 值，再以罚项弱施加。

## 压力求解器

压力泊松矩阵对称正定，采用 Jacobi 预条件 CG。矩阵–向量乘积按需计算，不显式组装稀疏矩阵；压力算子只在液相材料点上求和，以减少双相重复积分。

## 输入、输出与求解策略

输入包括两相初始几何、材料密度、孔隙率、渗透率/代表粒径、黏度、固相本构、边界条件与时间步。输出包括两相位置/速度、孔压、固相应力、孔隙率和相分离形态。每步执行 10 个阶段，详见论文第 4.3 节。

## 假设与失效边界

- 当前验证以完全饱和、等温问题为主；
- 固相使用超弹性，未实际验证塑性；
- 自由液面、核修正与粒子重排对复杂大变形不可省略；
- 时间步仍受固相波速和高速液体射流限制；
- CG 压力泊松占主要成本。

## 关联页面

- [[papers/juel2026-stabilized-fractional-step-mpm-analysis]]
- [[papers/juel2026-stabilized-fractional-step-mpm-results]]
- [[papers/juel2026-stabilized-fractional-step-mpm-critical]]
- [[entities/stabilized-fractional-step-two-phase-mpm]]
