---
id: comparison--scan-vs-hash-sparse-mpm
title: 扫描式与哈希式稀疏 MPM 实现比较
type: comparison
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- method/evaluation
- evidence/paper
keywords:
- architecture-specific
- cpu-prefix-scan
- gpu-hash-table
- sparse-grid-construction
sources:
- sources/papers/zhao2026-unified-sparse-mpm.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
---

# 扫描式与哈希式稀疏 MPM 实现比较

## 共同目标

两种实现都构造 [[concepts/active-node-compact-indexing]]，并使用相同的块级稀疏存储和原 MPM 更新公式。差异只在于如何发现活跃块并分配连续编号。^[sources/papers/zhao2026-unified-sparse-mpm.md]

## 结构化比较

| 维度 | CPU 扫描式 | GPU 哈希式 |
|---|---|---|
| 活跃集合视角 | 候选块域的全局二值掩码 | 从粒子支撑局部并行插入 |
| 索引生成 | 并行 exclusive prefix scan | 原子计数器在线分配 |
| 数据访问 | 规则、连续、缓存友好 | 随机哈希访问、大量并发 |
| 同步成本 | 全局扫描及线程偏移汇总 | atomic CAS/add 与冲突探测 |
| 元数据风险 | 候选域很大时掩码成本上升 | 高负载、碰撞和溢出重建 |
| 适配硬件 | CPU | GPU |
| Blatten 证据 | 约比哈希式快 10% | 约比扫描式快 35% |

## 为什么结果相反

CPU 强依赖缓存和连续内存，规则掩码与扫描通常优于随机哈希。GPU 擅长大量轻量线程，却不适合对大候选域执行全局扫描；从粒子支撑局部插入可以避免遍历空域，原子操作成本则由并行度摊薄。

## 选择建议

- CPU 单机：优先块级扫描，尤其当候选块域仍可容纳且需要稳定连续布局时；
- GPU 单机：优先块级哈希，尤其在潜在域巨大而活跃区域局部时；
- 低稀疏度：应评估继续使用稠密数组，因为两种稀疏构造都可能没有净收益；
- 跨平台框架：共享活跃集合和索引接口，而不是强制共享底层构造算法。

## 比较边界

10% 与 35% 来自 Blatten 算例和特定 Matter/GeoWarp 实现，不是所有 CPU/GPU 的普适比值。块大小、哈希负载率、候选域尺寸、线程数和内存分配器均会改变结论。

## 关联页面

- [[entities/unified-sparse-mpm]]
- [[zhao2026-unified-sparse-mpm-method]]
- [[zhao2026-unified-sparse-mpm-results]]
- [[zhao2026-unified-sparse-mpm-critical]]
