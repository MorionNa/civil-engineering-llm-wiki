---
title: "Wang & Zhong (2024) — NAS-PINN: Neural architecture search-guided physics-informed neural network"
created: 2026-07-30
updated: 2026-07-30
type: paper-analysis
tags: [physics-informed, pinn, neural-architecture-search, differentiable-nas, bi-level-optimization, ai4s, pde]
sources: [raw/papers/wang2024-nas-pinn-source.md]
methods: [darts, continuous-search-space, mask-based-search, architecture-parameter-optimization, weight-parameter-optimization]
results: [poisson-equation, burgers-equation, advection-equation, irregular-domain, high-dimensional-pde]
failure_modes: [search-cost, small-search-space, PDE-specific-architecture, no-code-release, data-availability-limited]
datasets: [poisson-equation, burgers-equation, advection-equation]
reproducibility: medium
confidence: high
---

# NAS-PINN: Neural architecture search-guided physics-informed neural network for solving PDEs

> **作者：** Yifan Wang, Linlin Zhong  
> **期刊：** Journal of Computational Physics 496 (2024) 112603  
> **一句话定位：** NAS-PINN 将神经架构搜索引入 PINN，通过连续化搜索空间和双层优化自动寻找适合特定 PDE 的网络深度与宽度，避免依赖人工经验设计 PINN 网络结构。

## 1. 工程背景 (Engineering Background)

PINN 通过将 PDE 物理约束写入损失函数实现无监督求解，但网络结构通常依赖经验设计。作者指出，传统 PINN 常采用固定 4–6 层、每层相同神经元数量的全连接网络，这种经验规则无法保证针对不同 PDE 达到最优性能。fileciteturn23file0L71-L74

## 2. Research Gap

已有 PINN 研究主要关注损失函数、采样策略和梯度优化，而网络架构设计研究较少。论文认为，神经网络结构会显著影响 PINN 性能，但此前探索往往零散且耗时。fileciteturn23file0L70-L76

## 3. Scientific Question

不同 PDE 是否存在不同的高效 PINN 网络结构？能否自动搜索网络深度、宽度以及残差结构，而不是依靠人工经验？

## 4. Research Objective

本文目标：

- 构建自动化 PINN 架构搜索方法；
- 在有限计算成本下搜索不同 PDE 的有效网络结构；
- 总结不同 PDE 对网络结构的偏好规律。

## 5. Method & Mechanism

→ [[wang2024-nas-pinn-method]]

NAS-PINN 基于可微 NAS 思想，将离散架构搜索转化为连续优化问题。论文将网络参数 θ 与架构参数 α 分离：

```text
架构参数 α
      ↓
决定层数、神经元数量、残差连接
      ↓
权重参数 θ 优化
      ↓
外层更新 α
      ↓
得到离散最优网络
```

方法包含：

1. **连续搜索空间**：借鉴 DARTS，将候选结构松弛为连续权重；
2. **Mask机制**：通过 zero-one mask 模拟不同神经元数量；
3. **Identity operation**：通过跳跃层选择实现网络深度搜索；
4. **双层优化**：内层优化网络权重，外层优化架构参数。论文明确将该过程描述为 bi-level optimization。fileciteturn23file0L227-L236

## 6. Result & Evidence

→ [[wang2024-nas-pinn-results]]

论文测试：

- Poisson equation
- Burgers equation
- Advection equation
- 非规则计算域
- 高维 Burgers 方程

主要发现：

- NAS-PINN 可以找到搜索空间中的有效架构；
- 更深网络并不一定更好；
- Poisson 和 Advection 更偏向浅层宽网络；
- 复杂问题中残差连接可能提升性能。fileciteturn23file0L21-L28

Poisson 方程实验中，NAS-PINN 找到架构误差最低，优于人工架构和 SMAC 搜索结果。fileciteturn23file0L309-L317

## 7. Contribution

1. 首次将 NAS 系统性引入 PINN 网络结构设计；
2. 将层数、神经元数量和残差连接统一纳入搜索空间；
3. 证明不同 PDE 对网络结构具有不同偏好；
4. 提供自动化 PINN architecture design 思路。

## 8. Core Knowledge

- PINN 的性能不仅取决于 loss、采样和优化器，网络表示能力同样重要。
- “更深网络一定更强”在 PINN 中并不成立。
- PDE 类型、复杂度和结构特征决定有效网络形态。
- NAS 可以作为 PINN 自动设计工具，而不是仅用于视觉模型。

## 9. Negative Knowledge

→ [[wang2024-nas-pinn-critical]]

- 搜索仍需要针对特定 PDE 进行，未证明跨 PDE 泛化；
- 架构搜索本身仍增加额外计算成本；
- 搜索空间限制会影响最终结构；
- 没有公开代码，复现需要自行实现。

## 10. Transferable Knowledge

| NAS-PINN机制 | 结构动力 PINN迁移 |
|-|-|
| 自动搜索网络深度 | 根据自由度规模自动调整网络容量 |
| 宽度搜索 | 适配高维结构响应输出 |
| residual layer搜索 | 建立适合长时间动力响应传播的结构 |
| 双层优化 | 自动寻找网络-物理约束组合 |

## 11. Research Opportunity

1. 将 NAS 与结构动力 PINN 结合，搜索适合非线性地震响应的网络；
2. 联合搜索网络结构、损失权重和采样策略；
3. 使用图神经网络 NAS 搜索结构拓扑感知 PINN；
4. 与 [[kolzhetsov2026-rl-adaptive-loss-control-analysis]] 结合，形成自动 PINN solver design。

## 12. Reproducibility

| 项目 | 评价 |
|-|-|
| 等级 | 🟡 中 |
| PDE | Poisson/Burgers/Advection |
| 搜索 | 可微 NAS + mask |
| 优化 | Adam |
| 代码 | 未提供 |
| 数据 | 解析 PDE，可自行生成 |

## 关联页面

- [[wang2024-nas-pinn-method]]
- [[wang2024-nas-pinn-results]]
- [[wang2024-nas-pinn-critical]]
- [[pinn]]
- [[neural-architecture-search]]
