---
id: entity--qpinn-rar
title: QPINN-RAR — Residual adaptive quantum physics-informed neural network
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- method/pinn
- entity/model
- evidence/paper
keywords:
- quantum-pinn
- parametrized-quantum-circuit
- residual-based-adaptive-refinement
- adaptive-collocation
sources:
- sources/papers/li2026-qpinn-rar.md
created: '2026-08-06'
updated: '2026-08-06'
confidence: high
---

# QPINN-RAR

## 定义

QPINN-RAR 是 Li 等提出的混合量子—经典物理信息网络：以参数化量子线路替代经典 PINN 的中部隐藏模块，并在训练过程中使用残差自适应加点，把新的配置点集中到当前 PDE 残差较大的区域。^[sources/papers/li2026-qpinn-rar.md]

## 核心组成

- 两层、每层 20 个 Tanh 神经元的经典前处理网络；
- 五量子比特参数化量子线路，包含 angle embedding、$R_X/R_Z$ 旋转门和纠缠操作；
- 对称的经典后处理网络；
- 初值、边界与控制方程残差组成的物理损失；
- [[residual-based-adaptive-refinement]]；
- Adam 训练后使用 L-BFGS 精修。

## 论文中的角色

该实体用于区分四个实验对象：PINN、PINN-RAR、QPINN 与 QPINN-RAR。QPINN-RAR 同时改变中部函数逼近模块和配置点分布，因此其结果不能仅归因于量子线路；论文中的 PINN-RAR 与 QPINN 对照分别用于观察自适应采样和量子模块的影响。

## 证据摘要

论文报告 QPINN-RAR 在三个表格算例中取得最低平均相对 $L_2$ 误差，并将参数量从经典基线的 2128/2221 降至 1186/1226，约减少 44%。这些结果来自 PennyLane/PyTorch 混合实现和十次独立运行，不包含真实量子硬件或墙钟加速证据。

## 证据边界

- 未验证真实量子硬件的噪声、退相干、有限 shots 和门误差；
- 未报告端到端训练时间、量子模拟成本或能耗；
- 三个算例均为固定 PDE 与解析解同分布评价；
- 论文第二个算例的显示方程、名称和解析解存在一致性疑问；
- 参数量更少不能解释为已经获得量子计算优势。

## 项目角色

对结构动力研究，当前最有价值的是 RAR 的残差反馈采样思想。量子线路应作为待验证的低参数逼近器，与同参数量 MLP、Fourier 特征、KAN 和神经算子在统一计算预算下比较。

## 关联页面

- [[li2026-qpinn-rar-analysis]]
- [[li2026-qpinn-rar-method]]
- [[li2026-qpinn-rar-results]]
- [[li2026-qpinn-rar-critical]]
- [[residual-based-adaptive-refinement]]
- [[pinn]]
