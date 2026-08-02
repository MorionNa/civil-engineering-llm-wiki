---
id: sources--papers--liu2025-incompressible-crack-mpm
title: "Liu et al. (2025) — 体积保持 MPM 不可压缩裂纹模型"
type: source
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- continuum-damage-mechanics
- fracture
- incompressible-crack
- material-point-method
- volume-preserving-debris
sources:
- raw/papers/liu2025-incompressible-crack-mpm-source.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
evidence_scope: full-text
code_url: []
dataset_url: []
---

# 来源记录：体积保持 MPM 不可压缩裂纹模型

## 文献信息

- **英文题名：** An Incompressible Crack Model for Volume Preserving MPM Fracture
- **作者：** Shiguang Liu、Maolin Wu、Chenfanfu Jiang、Yisheng Zhang
- **期刊：** Proceedings of the ACM on Computer Graphics and Interactive Techniques, 8(1), Article 6
- **日期：** May 2025
- **DOI：** 10.1145/3728298
- **证据范围：** 用户提供的 18 页正式全文。

## 证据地图

- 第 1–3 页：问题背景、CDM 应力软化在压缩裂纹中的缺陷、主要贡献。
- 第 4–8 页：MPM/本构背景、Weibull 失效应力、局部损伤演化与完全损伤相变。
- 第 8–11 页：Drucker–Prager 碎屑塑性、非关联流动与额外体积变形梯度。
- 第 11–16 页：巴西圆盘、复杂网格、参数研究、碎屑体积保持与性能比较。
- 第 17 页：结论与网格分辨率相关裂纹增厚局限。

## 证据边界

论文目标是计算机图形学中的动态断裂效果，主要证据为视觉比较、参数实验和运行时间。论文没有提供真实混凝土/岩石材料标定、断裂能客观性系统验证、网格收敛研究、裂纹面几何误差或工程尺度试验对照。涉及 RC 倒塌、混凝土压碎和工程预测的内容必须标记为迁移推论。

## 生成页面

- [[papers/liu2025-incompressible-crack-mpm-analysis]]
- [[papers/liu2025-incompressible-crack-mpm-method]]
- [[papers/liu2025-incompressible-crack-mpm-results]]
- [[papers/liu2025-incompressible-crack-mpm-critical]]
- [[entities/incompressible-crack-mpm]]
- [[concepts/compression-aware-damage-transition]]
- [[concepts/volume-preserving-debris-plasticity]]
