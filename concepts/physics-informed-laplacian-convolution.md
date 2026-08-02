---
id: concept--physics-informed-laplacian-convolution
title: 物理信息 Laplacian 卷积 — 用固定差分核构造 PDE 残差
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- finite-difference
- laplacian-kernel
- pde-residual
- physics-informed-cnn
sources:
- sources/papers/pantidis2026-ifenn-phase-field.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
---

# 物理信息 Laplacian 卷积

## 定义

在规则像素网格上，使用固定、不可训练的有限差分卷积模板计算网络输出场的 Laplacian，再把结果代入 PDE 强式残差作为训练损失。本文采用修改后的 9 点模板计算相场 $\nabla^2\phi$。^[sources/papers/pantidis2026-ifenn-phase-field.md]

## 机制

可训练卷积层负责从历史能量场提取局部特征并预测相场；固定 Laplacian 层负责显式注入空间微分算子。最终损失是相场 PDE 残差的二范数，因此无需标签相场数据。

## 优点

- 微分算子透明且无需自动微分高阶导数；
- 与规则图像张量和 GPU 卷积高度兼容；
- 训练和推理尺寸可变；
- 便于检查离散阶数、边界处理和模板误差。

## 边界

固定模板依赖规则、均匀网格。非结构网格、曲边界、局部加密和各向异性算子需要投影、图 Laplacian、有限体积或可学习但受约束的离散算子。卷积残差正确也不保证网络满足全局能量最小化。

## 迁移价值

可用于扩散、热传导、压力泊松、损伤梯度和相场方程等局部椭圆算子代理；在结构动力问题中，高阶时间导数和不规则结构图需采用不同离散方式。

## 关联页面

- [[entities/picnn-ifenn-phase-field]]
- [[concepts/spatial-coupling-without-temporal-features]]
- [[papers/pantidis2026-ifenn-phase-field-method]]
- [[papers/pantidis2026-ifenn-phase-field-results]]
