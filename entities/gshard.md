---
title: "GShard"
created: 2026-06-13
updated: 2026-06-13
type: entity
tags: [mixture-of-experts, automatic-sharding, spmd]
sources: [raw/papers/lepikhin2021_gshard.md]
---

# GShard

GShard 是 Google 提出的自动分片 + 条件计算框架，将 MoE Transformer 扩展至 600B 参数，仅用 4 天训练完成，开创了大规模稀疏模型的高效训练范式。

## 关键信息
- **类型**: model
- **提出**: Dmitry Lepikhin et al. (Google), 2021
- **发表**: ICLR 2021
- **核心贡献**: 将 MoE 层与自动分片编译器结合，实现 SPMD 编程模型下的 600B 参数稀疏 Transformer 高效训练

## 架构要点

- **GShard 编译器**: 自动将计算图分片到多设备，无需手动管理 device placement
- **MoE 层设计**: 每隔一个 FFN 层替换为 MoE 层，Top-2 gating，支持条件计算
- **SPMD 编程**: 单一程序多数据——开发者写单设备代码，编译器负责分布式
- **Expert Capacity**: 动态限制每个专家的 token 容量，配合辅助损失实现负载均衡
- **并行策略混合**: 数据并行 + 模型并行 + expert parallelism 三者自动组合

## 关键结果

- 600B 参数多语言翻译模型，4 天 2048 TPU v3 训练
- 100+ 语言翻译质量超越密集基线
- 自动分片策略在多种任务中通用有效

## 关联页面
- [[lepikhin2021-gshard-analysis]] — 完整论文分析
- [[lepikhin2021-gshard-method]] — 方法机制
