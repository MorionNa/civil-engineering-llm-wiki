---
id: concept--local-smooth-contact-barrier
title: "局部光滑接触障碍势 — 有限支撑的非穿透能量"
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- barrier-energy
- unsigned-distance
- local-support
- contact-mechanics
sources:
- sources/papers/li2020-incremental-potential-contact.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
---

# 局部光滑接触障碍势

## 定义

对原语间无符号距离 $d$，构造在 $d\to0$ 时发散、在激活距离 $\hat d$ 外严格为零、并在截断点保持足够光滑的障碍能。它把非穿透约束转化为无约束最小化中的局部能量项。^[sources/papers/li2020-incremental-potential-contact.md]

## 关键性质

- **零距离发散：** 防止求解器到达穿透状态；
- **有限支撑：** $d\ge\hat d$ 时严格为零，可安全剔除远距离原语对；
- **光滑截断：** 支持 Newton 型方法的快速收敛；
- **精度可解释：** $\hat d$ 直接表示允许的接触间隙尺度；
- **局部组装：** 每个障碍只涉及一个点–三角形或边–边 stencil。

## 与惩罚法的区别

普通惩罚法允许穿透后再施加有限恢复力，刚度需要经验调节；障碍势在零距离处趋于无穷，并与可行线搜索配合，使迭代不进入穿透区域。

## 风险与边界

- 初始距离必须为正；
- $\hat d$ 太小会增强非线性与条件数问题；
- $\kappa$ 太大或太小都会降低求解效率；
- 近似平行边–边处还需额外 mollifier；
- 障碍势本身不能阻止一次过大的搜索步跨越零距离，必须结合 [[concepts/ccd-filtered-feasible-line-search]]。

## 迁移价值

该机制可迁移到 FEM、壳、杆、粒子表面或混合离散的接触层，只要能够定义可微距离和安全步长。对于结构倒塌，它提供比经验接触刚度更可控的几何精度接口。

## 关联页面

- [[entities/incremental-potential-contact]]
- [[li2020-incremental-potential-contact-method]]
- [[concepts/ccd-filtered-feasible-line-search]]
