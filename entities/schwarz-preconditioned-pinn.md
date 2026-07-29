---
title: "Schwarz-preconditioned PINN — 参数空间域分解训练"
created: 2026-07-28
updated: 2026-07-28
type: entity
tags: [physics-informed, pinn, schwarz-method, nonlinear-preconditioning, quasi-newton, layerwise-decomposition, model-parallelism]
sources: [raw/papers/kopanicakova2024-dd-preconditioning.pdf]
confidence: high
---

# Schwarz-preconditioned PINN

## 定义

Schwarz-preconditioned PINN 把神经网络层参数看作非线性“子域”，先对各层组做局部 L-BFGS 校正，再执行全局 L-BFGS，以改善 PINN 复合 loss 的条件性。

## 两种算法

| 变体 | 信息流 | 计算环境 | 特点 |
|---|---|---|---|
| ASPQN | 加法、并行叠加局部校正 | 多 GPU | 墙钟最短，但复制全网 |
| MSPQN | 乘法、顺序传播局部校正 | 单 GPU | 纯算法效率更公平 |

代表论文：[[kopanicakova2024-dd-preconditioning-analysis]]。

## 与输入域分解的区别

[[fbpinn]] 和 [[xpinn]] 切分物理/输入域，降低局部函数复杂度；Schwarz-preconditioned PINN 切分参数域，降低优化病态。两类方法可嵌套，但通信、显存与局部循环也会叠加。

## 关键证据

四类 PDE 中，MSPQN 相对 L-BFGS 平均 time-to-solution 约快 10×；ASPQN 约快 28×，但使用 6–8 GPU，不能视为等资源 speedup。→ [[kopanicakova2024-dd-preconditioning-results]]

## 适用场景

全批量 PINN、L-BFGS 容易停滞、网络层结构清晰且可承担局部优化的任务。

## 局限

固定按层分组未必匹配曲率；无重叠/粗层；ASPQN 每 GPU 复制完整网络；mini-batch 噪声与大模型未验证。

## 关联页面

- [[kopanicakova2024-dd-preconditioning-method]]
- [[kopanicakova2024-dd-preconditioning-critical]]
- [[pinn]] · [[fbpinn]]