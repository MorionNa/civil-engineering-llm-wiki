---
id: entities--peer-strong-motion-database
title: PEER Strong Motion Database
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- entity/dataset
keywords:
- benchmark
- dataset
- domain/civil-engineering
- entity/dataset
- ground-motion
- peer-database
- seismic-response
sources:
- raw/papers/zhang2020-phylstm.md
created: '2026-06-10'
updated: '2026-07-31'
confidence: high
---

# PEER Strong Motion Database

## 概述

PEER (Pacific Earthquake Engineering Research Center) 强震数据库是地震工程领域最广泛使用的地震动记录数据库之一。在 PhyLSTM 论文中，该数据库被用作结构地震响应仿真的输入数据源。

## 在 PhyLSTM 论文中的使用

- **目标区域：** Pomona, California（经纬度 34.0608°N, 117.7558°W）
- **危险性水平：** 50 年 10% 超越概率
- **选波工具：** Baker & Lee (2018) 条件谱选波算法
- **选择数量：** 97 条地震动记录
- **缩放：** 匹配原型建筑的设计谱

### 数据处理流程

1. **IDA（增量动力分析）：** 每条地震动按不同强度（幅值）缩放
2. **生成：** 97 × 多级缩放 = 806 个输入-输出对
3. **聚类选训练集：** 对条件谱加速度 Sa 做无监督聚类（7 个簇）
4. **训练/验证：** 7 个簇中心最近的地震 × IDA = 46 个样本
5. **测试：** 其余 90 条地震 × IDA = 760 个样本

### 关键设计考量

- 聚类选择确保训练数据**多样性最大化**
- 训练集仅占总数据的 ~5.7%（46/806）——测试"少数据"场景
- 输出变量：位移 u, 速度 ẇ, 质量归一化恢复力 g（后者仅用于测试评估）

## 关联

- [[zhang2020-phylstm-analysis]] — 论文完整分析
- [[phylstm2]] — PhyLSTM2 架构
- [[phylstm3]] — PhyLSTM3 架构

## Evidence By Source

### `raw/papers/zhang2020-phylstm.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/zhang2020-phylstm.md]
