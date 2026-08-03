---
id: concept--alternating-neural-symbolic-proof-search
title: 神经–符号交替证明搜索
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/automated-reasoning
- domain/ai4s
keywords:
- language-model-guidance
- symbolic-verification
- beam-search
sources:
- sources/papers/trinh2024-alphageometry.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
---

# 神经–符号交替证明搜索

生成模型每轮提出一个开放式辅助构造，符号引擎随后计算确定性闭包并验证目标；若失败，再以扩展后的状态继续生成。^[sources/papers/trinh2024-alphageometry.md]

这种分工让模型处理无限分支，让符号系统承担可靠性，但效果受规则覆盖、搜索预算和接口语法限制。

## 关联页面

- [[trinh2024-alphageometry-method]]
- [[concepts/dependency-difference-auxiliary-construction]]
- [[entities/alphageometry]]
