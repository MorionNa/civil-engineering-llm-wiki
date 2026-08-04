---
id: concept--dependency-difference-auxiliary-construction
title: 依赖差驱动的辅助构造学习
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/llm
- domain/ai4s
keywords:
- dependency-difference
- auxiliary-construction
- exogenous-term-generation
sources:
- sources/papers/trinh2024-alphageometry.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
---

# 依赖差驱动的辅助构造学习

## 定义

在最小证明图中，参与证明但不属于结论对象构造依赖的对象，被识别为 dependency difference，并从前提侧移动到证明动作侧，形成辅助构造训练监督。^[sources/papers/trinh2024-alphageometry.md]

## 意义

它把原本需要人工标注的“何时引入什么新对象”转化为可由符号回溯自动产生的序列学习目标。

## 边界

结果依赖符号引擎和最小证明质量；规则库缺失、近似 traceback 或冗余证明都会影响构造监督。

## 关联页面

- [[trinh2024-alphageometry-method]]
- [[concepts/traceback-synthetic-theorem-generation]]
- [[entities/alphageometry]]
