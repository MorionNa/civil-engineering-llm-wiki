---
id: papers--zeraatkar2026-pgt-results
title: Physics-Guided Transformer 结果与证据
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
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
- method/pinn
- method/transformer
sources:
- sources/papers/zeraatkar2026-pgt.md
created: '2026-07-31'
updated: '2026-07-31'
confidence: medium
---

# Physics-Guided Transformer 结果与证据

## 1D Heat Diffusion

论文在稀疏观测数量变化下比较 SIREN、PINN 和 PGT。100 个观测点时：

| 方法 | Relative L2 error |
|---|---:|
| PGT | $5.90\times10^{-3}$ |
| PINN | $2.26\times10^{-1}$ |
| SIREN | $5.40\times10^{-1}$ |

PGT 相对 PINN 约降低 38 倍，相对 SIREN 接近 90 倍。随着观测增加，PGT 仍保持更低场重构误差。

## Optimization Curves

训练曲线显示 PINN 和 SIREN 在较高误差附近较早停滞，而 PGT 的误差继续单调下降。这支持架构传播偏置有助于优化，但不能单独区分其与模型容量、FiLM decoder 和损失权重的贡献。

## Computational Trade-Off

PGT 的精度提升伴随更高成本：

- 参数量高于 SIREN/PINN；
- FLOPs 约 116–190 GFLOPs，而简单基线约 1.7–1.9 GFLOPs；
- 训练时间最高约 $1.67\times10^3$ s，而简单基线约 65 s。

因此结论是精度—成本前沿改善，而不是 PGT 在所有资源预算下最优。

## Cylinder-Wake Navier–Stokes

1500 个散点观测时，论文报告：

- PDE residual loss $8.3\times10^{-4}$；
- overall relative L2 error 0.034。

PGT 在保持较低 residual 的方法中取得更低整体误差，说明传播偏置与 residual loss 可以同时工作。

## Ablation

消融表明：

- 移除 physics-guided attention 会降低重构精度；
- 移除 PDE loss 会提高物理残差；
- 两者共同使用表现最好。

这支持“架构内物理 + 目标函数物理”互补，而非相互替代。

## Evidence Boundaries

- 验证集中于一维热方程和二维流动；
- Green bias 的准确性依赖已知物理参数；
- 与基线的参数/FLOPs 不等，消融需要结合容量控制；
- 结果不覆盖复杂边界、强非线性滞回、接触和断裂。

## Structural-Dynamics Interpretation

PGT 说明物理传播规律可直接调制 attention。结构研究需要分别评价低频全局位移、高频局部加速度、模态传播、屈服后状态变化和计算成本，不能只复用热核。

## Related Pages

- [[zeraatkar2026-pgt-analysis]]
- [[zeraatkar2026-pgt-method]]
- [[zeraatkar2026-pgt-critical]]
- [[pgt]]

## Evidence By Source

### `sources/papers/zeraatkar2026-pgt.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/2603.27929v1.pdf`

^[sources/papers/zeraatkar2026-pgt.md]
