---
title: "Li et al. (2025) — Functional Scaling Laws：学习率计划下完整损失轨迹的函数型缩放律"
created: 2026-07-28
updated: 2026-07-28
type: paper-analysis
tags: [deep-learning, large-language-model, scaling-law, kernel-regression, stochastic-gradient-descent, learning-rate-schedule, intrinsic-time, compute-optimal-training]
sources: [raw/papers/li2025-functional-scaling-laws.pdf]
methods: [intrinsic-time-sde, functional-scaling-law, power-law-kernel-regression, volterra-integral-equation, learning-rate-schedule-analysis]
results: [full-loss-trajectory-prediction, wsd-scaling-efficiency, llm-loss-curve-transfer, learning-rate-schedule-optimization]
failure_modes: [kernel-surrogate-scope, continuous-time-approximation, asymptotic-constants, unreleased-code-data, unreported-compute-resources]
datasets: [power-law-kernel-simulation, llama-pretraining, qwenmoe-pretraining, gpt2-pretraining]
reproducibility: medium
confidence: high
---

# Functional Scaling Laws in Kernel Regression: Loss Dynamics and Learning Rate Schedules

> **作者：** Binghui Li, Fengling Chen, Zixun Huang, Lean Wang, Lei Wu  
> **会议：** NeurIPS 2025  
> **arXiv：** 2509.19189  
> **一句话定位：** 传统 scaling law 只预测训练结束时的 loss；本文用“内禀时间 + 遗忘核卷积”建立 Functional Scaling Law（FSL），统一描述任意学习率计划下 SGD 的完整损失轨迹，并解释为什么 WSD 通常优于纯衰减和恒定学习率。

## 1. 工程背景 (Engineering Background)

大模型预训练需要在模型规模、数据量、计算预算、峰值学习率与学习率衰减方式之间进行昂贵权衡。Kaplan/Chinchilla 型缩放律能预测最终 loss，却无法回答训练过程中的更直接问题：当前 loss 为什么这样下降、学习率衰减何时开始、不同计划能否在相同预算下互相迁移预测，以及一条训练曲线能否用于设计另一条更优计划。

## 2. Research Gap

现有研究主要有两个空白：

1. **只看终点，不看轨迹：** 传统缩放律把训练过程压缩为最终一步，无法描述 stable phase、decay phase 和噪声消散造成的曲线形状；
2. **学习率计划缺乏统一理论：** 恒定、指数衰减、cosine、WSD、multi-step 等计划通常分别分析或依靠经验选择，缺少可对任意计划共同适用的表达式。

## 3. 科学问题 (Scientific Question)

在具有幂律谱结构的学习问题中，能否把 SGD 的完整期望风险轨迹写成一个统一函数，使模型容量、任务难度、数据/计算预算以及学习率计划的作用彼此可分解，并由此推导不同计划的数据最优与计算最优缩放关系？

## 4. 研究目标 (Research Objective)

作者以 power-law kernel（PLK）回归作为可解析代理，目标是：

- 用内禀时间替代原始迭代步数，统一不同学习率计划的“有效训练进度”；
- 建立适用于一般学习率计划的完整损失轨迹缩放律；
- 推导恒定、指数衰减和 WSD-like 计划的显式数据/计算最优关系；
- 验证该函数形式能否拟合并迁移预测 0.1B–1B LLM 的预训练 loss；
- 通过拟合后的 FSL 反向优化学习率计划。

## 5. 方法机制 (Method & Mechanism)

→ 详见 [[li2025-functional-scaling-laws-method]]

论文先将 one-pass SGD 近似为连续时间 SDE，再定义累计步长形成的内禀时间：

$$t=T(\tau)=\int_0^\tau \phi(r)\,dr.$$

在该坐标下，学习率从漂移项中消失，只通过扩散强度 $\gamma(t)$ 控制随机噪声。核心 FSL 将期望风险分成四部分：

$$
\mathbb E[R(\nu_t)]-\frac{\sigma^2}{2}
\asymp
M^{-s\beta}+e(t)+\int_0^t K(t-z)[e(z)+\sigma^2]\gamma(z)\,dz,
$$

其中 $e(t)=(1+t)^{-s}$ 表示信号学习，$K(t)=(1+t)^{-(2-1/\beta)}$ 是噪声遗忘核，学习率/批大小计划通过卷积函数进入。

## 6. 结果证据 (Result & Evidence)

→ 详见 [[li2025-functional-scaling-laws-results]]

