---
id: papers--zhang2026-legonet-results
title: LegONet 结果：跨 PDE 组合、长时稳定与结构保持
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/paper
- method/neural-operator
- method/pinn
keywords:
- long-horizon-rollout
- neural-operator
- structure-preserving
sources:
- sources/papers/zhang2026-legonet.md
created: '2026-07-28'
updated: '2026-07-31'
confidence: high
---

# LegONet 实验结果

## Benchmark

论文在 4 类 baseplate 和 10 个时变 PDE 上测试，包括 1D、2D、3D 系统。

## 主要结果

- 1D Burgers：独立训练的扩散块和输运块组合后保持耗散和 Hamiltonian 结构；闭环稳定性优于 PINN、FNO 和 DeepONet。
- 2D Navier–Stokes：长时间湍流 rollout 中保持稳定，结构诊断显示机制块行为保持。
- 3D Swift–Hohenberg：通过重复使用 Laplacian block 处理高阶刚性算子，在 OOD 初值下仍保持较低误差。

## 核心验证

论文重点验证：

1. block 可以跨 PDE 重新组合；
2. boundary reconfiguration 不需要重新训练；
3. 结构保持约束能改善长时稳定性。

## 关联

- [[zhang2026-legonet-analysis]]
- [[zhang2026-legonet-critical]]

## Evidence By Source

### `sources/papers/zhang2026-legonet.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/2603.07882v1.pdf`

^[sources/papers/zhang2026-legonet.md]
