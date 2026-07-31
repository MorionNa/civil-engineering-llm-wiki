---
id: entities--backlund-transformation-pinn
title: Bäcklund Transformation PINN — 变换约束的双方程物理信息学习
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/computational-mechanics
- entity/model
- method/pinn
keywords:
- ai4s
- deep-learning
- domain/ai4s
- domain/computational-mechanics
- entity/model
- method/pinn
- neural-network
- nonlinear-systems
- physics-informed
- physics-simulation
- pinn
- soft-constraint
sources:
- raw/papers/10_1007_s11071-024-10359-7.pdf
created: '2026-07-16'
updated: '2026-07-31'
confidence: high
methods:
- backlund-transformation
- multi-output-pinn
- relation-constrained-learning
- automatic-differentiation
results:
- two-equation-simultaneous-solution
- unsupervised-target-field-reconstruction
failure_modes:
- nonunique-inverse
- spurious-solution-risk
- loss-weight-imbalance
- no-target-reference-solution
datasets:
- modified-kdv-one-soliton
- modified-kdv-two-soliton
- gaussian-initial-wave
reproducibility: low
---

# Bäcklund Transformation PINN

## 定义

**Bäcklund Transformation PINN** 是把两个非线性 PDE 之间的 Bäcklund 变换写成可微损失项的多输出 [[pinn]]。Li 与 Wang（2025）的实现用同一网络预测 mKdV 解 $u$ 和目标方程解 $v$，只向 $u$ 提供初边值数据，再以两条 PDE 残差与变换残差恢复无标签的 $v$。

## 中心关系

$$u=\sin v-v_x,\qquad BT(u,v)=u-\sin v+v_x=0.$$

该关系由 $v$ 到 $u$ 可直接求值，但由 $u$ 到 $v$ 不是显式唯一映射。因此方法实际求解的是联合约束问题：

$$F(u)=0,\qquad G(v)=0,\qquad BT(u,v)=0,$$

并以 $u$ 的初边界数据锚定解空间。完整损失见 [[li2025-localized-waves-pinn-method]]。

## 与经典 PINN 的区别

| 维度 | 经典 [[raissi2019-pinn-analysis]] | Bäcklund Transformation PINN |
|------|-----------------------------------|-------------------------------|
| 输出 | 单个 PDE 状态 | 两个相互变换的状态 $(u,v)$ |
| 数据 | 目标方程 IC/BC | 只给已知侧 $u$ 的 IC/BC |
| 物理损失 | 一条 PDE 残差 | 两条 PDE + 一个跨方程关系残差 |
| 目标 | 直接求解 PDE | 数值实现不可直接逆用的解析变换 |

## 方法价值

它提供了一个可推广模板：当 Miura、Darboux、Lax 对、守恒律或本构映射连接两个系统，而某一方向不可直接求逆时，可用“已知侧数据 + 双侧方程 + 关系残差”构造可微逆问题。这种贡献位于约束设计层，与 [[wang2024-kinn-analysis]] 的骨干网络设计互补。

## 必要验证

1. 已知侧：报告 $\hat u$ 相对解析/高精度数值解的误差。
2. 关系层：在独立验证网格上报告 $BT(\hat u,\hat v)$。
3. 目标侧：用独立数值方法验证 $\hat v$，而非只报告训练残差。
4. 多解性：改变初始化、采样和权重，检查是否得到不同但同样低残差的 $v$。
5. 复杂度：从单波到多波报告迭代数、耗时和误差增长。

## 已知局限

- 软 BT 约束不能保证严格满足变换，更不能证明逆解唯一。
- 同时平衡数据、两条 PDE 和关系残差，容易出现梯度量级不匹配。
- 目标侧无真值时可能出现 [[wang2023-pinn-spurious-analysis]] 所述的低残差伪解。
- Li 与 Wang（2025）未公开代码或权重更新规则，方法目前难以逐数值复现。

## 来源论文

- [[li2025-localized-waves-pinn-analysis]] — 12 维度总览
- [[li2025-localized-waves-pinn-results]] — 单波、双波与 Gaussian 证据
- [[li2025-localized-waves-pinn-critical]] — 证据边界与研究路线

## Evidence By Source

### `raw/papers/10_1007_s11071-024-10359-7.pdf`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/10_1007_s11071-024-10359-7.pdf]
