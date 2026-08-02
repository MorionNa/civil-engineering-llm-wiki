---
id: paper--zhao2026-unified-sparse-mpm-results
title: "Zhao et al. (2026) — 大规模 MPM 统一稀疏框架结果证据"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
keywords:
- blatten-landslide
- memory-reduction
- scalability
- sparsity-ratio
- speedup
sources:
- sources/papers/zhao2026-unified-sparse-mpm.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
evidence_scope: full-text
---

# 结果与证据

## 对比条件

CPU 扫描式实现基于 Matter，GPU 哈希式实现基于 GeoWarp/sparse_MPM。测试工作站采用 Intel Core Ultra 9 285K CPU、NVIDIA RTX 5070 Ti 17 GB；CPU 使用 8 线程。速度提升定义为稠密运行时间除以稀疏运行时间，内存缩减定义为稠密内存除以稀疏内存。^[sources/papers/zhao2026-unified-sparse-mpm.md]

## 稀疏度指标

论文用整个模拟期间的最小活跃节点占比定义稀疏比：

$$
r_{active}=\min_t\frac{n_{dense}}{n_{active}(t)}.
$$

滑块、颗粒柱坍塌和 Blatten 滑坡的稀疏比分别约为 2.9、5.5 和 373；正文也将 Blatten 概括为接近 400 的强稀疏问题。

## 滑块：低稀疏度

四个坡角 $14^\circ,20^\circ,25^\circ,30^\circ$ 的位移曲线与 Coulomb 摩擦解析解一致，稀疏与稠密 MPM 结果重合。由于粒子占据域比例较高，活跃网格构建开销抵消了多数收益，速度和内存比接近 1。

## 颗粒柱坍塌：中等稀疏度

在内摩擦角 $20^\circ,30^\circ,40^\circ$ 下，稀疏与稠密 MPM 给出相同沉积轮廓。随着稀疏比增至 5.5，稀疏框架开始表现出可测的运行时间与内存优势，说明收益随活跃区域相对缩小而增长。

## Blatten 滑坡：强稀疏度

算例模拟 2025 年瑞士 Blatten 岩冰崩滑：估算体积约 $9.3\times10^6\,\mathrm{m^3}$，高差约 1000 m，最终沉积约 2 km 长、50–200 m 宽，早期模拟速度约达 100 m/s。大范围潜在运动域中，活跃区域始终局部化。

## 运行时间与内存

- CPU：强稀疏 Blatten 算例的总运行时间相对稠密版本降低约两个数量级；
- GPU：总运行时间降低约一个数量级；
- 内存：强稀疏场景降低一至两个数量级；
- 随分辨率提高，稀疏版本的时间与内存总体近似随粒子数增长，而稠密版本受完整包围域控制；
- GPU 稠密版本很快触及 17 GB 内存上限，$h=2\,\mathrm{m}$、约 1070.8 万粒子的最细算例仅稀疏版本可在单 GPU 上完成；
- 在相同设置下，作者报告 GPU 稀疏实现比 Houdini MPM 求解器快 1.5 倍以上。

## CPU 与 GPU 实现选择

在 Blatten 算例的跨实现测试中，CPU 上扫描式约比哈希式减少 10% 运行时间；GPU 上哈希式约比扫描式减少 35%。这支持“统一框架、架构专用实现”的设计，而不支持把某一数据结构视为跨硬件最优方案。

## 数值一致性

滑块与颗粒坍塌显示稀疏和稠密方案产生相同结果，符合框架仅改变节点存储与访问、不改变 APIC-MPM 公式的预期。论文没有给出逐浮点位完全一致的误差表，也没有把 Blatten 模拟结果与实测时程或沉积统计进行系统校准。

## 解释边界

- 速度提升取决于稠密基线实现、潜在域定义、硬件和稀疏度，不能视为固定常数；
- Houdini 比较只覆盖文中同一设置，不是全面软件基准；
- Blatten 案例主要证明计算可扩展性，而非灾害预报精度；
- 多 GPU、分布式内存、隐式时间积分和多相问题未包含在结果中。

## 关联页面

- [[zhao2026-unified-sparse-mpm-analysis]]
- [[zhao2026-unified-sparse-mpm-method]]
- [[zhao2026-unified-sparse-mpm-critical]]
- [[entities/unified-sparse-mpm]]
- [[comparisons/scan-vs-hash-sparse-mpm]]
