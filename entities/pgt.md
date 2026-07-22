---
title: "Physics-Guided Transformer (PGT)：物理感知注意力机制"
created: 2026-07-22
updated: 2026-07-22
type: entity
tags: [PINN, Transformer, physics-guided-learning]
---

# Physics-Guided Transformer (PGT)

## 定义

PGT是一种将物理传播规律嵌入 Transformer attention 的物理信息神经网络框架。其核心思想是：物理知识不仅用于训练约束，也用于决定神经网络内部的信息传播方式。

## 核心机制

通过 Green 函数构造 attention bias：

$$Attention=softmax(QK^T+\Gamma)V$$

使注意力权重符合 PDE 的空间传播和时间因果规律。

## 与其他方法关系

- PINN：物理进入损失函数；
- PGT：物理进入信息传播；
- SeisGPT：物理进入结构表示和传播算子。

## 结构动力学启发

可将结构质量、刚度、阻尼和模态信息构造为 physics bias，用于大型结构响应预测。

## 局限

目前主要验证 PDE 场重构，对结构强非线性、本构演化和倒塌问题仍需扩展。
