---
id: comparison--one-structure-one-model-contract-2026-08-03
title: 一结构一模型：当前结构动力学 PINN 的适用边界
type: comparison
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/ai4s
- method/pinn
- method/evaluation
- evidence/report
keywords:
- one-structure-one-model
- per-structure surrogate
- loading generalization
- constitutive replacement
sources:
- ../../../docs/plans/mtp_mechconv_v2_implementation_log_2026-07-31.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
---

# 一结构一模型：当前结构动力学 PINN 的适用边界

本项目的目标边界是**一个结构对应一个独立训练模型**，不要求同一组权重跨结构、跨自由度数或跨拓扑直接泛化。因此，3DOF 训练后零样本用于 5DOF、50DOF 或 50kDOF，不再是方法成立的必要条件；它只能作为额外能力报告，不能反过来否定一个在目标结构上重新训练后合格的模型。

## 必须保留的泛化要求

“一结构一模型”并不等于记忆单条响应。对固定结构，模型仍需在预注册的加载族内泛化，并在未参与训练的激励上报告：

- 位移、速度、加速度与恢复力的 pooled、逐样本平均和最差样本 R²；
- 低频与项目定义的高频工况；其中高频至少覆盖 6 m 素混凝土梁突然施加竖向荷载后的受迫振动；
- 独立运动方程残差、初边值条件、能量或耗散检查；
- 单条与批量推理时间，并与相同结构、相同时间步、相同硬件和相同输出范围的 OpenSeesPy 对照；
- 训练总时间、epoch 数、硬件、精度和数据量。

## 本构替换的含义

本构可插拔允许替换本构模块后**重新训练该结构的模型**。它不要求原权重零样本跨本构迁移，但要求：接口不改、训练/推理流程不改、独立本构回放通过，并且替换后重新满足精度与速度门槛。若替换本构后只能运行、但没有完整精度和速度结果，只能称为“接口可插拔”，不能称为“性能可插拔”。

## 与既有负面结果的关系

既有 3DOF→5DOF、halo/full-graph 和 50→50kDOF 结果仍有价值：它们揭示边界节点、加速度、恢复力和分组开销的失败模式，但不再承担跨结构泛化证明。后续正式比较应以“每个结构单独训练、同结构公平测试”为主，参照 [[current-structural-pinn-ranking-2026-08-03]] 和 [[reproduction-failure-prevention-contract-2026-08-03]]。

## Provenance

^[../../../docs/plans/mtp_mechconv_v2_implementation_log_2026-07-31.md]
