---
title: "Muon — MomentUm Orthogonalized by Newton–Schulz"
created: 2026-07-29
updated: 2026-07-29
type: entity
tags: [neural-network, optimizer, muon, matrix-orthogonalization, newton-schulz, sgd-momentum, preconditioning, spectral-norm, training-efficiency]
sources: [notes/articles/jordan2024-muon-optimizer.md]
confidence: high
---

# Muon

## 定义

Muon 是面向神经网络隐藏层二维矩阵参数的优化器。它先形成带动量的随机梯度更新，再通过少量 Newton–Schulz 迭代近似正交化更新矩阵，使不同奇异方向获得更均衡的步长。详细来源见 [[notes/articles/jordan2024-muon-optimizer]]。

## 更新机制

给定梯度 $G_t$ 和动量缓冲 $B_t$：

$$
B_t=\mu B_{t-1}+G_t,\qquad
O_t=\operatorname{NewtonSchulz5}(B_t),\qquad
\theta_t=\theta_{t-1}-\eta O_t.
$$

Newton–Schulz 步骤近似把奇异值压向相同尺度，因此可视为对更新方向的矩阵级预条件。Muon 不替代所有参数的优化：embedding、输出层以及标量或向量参数通常仍交给 AdamW。

## 适用范围

- 隐藏层中的二维权重矩阵，尤其是 Transformer 的线性变换。
- 希望同时讨论样本效率与墙钟效率的训练场景。
- 可与 [[functional-scaling-law]] 的完整训练轨迹分析结合，区分早期收益、渐近收益和学习率计划影响。

## 边界与风险

- “近似正交更新”不等于权重矩阵本身保持正交。
- Muon 的收益依赖矩阵形状、缩放规则、实现内核和分布式通信；不能只用迭代步数判断实际效率。
- 技术博客证据并非同行评审结果，跨模型规模与任务的优势仍需独立复现。

## 关联页面

- [[notes/articles/jordan2024-muon-optimizer]] — 来源、推导、实现细节和实验边界
- [[functional-scaling-law]] — 优化器与学习率计划的训练轨迹分析
- [[legonet]] — 科学机器学习模型，可作为比较不同优化器训练动力学的对象
