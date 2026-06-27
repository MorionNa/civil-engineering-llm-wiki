---
title: "Wang et al. (2021) PINN 失败机制 — 方法展开：NTK 推导与自适应算法"
created: 2026-06-27
updated: 2026-06-27
type: paper-analysis
tags: [physics-informed, pinn, neural-tangent-kernel, spectral-bias, gradient-pathology, multi-task-learning]
confidence: high
---

# 方法展开：NTK 推导与自适应学习率

## 5.1 PINN 的 NTK 形式化

### 标准 NTK 回顾

对标准监督学习 $f(x; \theta)$，NTK 定义为：
$$\Theta(x, x') = \sum_{p=1}^{P} \frac{\partial f(x;\theta)}{\partial \theta_p} \frac{\partial f(x';\theta)}{\partial \theta_p}$$

在无限宽度极限下，NTK 收敛到确定性常核 $\Theta^*$，训练动力学退化为线性 ODE。

### PINN 的多损失 NTK

PINN 损失函数包含多项：
$$\mathcal{L}(\theta) = \lambda_r \mathcal{L}_r + \lambda_b \mathcal{L}_b + \lambda_0 \mathcal{L}_0$$

其中：
- $\mathcal{L}_r$：PDE 残差损失（域内配点）
- $\mathcal{L}_b$：边界条件损失
- $\mathcal{L}_0$：初始条件损失

PINN 的多输出 NTK 矩阵为分块结构：
$$\mathbf{K} = \begin{bmatrix} K_{rr} & K_{rb} & K_{r0} \\ K_{br} & K_{bb} & K_{b0} \\ K_{0r} & K_{0b} & K_{00} \end{bmatrix}$$

### 关键理论结果

1. **NTK 收敛定理：** 在无限宽度极限下，PINN 的 NTK 在训练过程中保持不变
2. **对角块 $K_{rr}$ (PDE 残差对应) 的特征值**远小于 $K_{bb}$ (边界条件对应)
3. **梯度下降收敛速率** $\propto$ 相应块的最大特征值 —— 谱偏差

## 5.2 谱偏差的数学分析

### 收敛速率差异

对第 k 个损失分量：
$$\frac{d\mathcal{L}_k}{dt} \approx -\eta \cdot \lambda_{\max}(K_{kk}) \cdot \mathcal{L}_k$$

由于 $\lambda_{\max}(K_{rr}) \ll \lambda_{\max}(K_{bb})$：
- 边界条件损失 → 快速收敛（1-100 次迭代）
- PDE 残差损失 → 缓慢收敛（1000-10000 次迭代）

### 梯度主导效应

在多任务学习中，梯度方向受最大特征值对应的分量主导：
$$\nabla_\theta \mathcal{L} \approx \nabla_\theta \mathcal{L}_b \quad (\text{如果 } \lambda_{\max}(K_{bb}) \gg \lambda_{\max}(K_{rr}))$$

这导致网络优先满足边界条件，PDE 物理约束长期得不到满足。

## 5.3 自适应学习率退火算法

### 核心思想

根据 NTK 特征值动态调整各损失项的权重/学习率：

$$\eta_k^{(t)} = \eta \cdot \frac{\bar{\lambda}}{\lambda_{\max}(K_{kk})}$$

其中 $\bar{\lambda} = \max_k \lambda_{\max}(K_{kk})$ 是全局最大特征值。

### 算法流程

```
输入: 网络 f_θ, PDE 配点集, BC/IC 配点集
初始化: θ ~ N(0, σ²)

for t = 1 to T:
    # 每 m 步计算 NTK
    if t % m == 0:
        计算各损失分量的 NTK 块
        提取 λ_max(K_rr), λ_max(K_bb), λ_max(K_0)
        更新自适应学习率 η^{(t)}
    
    # 标准梯度下降
    计算各损失分量的梯度
    θ ← θ - [η_r·∇L_r + η_b·∇L_b + η_0·∇L_0]
```

### 复杂度

- NTK 计算: O(N²P)，N 为配点数，P 为参数数
- 实际使用中仅每 m=100 步计算一次，总开销 < 5% 训练时间

## 5.4 关键参数

| 参数 | 含义 | 典型值 |
|------|------|--------|
| m | NTK 重计算间隔 | 100 |
| σ² | 初始化方差 | 1/fan_in |
| η | 基础学习率 | 1e-3 |
| λ_r, λ_b, λ_0 | 初始损失权重 | 1.0 |

## 方法关联

- [[wang2021-pinn-ntk-failure-analysis|← 总览]]
- [[wang2021-pinn-ntk-failure-results|结果展开 →]]
- [[wang2021-pinn-ntk-failure-critical|批判分析 →]]
