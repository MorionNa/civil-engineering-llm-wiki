---
id: entities--phy-rlk
title: Phy-RLK — Physical Residual LSTM-KAN
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
- equation-of-motion
- ground-motion
- lstm
- method/pinn
- neural-network
- nonlinear-systems
- physics-informed
- restoring-force
- seismic-response
- sequence-modeling
- structural-dynamics
sources:
- raw/papers/10_1016_j_cma_2025_118422.xml
created: '2026-07-16'
updated: '2026-07-31'
confidence: high
contested: false
---

# Phy-RLK

## 定义

Phy-RLK（Physical Residual LSTM-KAN）是 Guo & Xu (2026) 提出的双向地震结构响应监督代理。它把 Newmark-β 推导的加速度、速度和位移残差加入 LSTM 的 cell state 与 output gate，再以 KAN 解码时序隐特征，输出各楼层两个方向的加速度、速度和位移。

原始论文：[[guo2026-phy-rlk-analysis]]。

## 核心架构

```text
[ag_x(t), ag_y(t)]
  → physical residuals Ra, Rv, Ru
  → 3 × modified LSTM cells
  → bidirectional latent sequences
  → floor/direction-specific KAN decoders
  → [a, v, u] for every floor and direction
```

| 模块 | 作用 |
|------|------|
| Newmark-β residual | 检查预测状态与离散动力/运动学更新的偏差 |
| residual LSTM | 把偏差直接加入长期状态和输出通路 |
| KAN decoder | 用可学习 B-spline 映射提炼非线性响应特征 |
| data loss | 监督拟合 OpenSees 的 $u,\dot u,\ddot u$；没有单独 physics loss |

## 物理定位

Phy-RLK 处理的是**材料本构/结构动力非线性**：训练标签来自使用 Concrete01、Steel01/02、Pinching4 和纤维梁柱的 OpenSees NLTHA。它不求解非线性 PDE，也没有把这些材料本构直接写进网络；内嵌的是 Newmark-β 残差。

## 与前序模型的关系

| 模型 | 物理注入位置 | 本构处理 | 训练信号 |
|------|--------------|----------|----------|
| [[phylstm2]] | EOM/状态依赖 loss | 隐式恢复力 | 数据 + physics loss |
| [[phylstm3]] | EOM/滞回演化 loss | 显式滞回隐变量 | 数据 + physics loss |
| [[cm-pinns]] | EOM + 本构一致性 loss | 独立本构模块 | 数据 + 多 physics loss |
| Phy-RL | LSTM state/output 内部 | Newmark 残差 | data loss only |
| **Phy-RLK** | LSTM state/output + KAN | Newmark 残差；KAN 解码 | data loss only |

与 [[bouc-wen-model]] 不同，本论文使用更细致的 RC 构件材料模型生成标签，但没有学习或显式输出统一的滞回状态变量。

## 训练配置

- hidden size 64，三层 residual LSTM；
- residual activation=tanh；
- Adam，learning rate 0.001，batch size 16；
- sequence length 1500，最多 1500 epochs，patience 20；
- 输入输出 MinMax 到 $[-1,1]$；
- 双向 SRM 人工地震动，OpenSees NLTHA 标签。

## 关键证据

- 六层 RC：$R^2=0.921/0.919/0.896$（加速度/速度/位移）；
- 五层 RC：$R^2=0.932/0.944/0.959$；
- 六层峰值位移误差 $0.074\pm0.077$；
- 推理为毫秒—秒级，OpenSees 为千秒级，但论文的具体加速倍数存在算术不一致。

完整数据见 [[guo2026-phy-rlk-results]]。

## 适用场景

- 固定结构模型下的大批量双向地震响应快速重建；
- 需要同步获得楼层加速度、速度、位移和峰值 EDP；
- OpenSees 数据已生成、需要替代重复 NLTHA 的场景；
- 易损性分析前端代理，但需先补充概率校准。

## 局限

- 仍依赖大量结构专属 OpenSees 标签；
- 没有真实记录/实测结构外部验证；
- 物理残差未作为独立指标验证；
- 无公开代码和数据；
- 不确定度和跨结构 zero-shot 泛化尚未证明；
- KAN 配置、$F_{mrf}$ 接口和计时口径披露不足。

## 关联页面

- [[guo2026-phy-rlk-method]] — 残差门控与训练细节
- [[guo2026-phy-rlk-results]] — 两个 RC 框架结果
- [[guo2026-phy-rlk-critical]] — 证据与泛化边界
- [[kin]] — KAN 用于 physics-informed 学习的另一条路线

## Evidence By Source

### `raw/papers/10_1016_j_cma_2025_118422.xml`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/10_1016_j_cma_2025_118422.xml]
