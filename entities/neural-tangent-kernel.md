---
title: "Neural Tangent Kernel (NTK)"
created: 2026-06-27
updated: 2026-06-27
type: entity
tags: [neural-tangent-kernel, spectral-bias, gradient-pathology, neural-network-theory]
confidence: high
---

# Neural Tangent Kernel (NTK)

## 定义

神经正切核 (NTK) 是描述无限宽度神经网络在梯度下降训练下行为的一个确定性核函数，由 Jacot et al. (2018) 提出：

$$\Theta(x, x') = \mathbb{E}_{\theta \sim \mathcal{N}(0,I)} \left[ \sum_{p} \frac{\partial f(x;\theta)}{\partial \theta_p} \frac{\partial f(x';\theta)}{\partial \theta_p} \right]$$

在 **无限宽度极限** 下，NTK 在训练中保持不变，网络退化为核回归，训练动力学完全由该核的特征谱决定。

## NTK 在 PINN 中的应用

[[wang2021-pinn-ntk-failure-analysis|Wang et al. (2021)]] 将 NTK 扩展到物理信息神经网络：

### 关键发现
1. PINN 的 NTK 为**分块矩阵**，各块对应不同损失分量（PDE 残差 / BC / IC）
2. **谱偏差 (Spectral Bias):** $\lambda_{\max}(K_{rr}) \ll \lambda_{\max}(K_{bb})$ — PDE 物理项的特征值比边界条件小 2-4 个数量级
3. 梯度下降的收敛速率正比于各块的最大特征值 → PDE 物理很难学

### 解决方案
基于 NTK 特征值的自适应学习率退火：
$$\eta_k = \eta \cdot \frac{\max_j \lambda_{\max}(K_{jj})}{\lambda_{\max}(K_{kk})}$$

## 与相关方法的区别

| 方法 | 机制 | 是否基于 NTK |
|------|------|:---:|
| 手动调 λ | 经验调整损失权重 | ✗ |
| Self-adaptive PINN | 可训练权重 | ✗ |
| **NTK 退火** | 特征值自适应学习率 | ✓ |

## 局限

- 仅在无限宽度严格成立，有限网络会偏离
- 计算开销 O(N²P)，大规模受限
- 仅适用于梯度下降，不适用于 Adam 的非线性轨迹

## 交叉引用

- [[wang2021-pinn-ntk-failure-analysis]] — 在 PINN 中的核心应用
- [[wang2023-pinn-spurious-analysis]] — 谱偏差的建筑学表现
- [[pinn]] — PINN 实体
- [[bayesian-pinn]] — Bayesian PINN 中梯度平衡的相关性
- [[physics-constrained-training-failure-modes]] — 物理约束训练失败的总结
