---
id: paper--zhao2026-unified-sparse-mpm-method
title: "Zhao et al. (2026) — 大规模 MPM 统一稀疏框架方法机制"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
keywords:
- active-block
- apic-mpm
- compact-index-map
- hash-table
- prefix-scan
sources:
- sources/papers/zhao2026-unified-sparse-mpm.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
evidence_scope: full-text
---

# 方法机制

## 总体数据流

```text
粒子位置与形函数支撑 S(p)
  → 构造活跃块/活跃节点集合 A
  → 建立物理网格坐标 n 到紧凑存储索引 φ(n)
  → 仅为活跃块分配质量、动量、速度、力等数组
  → 按原 APIC-MPM 执行 P2G、网格更新、G2P
  → 下一时间步根据新粒子位置重建稀疏网格
```

稀疏层只改变网格数据的存储和访问，不改变控制方程、形函数、P2G/G2P 或本构更新。^[sources/papers/zhao2026-unified-sparse-mpm.md]

## 基础 MPM 与活跃节点定义

论文采用 updated-Lagrangian 显式 Euler APIC-MPM。粒子 $p$ 携带 $x_p,m_p,V_p,v_p,\sigma_p,F_p$，并通过紧支撑形函数与节点集合 $S(p)$ 交互。活跃节点集合定义为

$$
A=\bigcup_p S(p),\qquad |A|=n_{active}.
$$

紧凑索引映射为

$$
\phi:A\rightarrow\{0,1,\ldots,|A|-1\}.
$$

节点三元组 $(i,j,k)$ 表示物理位置，$\phi(n)$ 表示该节点在稀疏数组中的位置。这个解耦由 [[concepts/active-node-compact-indexing]] 统一描述。

## 块级稀疏表示

为降低逐节点掩码和索引开销，两种实现都以 $B\times B\times B$ 节点块为分配单位，论文取 $B=4$。只要块中至少有一个节点受粒子影响，该块即被标记为活跃；块内所有节点连续存储。节点索引由活跃块紧凑索引和块内局部索引组合得到。

收益是更小的元数据、较好的空间局部性和规则数组访问；代价是活跃块内部可能包含部分实际非活跃节点。

## CPU 扫描式实现

1. 从粒子支撑包围盒确定候选块域；
2. 并行遍历粒子及其支撑节点，标记块级二值活动掩码；
3. 将掩码展平，由各线程执行局部 exclusive scan；
4. 对线程局部总和再做 prefix sum，得到线程偏移；
5. 把偏移加回局部结果，生成连续活跃块编号；
6. 构造紧凑块映射并分配连续节点数组。

该实现依赖规则数组、连续内存和较少随机访问，符合 CPU 缓存层次特性。

## GPU 哈希式实现

GPU 不建立整个候选域的全局掩码，而让线程从粒子局部支撑直接插入活跃块：

1. 块坐标加偏置后打包为 64 位唯一 key；论文每轴使用 21 bit，支持正负大范围索引；
2. 通过 64 位 mixing 函数打散相邻坐标的结构化位模式；
3. 用位掩码映射到容量为 2 的幂的哈希槽；
4. 使用 open addressing 与线性探测处理冲突；
5. 用 atomic compare-and-swap 抢占空槽，用 atomic add 分配紧凑块编号；
6. 若探测或容量溢出，则扩大容量并重建哈希表。

这避免了全网格同步扫描，但引入哈希碰撞、原子竞争和容量管理。详见 [[comparisons/scan-vs-hash-sparse-mpm]]。

## 物理更新

构造索引后，P2G 的 APIC 质量、动量与内力公式保持原样；每次访问节点 $n\in S(p)$ 时先查询 $\phi(n)$。节点显式动量更新后，G2P 同样通过紧凑索引读取节点速度，并更新粒子速度、位置、APIC 仿射矩阵和变形梯度。本构可替换，论文分别使用弹性和 Drucker–Prager 弹塑性模型。

## 输入、输出与复杂度边界

输入包括粒子状态、形函数支撑、网格间距、块大小、候选域或哈希容量、线程/硬件配置。输出是活跃块列表、紧凑索引映射及活跃网格数组。

框架收益取决于 $n_{dense}/n_{active}$。它减少网格分配、清零和节点遍历，但仍需遍历所有粒子及其支撑，且每步重建活跃集合。低稀疏度、哈希高负载、过大块尺寸或高度碎片化的活跃区域都可能降低收益。

## 关联页面

- [[zhao2026-unified-sparse-mpm-analysis]]
- [[zhao2026-unified-sparse-mpm-results]]
- [[zhao2026-unified-sparse-mpm-critical]]
- [[entities/unified-sparse-mpm]]
- [[concepts/active-node-compact-indexing]]
- [[comparisons/scan-vs-hash-sparse-mpm]]
