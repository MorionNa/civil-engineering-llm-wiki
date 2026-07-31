---
id: papers--song2025-rl-pinns-results
title: RL-PINNs 结果与证据
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/paper
- method/pinn
- method/reinforcement-learning
keywords:
- domain/ai4s
- evidence/paper
- method/pinn
- method/reinforcement-learning
sources:
- sources/papers/song2025-rl-pinns.md
created: '2026-07-31'
updated: '2026-07-31'
confidence: medium
---

# RL-PINNs 结果与证据

## Benchmark Summary

论文比较 uniform、RAR、RAD 和 RL-PINNs，覆盖尖峰 Poisson、双峰 Poisson、Burgers、wave、10D Poisson 与 biharmonic 六类任务。

| 案例 | RL-PINNs relative L2 | 最佳对照 | 改善 |
|---|---:|---:|---:|
| Single-Peak Poisson | 0.1462 | RAR 0.2871 | 49.1% |
| Dual-Peak Poisson | 0.1878 | RAR 0.3659 | 48.7% |
| Burgers | 0.0534 | RAR 0.1323 | 59.6% |
| Wave | 0.0053 | RAR 0.0339 | 84.4% |
| 10D Poisson | 0.0394 | RAR 0.0956 | 58.8% |
| Biharmonic | 0.0851 | RAR 0.1611 | 47.2% |

## Sampling Patterns

可视化显示新增点倾向于：

- 单/双高斯峰邻域；
- Burgers 激波或陡峭过渡；
- 波动传播前沿；
- 10D Poisson 的原点附近；
- biharmonic 高曲率区域。

这些图支持 function variation 能识别部分局部复杂度，但不直接证明它等价于 residual 或最优实验设计。

## Sampling Cost

采样阶段报告约 3.32–35.45 s，而最终 PINN 训练约 588–3591 s。作者据此认为 sampling overhead 较低。严格比较仍应计入预训练和 DQN 训练，并在相同硬件、相同最终训练预算下复核。

## High-Dimensional And High-Order Evidence

10D Poisson 表明局部动作 DQN 可以在高维坐标中工作；biharmonic 案例表明无需在候选池计算四阶 residual。两项结果说明无导数 reward 的潜在优势，但规则域和解析解条件仍较理想化。

## Comparison Boundary

RAR/RAD 的性能取决于采样轮次、候选池和每轮训练预算。论文报告的优势是在其统一设置下得到，不能直接推广为所有 residual-adaptive 实现均较差。

## Missing Ablations

论文没有系统拆分：

- reward 使用 $|\Delta u|$ 与 residual/gradient/uncertainty 的差异；
- 阈值 $\varepsilon$；
- 动作步长；
- 折扣因子；
- target 更新频率；
- episode 终止准则。

因此尚不能确定哪个 RL 组件是主要增益来源。

## Engineering Interpretation

对结构时程，采样策略可能集中于屈服、卸载、峰值和能量突变时刻。但必须避免预训练模型漏检导致的 bootstrap blind spot，并在复杂构件图上重新定义动作空间。

## Related Pages

- [[song2025-rl-pinns-analysis]]
- [[song2025-rl-pinns-method]]
- [[song2025-rl-pinns-critical]]
- [[rl-pinns]]

## Evidence By Source

### `sources/papers/song2025-rl-pinns.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/2504.12949v1.pdf`

^[sources/papers/song2025-rl-pinns.md]
