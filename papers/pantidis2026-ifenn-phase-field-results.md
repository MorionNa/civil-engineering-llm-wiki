---
id: paper--pantidis2026-ifenn-phase-field-results
title: "Pantidis et al. (2026) — PICNN-IFENN 相场断裂结果证据"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
keywords:
- convergence
- geometry-generalization
- mesh-generalization
- multi-crack
- training-efficiency
sources:
- sources/papers/pantidis2026-ifenn-phase-field.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
evidence_scope: full-text
---

# 结果与证据

## 极少样本训练

PICNN 仅使用单缺口拉伸算例中两个传播增量的历史变量场训练。训练 10000 epochs，在 GTX 1650 Ti 笔记本上约 5 min，预测相场与 FEM 相场总体一致。^[sources/papers/pantidis2026-ifenn-phase-field.md]

## 载荷步泛化

同一网络用于 350、700 和 1500 增量方案。IFENN 的反力、能量和裂纹轨迹与 FEM 接近，说明不学习时间序列仍可适配不同载荷步安排。

## 网格分辨率泛化

网络从 40000 单元训练域迁移到 61504 和 90000 单元，对应像素输入从 $400\times400$ 扩展到 $496\times496$ 和 $600\times600$。全卷积结构可直接接受不同尺寸输入，且相场传播计算节省随网格细化增大。

## 长度尺度行为

FEM 在固定 $l_c$ 下保持相近物理裂纹宽度，IFENN 在更细网格上预测略窄裂纹。结果表明网络更接近学习 $l_c/l_{elem}$ 对应的像素宽度，而不是绝对 $l_c$。当比例保持为 6.0、绝对长度尺度改变时，IFENN 与 FEM仍接近。

## 多轮交错收敛

关键传播增量中，FEM 需要接近 $10^3$ 次迭代。若从增量开始即激活 PICNN，IFENN 所需迭代数降低近一个数量级，同时保持正确反力突降和相场轮廓。

## 多裂纹与几何泛化

对称双缺口算例中，网络识别两个未见过的裂纹前沿并预测其汇合。非对称双缺口算例改变裂纹方向、位置、载荷方向和域长宽比，网络仍预测两条竖向裂纹及对角汇合，体现较强空间泛化。

## 已观察误差

- IFENN 裂纹往往略窄、略长；
- Gaussian 平滑把峰值从约 1 降至 0.95–0.96，引入残余刚度；
- 非对称裂纹汇合区相场停滞在约 0.7–0.75，反力未完全降为零；
- 传播精度好不等于起裂预测已被网络解决。

## 性能解释边界

论文主要报告相场变量计算时间与迭代数，而非端到端全流程在统一硬件上的普适加速比。训练成本较低，但 FEM 起裂阶段、数据变换、平滑和机械平衡求解仍保留。

## 关联页面

- [[pantidis2026-ifenn-phase-field-analysis]]
- [[pantidis2026-ifenn-phase-field-method]]
- [[pantidis2026-ifenn-phase-field-critical]]
- [[entities/picnn-ifenn-phase-field]]
