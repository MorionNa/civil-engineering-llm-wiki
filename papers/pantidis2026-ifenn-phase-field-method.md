---
id: paper--pantidis2026-ifenn-phase-field-method
title: "Pantidis et al. (2026) — PICNN-IFENN 相场断裂方法机制"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
keywords:
- at2-phase-field
- ifenn
- laplacian-convolution
- staggered-solver
- symmetric-kernel
sources:
- sources/papers/pantidis2026-ifenn-phase-field.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
evidence_scope: full-text
---

# 方法机制

## 总体数据流

```text
快速 FEM 单缺口分析
  → 提取两个传播增量的 Gauss 点历史变量 H
  → H 像素化
  → 对称 PICNN 预测 φ
  → 固定卷积模板计算 ∇²φ
  → 最小化相场 PDE 残差
  → 在线 IFENN：FEM 平衡 ↔ PICNN 相场，迭代至收敛
```

## 相场基线

论文采用 AT2 脆性相场模型。位移场由力学平衡控制，相场由包含断裂韧度、长度尺度、Laplacian 和历史变量 $H$ 的椭圆 PDE 控制。$H$ 保存过去最大拉伸应变能密度，以保证裂纹不可逆。^[sources/papers/pantidis2026-ifenn-phase-field.md]

## IFENN 分工

传统 FEM 继续求解机械平衡，PICNN 替代传播阶段的相场 PDE。每个增量内依次：求位移与 $H$、将 Gauss 点 $H$ 重排为像素矩阵、预测 $\phi$、映射回 Gauss 点、检查收敛。两个求解器互相交换字段。

## 无时序空间耦合

[[concepts/spatial-coupling-without-temporal-features]] 把路径依赖主要交给历史变量 $H$，网络只学习局部空间映射 $H\mapsto\phi$。因此网络不需要固定长度序列，也不依赖在线载荷步数量。

## Gauss 点到像素

均匀一阶方形单元使 Gauss 点与像素中心近似一一对应，避免额外的 $L^2$ 投影。输入尺寸可随网格改变，因为网络完全由卷积层构成，没有池化、展平或全连接层。

## PICNN 架构

网络含四层对称卷积：前三层后接 Tanh，最后一层接 Sigmoid，使 $\phi\in[0,1]$。各层使用 $5\times5$ 双反射对称核，将每个核的独立参数由 25 个降为 6 个，并形成 90° 旋转对称性。

## 物理损失

[[concepts/physics-informed-laplacian-convolution]] 用固定 9 点卷积模板近似 $\nabla^2\phi$。损失是相场强式残差的二范数，不需要相场标签；训练使用 Adam。

## 在线稳定化细节

- 对输入 $H$ 截断，避免推理范围超出训练域；
- 同时对 $H$ 和 $\phi$ 强制不可逆；
- 对预测 $\phi$ 使用 Gaussian 平滑，补偿网络倾向产生较窄裂纹；
- 先由 FEM 完成起裂阶段，再在传播阶段激活 IFENN。

## 训练配置

训练算例为 $1\times1$ mm 单缺口拉伸域、40000 单元。仅使用增量 300 和 310 的 $H$ 场，训练 10000 epochs，学习率 $10^{-4}$，在 GTX 1650 Ti 笔记本上约 5 min。

## 适用边界

当前像素映射要求矩形域和均匀结构化网格；卷积不显式编码 $l_c$，主要学习像素尺度的裂纹宽度。当前网络主要覆盖传播阶段和 Mode-I 路径。

## 关联页面

- [[pantidis2026-ifenn-phase-field-analysis]]
- [[pantidis2026-ifenn-phase-field-results]]
- [[pantidis2026-ifenn-phase-field-critical]]
- [[entities/picnn-ifenn-phase-field]]
