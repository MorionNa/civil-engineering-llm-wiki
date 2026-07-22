---
title: "PGT 批判性分析"
created: 2026-07-16
updated: 2026-07-16
type: paper-analysis
---

# PGT 批判性分析

## Contribution

1. 将物理知识从 PINN loss 提升到 Transformer attention；
2. 提供物理引导的信息传播机制；
3. 改善稀疏数据条件下 PDE 重构。

## Negative Knowledge

- 当前主要验证 PDE 场问题；
- 尚未证明适用于复杂非线性结构动力学；
- physics bias 需要已知传播规律；
- 对材料非线性、滞回、损伤演化仍缺少机制表达。

## Research Opportunity

对于结构动力：

1. 构造基于质量刚度矩阵的 attention bias；
2. 将模态传播作为 attention kernel；
3. 结合本构模型约束；
4. 研究 physics-aware Transformer foundation model。

## 关联页面

- `[[zeraatkar2026-pgt-analysis]]`
- `[[seisgpt]]`
- `[[cm-pinns]]`
