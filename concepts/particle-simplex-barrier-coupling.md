---
id: concept--particle-simplex-barrier-coupling
title: "粒子–单纯形障碍耦合"
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
keywords:
- particle-simplex-contact
- barrier-energy
- heterogeneous-discretization
sources:
- sources/papers/li2022-bfemp.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
---

# 粒子–单纯形障碍耦合

## Definition

粒子–单纯形障碍耦合是在异构离散之间，以粒子位置和网格边界单纯形之间的无符号距离构造局部障碍势，并通过链式法则把接触力传递至实际求解自由度的耦合机制。^[sources/papers/li2022-bfemp.md]

## Mechanism

- 二维采用粒子–边距离，三维采用粒子–三角形距离；
- 距离低于激活阈值时障碍能增长，趋近零距离时发散；
- 粒子若由网格插值得到，其接触梯度继续传至网格节点；
- CCD 过滤线搜索防止迭代越过障碍到另一侧。

## Why It Matters

该机制允许不同域保持各自离散和状态变量，无需匹配界面网格或把一种离散嵌入另一种离散的自由度系统。

## Assumptions and Risks

- 初始状态必须严格可行；
- 粒子中心距离不能完整描述有限粒子域几何；
- 表面粒子权重和边界识别会影响接触压力；
- 密集接触会显著增加 Hessian 和线性求解成本。

## Relations

- implemented by [[entities/bfemp]];
- based on [[concepts/local-smooth-contact-barrier]];
- feasibility is maintained by [[concepts/ccd-filtered-feasible-line-search]].
