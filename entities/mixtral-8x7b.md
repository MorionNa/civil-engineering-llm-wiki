---
id: entities--mixtral-8x7b
title: Mixtral 8x7B
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/llm
- entity/model
keywords:
- domain/llm
- entity/model
- large-language-model
- mixture-of-experts
sources:
- raw/papers/jiang2024_mixtral_of_experts.pdf
created: '2026-06-13'
updated: '2026-07-31'
confidence: medium
---

# Mixtral 8x7B

Mixtral 8x7B 是 Mistral AI 发布的稀疏 MoE 大语言模型，包含 8 个专家并使用 Top-2 路由，仅激活 13B 参数即可超越 Llama 2 70B 的性能，是首个开源实用级 MoE LLM。

## 关键信息
- **类型**: model
- **提出**: Albert Q. Jiang et al. (Mistral AI), 2024
- **发表**: 技术报告 (arXiv)
- **核心贡献**: 首个开源实用级稀疏 MoE LLM，Top-2 routing + 8 experts 设计，13B active params 性能超越密集 70B 模型

## 架构要点

- **Sparse Mixture-of-Experts**: 8 个前馈专家，每 token 经 Top-2 gating 选 2 个
- **Router**: 线性层 + softmax，选择概率最高的两个专家
- **Load Balancing**: 无额外负载均衡损失，依赖自然 token 分布
- **Context Length**: 32k token 上下文窗口
- **与 Mistral 7B 关系**: 每个专家结构与 Mistral 7B FFN 一致，权重初始化自 Mistral 7B

## 关键结果

- 多数基准测试超越 Llama 2 70B 和 GPT-3.5
- 推理速度相当于 12.9B 密集模型（因仅激活部分参数）
- 支持多语言（英/法/西/意/德）
- Apache 2.0 开源

## 关联页面
- [[jiang2024-mixtral-of-experts-analysis]] — 完整论文分析

## Evidence By Source

### `raw/papers/jiang2024_mixtral_of_experts.pdf`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/jiang2024_mixtral_of_experts.pdf]

## Related Indexes

- [[entities/index]]
