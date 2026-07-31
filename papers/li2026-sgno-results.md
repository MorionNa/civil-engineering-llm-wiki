---
id: papers--li2026-sgno-results
title: SGNO 结果与证据
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
keywords:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
sources:
- sources/papers/li2026-sgno.md
created: '2026-07-31'
updated: '2026-07-31'
confidence: medium
---

# SGNO 结果与证据

## Benchmark Protocol

论文在 APEBench 对齐的一步训练与闭环 rollout 协议上评估 10 个周期 PDE 任务，涵盖耗散、色散、输运和半线性动力。主指标是长时 rollout 的 GMean100，同时报告状态 nRMSE、谱能量、低频能量和相位误差。

## Main Long-Horizon Result

SGNO 在报告的 10 个任务上均取得最低长时误差。相对每个任务最强的非 SGNO 基线，GMean100 比值的中位数为 0.252，即中位误差降低 74.8%。单任务降低幅度约为 13.6%–92.9%，说明收益并非只来自一个特殊方程。

## Error-Growth Evidence

代表性 rollout 曲线显示：

- 在耗散任务中，普通模型可能过度衰减或积累高频噪声；
- 在色散/输运任务中，低一步误差仍可能转化为持续相位漂移；
- 在半线性任务中，错误能量转移会逐步污染频带；
- SGNO 的 carry-correction 结构通常使误差增长更慢。

## Fourier Diagnostics

论文的频谱诊断表明，SGNO 在可计算的任务上通常同时降低：

- 总谱能量误差；
- 低频带能量误差；
- 相位误差。

因此主指标改善并非仅由输出平滑或牺牲高频获得。

## Ablation Results

消融支持三个关键组件：

1. 去除非正生成元约束会增加长期增益漂移；
2. 仅使用稳定 carry 而缺少 correction 会降低非线性表达；
3. 普通残差块不能稳定复现 carry-correction 的综合效果。

## Resolution Extrapolation

论文在二维 Kolmogorov 类任务上补充了分辨率外推：模型在 $64^2$ 训练后，可不重训评估 $128^2$ 和 $256^2$，GMean100 保持相近。这依赖 Fourier 参数化的分辨率兼容性，不代表任意网格/边界均可零样本迁移。

## Efficiency Boundary

SGNO 保持一步 teacher forcing 训练，不需要整段 rollout 反传；但 Fourier transform、复数通道和双路径会增加单步成本。比较应同时报告参数、FLOPs、显存和长时达到同等误差所需成本。

## Interpretation Limits

- 所有核心任务具有周期结构；
- 200/100 步 rollout 证据不能外推为无限稳定；
- 非正 carry 只约束主干，correction 仍可能产生不稳定；
- 复杂几何、非周期边界和路径依赖本构尚未验证。

## Structural-Dynamics Relevance

对结构时程预测，最可迁移的结果是频率分解诊断与稳定主干设计。必须重新验证真实结构频率范围、地震动非平稳性、屈服导致的频率漂移和局部损伤高频成分。

## Related Pages

- [[li2026-sgno-analysis]]
- [[li2026-sgno-method]]
- [[li2026-sgno-critical]]
- [[sgno]]

## Evidence By Source

### `sources/papers/li2026-sgno.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/2602.18801v2.pdf`

^[sources/papers/li2026-sgno.md]
