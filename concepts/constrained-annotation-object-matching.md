---
id: concept--constrained-annotation-object-matching
title: 约束驱动的图纸标注—构件匹配
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/computer-vision
keywords:
- ocr
- attribute-matching
- spatial-constraint
- orientation-constraint
sources:
- sources/papers/zhao2021-structural-drawing-bim.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
---

# 约束驱动的图纸标注—构件匹配

## Definition

在 OCR 得到“无主”文本后，利用空间距离、文本组成和方向一致性，把构件属性分配给相应图形对象的方法。^[sources/papers/zhao2021-structural-drawing-bim.md]

## Core Constraints

- **距离约束：** 候选标注与构件中心距离最短且小于阈值；
- **语义形式约束：** 构件标注通常同时包含字母和数字；
- **方向约束：** 梁的方向与文字方向一致，以减少交叉梁附近误配。

## Why It Matters

工程图纸中的标注不是直接嵌入构件几何，而是以邻近文字表达。仅靠 OCR 或最近邻会在密集梁柱、标高、剖面号和重叠文字中产生大量归属错误。

## Limitations

原论文采用局部贪心式规则，未保证一个标注只分配给一个构件，也未处理跨图索引、引线、共享标注、集中表格和全局拓扑冲突。

## Extension Opportunities

- 将匹配写成二分图或因子图全局优化；
- 引入构件编号唯一性、轴网位置、梁柱邻接和标注引线；
- 输出匹配置信度和备选候选；
- 支持多图纸之间通过构件编号建立索引表。

## Related Pages

- [[zhao2021-structural-drawing-bim-method]]
- [[concepts/grid-anchored-drawing-coordinate-system]]
- [[entities/hybrid-structural-drawing-to-ifc]]
