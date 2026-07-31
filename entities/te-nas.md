---
id: entities--te-nas
title: TE-NAS
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- entity/model
- method/neural-architecture-search
keywords:
- entity/model
- method/neural-architecture-search
- nas-bench-201
- neural-tangent-kernel
- training-free-nas
sources:
- raw/papers/TE-NAS_chen2021_ICLR.pdf
created: '2026-06-13'
updated: '2026-07-31'
confidence: medium
---

# TE-NAS

TE-NAS 是一种免训练的神经架构搜索方法，通过 NTK 条件数（Trainability）和线性区域数（Expressivity）两个零成本指标，仅需 4 GPU 小时即可在 NAS-Bench-201 和 ImageNet 上完成搜索。

## 关键信息
- **类型**: model
- **提出**: Wuyang Chen et al. (UT Austin), 2021
- **发表**: ICLR 2021
- **核心贡献**: 提出两个理论驱动的训练无关指标（NTK condition number + linear regions number）替代传统训练评估，NAS 搜索成本降至零

## 架构要点

- **Trainability 指标（NTK Cond）**: 架构的 NTK 条件数越小，梯度下降越易收敛，预测架构最终精度
- **Expressivity 指标（#Linear Regions）**: 架构划分输入空间的线性区域数越多，表达能力越强
- **双重排序**: 两个指标分别排名后取交集，筛选出既易训练又强表达能力的架构
- **搜索空间**: NAS-Bench-201（cell-based 搜索）及 DARTS 空间，支持 ImageNet

## 关键结果

- NAS-Bench-201 上 Kendall-τ 0.7+ 与真实精度排名相关
- ImageNet 上仅用 4 GPU 小时完成搜索（传统 NAS 需数千 GPU 小时）
- 搜索架构 ImageNet Top-1 达 76.8%（mobile setting），与训练式 NAS 相当
- 免训练特性使其被纳入 NAS-Bench-301 / 201 标准评估指标

## 关联页面
- [[chen2021-tenas-analysis]] — 完整论文分析

## Evidence By Source

### `raw/papers/TE-NAS_chen2021_ICLR.pdf`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/TE-NAS_chen2021_ICLR.pdf]

## Related Indexes

- [[entities/index]]
