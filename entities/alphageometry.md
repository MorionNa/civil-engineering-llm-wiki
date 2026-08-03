---
id: entity--alphageometry
title: AlphaGeometry
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/automated-reasoning
- domain/ai4s
- entity/system
keywords:
- geometry-theorem-prover
- neuro-symbolic
- synthetic-data
sources:
- sources/papers/trinh2024-alphageometry.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
---

# AlphaGeometry

## 定义

AlphaGeometry 是一个欧氏平面几何神经–符号定理证明系统：语言模型生成辅助构造，DD+AR 符号引擎完成并验证其余推导。^[sources/papers/trinh2024-alphageometry.md]

## 数据闭环

随机前提 → 符号闭包 → traceback → dependency difference → 合成证明训练 → 神经–符号交替搜索。

## 能力与边界

论文在 IMO-AG-30 上报告 25/30；但系统依赖专用几何语言、人工构建的规则与大规模计算，且证明可读性和跨域通用性有限。

## 项目角色

它是自动科研 Agent 中“生成候选 + 符号验证 + 合成监督”的代表实体，而不是通用物理推导器。

## 关联页面

- [[trinh2024-alphageometry-analysis]]
- [[concepts/dependency-difference-auxiliary-construction]]
- [[concepts/traceback-synthetic-theorem-generation]]
- [[concepts/alternating-neural-symbolic-proof-search]]
