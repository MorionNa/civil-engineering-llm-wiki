---
title: "Hamiltonian Monte Carlo (HMC)"
created: 2026-06-27
updated: 2026-06-27
type: entity
tags: [bayesian-inference, hamiltonian-monte-carlo, uncertainty-quantification, mcmc, physics-informed, pinn]
sources: [raw/papers/10_1016_j_cma_2022_115346_extracted.txt]
---

# Hamiltonian Monte Carlo (HMC)

## 概述

Hamiltonian Monte Carlo (HMC) 是一种基于哈密顿动力学的马尔可夫链蒙特卡洛（MCMC）采样方法，用于从高维概率分布中高效采样。与传统的随机游走 Metropolis-Hastings 不同，HMC 利用目标分布的梯度信息，在参数空间中沿"物理轨迹"运动，极大提高了高维空间中的采样效率。

**核心思想：** 将采样问题转化为模拟物理系统——引入辅助动量变量 p，定义哈密顿量 H(Θ, p) = -log P(Θ) + ½pᵀM⁻¹p，然后沿等能量面模拟哈密顿动力学来探索参数空间。

## 在 BPINN 中的应用

在 Linka et al. (2022) 的 BPINN 框架中，HMC（具体为 NUTS 变体）用于从联合后验中采样：

$$P(Θ|x̂, r) ∝ P(x̂|Θ) · P(r|Θ) · P(Θ)$$

其中 Θ = {网络权重 W_k, b_k, 物理参数 c, k, x₀}。

每个 HMC 步需要：
1. 计算对数后验的梯度 ∇_Θ log P(Θ|x̂, r)
2. 这包括对网络前向传播 + 物理残差计算的反向传播
3. 在网络参数空间中模拟哈密顿轨迹

## 关键变体

- **NUTS (No-U-Turn Sampler)：** Hoffman & Gelman (2014)，自动调节步长和轨迹长度，无需手动指定 leapfrog 步数
- **PyMC3 实现：** Python 概率编程库，使用 Theano/Aesara 自动微分计算梯度

## HMC 的优劣

| 优点 | 缺点 |
|------|------|
| 高效探索高维空间（利用梯度） | 每次迭代需要计算全梯度 → 大网络时极慢 |
| 自相关低，混合好（vs 随机游走 MCMC） | 对步长敏感（NUTS 缓解） |
| 适用于非共轭后验 | 对多模态分布混合困难 |
| NUTS 自动调参，零调优 | 在高维（>1000 维）时仍可能混合慢 |

## 在 BPINN 中的计算瓶颈

BPINN 使用 HMC 时的主要瓶颈：
- 网络权重维度可能达数百至数千
- 每次 HMC 迭代需完整前向+反向传播
- 通常需要数千次采样 + 预热期 → 总计算成本是 PINN 的 100-1000×

## 替代方案（研究机会）

- **变分推理 (VI)：** Bayes by Backprop, MFVI — 速度提升 10-100×，但后验近似有偏
- **Stein 变分梯度下降 (SVGD)：** 粒子法，非参数后验近似
- **拉普拉斯近似：** 在 MAP 估计点用 Hessian 近似后验

## 关联

- [[bayesian-pinn]] — BPINN：HMC 的核心应用场景
- [[linka2022-bayesian-pinn-analysis]] — 原始论文
- [[linka2022-bayesian-pinn-critical]] — BPINN 的 HMC 计算成本讨论
