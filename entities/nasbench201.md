---
title: "NAS-Bench-201"
created: 2026-06-13
updated: 2026-06-13
type: entity
tags: [dataset, benchmark, neural-architecture-search, nas-bench-201]
sources: [raw/papers/TE-NAS_chen2021_ICLR.pdf]
confidence: high
---

# NAS-Bench-201

Dong & Yang 在 ICLR 2020 提出的神经架构搜索（NAS）基准数据集。包含 15,625 个架构在 CIFAR-10、CIFAR-100 和 ImageNet-16-120 上的完整训练与评估结果，广泛用于 NAS 方法评测。

## 关键信息

- **类型**: dataset / benchmark
- **作者**: Xuanyi Dong, Yi Yang (UTS)
- **发表**: ICLR 2020
- **规模**: 15,625 个架构 × 3 个数据集（CIFAR-10, CIFAR-100, ImageNet-16-120）
- **核心贡献/角色**: 首个提供完整架构-性能映射表的 NAS benchmark，使 NAS 方法可在秒级完成评测

## 搜索空间

每个 cell 由 4 个节点和 6 条边组成的有向无环图（DAG），每条边从 5 种操作中选择：
- none（skip）
- skip_connect
- conv_1x1
- conv_3x3
- avg_pool_3x3

总计 $5^6 = 15,625$ 个可能架构。

## 在 TE-NAS 中的使用

TE-NAS (Chen et al., ICLR 2021) 使用 NAS-Bench-201 作为主要 benchmark 来验证基于训练无关指标（NTK 条件数 + 线性区域数）的架构排序方法，证明无需训练即可有效 rank 架构。

## 关联页面

- [[chen2021-tenas-analysis]] — TE-NAS 论文分析
- [[chen2021-tenas-results]] — TE-NAS 实验结果
- [[chen2021-tenas-method]] — TE-NAS 方法细节
