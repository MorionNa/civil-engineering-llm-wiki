---
id: entities--glm-5
title: GLM-5.0
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/llm
- entity/model
- method/transformer
keywords:
- agent
- coding
- domain/llm
- entity/model
- glm
- large-language-model
- method/transformer
- open-source
- reasoning
sources:
- notes/briefings/glm-hydropower-2026.md
created: '2026-06-13'
updated: '2026-07-31'
confidence: high
---

# GLM-5.0

智谱AI 于 2026 年发布的通用大语言模型。在 Artificial Analysis Intelligence Index v4.0 中排名**全球第四、开源第一**，是当时开源阵营中最强的模型，核心能力覆盖推理、编程与 Agent 任务。

## 关键信息

- **类型**: model
- **开发者**: 智谱AI (Zhipu AI)
- **发布时间**: 2026 年（规划于 2026 年 2 月）
- **AI Index 得分**: 50（逼近 Claude Opus 4.5 的 60 分）
- **开源排名**: 开源模型中领先 DeepSeek V3.2、Kimi K2.5、Grok 4 等
- **核心贡献/角色**: 通用基础大模型 (L0)，为 HydroGLM 等行业大模型提供底座能力

## 架构特点

- 基于 Transformer / MoE（混合专家）架构
- 支持语言、多模态、时序多能力融合
- 国产自主可控，在 GLM 系列中继承 ChatGLM 路线

## 在 HydroGLM 项目中的角色

GLM-5.0 作为 L0 基础大模型，经领域预训练 + SFT 微调后派生出 L1 行业大模型 HydroGLM（Flash/Plus 版本）。智谱AI 刘丁枭带队（10 人）负责底座模型供应与训练优化。

## 关联页面

- [[notes/briefings/glm-hydropower-2026]] — GLM 水利水电行业大模型汇报笔记（完整项目背景）
- [[hydroglm]] — HydroGLM 行业大模型
- [[zhipu-ai]] — 智谱AI 公司
- [[fedus2021-switch-transformer-analysis]] — MoE 架构参考

## Evidence By Source

### `notes/briefings/glm-hydropower-2026.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[notes/briefings/glm-hydropower-2026.md]
