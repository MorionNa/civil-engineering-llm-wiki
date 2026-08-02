---
id: paper--feng2026-mpm-lite-method
title: "Feng et al. (2026) — MPM Lite 方法机制"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- apic-transfer
- incremental-potential
- kirchhoff-stress
- linear-q1-kernel
- stretch-reconstruction
sources:
- sources/papers/feng2026-mpm-lite.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
evidence_scope: full-text
---

# 方法机制

## 总体数据流

```text
粒子状态 (x, v, F, G, 材料历史)
  → Unload：线性核 P2C，累积 m、mv、G、V、Vτ
  → C2G：固定权重 gather 到网格节点
  → Integrate：显式内力更新，或网格上的增量势隐式优化
  → G2C：节点速度与速度梯度采样到单元中心
  → Load：C2P 更新 v、G、x、F 与材料历史
```

该结构把粒子通信模块与 FEM 式积分模块分离。^[sources/papers/feng2026-mpm-lite.md]

## 运动学传递

粒子到单元中心采用多线性核。质量和动量与 APIC 一致，粒子携带速度梯度 $G_p$，中心速度包含仿射修正。中心速度梯度用质量加权平均，之后通过线性插值返回粒子。附录证明两跳 P2G 速度、G2P 速度和 G2P 梯度相对于二次 B-spline APIC 的差异均为 $O(\Delta x^2)$。

## 应力传递

方法不传递或平均 $F$。连续内力积分要求保持的是 Kirchhoff 应力的广延矩 $V\tau$：

$$
V_c=\sum_p w_{cp}V_p,\qquad
\tau_c=\frac{\sum_p w_{cp}V_p\tau_p}{V_c}.
$$

这样保持 $\sum_cV_c\tau_c=\sum_pV_p\tau_p$，避免不同旋转的变形梯度平均后污染应力和切线。

## 单元中心到节点与固定网格积分

单元中心视为体素六面体的单点积分位置。中心到相邻节点使用常数权重，可用无写冲突的 gather 实现；通过中心作为中介，写目标与访存局部性优于粒子直接散射到 27 个节点。网格节点完成内力、边界条件和时间积分，构成 [[concepts/particle-independent-grid-integration]]。

## 显式积分

显式模式直接在节点组装

$$
f_i^n=-\sum_cV_c^n\tau_c^n\nabla w_{ic},
$$

并更新节点速度。此时不同材料的 $V\tau$ 可直接相加，无需在同一中心复制材料积分点。

## 隐式增量势

应力率式 Jaumann 隐式更新会因旋转项产生非对称 Jacobian，不能由弹性势导出。MPM Lite 改用速度主变量的 backward Euler 增量势：

$$
\min_v\sum_i\frac12m_i\|v_i-v_i^n\|^2+
\sum_cV_c^n\psi\!\left((I+\Delta tG_c(v))F_c^{base}\right).
$$

这成为标准六面体有限元优化问题，可接入 PCG、multigrid 或 VBD。

## 旋转无关伸长参考态

[[concepts/rotation-free-stretch-reconstruction]] 从传递后的 $\tau_c$ 恢复 $S_c$，使 $P(S_c)S_c^\top=\tau_c$。对各向同性材料，旧旋转不影响单步能量和切线；附录给出相对于保留旋转的速度差 $O(\Delta t^2)$。论文分别推导 Hencky-StVK 的闭式反演和分裂 Neo-Hookean 的二维闭式/三维三次方程反演。

## 塑性、流体与材料混合

塑性采用 Newton 迭代内部更新的固定点全隐式策略，弹性仍由矩阵自由 CG 处理。不可压缩流体只跟踪体积比 $J_p$，由传递压力反演基准 $J_c^{base}$。多材料共享单值速度场，但分别保存 $(V_{c,k},\tau_{c,k})$ 并独立贡献能量。

## 输入、输出与求解边界

输入包括粒子位置、质量、静止体积、速度、变形梯度、速度梯度、材料类型、网格、边界条件和时间步；输出为更新后的粒子状态与材料历史。主要边界包括各向同性假设、体素网格、单点积分、单速度材料混合和对自由表面粒子采样质量的依赖。

## 关联页面

- [[papers/feng2026-mpm-lite-analysis]]
- [[papers/feng2026-mpm-lite-results]]
- [[papers/feng2026-mpm-lite-critical]]
- [[entities/mpm-lite]]
