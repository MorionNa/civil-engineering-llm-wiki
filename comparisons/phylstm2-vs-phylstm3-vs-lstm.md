---
id: comparisons--phylstm2-vs-phylstm3-vs-lstm
title: PhyLSTM2 vs PhyLSTM3 vs LSTM — Performance Comparison
type: comparison
status: active
project: civil-engineering-llm-wiki
tags:
- method/evaluation
keywords:
- architecture-selection
- benchmark
- comparison
- lstm
- phylstm2
- phylstm3
- rate-dependent
- rate-independent
sources:
- raw/papers/zhang2020-phylstm.md
created: '2026-06-10'
updated: '2026-07-31'
confidence: high
results:
- cross-domain-generalization
- extrapolation-ability
failure_modes:
- architecture-mismatch-failure
---

# PhyLSTM2 vs PhyLSTM3 vs LSTM — 性能对比

> 基于 Zhang et al. (2020) 两个验证案例的数据。

## 架构对比

| 维度 | LSTM (baseline) | PhyLSTM2 | PhyLSTM3 |
|------|-----------------|----------|----------|
| 网络数 | 1 | 2 + 微分器 | 3 + 微分器 |
| 物理约束 | ✗ 无 | ✓ EOM + 状态依赖 + 滞回 | ✓ EOM + 状态依赖 + 滞回微分方程 |
| 可预测 r（滞回参数） | ✗ | ✓ | ✓ |
| 可预测 g（恢复力） | ✗ | ✓ | ✓ |
| 参数解释性 | 黑箱 | 有物理意义 | 有物理意义 |
| 训练数据需求 | 高 | 低 | 低 |

## Example 1: 3-story MRF（率无关滞回）

训练数据：46 样本 | 测试数据：760 样本

### 位移预测

| 指标 | PhyLSTM2 | PhyLSTM3 | LSTM |
|------|----------|----------|------|
| 多数样本 γ | **> 0.9** | > 0.9 | 分散 |
| 最差 γ | **0.74** | 0.76 | 0.25 |
| 残余漂移预测 | ✓ | ✓ | ✗ |
| 外推能力 | ✓ | ✓ | ✗ |

### 速度预测

| 指标 | PhyLSTM2 | PhyLSTM3 | LSTM |
|------|----------|----------|------|
| 准确度 | 优 | 优 | 可接受 |

> 速度时间历程相对简单（无残余），纯 LSTM 也能较好预测。

### 恢复力 g 预测

| 指标 | PhyLSTM2 | PhyLSTM3 | LSTM |
|------|----------|----------|------|
| 可否预测 | ✓ | ✓ | ✗ 不可能 |

> 恢复力在训练中无测量值，纯 LSTM 完全无法建模。

### 结论（率无关）

**PhyLSTM2 ≈ PhyLSTM3 > LSTM**。PhyLSTM2 以更简洁的架构达到同等或略优效果。

---

## Example 2: SDOF Bouc-Wen（率相关滞回）

训练数据：10 样本 | 测试数据：90 样本

### 位移预测

| 指标 | PhyLSTM3 | PhyLSTM2 | LSTM |
|------|----------|----------|------|
| 最差 γ | **0.77** | 0.19 | — |
| 多数样本 γ | > 0.9 | 分散 | — |

### 跨域泛化（BLWN → 真实地震 97 条）

| 指标 | PhyLSTM3 |
|------|----------|
| γ > 0.9 的样本比例 | **> 95%** |
| 最差场景 | γ = 0.79 |

### 恢复力 g 预测

| 指标 | PhyLSTM3 |
|------|----------|
| γ | **≈ 1.0** |
| 滞回曲线复现 | 完美 |

### 结论（率相关）

**PhyLSTM3 >> PhyLSTM2**。架构与物理不匹配导致 PhyLSTM2 严重失效。

---

## 总判决

```
率无关滞回:  PhyLSTM2 ≥ PhyLSTM3 >> LSTM
率相关滞回:  PhyLSTM3 >> PhyLSTM2 ( >> LSTM)
```

### 选型指南

| 场景 | 推荐架构 | 理由 |
|------|----------|------|
| 率无关滞回 + 追求简洁 | PhyLSTM2 | 更少参数，效果相当或更好 |
| 率相关滞回 | **PhyLSTM3** | PhyLSTM2 会严重失效 |
| 不确定滞回类型 | PhyLSTM3 | 更通用，容错性高 |
| 数据极度稀缺（<20 样本） | PhyLSTM3 | 物理约束更强 |
| 纯数据驱动 baseline | LSTM | 无物理知识时的下限参考 |

## 关联

- [[zhang2020-phylstm-analysis]] — 论文完整分析
- [[phylstm2]] — PhyLSTM2 架构
- [[phylstm3]] — PhyLSTM3 架构
- [[bouc-wen-model]] — Bouc-Wen 滞回模型

## Evidence By Source

### `raw/papers/zhang2020-phylstm.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/zhang2020-phylstm.md]
