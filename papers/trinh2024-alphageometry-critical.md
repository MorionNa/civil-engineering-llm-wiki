---
id: paper--trinh2024-alphageometry-critical
title: "Trinh et al. (2024) — AlphaGeometry 批判性分析"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/llm
- domain/ai4s
- evidence/paper
keywords:
- representation-boundary
- compute-cost
- proof-readability
- domain-transfer
sources:
- sources/papers/trinh2024-alphageometry.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
---

# AlphaGeometry 批判性分析

## 核心贡献判断

最重要的贡献是以 traceback 和 dependency difference 自动生成“辅助构造监督”，并形成生成模型负责开放决策、符号引擎负责验证的分工，而不只是榜单上的 25/30。^[sources/papers/trinh2024-alphageometry.md]

## 优点

- 不依赖人工证明示例；
- 合成数据生成、训练和测试使用同一符号语义；
- 输出可被符号引擎验证并可转为人类可读证明；
- 消融清楚区分 AR、预训练、微调和搜索预算的作用；
- 代码与模型检查点公开。

## 局限

1. 专用语言只覆盖一部分欧氏平面几何；
2. 题目经过人工翻译，机器–人类比较只是近似；
3. 证明常比人类方案低层、冗长且缺少高层结构；
4. 符号规则缺失会同时限制合成数据覆盖和测试推理；
5. 完整数据生成与搜索的计算资源极大；
6. 迁移到新领域需要重新实现对象、采样器、符号引擎和 traceback，并非直接通用。

## 不应照搬

- 不能把 25/30 写成“已解决所有奥赛数学”；
- 不能把专用几何验证等同于 Lean 中的通用形式化证明；
- 不能把大规模合成数据自动视为无偏，规则库和构造语言决定了可见空间；
- 不能让语言模型绕过验证器直接输出工程结论。

## 对自动力学推导的迁移推论

可采用三层结构：生成模型提出变量替换、无量纲组、辅助场或分解；符号层检查代数、维度和边界条件；数值层用随机参数和极限案例寻找反例。该方案是迁移推论，论文没有验证连续介质或结构动力学。

## 研究机会

- 高层引理自动发现与压缩；
- 证明图到结构化解释；
- 计算预算自适应；
- 与 Lean/SMT/CAS/数值模拟联合；
- 面向物理方程的依赖差定义；
- 失败轨迹生成反例驱动训练。

## 关联页面

- [[trinh2024-alphageometry-analysis]]
- [[trinh2024-alphageometry-method]]
- [[trinh2024-alphageometry-results]]
- [[entities/alphageometry]]
- [[concepts/dependency-difference-auxiliary-construction]]
- [[concepts/alternating-neural-symbolic-proof-search]]
