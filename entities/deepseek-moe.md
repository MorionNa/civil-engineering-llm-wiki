---
title: "DeepSeekMoE"
created: 2026-06-13
updated: 2026-06-13
type: entity
tags: [mixture-of-experts, large-language-model, conditional-computation]
sources: [raw/papers/dai2024_deepseek_moe.pdf]
---

# DeepSeekMoE

DeepSeekMoE 是 DeepSeek 提出的细粒度 MoE 架构，通过专家分割（Expert Segmentation）和共享专家隔离（Shared Expert Isolation），仅用 40% 计算量达到 7B 密集模型水平。

## 关键信息
- **类型**: model
- **提出**: Damai Dai et al. (DeepSeek), 2024
- **发表**: arXiv 2024
- **核心贡献**: 细粒度专家分割 + 共享专家隔离双策略，MoE 计算效率显著超越同等规模密集模型

## 架构要点

- **细粒度专家分割（Fine-Grained Expert Segmentation）**: 将一个标准 FFN 专家切分为多个更小的专家（如将 1 个切为 m 个），增大路由灵活性
- **共享专家隔离（Shared Expert Isolation）**: 设定若干专家为共享专家（所有 token 均激活），其余为路由专家（Top-K 选择），减少路由负担
- **负载均衡**: 辅助损失约束 expert-level 和 device-level 负载均衡
- **Device-Level 均衡**: 确保不同设备上的专家利用率相近，减少流水线气泡

## 关键结果

- 2B 参数 DeepSeekMoE 以 40% 计算量达 7B 密集模型性能
- 16B 参数版本在多个基准上与 LLaMA 2 7B 竞争
- 专家分割策略通用，适用于各种 MoE 架构

## 关联页面
- [[dai2024-deepseek-moe-analysis]] — 完整论文分析