- FSL 能追踪 cosine、WSD-like 和非标准 cyclic 计划下离散 SGD 的完整 risk 轨迹；
- 三种代表性计划的缩放效率排序为 **WSD > 指数衰减 > 恒定学习率**；
- 更高容量模型通常更具数据与计算效率，但也可能更慢遗忘早期注入的噪声；
- 计算最优分配一致倾向于让数据规模增长快于模型规模；
- 在 400M/1B LLaMA 上，仅用 8-1-1 曲线拟合参数，即可预测未见的 cosine 与 WSD 曲线；
- 在 1B QwenMoE、相同 20B token 预算下，FSL 优化得到的计划呈 WSD-like，并取得低于基线的最终 loss。

## 7. 贡献 (Contribution)

1. 将缩放律从“最终标量”提升为“整条损失函数轨迹”；
2. 提出内禀时间坐标，分离确定性信号学习与随机噪声效应；
3. 用遗忘核卷积统一表达任意学习率/批大小计划；
4. 给出恒定、指数衰减与 WSD 在数据受限和计算受限条件下的显式缩放关系；
5. 将理论函数作为 LLM loss surrogate，用于跨计划预测与计划优化。

## 8. 核心知识点 (Core Knowledge)

- **步数不是稳定的训练进度坐标。** 当学习率变化时，累计步长比迭代次数更能代表已经完成的优化工作。
- **学习率计划同时控制“学多久”和“注入多少噪声”。** 降低学习率会抑制新噪声，但也减少可用内禀时间。
- **早期噪声不会立即消失。** 它通过 $K(t-z)$ 对未来 loss 保留记忆，因此计划设计本质上包含噪声注入与遗忘的时间权衡。
- **WSD 的 stable phase 与 decay phase 分工不同。** 前者积累足够内禀时间用于学习，后者降低噪声并促进最终收敛。
- **容量存在双重作用。** 更高容量能加快信号学习，却可能减慢噪声遗忘，不能只用“模型越大越快”概括。

## 9. Negative Knowledge

→ 详见 [[li2025-functional-scaling-laws-critical]]

- 主定理建立在 PLK/核回归、幂律谱和连续时间 SDE 近似上，不是现代 Transformer 非凸训练的严格定理；
- 多个结论是渐近阶意义上的 $\asymp$，隐藏常数决定有限预算下的实际交叉点；
- 一般随机特征扩展主要覆盖 $s\le 1$，更容易任务的差异仍留作未来工作；
- LLM 实验验证了 surrogate 的实用性，但规模仅 0.1B–1B，不能直接外推到超大模型；
- 论文未公开代码/数据，也未报告完整计算资源。

## 10. 可迁移知识 (Transferable Knowledge)

| 机制 | 可迁移方向 |
|---|---|
| 内禀时间 | 比较不同优化器/学习率计划时，用累计有效步长重参数化训练过程 |
| 信号学习 + 噪声记忆分解 | 诊断 PINN、多任务物理损失或结构响应代理训练中的 plateau 与 late-stage improvement |
| 遗忘核 | 为长期依赖的优化噪声建立“何时注入、多久消散”的可解释模型 |
| 轨迹级 surrogate | 用短期或单计划训练曲线预测其他计划，减少完整超参数搜索 |
| stable-then-decay | 在需要长时间学习低频/刚性物理模式的任务中，先保证进度再压低噪声 |

## 11. 研究机会 (Research Opportunity)

以下为基于本文机制的迁移推断，而非论文已经验证的结论：

1. 在高自由度结构动力响应网络中，以模态/图谱分量构造类似 $e(t)$ 与 $K(t)$ 的学习—遗忘诊断；
2. 对 PINN 的方程、初边值、能量与数据损失分别拟合轨迹级 scaling law，识别各任务的有效难度；
3. 将 intrinsic time 用于 Adam/AdamW 的有效步长修正，而不是直接套用 SGD 步数；
4. 用少量训练预算拟合 FSL surrogate，自动搜索 PINN 或神经算子的 warmup、stable 与 decay 比例；
5. 研究非平稳本构、路径依赖和图规模增大时，噪声遗忘核是否出现多时间尺度或非幂律尾部。

## 12. 可复现性 (Reproducibility)

| 项目 | 评价 |
|---|---|
| 等级 | 🟡 中等 |
| 理论 | 假设、定理与证明完整，附录给出 Volterra 方程和缩放推导 |
| PLK 实验 | 参数、重复次数、步数与拟合方式较详细 |
| LLM 实验 | 给出模型规模、token、batch、step、优化流程等关键设置 |
| 代码/数据 | 未公开 |
| 计算资源 | 未报告具体 GPU/时长/总算力 |

## 关联页面

- [[functional-scaling-law]]
- [[li2025-functional-scaling-laws-method]]
- [[li2025-functional-scaling-laws-results]]
- [[li2025-functional-scaling-laws-critical]]
- [[wang2021-pinn-ntk-failure-analysis]]
