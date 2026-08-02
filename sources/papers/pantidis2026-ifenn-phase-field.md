---
id: sources--papers--pantidis2026-ifenn-phase-field
title: "Pantidis et al. (2026) — PICNN-IFENN 相场断裂"
type: source
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
keywords:
- ifenn
- phase-field-fracture
- physics-informed-cnn
- hybrid-fem-ml
- generalization
sources:
- raw/papers/pantidis2026-ifenn-phase-field-source.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
evidence_scope: full-text
code_url:
- https://github.com/ppantidis/IFENN-with-PICNNs-for-phase-field-propagation
dataset_url: []
---

# 来源记录：PICNN-IFENN 相场断裂

## 文献信息

- **英文题名：** Integrated Finite Element Neural Network (IFENN) for phase-field fracture with minimal input and generalized geometry-load handling
- **作者：** Panos Pantidis、Lampros Svolos、Diab Abueidda、Mostafa E. Mobasher
- **期刊：** Computer Methods in Applied Mechanics and Engineering 448 (2026), 118485
- **DOI：** 10.1016/j.cma.2025.118485
- **证据范围：** 用户提供的 23 页正式全文。

## 证据地图

- 第 1–3 页：研究缺口、IFENN 定位、主要贡献与超小样本训练声明。
- 第 3–5 页：AT2 相场断裂、历史变量、弱式与交错 FEM 基线。
- 第 5–10 页：IFENN 三阶段流程、PICNN、Gauss 点到像素映射、对称卷积核、PDE 残差训练与在线迭代。
- 第 10–12 页：单缺口训练问题、两增量训练数据、网络结构与约 5 min 训练。
- 第 12–20 页：载荷步、网格分辨率、多轮交错、双裂纹、旋转载荷与矩形域泛化。
- 第 20–21 页：结论、局限、未来工作与代码地址。

## 证据边界

论文验证的是二维、矩形、均匀结构化网格上的准静态 Mode-I 为主的相场断裂传播。相场起裂阶段仍由 FEM 完成；PICNN 主要替代传播阶段的相场方程。当前未验证三维、非结构网格、混合模态分叉、参数化材料空间、动态断裂或工程尺度 RC 构件。

## 生成页面

- [[papers/pantidis2026-ifenn-phase-field-analysis]]
- [[papers/pantidis2026-ifenn-phase-field-method]]
- [[papers/pantidis2026-ifenn-phase-field-results]]
- [[papers/pantidis2026-ifenn-phase-field-critical]]
- [[entities/picnn-ifenn-phase-field]]
- [[concepts/spatial-coupling-without-temporal-features]]
- [[concepts/physics-informed-laplacian-convolution]]
