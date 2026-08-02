---
id: entity--picnn-ifenn-phase-field
title: PICNN-IFENN — 相场断裂混合 FEM–神经求解器
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/computational-mechanics
- entity/model
- evidence/paper
keywords:
- ifenn
- phase-field-fracture
- physics-informed-cnn
- staggered-fem
sources:
- sources/papers/pantidis2026-ifenn-phase-field.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
---

# PICNN-IFENN

## 定义

PICNN-IFENN 是 Pantidis 等提出的相场断裂混合求解器：FEM 求解机械平衡，物理信息卷积网络在传播阶段近似相场 PDE，两者在每个载荷增量内交替交换历史能量密度和相场。^[sources/papers/pantidis2026-ifenn-phase-field.md]

## 核心组成

- AT2 相场断裂与历史变量不可逆性；
- [[concepts/spatial-coupling-without-temporal-features]]；
- Gauss 点到像素的一一映射；
- 双反射对称 $5\times5$ 卷积核；
- [[concepts/physics-informed-laplacian-convolution]]；
- FEM–PICNN 交错迭代、输入截断、双重不可逆和 Gaussian 平滑。

## 训练与部署特征

网络仅用单缺口算例两个传播增量训练，约 5 min；由于全卷积结构，可接受不同像素尺寸，并用于不同网格、载荷步、裂纹数量和矩形域。

## 数值角色

该模型不是完全替代 FEM。FEM 提供平衡、历史变量和起裂阶段；网络主要减少传播阶段相场自由度求解和交错迭代成本。

## 适用边界

当前限于二维矩形规则网格、均匀离散和以 Mode-I 为主的脆性传播。未验证三维、非结构网格、材料参数泛化、动态断裂和工程 RC 构件。

## 项目角色

可作为“高成本内部损伤场神经替代器”的参考，与 [[mpm-lite]] 和 [[unified-sparse-mpm]] 分别在求解器积分和稀疏存储层形成互补。

## 关联页面

- [[papers/pantidis2026-ifenn-phase-field-analysis]]
- [[papers/pantidis2026-ifenn-phase-field-method]]
- [[papers/pantidis2026-ifenn-phase-field-results]]
- [[papers/pantidis2026-ifenn-phase-field-critical]]
