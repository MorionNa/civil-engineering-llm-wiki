---
id: concept--grid-anchored-drawing-coordinate-system
title: 轴网锚定的图纸坐标系
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/computer-vision
keywords:
- grid-system
- pixel-to-drawing
- coordinate-transformation
- dimension-annotation
sources:
- sources/papers/zhao2021-structural-drawing-bim.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
---

# 轴网锚定的图纸坐标系

## Definition

利用成对轴网端头、轴线交点和轴间尺寸，从像素坐标中恢复工程图纸坐标的机制。它把局部视觉检测结果映射到具有物理长度和全局拓扑意义的坐标系统。^[sources/papers/zhao2021-structural-drawing-bim.md]

## Mechanism

1. 配对轴网端头并连接为水平/竖向轴线；
2. 选择基准轴线交点作为原点；
3. 读取相邻轴线尺寸并累加得到各轴坐标；
4. 用已知轴距和像素距离估计 X/Y 比例尺；
5. 将构件像素位置转换为工程坐标；
6. 用轴网跨度修正检测框不能精确表达的构件长度。

## Value

- 将“看见构件”转化为“定位构件”；
- 对扫描缩放、平移和边界框偏差具有纠错作用；
- 为跨图纸构件索引和结构拓扑建立统一空间基准。

## Assumptions

图纸需存在可识别轴网和可信尺寸；轴网端头应可正确配对；扫描畸变若不是简单线性缩放，需要更一般的仿射或非线性校正。

## Failure Modes

- 轴网缺失、断裂或编号误配；
- 尺寸 OCR 错误；
- 多套局部轴网或旋转轴网未被区分；
- 图纸存在透视、非均匀扫描变形；
- 构件并非严格位于轴线或轴间。

## Related Pages

- [[zhao2021-structural-drawing-bim-method]]
- [[concepts/constrained-annotation-object-matching]]
- [[entities/hybrid-structural-drawing-to-ifc]]
