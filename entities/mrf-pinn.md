---
title: "MRF-PINN — Multi-Receptive-Field Physics-Informed Neural Network"
created: 2026-07-16
updated: 2026-07-16
type: entity
evidence_scope: abstract-only
tags: [neural-network, physics-informed, deep-learning, finite-difference, physics-constrained-loss, soft-constraint, adaptive-weighting, nonlinear-systems, multi-scale-context, pinn, ai4s, physics-simulation, limitation]
sources: [raw/papers/extracted/10_1007_s00466-024-02554-5_abstract_extracted.txt]
methods: [multi-receptive-field-convolution, taylor-virtual-node-padding, high-order-finite-difference, dimensional-balance-loss-weighting]
results: [multi-scale-feature-extraction, elliptic-pde, parabolic-pde, hyperbolic-pde, navier-stokes]
failure_modes: [below-fem-fvm-competitiveness, finite-difference-discretization-error, abstract-only-evidence, unverified-architecture, missing-code]
datasets: []
reproducibility: low
code_url: []
dataset_url: []
confidence: medium
---

# MRF-PINN

> **证据范围：ABSTRACT ONLY（仅出版社摘要）**
> 本实体记录的是摘要可确认的模型轮廓；所有实现细节均待全文核验。

## 定义

**MRF-PINN（Multi-Receptive-Field Physics-Informed Neural Network）** 是 Zhang 等（2025）提出的卷积型 [[pinn]]。其核心思路是以多个感受野提取 PDE 解的多尺度特征，再通过物理损失训练。

## 摘要确认的组成

```text
PDE field/grid
    └─► multiple receptive fields ─► multi-scale representation
             ├─► Taylor virtual-node padding at boundaries
             ├─► high-order finite differences for spatial derivatives
             └─► dimensional-balance weighting for physics losses
```

| 模块 | 可确认作用 | 尚未核实 |
|------|------------|----------|
| 多感受野卷积 | 捕获不同尺度特征 | 感受野数量、卷积核、层数、融合结构 |
| Taylor 虚拟节点 | 为边界附近高阶差分补点 | Taylor 阶数、边界条件实现 |
| 高阶有限差分 | 计算空间导数 | 阶数、误差、稳定性与网格要求 |
| dimensional balance | 调节不同损失项权重 | 公式、静态/动态方式、调参范围 |

## 已知验证范围

摘要称模型用于椭圆、抛物、双曲 PDE 和 Navier–Stokes。Navier–Stokes 属于 PDE 算子非线性验证，不能推导出 MRF-PINN 已验证材料本构非线性。

作者定性报告其精度/收敛优于部分 MLP-PINN 与 UNet-PINN，但同时明确指出，其精度和计算成本竞争力仍不及传统 FEM/FVM。数字、统计显著性和具体算例需见全文；参见 [[zhang2025-mrf-pinn]]。

## 方法定位

- 相对普通 MLP-PINN：通过卷积和多感受野增强多尺度空间表达。
- 相对纯 AD PINN：空间导数采用高阶有限差分，因此带有显式离散误差与边界闭合问题。
- 相对 FEM/FVM：目前是研究型神经 PDE 求解器，尚未在精度/成本上替代传统方法。
- 相对综述中的其他增强方法：可在 [[luo2025-pinn-pde-review-analysis]] 中作为“架构 + 数值微分 + 损失平衡”组合路线定位。

## 待全文核验清单

1. 网络层数、通道数、卷积核和多感受野融合方式。
2. Taylor 展开与高阶差分的具体阶数、边界条件和误差分析。
3. dimensional-balance 权重公式及是否随训练更新。
4. 训练点/网格、优化器、停止准则与随机种子。
5. 各 PDE 的参数、误差数字、消融、FEM/FVM 成本对比。
6. 官方代码、数据、许可证和运行环境。

## 关联页面

- [[zhang2025-mrf-pinn]] — 摘要级论文概览
- [[pinn]] — PINN 基础实体
- [[luo2025-pinn-pde-review-analysis]] — PDE-PINN 方法综述
