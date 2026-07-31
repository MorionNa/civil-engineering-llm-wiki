---
id: entities--cm-pinns
title: CM-PINNs — Constitutive model-constrained physics-informed neural networks
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- entity/model
- method/pinn
keywords:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- entity/model
- hysteresis
- lstm
- metamodeling
- method/pinn
- physics-informed
- pinn
- restoring-force
- seismic-response
- structural-dynamics
sources:
- raw/papers/wu2025-cm-pinn-extracted.md
created: '2026-07-01'
updated: '2026-07-31'
confidence: high
---

# CM-PINNs

## 定义

CM-PINNs（Constitutive model-constrained physics-informed neural networks）是 Wu et al. (2025) 提出的非线性结构地震响应预测框架。其核心思想是：在 physics-informed 序列模型中，不仅约束运动方程，还把**非线性本构模型计算出的恢复力**作为显式 loss 约束，从而提高少样本下的峰值响应预测和物理可解释性。

## 为什么重要

结构动力响应的非线性常常不是 PDE 算子非线性，而是由材料/构件本构决定的恢复力非线性：

```text
M u_ddot + C u_dot + F_s(u, history) = M Γ a_g
```

如果 $F_s$ 完全由黑箱网络学习，模型可能满足动力平衡但违反材料行为；如果完全依赖固定本构，又难吸收数据中复杂误差。CM-PINNs 用双恢复力机制平衡二者。

## 架构

| 模块 | 作用 |
|---|---|
| FC-SLSTM1 | $a_g \rightarrow Z=\{u,\dot u,r\}$，预测位移、速度、滞回隐变量 |
| CDM | 中心差分计算 $\dot u,\ddot u,\dot r$ |
| FC-SLSTM2 | 从状态 $Z$ 预测数据驱动恢复力加速度 $f_{s1}$ |
| FC-SLSTM3 | 从 $\{\Delta\dot u,r\}$ 预测滞回变量演化 $\dot r$ |
| NLCM/BLCM | 根据本构模型计算物理恢复力加速度 $f_{s2}$ |
| loss | 数据项 + 位移速度一致性 + EOM + 本构一致性 + 滞回演化 |

## 与 PhyLSTM 的关系

CM-PINNs 可看作 `[[zhang2020-phylstm-analysis]]` 的本构显式化扩展：

| 维度 | PhyLSTM | CM-PINNs |
|---|---|---|
| 物理约束 | EOM、状态依赖、滞回损失 | EOM + 状态依赖 + 滞回损失 + 本构恢复力一致性 |
| 主干网络 | 多 LSTM | FC-SLSTM |
| 本构模块 | 不作为独立模块 | NLCM/BLCM 独立计算 $f_{s2}$ |
| 关键收益 | 少样本预测不可观测滞回变量 | 峰值预测与物理解释性进一步提升 |

## 适用场景

- 非线性 SDOF/MDOF 地震响应快速预测；
- 剪切楼层模型、层间位移控制的恢复力模型；
- 已知或可近似的本构关系，如双线性弹塑性、Bouc-Wen、退化滞回；
- 少样本但物理模型明确的结构响应 metamodeling。

## 局限

- 需要可张量化、可反传或至少可嵌入训练图的本构模块；
- 目前验证主要是双线性本构 + BLWN 合成地震动 + 低维剪切模型；
- 对真实 RC 退化、捏拢、局部破坏、大规模结构和噪声数据的泛化仍未充分验证；
- 加速度响应改善弱于位移/速度。

## 关联论文

- [[wu2025-cm-pinn-analysis]] — 原始论文概述
- [[wu2025-cm-pinn-method]] — 方法机制
- [[wu2025-cm-pinn-results]] — 实验结果
- [[wu2025-cm-pinn-critical]] — 批判性分析

## 关联实体

- [[pinn]] — 基础 physics-informed neural network 范式
- [[phylstm2]] / [[phylstm3]] — 直接先导方法
- [[bouc-wen-model]] — 可扩展的率相关滞回本构
- [[pseudo-time-stepping]] — 可组合的 PINN 训练稳定化方法

## Evidence By Source

### `raw/papers/wu2025-cm-pinn-extracted.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/wu2025-cm-pinn-extracted.md]
