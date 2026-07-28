---
title: "玻尔兹曼方程 (Boltzmann Equation)"
created: 2026-07-28
updated: 2026-07-28
type: entity
tags: [statistical-mechanics, kinetic-theory, entropy, irreversibility, boltzmann-equation, hard-sphere-dynamics, boltzmann-grad-limit]
sources:
  - raw/transcripts/bv1ph3c6teqt/transcript.md
confidence: medium
---

# 玻尔兹曼方程

玻尔兹曼方程描述稀薄气体单粒子分布函数 \(f(t,x,v)\) 的演化：

\[
\partial_t f+v\cdot\nabla_x f=Q(f,f).
\]

左侧描述自由输运，右侧碰撞算子描述二体碰撞导致的速度分布流入与流出。对速度积分可得到密度、平均速度、能量和压强，因此它连接微观粒子动力学与宏观连续介质模型。

## 关键统计结构

经典碰撞闭合依赖碰撞前二粒子近似独立，即分子混沌。重碰撞和精细制备的速度反演态会产生相关性；严格推导必须证明在相应极限下这些相关贡献足够小。

## H 定理

\[
H[f]=\int f\log f\,dx\,dv
\]

在玻尔兹曼演化及适用假设下不增加，相应熵 \(-H\) 不减少。H 定理给出宏观不可逆性的动理学描述，但不意味着每个可逆微观初态都必须沿两个时间方向熵增。

## 严格推导与边界

- Lanford（1975）证明了 Boltzmann–Grad 极限下的短时间硬球—玻尔兹曼推导。
- Deng、Hani、Ma（2024）把推导延伸到玻尔兹曼正则解存在区间内的任意有限时间。
- 适用条件包括稀薄气体、特定尺度极限和正则性；真实分子的内部自由度、稠密效应、长程势及量子效应需要更一般模型。

## 关联页面

- [[hilbert-sixth-problem]] — 玻尔兹曼方程在物理公理化和流体方程推导中的位置
- [[notes/videos/boltzmann-entropy-hilbert-sixth-problem]] — 视频中的直观推导、反演悖论与长时间证明
- [[pinn]] — 以 PDE 约束机器学习的计算范式
