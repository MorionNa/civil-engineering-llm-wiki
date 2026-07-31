---
id: entities--causal-training
title: Causal Training — 因果训练 (PINN 时域训练范式)
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- entity/model
- method/neural-operator
- method/pinn
keywords:
- ai4s
- deep-learning
- domain/ai4s
- entity/model
- method/neural-operator
- method/pinn
- physics-informed
- pinn
- time-marching
sources:
- raw/papers/10_1016_j_cma_2024_116813_extracted.txt
- raw/papers/10_1016_j_jcp_2026_115071_extracted.txt
created: '2026-06-27'
updated: '2026-07-31'
confidence: high
---

# Causal Training — 因果训练 (PINN 时域训练范式)

## 定义

因果训练 (Causal Training) 是由 Wang et al. (2024) 提出的一种 PINN 训练范式，核心思想是**在损失函数中显式编码物理系统的时空因果结构**，使网络严格按照时间顺序学习 PDE 解——先学好早期动力学，再逐步推进到后期——从而消除标准 PINN 中"先猜未来再反推过去"的根本性错误。

## 核心机制

标准 PINN 同时优化全部时空点的 PDE 残差，网络的梯度更新不受时间方向的约束——它可以在 $t=T$ 处先降低残差，再"回填" $t=0$ 附近的解。

因果训练通过**因果权重**重写损失函数：

$$w_i = \exp\left(-\epsilon \sum_{k=1}^{i-1} \mathcal{L}_k\right), \quad \mathcal{L}_{causal} = \frac{1}{M}\sum_{i=1}^{M} w_i \mathcal{L}_i$$

- $t_1$ 的权重始终为 1 → 网络先学初始动力学
- $t_i$ 的权重由之前时间片的残差累积决定 → 只有前面学好了，后面的权重才被激活
- 权重演化天然构成训练的"物理进度条"

## 历史脉络

| 时间 | 事件 |
|------|------|
| 2021 | Wang et al. 发现 PINN 训练的 NTK 谱偏差（梯度不平衡） |
| 2023 | Wang et al. 发现 PDE 残差 loss 的伪解问题（loss 小 ≠ 解正确） |
| **2024** | **Wang et al. 提出因果训练——诊断因果违反为最根本的失败根因** |
| 2025 | Li et al. 将因果训练迁移到桥梁动力学的移动荷载 PINN |
| **2026** | **Zhao et al. 提出 Causal Attention (CA)——用初始条件误差替代累积残差驱动因果权重，实现采样解耦 + 免退火** |

## 与相关方法的关系

| 方法 | 解决的问题 | 层次 |
|------|-----------|:---:|
| NTK 自适应退火 (2021) | 各损失项的梯度不平衡 | 收敛速率 |
| 伪时间步进 (2023) | PDE 残差 loss 接受伪解 | 解的正确性 |
| **因果训练 (2024)** | **时空因果结构违反** | **信息传播方向** |

三者互补——因果训练解决"信息往哪流"的问题，NTK 退火解决"流得是否均衡"，伪时间步进解决"稳态是否收敛到正确解"。

## 关键特征

1. **极简实现：** 仅修改损失函数，不改网络架构
2. **自动推进：** 无需指定时间片何时被激活，因果权重自动根据残差收敛状态推进
3. **内置诊断：** 因果权重的演化提供了比传统 loss 曲线更可靠的训练状态信号
4. **混沌突破：** 首次使 PINN 成功模拟 Lorenz 吸引子、KS 时空混沌等此前不可能的系统

## 工程应用

- **桥梁动力学：** [[li2025-movingload-pinn-analysis|Li et al. (2025)]] 使用因果权重处理桥梁移动荷载时域响应
- **流体力学：** 混沌/湍流系统的 PINN 仿真
- **传播到其他时序范式：** 因果训练思想可推广到 DeepONet、PhyLSTM 等时序物理模型

## 关联论文（本 Wiki）

- [[wang2024-causal-pinn-analysis]] — 因果训练 PINN 论文分析总览
- [[wang2024-causal-pinn-method]] — 因果训练方法展开
- [[wang2024-causal-pinn-results]] — 因果训练实验结果
- [[wang2024-causal-pinn-critical]] — 贡献 / Negative / 可迁移 / 研究机会
- [[zhao2026-causal-attention-analysis]] — **Causal Attention (CA)** — 新一代因果加权（采样解耦 + 免退火）
- [[causal-attention]] — CA 实体页
- [[wang2021-pinn-ntk-failure-analysis]] — 同作者 (2021) NTK 谱偏差
- [[wang2023-pinn-spurious-analysis]] — 同作者 (2023) 伪时间步进
- [[li2025-movingload-pinn-analysis]] — 因果训练在结构动力学中的工程应用
- [[pinn]] — PINN 实体

## Evidence By Source

### `raw/papers/10_1016_j_cma_2024_116813_extracted.txt`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/10_1016_j_cma_2024_116813_extracted.txt]
