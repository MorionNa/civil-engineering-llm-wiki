---
title: "Bouc-Wen Hysteresis Model"
created: 2026-06-10
updated: 2026-06-10
type: entity
tags: [bouc-wen, rate-dependent, hysteresis, sdof, nonlinear-systems, structural-dynamics]
sources: [raw/papers/zhang2020-phylstm.md]
datasets: [blwn, peer-database]
confidence: high
---

# Bouc-Wen Hysteresis Model

## 概述

Bouc-Wen 模型是一种广泛使用的**率相关滞回模型**，用于描述非线性结构/机械系统在循环荷载下的力-位移关系。在 Zhang et al. (2020) 中，Bouc-Wen 模型被用作第二个验证案例，用于测试 PhyLSTM3 对率相关滞回系统的建模能力。

**原始提出：** Bouc (1967), Wen (1976)
**在 PhyLSTM 论文中的用途：** 验证 PhyLSTM3 的率相关滞回建模能力

## 数学形式

对于第 i 个自由度，率相关滞回微分方程为：

$$\dot{r}_i = \Delta\dot{u}_i - \alpha_i |\Delta\dot{u}_i| |r_i|^{n_i-1} r_i - \beta_i \Delta\dot{u}_i |r_i|^{n_i}$$

其中：
- $\Delta\dot{u}_i = \dot{u}_i - \dot{u}_{i-1}$（相对速度，i ≥ 2；i = 1 时 $\Delta\dot{u}_1 = \dot{u}_1$）
- $\alpha_i$, $\beta_i$, $n_i$：非线性参数，控制滞回环的形状
- $r_i$：滞回位移

## PhyLSTM 论文中的参数配置

| 参数 | 取值 |
|------|------|
| m (质量) | 500 kg |
| c (阻尼) | 0.35 kNs/m |
| k (刚度) | 25 kN/m |
| α | 2 |
| β | 2 |
| n | 3 |
| λ (屈服后刚度比) | 0.5 |
| 自然频率 | 1.13 Hz |

- 单自由度（SDOF）系统
- 激励：随机带限白噪声（BLWN），30 s，50 Hz 采样率 → 1501 数据点/条
- 100 条数据：10 条训练/验证（8:2 分割），90 条测试
- 额外 50 个配点样本用于物理损失

## 关键实验结果

- **PhyLSTM3 完美复现滞回曲线**（u-g 曲线，γ ≈ 1.0）
- **PhyLSTM2 严重失效**（最差 γ = 0.19）——架构与物理不匹配
- **跨域泛化成功：** BLWN 训练的 PhyLSTM3 直接预测 97 条真实地震记录响应（>95% γ > 0.9）

## 关联

- [[zhang2020-phylstm-analysis]] — 论文完整分析
- [[phylstm3]] — PhyLSTM3（适用此模型）
- [[phylstm2]] — PhyLSTM2（不适用此模型）
- [[phylstm2-vs-phylstm3-vs-lstm]] — 性能对比
