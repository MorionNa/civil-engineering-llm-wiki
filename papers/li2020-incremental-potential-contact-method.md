---
id: paper--li2020-incremental-potential-contact-method
title: "Li et al. (2020) — IPC 方法机制"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- incremental-potential
- contact-barrier
- projected-newton
- continuous-collision-detection
- variational-friction
sources:
- sources/papers/li2020-incremental-potential-contact.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
---

# IPC 方法机制

以下方法机制均依据论文全文整理。^[sources/papers/li2020-incremental-potential-contact.md]

## 1. 增量势时间推进

对每个时间步，IPC 将隐式 Euler 或 Newmark 更新写成关于新节点位置 $x$ 的增量势最小化。动力学、外力和超弹性统一进入 $E(x)$，接触通过障碍势加入。

## 2. 无符号距离接触模型

接触约束由非相邻点–三角形和边–边原语对的无符号距离 $d_k(x)>0$ 表示。该表示兼容体、面、线和点型障碍，并避免局部法向或有向体积代理的方向失效。

## 3. 局部光滑障碍势

IPC 使用

$$b(d,\hat d)=\begin{cases}-(d-\hat d)^2\ln(d/\hat d),&0<d<\hat d,\\0,&d\ge\hat d.\end{cases}$$

它在零距离发散，在激活距离 $\hat d$ 外严格为零，并在截断点保持 $C^2$。因此只需计算接近接触的原语对，同时不改变远场解。

## 4. Barrier-aware Projected Newton

总势为

$$B_t(x)=E(x)+\kappa\sum_k b(d_k(x)).$$

每次迭代将弹性能、障碍能和摩擦能的局部 Hessian 投影到半正定锥，再与质量项组装为 SPD 系统。障碍刚度 $\kappa$ 自适应更新，以平衡接触力尺度与条件数。

## 5. 可行线搜索

Newton 方向不能直接采用普通回溯，因为能量下降点可能已穿过几何障碍。IPC 先用连续碰撞检测计算最大安全步长，再从该上界回溯。配合非反转弹性能的反转检测，所有迭代均保持无交叉、无反转。

## 6. 原语距离与退化处理

点–三角形和边–边距离根据最近点活跃集分解为点–点、点–边、点–三角形或边–边闭式公式。近似平行边–边处距离梯度不连续，论文使用局部多项式 mollifier 平滑相应障碍项。

## 7. 变分摩擦

Coulomb 摩擦先在小速度区间内平滑静摩擦转变，再把接触法向力和滑动基滞后到前一次非线性求解，从而得到可积的耗散势。通过交替更新滞后量提高摩擦方向与幅值的一致性。

## 8. 输入、输出与容差

- 输入：有限元网格、质量、材料能、边界与外力、摩擦系数、时间积分参数；
- 输出：下一时刻无交叉配置与速度；
- 用户容差：动力学精度 $\epsilon_d$、几何间隙精度 $\hat d$、静摩擦精度 $\epsilon_v$。

## 9. 假设与失败边界

- 初始几何必须严格无交叉并具有正间隙；
- 无反转依赖使用非反转材料能；
- 摩擦滞后迭代没有一般收敛保证；
- 极高接触密度与大网格使线性系统和内存成为主要瓶颈；
- 该方法不负责网格断裂和拓扑重构。

## 关联页面

- [[li2020-incremental-potential-contact-analysis]]
- [[li2020-incremental-potential-contact-results]]
- [[li2020-incremental-potential-contact-critical]]
- [[concepts/local-smooth-contact-barrier]]
- [[concepts/ccd-filtered-feasible-line-search]]
