---
id: paper--zhao2021-structural-drawing-bim-method
title: "Zhao et al. (2021) — 二维结构图纸重建 BIM 方法机制"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/computer-vision
- evidence/paper
keywords:
- faster-r-cnn
- ocr
- attribute-matching
- coordinate-transformation
- ifc-generation
sources:
- sources/papers/zhao2021-structural-drawing-bim.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
---

# 方法机制

## 1. 输入与输出

输入是扫描得到的结构框架平面图。输出是包含梁柱几何、位置、属性和空间关系的 IFC 楼层模型。论文假定图中至少包含轴网、尺寸、梁柱图形和相应标注。^[sources/papers/zhao2021-structural-drawing-bim.md]

## 2. 图像预处理与增强

扫描图依次进行灰度化、二值化和腐蚀，使细线与文字加粗并降低三通道计算量。训练图像通过水平/竖直翻转、旋转、平移以及高斯或椒盐噪声扩增。

## 3. Faster R-CNN 对象检测

检测类别包括：轴网端头、柱、水平梁、竖向梁和斜梁。Faster R-CNN 由特征提取、区域建议、ROI pooling、分类与边界框回归组成。论文分别研究 ResNet50、101 和 152 作为特征主干。

## 4. OCR 与标注分类

py-tesseract 提取文本及其像素坐标。依据文本内容和位置，将文字分为尺寸标注与构件属性标注。字体差异导致 `B/8`、`0/O` 等混淆，论文用 jTessBoxEditor 训练工程字体。

## 5. 构件—属性匹配

对构件中心 $O_i$ 与标注中心 $A_k$，候选匹配需同时满足：

1. 距离最近且低于阈值；
2. 字符串同时含字母和数字，以排除纯数字标高或剖面编号；
3. 梁框长边方向与文字方向一致。

该规则减少相邻梁、不同方向梁和非属性文本之间的误配。

## 6. 轴网驱动的图纸坐标系

成对轴网端头连接形成水平、竖向轴线。最左下水平轴与竖轴交点设为 DCS 原点，轴网尺寸标注用于累加确定每条轴线的工程坐标。

像素点 $(u,v)$ 转换为图纸坐标 $(x,y)$：

$$x=(u-u_0)\,Scale_x,\qquad y=(v_0-v)\,Scale_y.$$

比例尺由已知轴网间距和像素距离分别在两个方向估计。

## 7. 几何纠错与中间表示

目标框仅代表检测区域，论文不直接采用框长作为梁长，而使用梁两端轴网间距。对象信息写入 XML，字段包括 id、type、isSecondary、section、length、grid、DCS 坐标、像素框坐标和检测置信度。

## 8. IFC 生成

梁、柱分别映射为 IfcBeam 和 IfcColumn。矩形截面通过 IfcRectangleProfileDef，拉伸实体通过 IfcExtrudedAreaSolid 表示；IfcRelAggregates 和 IfcRelContainedInSpatialStructure 建立项目—场地—建筑—楼层—构件关系。

## 9. 求解策略与误差控制

该流程采用级联处理：检测结果进入 OCR 匹配，随后由轴网坐标纠正几何，再生成 IFC。论文强调在后处理阶段利用工程规则修正视觉检测误差，而不是假定神经网络输出已经是精确工程数据。

## 10. 假设和失败边界

- 只处理框架平面图中的轴网、梁和柱；
- 梁长按轴网跨度计算，未扣除柱截面；
- 柱截面、配筋和标高需来自其他图纸，本文未解析；
- OCR 和匹配依赖字体、文本方向及阈值；
- IFC 高度采用默认值，无法表达真实三维竖向信息；
- 输入图若缺少尺寸或轴网，DCS 机制无法完整工作。

## 关联页面

- [[zhao2021-structural-drawing-bim-analysis]]
- [[zhao2021-structural-drawing-bim-results]]
- [[zhao2021-structural-drawing-bim-critical]]
- [[concepts/grid-anchored-drawing-coordinate-system]]
- [[concepts/constrained-annotation-object-matching]]
