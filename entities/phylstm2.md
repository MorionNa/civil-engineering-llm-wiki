---
title: "PhyLSTM2 — Physics-informed Double-LSTM Network"
created: 2026-06-10
updated: 2026-06-10
type: entity
tags: [phylstm2, multi-lstm, rate-independent, physics-constrained-loss, tensor-differentiator, soft-constraint, physics-informed, lstm]
sources: [raw/papers/zhang2020-phylstm.md]
methods: [physics-constrained-loss, tensor-differentiator, soft-constraint]
confidence: high
---

# PhyLSTM2 — Physics-informed Double-LSTM Network

## 概述

PhyLSTM2 是一种物理信息引导的**双 LSTM 网络架构**，用于非线性结构系统的 metamodeling（代理建模）。它将物理知识编码为损失函数的约束项，使得网络能在极少训练数据下准确预测结构地震响应，包括不可观测的隐变量。

**首次提出：** Zhang et al., CMAME 2020
**适用场景：** 率无关滞回（rate-independent hysteresis）系统
**GitHub：** https://github.com/zhry10/PhyLSTM

## 架构

```
ag (地震动输入)
  │
  ▼
┌────────────────────────┐
│       LSTM1            │  映射: ag → Z = {u, ẇ, r}
│  (多层 LSTM + FC)      │  输出完整状态空间变量
└───────────┬────────────┘
            │ Z = {u, ẇ, r}
            ▼
┌────────────────────────┐
│  Tensor Differentiator  │  中心有限差分数值微分
│  (Finite Difference)    │  计算 Ż = {ẇ, ü, ṙ}
└───────────┬────────────┘
            │ (Z, Ż)
            ▼
┌────────────────────────┐
│       LSTM2            │  映射: (Z, Ż) → g
│  (多层 LSTM + FC)      │  输出质量归一化非线性恢复力
└───────────┬────────────┘
            │ g
            ▼
      恢复力预测
```

## 损失函数

PhyLSTM2 的总损失由数据项和三个物理约束项组成：

**J = Jd + αJe + βJg + γJh**

| 损失项 | 含义 | 约束内容 |
|--------|------|----------|
| **Jd（数据损失）** | LSTM1 预测与测量值的偏差 | ‖ẑ₁ - u_d‖² + ‖ẑ₂ - ẇ_d‖² |
| **Je（EOM 损失）** | 运动方程残差 | ‖ü + g + Γag‖² |
| **Jg（状态依赖损失）** | 恢复力对状态的连续性 | g 对 Z 的 Lipschitz 约束 |
| **Jh（滞回损失）** | 滞回本构关系 | 如 Masing 规则等 |

## 训练配置

- **优化器：** Adam (lr=0.001, decay=1e-4) → L-BFGS 精调
- **配点样本：** 额外 200 个无标签地震动样本用于计算物理损失
- **数据增强：** 每 epoch 前随机打乱训练/验证集
- **框架：** TensorFlow

## 关键特性

1. **可预测不可观测变量 r 和 g：** 虽然训练时没有 r 和 g 的测量值，物理约束使网络能推断它们
2. **外推能力：** IDA 线性缩放输入，输出非线性响应正确分化
3. **数据高效：** 仅 46 个训练样本即可达到纯 LSTM 需要海量数据才能达到的精度
4. **推理速度：** >10³ 倍于 FEM 仿真

## 适用条件

- ✅ 率无关滞回系统（如钢材 MRF 结构）
- ✅ 已知运动方程的一般形式（不需精确参数）
- ✅ 有少量可观测状态测量数据（u, ẇ）
- ❌ 率相关滞回系统（应使用 [[phylstm3]]）
- ❌ 高维系统（>100 DOF，未验证）

## 关联

- [[zhang2020-phylstm-analysis]] — 论文完整分析
- [[phylstm3]] — 三 LSTM 架构（率相关滞回）
- [[phylstm2-vs-phylstm3-vs-lstm]] — 性能对比
- [[bouc-wen-model]] — Bouc-Wen 滞回模型
