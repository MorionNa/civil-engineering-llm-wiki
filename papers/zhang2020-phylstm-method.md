---
id: papers--zhang2020-phylstm-method
title: Zhang et al. (2020) — 方法机制展开
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/paper
- method/pinn
keywords:
- adam-lbfgs
- collocation-strategy
- finite-difference
- multi-lstm
- phylstm2
- phylstm3
- physics-constrained-loss
- physics-informed
- sequence-modeling
- soft-constraint
- tensor-differentiator
- two-phase-optimization
sources:
- sources/papers/zhang2020-phylstm.md
created: '2026-06-10'
updated: '2026-07-31'
confidence: high
methods:
- physics-constrained-loss
- adam-lbfgs
- collocation-strategy
- two-phase-optimization
- soft-constraint
- tensor-differentiator
- finite-difference
- sequence-modeling
---

# Zhang et al. (2020) — 方法机制展开

> 返回概述 → [[zhang2020-phylstm-analysis]]

## 核心思路

将物理定律作为**额外的损失函数项**（软约束，而非硬编码到网络结构中），嵌入多 LSTM 网络的训练目标，弱监督地引导网络学习物理可行的解。

---

## PhyLSTM2（双 LSTM + 微分器，率无关滞回）

### 数据流

```
ag (地震动) → ┌─────────────────────────────────────┐
               │              LSTM1                  │
               │  多层 LSTM + FC                     │
               │  映射: ag → Z = {u, ẇ, r}           │
               └──────────────┬──────────────────────┘
                              │ Z
                              ▼
               ┌─────────────────────────────────────┐
               │       Tensor Differentiator          │
               │  中心有限差分 → Ż = {ẇ, ü, ṙ}        │
               └──────────────┬──────────────────────┘
                              │ (Z, Ż)
                              ▼
               ┌─────────────────────────────────────┐
               │              LSTM2                  │
               │  映射: (Z, Ż) → g                   │
               │  g = 质量归一化非线性恢复力           │
               └─────────────────────────────────────┘
```

### 损失函数

总损失由 1 个数据项 + 3 个物理约束项组成：

**J = Jd + α·Je + β·Jg + γ·Jh**

| 损失项 | 公式含义 | 约束内容 | 所需数据 |
|--------|----------|----------|----------|
| **Jd** | Σᵢ ‖z₁(θ₁) - u_d‖² + ‖z₂(θ₁) - ẇ_d‖² | LSTM1 预测的 u, ẇ 与实测值的 MSE | 标注数据 {ag, u_d, ẇ_d} |
| **Je** | ‖ü + g + Γag‖² | 运动方程残差 → 0 | 仅需 ag（无标签） |
| **Jg** | g 对 Z 的 Lipschitz 连续性 | 恢复力对状态的平滑依赖 | 仅需 ag |
| **Jh** | 滞回本构约束（如 Masing 规则） | 加卸载路径的物理一致性 | 仅需 ag |

### 关键设计

- **θ₁ 是 LSTM1 的可训练参数**（权重+偏置），Jd 直接监督 θ₁
- Je/Jg/Jh 通过微分器连接 LSTM1 和 LSTM2，**反向传播同时更新两个网络**
- r 在训练中**无标注**——由物理损失间接约束其学习
- α, β, γ 是超参数，需手动调整

---

## PhyLSTM3（三 LSTM + 微分器，率相关滞回）

### 数据流

```
ag → [LSTM1] → Z = {u, ẇ, r}
                 ↓
        [Tensor Differentiator]
                 ↓
              Ż = {ẇ, ü, ṙ}
                 ↓
         ┌───────┴───────┐
         ▼               ▼
     [LSTM2]         [LSTM3]
    (Z,Ż) → g       (Z,Ż) → Φ = {∆ẇ, r}ᵀ
         │               │
         └─── 物理一致性 ──┘
```

### 与 PhyLSTM2 的关键区别

| 维度 | PhyLSTM2 | PhyLSTM3 |
|------|----------|----------|
| 网络数 | 2 | **3** |
| 滞回建模 | 隐式（通过 Jh 损失） | **显式**（LSTM3 输出基函数库 Φ） |
| 率相关处理 | 不区分 | **LSTM3 显式建模 ṙ = f(∆ẇ, r)** |
| 额外损失 | — | **JΦ**（基函数库与滞回微分方程一致性） |
| 参数量 | 较少 | 较多 |

### 扩展损失函数

**J = Jd + α·Je + β·Jg + γ·Jh + δ·JΦ**

JΦ 约束 LSTM3 输出的 Φ = {∆ẇ, r}ᵀ 满足滞回微分方程（如 Bouc-Wen 的 ṙ 表达式），使率相关物理被显式编码。

---

## 训练策略

### 两阶段优化

| 阶段 | 优化器 | 学习率 | Epochs | 目的 |
|------|--------|--------|--------|------|
| 预训练 | Adam | 0.001 | 10⁴ | 逃离差局部最优 |
| 精调 | L-BFGS | — | 至收敛 | 高精度收敛 |

### 配点策略（Collocation）

- 额外使用**无标签**地震动样本（仅输入 ag，无输出标注）
- 这些样本只用于计算物理损失 Je/Jg/Jh/JΦ，不参与 Jd
- **不消耗标注数据**即可增强物理约束
- 论文中 Example 1 使用 200 个配点样本

### 数据增强

- 每 epoch 前随机打乱训练/验证集（shuffle）
- 目的：在小数据集下最大化特征学习效率

### 实现框架

- TensorFlow
- 数据格式：3D 数组 [samples, timesteps, features]

---

## 关键设计决策

1. **软约束 > 硬约束：** 物理知识编码为损失项而非网络结构，允许不完整物理知识
2. **有限差分 > 自动微分：** 用于计算状态导数（Ż），引入数值误差但实现简单
3. **物理损失权重需调参：** α/β/γ/δ 对不同问题可能需重新调整
4. **一网络架构：** 多个 LSTM 通过微分器连接，反向传播同时更新所有网络

---

## 关联

- [[zhang2020-phylstm-analysis]] — 论文概述
- [[phylstm2]] — PhyLSTM2 实体页
- [[phylstm3]] — PhyLSTM3 实体页
- [[zhang2020-phylstm-results]] — 结果证据展开

## Evidence By Source

### `sources/papers/zhang2020-phylstm.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/zhang2020-phylstm.md`

^[sources/papers/zhang2020-phylstm.md]
