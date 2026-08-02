---
id: concept--spatial-coupling-without-temporal-features
title: 无时序特征的空间耦合学习 — 以历史变量承载路径依赖
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- history-variable
- path-dependence
- spatial-coupling
- time-agnostic
sources:
- sources/papers/pantidis2026-ifenn-phase-field.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
---

# 无时序特征的空间耦合学习

## 定义

该策略不让网络直接学习完整载荷时间序列，而由物理求解器维护不可逆历史变量，再让网络学习当前历史场到内部状态场的局部空间映射。在本文中，FEM 更新最大拉伸应变能密度 $H$，PICNN 学习 $H\mapsto\phi$。^[sources/papers/pantidis2026-ifenn-phase-field.md]

## 核心意义

路径依赖没有被删除，而是被压缩进满足物理定义的历史变量。网络因而不受固定序列长度和载荷增量方案约束，可在不同在线时间离散中复用。

## 适用条件

- 存在足以描述演化记忆的历史变量；
- 当前状态主要由历史变量的局部空间分布决定；
- 物理求解器持续更新历史变量并约束不可逆性；
- 传播模式未显著超出训练中出现的局部空间机制。

## 风险

历史变量可能不是完备状态描述。复杂混合模态、速率效应、循环加载、材料多尺度记忆或分叉可能需要更多状态变量、显式时间特征或递归结构。

## 迁移价值

可用于塑性累积量、损伤历史、孔压峰值或接触状态等内部场代理，但需要先证明选定历史变量对目标演化近似充分。

## 关联页面

- [[entities/picnn-ifenn-phase-field]]
- [[concepts/physics-informed-laplacian-convolution]]
- [[papers/pantidis2026-ifenn-phase-field-method]]
- [[papers/pantidis2026-ifenn-phase-field-critical]]
