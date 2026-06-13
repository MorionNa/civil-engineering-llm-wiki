---
title: "Switch Transformer"
created: 2026-06-13
updated: 2026-06-13
type: entity
tags: [mixture-of-experts, model-parallelism, distributed-training]
sources: [raw/papers/fedus2021_switch_transformer.md]
---

# Switch Transformer

Switch Transformer 是 Google 提出的稀疏 MoE 架构，采用 k=1 简化路由策略（每个 token 只发往一个专家），将模型参数规模推至万亿级别，训练速度相比 T5-XXL 提升 4 倍。

## 关键信息
- **类型**: model
- **提出**: William Fedus, Barret Zoph, Noam Shazeer (Google), 2021
- **发表**: JMLR 2022
- **核心贡献**: 简化 MoE 路由至 k=1 + 负载均衡损失，首次将稀疏 Transformer 推至 1.6T 参数，训练效率 4× 超越等量密集模型

## 架构要点

- **Switch Routing**: 每个 token 仅路由到 Top-1 专家（而非 Top-2），路由计算减半
- **Load Balancing Loss**: 辅助损失鼓励均匀路由，防止专家坍塌
- **Capacity Factor**: 限制每个专家处理的 token 上限，超出则丢弃，保证硬件效率
- **Selective Precision**: 路由部分 bfloat16，其余 float32，降低通信开销

## 关键结果

- C4 数据集上 1.6T Switch-C（2048 专家）在 101 种语言上超越 T5-XXL
- 相同计算量下精度持续优于密集模型
- 分布式训练中通信开销由 expert parallelism 策略缓解

## 关联页面
- [[fedus2021-switch-transformer-analysis]] — 完整论文分析
- [[fedus2021-switch-transformer-method]] — 方法机制
