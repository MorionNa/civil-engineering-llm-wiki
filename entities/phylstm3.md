---
title: "PhyLSTM3 — Physics-informed Triple-LSTM Network"
created: 2026-06-10
updated: 2026-06-10
type: entity
tags: [phylstm3, multi-lstm, rate-dependent, cross-domain-generalization, physics-constrained-loss, tensor-differentiator, physics-informed, lstm]
sources: [raw/papers/zhang2020-phylstm.md]
methods: [physics-constrained-loss, tensor-differentiator]
results: [cross-domain-generalization]
confidence: high
---

# PhyLSTM3 — Physics-informed Triple-LSTM Network

## 概述

PhyLSTM3 是物理信息引导的**三 LSTM 网络架构**，在 PhyLSTM2 的基础上增加了第三个 LSTM 网络，用于显式建模率相关滞回的微分方程关系。

**首次提出：** Zhang et al., CMAME 2020
**适用场景：** 率相关滞回（rate-dependent hysteresis）系统
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
            │ Z
            ▼
┌────────────────────────┐
│  Tensor Differentiator  │  有限差分 → Ż = {ẇ, ü, ṙ}
└───────────┬────────────┘
            │
     ┌──────┴──────┐
     ▼              ▼
┌──────────┐  ┌──────────┐
│  LSTM2   │  │  LSTM3   │
│ Z,Ż → g  │  │ Z,Ż → Φ  │  Φ = {∆ẇ, r}ᵀ 滞回基函数库
└────┬─────┘  └────┬─────┘
     │              │
     └──────┬───────┘
            ▼
    物理一致性约束
```

## 与 PhyLSTM2 的关键区别

| 维度 | PhyLSTM2 | PhyLSTM3 |
|------|----------|----------|
| LSTM 网络数 | 2 | 3 |
| 滞回建模方式 | 隐式（通过损失函数 Jh 约束） | **显式**（LSTM3 直接建模 ṙ = f(∆ẇ, r)） |
| 基函数库 Φ | 无 | {∆ẇ, r}ᵀ |
| 适用滞回类型 | 率无关 | **率相关** |
| 架构复杂度 | 低 | 高 |

## 损失函数

PhyLSTM3 的总损失扩展为：

**J = Jd + αJe + βJg + γJh + δJΦ**

新增的 JΦ 损失约束 LSTM3 输出的基函数库 Φ 与滞回微分方程（如 Bouc-Wen 模型）的一致性。

## 训练配置

与 PhyLSTM2 相同：
- **优化器：** Adam → L-BFGS 两阶段
- **配点策略：** 额外无标签激励样本用于物理损失
- **框架：** TensorFlow

## 关键性能（Bouc-Wen SDOF 验证）

- 仅 10 个训练样本（BLWN 激励）
- 位移预测最差 γ = 0.77（PhyLSTM2 仅 0.19）
- 恢复力 g 预测 γ ≈ 1.0
- **跨域泛化：** BLWN 训练 → 97 条真实地震记录测试，>95% 样本 γ > 0.9

## 适用条件

- ✅ 率相关滞回系统（如 Bouc-Wen 模型）
- ✅ 滞回本构关系可以微分方程形式表达
- ✅ 跨激励类型泛化（BLWN → 真实地震）
- ❌ 率无关滞回场景下不必要（PhyLSTM2 更简洁且效果相当或更好）
- ❌ 高维系统（>100 DOF，未验证）

## 关联

- [[zhang2020-phylstm-analysis]] — 论文完整分析
- [[phylstm2]] — 双 LSTM 架构（率无关滞回）
- [[phylstm2-vs-phylstm3-vs-lstm]] — 性能对比
- [[bouc-wen-model]] — Bouc-Wen 滞回模型
