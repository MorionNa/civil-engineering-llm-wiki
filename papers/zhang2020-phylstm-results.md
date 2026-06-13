---
title: "Zhang et al. (2020) — 结果证据展开"
created: 2026-06-10
updated: 2026-06-10
type: paper-analysis
tags: [mrfs, bouc-wen, rate-independent, rate-dependent, ida, cross-domain-generalization, benchmark, peer-database, blwn, extrapolation-ability, comparison]
sources: [raw/papers/zhang2020-phylstm.md]
results: [cross-domain-generalization, extrapolation-ability]
datasets: [blwn, peer-database]
confidence: high
---

# Zhang et al. (2020) — 结果证据展开

> 返回概述 → [[zhang2020-phylstm-analysis]]

---

## Example 1: 3-story MRF 结构（率无关滞回）

### 实验设置

| 项目 | 详情 |
|------|------|
| 原型 | 3 层钢抗弯框架（MRF），平面尺寸 55m×36.6m |
| 非线性模型 | 集中塑性铰（fiber + force-based beam-column） |
| 前三个模态频率 | 1.02 Hz, 3.61 Hz, 8.32 Hz |
| 阻尼 | Rayleigh 阻尼，前两阶 2% |
| 地震输入 | PEER 数据库，Pomona CA，50年10%超越概率 |
| 选波 | Baker & Lee (2018) 条件谱算法，97 条记录 |
| IDA | 每条地震多级强度缩放 → **806 个输入-输出对** |
| 训练/验证 | 聚类选 7 条地震×IDA = **46 样本**（80/20 分割） |
| 测试 | 90 条地震×IDA = **760 样本** |
| 配点 | 额外 200 个无标签样本用于物理损失 |

### 位移预测

| 指标 | PhyLSTM2 | PhyLSTM3 | LSTM (baseline) |
|------|----------|----------|-----------------|
| 多数样本 γ | > 0.9 | > 0.9 | 分散 |
| **最差 γ** | **0.74** | 0.76 | **0.25** |
| 残余漂移（塑性变形） | ✓ 准确 | ✓ 准确 | ✗ 无法预测 |
| 外推能力（IDA 线性缩放→非线性响应分化） | ✓ | ✓ | ✗ |

> LSTM 虽然峰值和相位尚可，但**无法预测残余漂移**——这说明纯数据驱动学不到滞回塑性行为。

### 速度预测

所有模型都能较好预测速度——速度时间历程无残余漂移，比位移简单。

### 恢复力 g 预测

| 指标 | PhyLSTM2 | PhyLSTM3 | LSTM |
|------|----------|----------|------|
| 可否预测 | ✓ | ✓ | ✗ 不可能 |

> g 在训练中无测量值。物理约束使 PhyLSTM 能推断 g，纯 LSTM 完全无法。

### 关键发现

- **率无关滞回场景：PhyLSTM2 ≈ PhyLSTM3 > LSTM**
- PhyLSTM2 以更简洁架构达到同等效果——证实"架构复杂度应与物理复杂度匹配"
- IDA 缩放验证外推：输入线性缩放，输出非线性正确分化

---

## Example 2: SDOF Bouc-Wen 模型（率相关滞回）

### 实验设置

| 项目 | 详情 |
|------|------|
| 模型 | SDOF Bouc-Wen，m=500kg, c=0.35kNs/m, k=25kN/m |
| 滞回参数 | α=2, β=2, n=3, λ=0.5 |
| 激励 | 随机带限白噪声（BLWN），30s, 50Hz |
| 总数据 | 100 条，每条 1501 点 |
| 训练/验证 | **仅 10 条**（80/20 分割） |
| 测试 | 90 条 |
| 配点 | 50 个无标签 BLWN 样本 |
| 跨域泛化测试 | 97 条真实 PEER 地震记录 |

### 位移预测

| 指标 | PhyLSTM3 | PhyLSTM2 |
|------|----------|----------|
| **最差 γ** | **0.77** | **0.19** |
| 多数样本 γ | > 0.9 | 高度分散 |

> **架构-物理不匹配的代价**：PhyLSTM2 在最差场景几乎完全失效（γ=0.19），而 PhyLSTM3 仍保持可用精度。

### 恢复力 g 预测

| 指标 | PhyLSTM3 |
|------|----------|
| 相关系数 γ | **≈ 1.0** |
| 滞回曲线 (u-g) 复现 | **完美** |

### 跨域泛化（BLWN → 真实地震）

| 指标 | PhyLSTM3 |
|------|----------|
| γ > 0.9 的样本占比 | **> 95%** |
| 最差 γ | 0.79 |

> 用简单随机激励训练，直接预测真实地震记录响应——证明模型学到的是物理规律而非数据分布。

### 推理速度

> **> 10³ 倍于 FEM 仿真**——使 IDA 易损性分析等大规模计算任务变得可行。

### 关键发现

- **率相关滞回场景：PhyLSTM3 >> PhyLSTM2**
- 跨域泛化是物理信息方法的核心优势：学物理 > 学数据
- 即使 10 个训练样本（极度稀缺），PhyLSTM3 仍保持高精度

---

## 汇总

```
率无关滞回 (MRF):     PhyLSTM2 ≥ PhyLSTM3 >> LSTM
率相关滞回 (Bouc-Wen): PhyLSTM3 >> PhyLSTM2 (>> LSTM)
```

## 关联

- [[zhang2020-phylstm-analysis]] — 论文概述
- [[zhang2020-phylstm-method]] — 方法机制展开
- [[phylstm2-vs-phylstm3-vs-lstm]] — 性能对比 + 选型指南
- [[bouc-wen-model]] — Bouc-Wen 模型细节
- [[peer-strong-motion-database]] — PEER 数据库细节
