---
id: sources--papers--zhao2026-unified-sparse-mpm
title: "Zhao et al. (2026) — 大规模 MPM 统一稀疏框架"
type: source
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
keywords:
- active-node-indexing
- block-sparse-grid
- hash-based-mpm
- scan-based-mpm
- sparse-mpm
sources:
- raw/papers/zhao2026-unified-sparse-mpm-source.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
evidence_scope: full-text
code_url:
- https://github.com/larsblatny/matter/
- https://github.com/Yidong-ZHAO/sparse_MPM
dataset_url: []
---

# 来源记录：大规模 MPM 统一稀疏框架

## 文献信息

- **英文题名：** Unified sparse framework for large-scale simulations using the material point method
- **作者：** Yidong Zhao、Lars Blatny、Xiang Feng、Mikkel M. Juel、Chenfanfu Jiang、Johan Gaume
- **版本：** arXiv:2605.28525v3 [cs.CE]，2026-07-28
- **证据范围：** 用户提供的 27 页完整预印本。
- **同行评审边界：** 所给版本是 arXiv 预印本，正文未声明期刊录用。

## 证据地图

- 第 1–3 页：背景、稀疏背景网格问题、统一活跃节点索引抽象和主要贡献。
- 第 4–6 页：活跃节点集、紧凑索引映射、CPU 扫描式与 GPU 哈希式实现总览。
- 第 7–12 页：滑块、颗粒柱坍塌和 Blatten 滑坡结果、速度与内存缩减、分辨率扩展。
- 第 13–20 页：标准显式 APIC-MPM、紧凑索引映射、块级 prefix scan、64 位 key、哈希碰撞和原子插入。
- 第 20–23 页：两种实现跨硬件比较、结论、扩展方向与开源代码。

## 证据边界

论文证明的是：保持原 MPM 控制方程、粒子网格传递和本构不变，仅改变活跃网格节点的存储与访问，可在空间强稀疏问题中显著降低计算和内存成本。它没有验证多 GPU、集群、隐式积分、多相耦合、结构倒塌或实际灾害预测精度。

## 生成页面

- [[papers/zhao2026-unified-sparse-mpm-analysis]]
- [[papers/zhao2026-unified-sparse-mpm-method]]
- [[papers/zhao2026-unified-sparse-mpm-results]]
- [[papers/zhao2026-unified-sparse-mpm-critical]]
- [[entities/unified-sparse-mpm]]
- [[concepts/active-node-compact-indexing]]
- [[comparisons/scan-vs-hash-sparse-mpm]]
