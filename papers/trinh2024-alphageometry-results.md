---
id: paper--trinh2024-alphageometry-results
title: "Trinh et al. (2024) — AlphaGeometry 结果"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/automated-reasoning
- evidence/paper
keywords:
- imo-ag-30
- ablation
- expert-evaluation
- larger-test-set
sources:
- sources/papers/trinh2024-alphageometry.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
---

# AlphaGeometry 结果与证据

## IMO-AG-30

|方法|解决题数 / 30|
|---|---:|
|Wu 方法|10|
|Gröbner basis|4|
|GPT-4 完整自然语言证明|0|
|DD|7|
|DD + AR|14|
|DD + AR + GPT-4 辅助构造|15|
|DD + AR + 人工启发式|18|
|AlphaGeometry|25|

^[sources/papers/trinh2024-alphageometry.md]

## 模块增益

相对 DD 的 7 题，AR 增加 7 题达到 14；语言模型辅助构造再增加 11 题达到 25。去掉预训练为 21，去掉微调为 23，说明纯推导预训练与构造聚焦微调均有贡献。

## 数据与搜索缩减

仅使用 20% 训练数据仍解出 21 题；beam size 从 512 降到 8，或搜索深度从 16 降到 2，也仍解出 21 题。

## 更大测试集

在 231 道教材、地区奥赛和著名定理组成的集合上，AlphaGeometry 报告 98.7%，人工启发式基线为 92.2%，Wu 方法为 75%。

## 人工专家评估

论文将 2000 和 2015 年全部几何题解提交给美国 IMO 队教练评阅，建议给予满分；但该比较只涉及几何题，不等同于完整 IMO 四领域竞赛表现。

## 证明质量

部分难题需要 100–187 步。Extended Data 显示，人类可用复数、重心坐标或高层定理给出更短结构化证明，而 AlphaGeometry 输出偏低层、冗长，代数中间过程还可能因 Gaussian elimination 隐式化而难读。

## 未解决案例

当符号引擎缺少 Reim、Pitot、位似等高层知识时，模型可能无法提出有效构造，甚至提供人类辅助点后仍不能完成证明。

## 关联页面

- [[trinh2024-alphageometry-analysis]]
- [[trinh2024-alphageometry-method]]
- [[trinh2024-alphageometry-critical]]
- [[entities/alphageometry]]
