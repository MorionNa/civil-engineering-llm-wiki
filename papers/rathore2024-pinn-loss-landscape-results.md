---
id: papers--rathore2024-pinn-loss-landscape-results
title: PINN 损失景观结果与证据
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/paper
- method/pinn
keywords:
- domain/ai4s
- evidence/paper
- method/pinn
sources:
- sources/papers/rathore2024-pinn-loss-landscape.md
created: '2026-07-31'
updated: '2026-07-31'
confidence: medium
---

# PINN 损失景观结果与证据

## Benchmarks

论文在 convection、reaction 和 wave 三类 PINN 上比较 Adam、L-BFGS、Adam+L-BFGS，以及末期加入 NysNewton-CG 的组合。网络宽度覆盖 50、100、200、400，并使用多个随机种子。

## Loss–Error Relationship

散点图显示，高精度解通常要求训练 loss 极低；在较高 loss 区域，L2 relative error 变化很大。该关系说明“loss 还没有下降到足够低”往往不能用泛化误差解释，但低 empirical loss 也不是连续域正确性的充分条件。

## Hessian Spectrum

三个任务在 Adam+L-BFGS 后仍呈现：

- 大量接近零的曲率方向；
- 少量跨多个数量级的离群大特征值；
- residual block 比边界/初值 block 更病态。

这提供了有限宽网络中的直接经验支持：微分残差会产生极不均匀曲率。

## Optimizer Comparison

调参后的结果总体支持：

- Adam 单独使用下降慢，尤其在局部病态阶段；
- L-BFGS 从随机初始化可能受鞍点或不良盆地影响；
- Adam→L-BFGS 在多数宽度/任务上优于单独方法；
- L-BFGS 有时因 line search 返回零步长而停止，尽管梯度范数并不小。

## Conditioning Improvement

将 L-BFGS 逆近似作为右预条件器后，Hessian 的最大谱尺度或有效条件数至少改善约 $10^3$。这解释了拟二阶阶段的收益，但并不意味着 L-BFGS 完全消除了近零方向。

## NNCG Post-Training

在 Adam+L-BFGS 结果上继续运行 NNCG，可进一步降低三类任务的 loss 和 L2RE。收益在 L-BFGS 已停滞而梯度仍明显时最有意义。

## Wall-Clock Boundary

NNCG 每一步代价很高；论文报告 wave 问题中单步成本可达到 L-BFGS 的约 322 倍。因此最优策略不是从头使用 NNCG，而是少量末期精修，并以 wall-clock 与误差共同判断。

## Theory–Experiment Alignment

理论说明微分算子谱可能导致条件数随 residual 点数多项式增长；实验中的谱与配点规模趋势与此一致。但理论假设不覆盖所有非线性 PDE 和有限训练动态。

## Interpretation Limits

- 三类 benchmark 规模有限；
- near-zero collocation loss 可能仍漏掉点间误差；
- 性能依赖高质量 HVP、damping 与预条件更新；
- 结果不排除采样、架构、因果性或 loss 权重是其他任务的主导因素。

## Related Pages

- [[rathore2024-pinn-loss-landscape-analysis]]
- [[rathore2024-pinn-loss-landscape-method]]
- [[rathore2024-pinn-loss-landscape-critical]]
- [[nysnewton-cg]]

## Evidence By Source

### `sources/papers/rathore2024-pinn-loss-landscape.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/rathore24a.pdf`

^[sources/papers/rathore2024-pinn-loss-landscape.md]
