---
id: paper--trinh2024-alphageometry-method
title: "Trinh et al. (2024) — AlphaGeometry 方法"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/llm
- domain/ai4s
- evidence/paper
keywords:
- deductive-database
- algebraic-reasoning
- traceback
- transformer
- beam-search
sources:
- sources/papers/trinh2024-alphageometry.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
---

# AlphaGeometry 方法

## 1. 几何表示

采用 GEX/JGEX 一类专用几何语言，显式表示构造、关系和数值常量；每个证明步骤可逻辑和数值验证。该语言能覆盖论文筛选范围中的约 75%，但不是通用形式化语言。^[sources/papers/trinh2024-alphageometry.md]

## 2. 一致前提采样

用构造式 diagram builder 逐个创建对象，而不是任意拼接多个约束，从而避免自相矛盾前提。作者从近 10 亿随机前提样本中运行符号推导。

## 3. DD + AR 符号引擎

- **DD:** 依据几何 Horn 规则执行前向推导；
- **AR:** 将角度、比值和距离等式转为线性系数矩阵，通过 Gaussian elimination 穷举线性结论；
- 两者交替交换新结论，直至联合闭包停止扩展。

## 4. Traceback 与最小证明

每个推导节点记录父依赖。等式用最短路径回溯；共线/共圆使用超图近似最小生成树；代数推导的最小前提转为混合整数线性规划。随后试删辅助点并重跑符号引擎，以剪除虚假或多余构造。

## 5. Dependency Difference

若某些点参与最小证明，却不属于结论对象的构造依赖，则将其从前提移到证明序列中，作为语言模型要学习的辅助构造动作。

## 6. 合成数据

100,000 个 CPU worker 运行 72 小时，先得到约 5 亿证明样本，规范化去重后保留 1 亿唯一 theorem–proof 对，其中约 900 万包含至少一个辅助构造。

## 7. 模型训练

151M 参数 transformer：12 层、1024 embedding、8 个 attention heads、4096 dense dimension、757 词表、1024 最大上下文。先在全部 1 亿证明上预训练，再在 900 万辅助构造证明上微调。

## 8. 证明搜索

语言模型每轮提出一个辅助构造；符号引擎扩张闭包并检查目标。beam size 为 512，最大深度 16，分支解码批量 32。报告配置使用 4 个 V100 模型副本和共享的 10,000 CPU symbolic workers。

## 9. 可迁移框架

迁移到其他域需要四项：对象与定义实现、随机前提采样器、符号引擎、符号引擎的 traceback。缺少任一项都不能直接复制 AlphaGeometry 数据闭环。

## 关联页面

- [[trinh2024-alphageometry-analysis]]
- [[trinh2024-alphageometry-results]]
- [[trinh2024-alphageometry-critical]]
- [[entities/alphageometry]]
- [[concepts/dependency-difference-auxiliary-construction]]
- [[concepts/traceback-synthetic-theorem-generation]]
- [[concepts/alternating-neural-symbolic-proof-search]]
