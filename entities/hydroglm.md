---
title: "HydroGLM"
created: 2026-06-13
updated: 2026-06-13
type: entity
tags: [large-language-model, domain-specific-llm, hydrology, glm, fine-tuning, mixture-of-experts]
sources: [notes/briefings/glm-hydropower-2026.md]
confidence: high
---

# HydroGLM

基于 GLM-5.0 微调的水利水电行业大模型（L1），由智谱AI、清华大学、国能大数据与大渡河公司四方联合研发，2026 年推出。在 9 大水利水电子领域评测中全面超越 DeepSeek-V3 和 DeepSeek-R1。

## 关键信息

- **类型**: model
- **基座模型**: GLM-5.0（智谱AI）
- **研发团队**: 60 人（四方联合）
- **版本**: Flash / Plus（轻量化设计，便于业务落地）
- **核心贡献/角色**: 水利水电垂直领域大模型，总体评测得分 88.6，远超通用模型

## 评测成绩（总分 100）

| 模型 | 总体 | 大气科学 | 水利工程建设 | 工程管理 | 水文水资源 | 水电运维 | 电气工程 |
|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| DeepSeek-V3 | 74.9 | 75.0 | 79.1 | 82.0 | 78.2 | 68.1 | 80.8 |
| DeepSeek-R1 | 78.5 | 69.6 | 85.0 | 84.1 | 87.6 | 75.4 | 77.2 |
| **HydroGLM** | **88.6** | **88.3** | **92.5** | **90.6** | **86.0** | **92.0** | **86.5** |

> HydroGLM 在全部 9 个领域全面碾压 DeepSeek 系列，总体领先 10–14 分。

## 训练数据与策略

- **预训练语料**: 231 GB（教材 1023 本 + 期刊 4.5 万篇 + 行业规范 606 个 + 政府文件等）
- **SFT 数据**: 577 万条（领域 60.5 万 + 通用 516.4 万）
- **训练流程**: 两轮增量预训练 → 多轮多策略 SFT
- **构建范式**: 以微调（③）为核心，辅以 RAG（②）和提示工程（①）

## 关联页面

- [[notes/briefings/glm-hydropower-2026]] — 项目完整汇报笔记
- [[glm-5]] — GLM-5.0 基座模型
- [[zhipu-ai]] — 智谱AI
- [[tsinghua-dhe]] — 清华大学水利系
- [[guoneng-bigdata]] — 国能大数据
- [[daduhe-company]] — 大渡河公司
