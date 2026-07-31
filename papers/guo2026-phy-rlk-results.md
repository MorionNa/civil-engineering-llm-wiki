---
id: papers--guo2026-phy-rlk-results
title: Guo & Xu (2026) Phy-RLK 结果：双向 RC 框架响应与峰值误差
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
- method/pinn
- method/transformer
keywords:
- comparison
- finite-element
- ground-motion
- lstm
- neural-network
- nonlinear-systems
- physics-informed
- seismic-response
- structural-dynamics
- synthetic-data
sources:
- sources/papers/guo2026-phy-rlk.md
created: '2026-07-16'
updated: '2026-07-31'
confidence: high
methods:
- physical-residual-lstm
- kan-decoder
- opensees-nltha
- srm-ground-motion
results:
- global-response-metrics
- peak-displacement-error
- pga-robustness
- cross-structure-validation
- inference-speedup
failure_modes:
- synthetic-label-dependence
- timing-inconsistency
- no-real-world-validation
datasets:
- srm-bidirectional-ground-motions
- opensees-six-story-rc-frame
- opensees-five-story-rc-frame
reproducibility: low
contested: false
---

# 结果展开：两类 RC 框架的全时程与峰值响应

> 返回概述 → [[guo2026-phy-rlk-analysis]]；方法 → [[guo2026-phy-rlk-method]]

## 6.1 对照设计

| 模型 | 物理残差 LSTM | 解码器 |
|------|:-------------:|--------|
| LSTM | 否 | MLP/线性输出 |
| Transformer | 否 | attention-based |
| Phy-RL | 是 | MLP |
| **Phy-RLK** | **是** | **KAN** |

LSTM/Transformer → Phy-RL 衡量架构内物理残差的增益，Phy-RL → Phy-RLK 衡量 KAN 解码器的增益。

## 6.2 算例 1：六层 RC 框架

六层框架使用位移型纤维梁柱；混凝土为 Concrete01，纵筋为 Steel01。10 个 PGA 水平（0.1–1.0 g）分别用 OpenSees NLTHA 生成标签。

### 全局指标

| 模型 | Acc. $R^2$ | Vel. $R^2$ | Disp. $R^2$ |
|------|------------:|------------:|-------------:|
| LSTM | 0.802 | 0.806 | 0.735 |
| Transformer | 0.683 | 0.654 | 0.689 |
| Phy-RL | 0.854 | 0.861 | 0.845 |
| **Phy-RLK** | **0.921** | **0.919** | **0.896** |

Phy-RLK 的对应 MSE 为 0.022/0.041/0.064，低于 Phy-RL 的 0.052/0.096/0.155。作者汇总其相对纯数据模型的 MSE/RMSE/MAE 降幅为 65.6%–93.1%；加速度 MSE 相对纯数据方法最高降 93.1%，位移 MSE 降 83.8%。

### KAN 消融

相对 Phy-RL，论文报告 KAN 使平均预测精度提升 9.2%，位移 MSE 降低 58.7%，速度 RMSE 降低 49.2%，位移 $R^2$ 提高 7.8%。这些数字按指标采用不同相对分母，不应简单相加；结论章节另报加速度/速度/位移精度提升 7.8%/7.5%/6.7%。

### 峰值位移

| 模型 | 峰值位移误差（均值 ± 离散） |
|------|-----------------------------:|
| Transformer | 0.222 ± 0.204 |
| LSTM | 0.199 ± 0.188 |
| **Phy-RLK** | **0.074 ± 0.077** |

Phy-RLK 的 IQR 为 0.084；相对 LSTM，95% 误差区间由 0.717 收窄至 0.295。该结果支持其在局部峰值 EDP 上比全数据模型更稳。

## 6.3 算例 2：五层 RC 框架

五层框架采用 Steel02、Concrete01 与节点区 Pinching4，考虑循环硬化、约束/非约束混凝土及节点区退化；15 个强度级覆盖 0–1.5 g。相同网络架构和参数直接用于该算例，但模型仍在该结构数据上训练，不能解释为零样本跨结构迁移。

| 模型 | Acc. $R^2$ | Vel. $R^2$ | Disp. $R^2$ |
|------|------------:|------------:|-------------:|
| LSTM | 0.783 | 0.804 | 0.790 |
| Transformer | 0.561 | 0.759 | 0.845 |
| Phy-RL | 0.861 | 0.872 | 0.890 |
| **Phy-RLK** | **0.932** | **0.944** | **0.959** |

Phy-RLK 的 MSE 为 0.067/0.014/0.066，所有 PGA 水平的三类响应 $R^2>0.89$。峰值位移误差均值为 0.054，低于 LSTM 的 0.16 和 Transformer 的 0.11；97.5 百分位为 0.19，低于 0.53/0.33。

## 6.4 计算效率

| 算例 | 训练 | 单次 Phy-RLK | 单次 OpenSees | 可审计表述 |
|------|------|--------------|----------------|------------|
| 六层 | 约 6000 s（文中另称 6 s/epoch × 1500） | `<50 ms` | 约 1200 s | 作者自报约 2400×；原始时间与倍数不一致 |
| 五层 | 约 1.5 h | 约 1 s | 约 2000 s | 约 2000×，即约 3.3 个数量级 |

论文在五层算例使用“thousands of orders of magnitude”，这是明显措辞错误；正确含义是**千倍量级**，不是“数千个数量级”。六层算例的 `<50 ms` 与 1200 s 若直接相除也不等于 2400，需原始测速脚本确认。

## 6.5 证据能支持的结论

1. 在两套 OpenSees RC 框架和人工双向地震动上，Phy-RLK 的全局与峰值指标均优于三个对照；
2. Phy-RL 消融支持 residual LSTM 有效，Phy-RLK 消融支持 KAN 进一步有效；
3. 同一超参数配置在第二种结构上仍表现较好，说明配置具有一定稳健性；
4. 证据尚不支持真实地震/实测数据泛化、结构零样本迁移、概率可靠性或替代 NLTHA 的普遍安全性。

## 6.6 数据质量提醒

- 五层结构正文称“across five floors”却列出 6 个最小 testing MSE（0.024、0.028、0.025、0.031、0.036、0.022），需要原始表或代码澄清；
- 六层训练“6 s/epoch × 1500 epochs”与“约 6000 s”不一致；
- 所有结果以归一化响应评价，工程量纲下的绝对误差需进一步核查。

## 页内导航

- [[guo2026-phy-rlk-analysis|← 概述]]
- [[guo2026-phy-rlk-method|← 方法]]
- [[guo2026-phy-rlk-critical|批判分析 →]]
- [[phy-rlk]] — 模型实体

## Evidence By Source

### `sources/papers/guo2026-phy-rlk.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/10_1016_j_cma_2025_118422.xml`

^[sources/papers/guo2026-phy-rlk.md]
