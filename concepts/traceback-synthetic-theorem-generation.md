---
id: concept--traceback-synthetic-theorem-generation
title: 回溯式合成定理–证明生成
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/automated-reasoning
keywords:
- forward-deduction
- traceback
- minimal-proof
- synthetic-data
sources:
- sources/papers/trinh2024-alphageometry.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
---

# 回溯式合成定理–证明生成

从随机一致前提出发执行前向符号推理，得到可达结论图；随后从任一结论回溯最小依赖子图，形成新的“前提–结论–证明”训练样本。^[sources/papers/trinh2024-alphageometry.md]

该方法不需要先给定人工猜想，但生成空间仍由构造语言和规则库决定。

## 关联页面

- [[trinh2024-alphageometry-method]]
- [[concepts/dependency-difference-auxiliary-construction]]
- [[entities/alphageometry]]
