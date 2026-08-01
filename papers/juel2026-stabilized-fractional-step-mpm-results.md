---
id: paper--juel2026-stabilized-fractional-step-mpm-results
title: "Juel et al. (2026) — 稳定化分步双相 MPM 结果证据"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
keywords:
- consolidation
- dam-break
- permeability-sensitivity
- phase-separation
- performance
sources:
- sources/papers/juel2026-stabilized-fractional-step-mpm.md
created: '2026-08-01'
updated: '2026-08-01'
confidence: high
evidence_scope: full-text
---

# 结果与证据

## 小应变固结与收敛

增量格式总体误差低于非增量格式；排除异常阻力方案后，修正误差由约 $6\times10^{-3}$ 收敛至 $3\times10^{-4}$。最优方案在误差低于 $10^{-3}$ 后出现平台，前期收敛率接近二阶。^[sources/papers/juel2026-stabilized-fractional-step-mpm.md]

## 渗透率敏感性

固定空间/时间离散，将渗透率从 $10^{-10}$ 降至 $10^{-12}\,\mathrm{m^2}$：非增量格式随阻力方案出现过度耗散或虚假压力峰值；增量格式曲线基本重合，仅因固定网格难以解析陡峭梯度而有小偏差。这是论文最关键的判别证据。

## SPGP 参数

在 $\tau_{stab}\in[0.01,100]\Delta t$ 中，固结误差在约 $2\Delta t$ 最小。溃坝完整运行 7 s 所需临界值约为 $1.33\Delta t$，因此作者推荐 $2\Delta t$。人工可压缩性达到能稳定溃坝的程度时，会显著损害固结精度。

## 自由液面与渗流

液体进入/离开孔隙率 0.5 的刚性多孔介质时，压力保持平稳，质心终值与修正理论值及 Mixed-VMS 结果接近。TPIC 比 PIC 更准确地外推零压界面，并减少网格穿越引起的高频“blip”。

## 大应变固结

模型把土柱压缩至原高的 24%，即 76% 压缩，孔压、孔隙率与沉降总体匹配有限应变解析解。固相表面附近应力与孔隙率出现噪声，提示高孔隙率梯度仍可能触发固相不稳定。

## 溃坝与多孔介质拦截

稳定化增量格式在液体溃坝中避免了非增量格式的压力尖峰，并与实验 95% 置信区间和 VMS 数值结果总体一致。穿过玻璃珠/碎石多孔柱的两组溃坝表面轮廓与实验及既有数值研究处于合理误差范围。

## 三维饱和球碰撞

低渗透率 $10^{-12}\,\mathrm{m^2}$ 时液体难排出、回弹较慢；高渗透率 $10^{-6}\,\mathrm{m^2}$ 时液体迅速分离并形成高速水射流。改进孔隙率映射对相分离稳定性至关重要，Shepard 映射会失稳。

## 计算性能

860 万粒子算例在 RTX 4070 Ti 上约需 100 min。每步耗时分布：压力泊松 79.28%，预测速度 4.86%，G2P 4.39%，P2G 2.89%，SPGP 投影 1.70%，自由面 0.41%。大规模下每步耗时近似线性随粒子数增长；32 线程 CPU 仍约比 GPU 慢 4 倍。

## 解释边界

- 部分验证依赖既有实验或数值结果，并非全部都有闭式解；
- 溃坝冲击时刻受墙面摩擦、闸门开启时间和形函数支撑宽度影响；
- 运行时间是特定 Taichi/GPU 实现结果，不应直接外推到其他硬件；
- 当前没有真实地质灾害全尺度验证。

## 关联页面

- [[papers/juel2026-stabilized-fractional-step-mpm-analysis]]
- [[papers/juel2026-stabilized-fractional-step-mpm-method]]
- [[papers/juel2026-stabilized-fractional-step-mpm-critical]]
- [[concepts/stabilized-pressure-gradient-projection]]
