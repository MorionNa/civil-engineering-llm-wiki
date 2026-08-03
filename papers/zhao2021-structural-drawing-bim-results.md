---
id: paper--zhao2021-structural-drawing-bim-results
title: "Zhao et al. (2021) — 二维结构图纸重建 BIM 结果与证据"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/computer-vision
- evidence/paper
keywords:
- detection-metrics
- dataset-size
- ocr-accuracy
- ifc-case-study
sources:
- sources/papers/zhao2021-structural-drawing-bim.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
---

# 结果与证据

## 1. 数据集

论文收集 500 张符合 BS 8110 的结构框架平面图，共标注 12,693 个对象：5152 个轴网端头、3073 个柱、2130 个水平梁、2120 个竖向梁和 218 个斜梁。经增强形成 4000 张图像、101,544 个对象。^[sources/papers/zhao2021-structural-drawing-bim.md]

## 2. 五类对象检测

在 100 张新平面图上，Faster R-CNN 的结果为：

| 类别 | Precision | Recall | F1 |
|---|---:|---:|---:|
| 轴网端头 | 94.41% | 92.07% | 93.22% |
| 柱 | 88.45% | 82.34% | 85.29% |
| 水平梁 | 90.41% | 92.82% | 91.60% |
| 竖向梁 | 93.27% | 91.36% | 92.31% |
| 斜梁 | 89.19% | 91.67% | 90.41% |

柱的表现最弱，作者归因于单个柱的图像占比最低且易受梁线干扰。在干扰较少的柱平面图中，柱检测的 precision、recall 和 F1 均超过 95%。

## 3. 数据规模影响

从 500 张原始数据扩展到 4000 张增强数据后：

- mAP：76.96% → 90.41%；
- wmAP：81.51% → 91.28%；
- 斜梁 AP：59.09% → 88.99%，增幅 29.90%。

这说明少数类更依赖扩增，但并不证明合成增强能覆盖不同国家或年代的真实图纸分布。

## 4. 主干网络影响

论文比较 ResNet50、101、152。图 16 报告 ResNet152 获得 mAP 91.29%、wmAP 92.17%，训练时间约 6.9 h；网络加深提高了指标，同时增加训练成本。正文中出现“Res152 mAP 81.29%”的文字，与图表 91.29% 不一致；知识页采用图表值并保留这一内部矛盾。

## 5. OCR 字体适配

通过建立工程字体文本集并使用 jTessBoxEditor 更新 Tesseract 字典，论文报告在 100 张测试图上的字符识别准确率为 94%。该指标未进一步拆分为尺寸、构件编号和截面字符串的字段级准确率。

## 6. 坐标与属性案例

案例中，梁 B13 被定位在 A–B 轴之间并跨 3 轴，输出 DCS 坐标为 (7300, 9000)，梁长按 A–B 轴距取 9000。图 14 展示了检测框、轴网坐标、XML 字段及置信度的中间结果。

## 7. IFC 案例

香港 Shek Lei Catholic Secondary School 的一层框架平面图被转换为包含 IfcBeam 和 IfcColumn 的 IFC 模型。图 15 显示生成的框架几何，但论文未报告 IFC 构件级完整率、属性级准确率、人工修正耗时或模型与真实建筑的逐字段对照。

## 8. 比较条件与解释边界

- Faster R-CNN 与 YOLO 使用相同的 4000 张增强图和 100 张测试图；除柱 recall 外，Faster R-CNN 指标略高。
- 评估重点是检测框，不是最终构件字段和 BIM 拓扑的端到端准确率。
- 数据主要符合一个标准体系，无法据此断言跨规范、跨年代或手绘图纸泛化。
- 单一真实案例只证明流程可运行，不足以证明工程规模可靠性。

## 关联页面

- [[zhao2021-structural-drawing-bim-analysis]]
- [[zhao2021-structural-drawing-bim-method]]
- [[zhao2021-structural-drawing-bim-critical]]
- [[entities/hybrid-structural-drawing-to-ifc]]
