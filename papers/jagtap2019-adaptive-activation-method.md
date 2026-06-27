---
title: "Jagtap et al. (2019) 自适应激活函数 — 方法展开"
created: 2026-06-27
updated: 2026-06-27
type: paper-analysis
tags: [physics-informed, pinn, adaptive-activation, convergence-acceleration, activation-function]
confidence: high
---

# 方法展开：全局/局部自适应激活函数

## 5.1 核心公式

### 全局自适应激活函数

单层前向传播：
$$y = \sigma(n a \cdot (Wx + b))$$

其中：
- $a \in \mathbb{R}^+$：全局可训练缩放因子
- $n \geq 1$：预定义缩放因子（默认 $n=1$ 或 $n=10$）
- $\sigma$：基础激活函数（通常 tanh）

### 局部自适应激活函数

每神经元独立缩放：
$$y_i = \sigma(n a_i \cdot (Wx + b)_i)$$

其中 $a_i$ 为第 i 个神经元的可训练参数，$i = 1, \dots, N_h$。

### 参数增量

| 模式 | 参数增量 | 示例 (4层, 每层50神经元) |
|------|:---:|------|
| 全局 | 每层 1 个 | 4 参数 |
| 局部 | 每层 $N_h$ 个 | 200 参数 |
| 原始 | 0 | 基准 |

## 5.2 斜率恢复项 (Slope Recovery Term)

防止 $a$ 退化到极小值：
$$\mathcal{L}_{slope} = \lambda \cdot \frac{1}{\frac{1}{L} \sum_{\ell=1}^{L} \max(0, a_\ell - 1)^2 + \epsilon}$$

推动 $a \to 1$（接近标准激活函数），同时允许偏离。

### 总损失

$$\mathcal{L}_{total} = \mathcal{L}_{PDE} + \mathcal{L}_{BC/IC} + \mathcal{L}_{slope}$$

## 5.3 训练策略

| 参数 | 值 |
|------|-----|
| 优化器 | Adam |
| 学习率 | $10^{-3} \to 10^{-5}$ (阶梯衰减) |
| 激活函数 | tanh (基础) |
| $n$ (预缩放) | 1, 5, 10 |
| $\lambda$ (斜率正则) | 0.1 |
| `a` 初始化 | 1.0 (全局), 1.0 (局部) |

## 5.4 直觉解释

$a > 1$ → 激活函数斜率更大 → 梯度更大 → 训练更快（高频区域受益）
$a < 1$ → 更平滑 → 低频区域更稳定

局部模式的`a_i`可以自动形成"高频神经元"（大 a）和"低频神经元"（小 a）——类似多尺度分解。

## 页内导航

- [[jagtap2019-adaptive-activation-analysis|← 总览]]
- [[jagtap2019-adaptive-activation-results|结果展开 →]]
- [[jagtap2019-adaptive-activation-critical|批判分析 →]]
