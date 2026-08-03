---
id: comparison--mtp-mechconv-v2-v21-m0-causal-audit
title: MTP-MechConv v2 V21-M0：顺序因果本构与硬平衡审计
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-02'
updated: '2026-08-02'
confidence: low
legacy_tags:
- mechconv
- causal-constitutive
- bouc-wen
- equation-of-motion
- subgraph
- high-frequency
legacy_sources:
- ../../../../docs/plans/sequential_causal_mechconv_v21_m0_20260802.md
- ../entities/hano-2025-history-aware-neural-operator.md
---

# V21-M0 审计

V21-M0 将每条构件边的本构状态作为唯一 owner，在时间步内与节点位移、速度和加速度共同推进；全局内力只通过 `B^T f_e` 装配。它通过了 50DOF/1501 步的硬 EOM、分区等价、R² 和高频门，说明“闭环正确性”可以从网络训练中独立出来审计。

这不是速度证书：固定质量 Cholesky 后 warm forward 为 `0.619668 s`，尚未证明远快于同硬件优化 Newmark/FEM；通用非线性本构也不具备可假设的精确 prefix scan。[[hano-2025-history-aware-neural-operator]] 可支持历史窗口编码动机，但不能替代显式状态更新或 MechConv 平衡。

下一步只允许把该 plugin/MechConv contract 作为既有时间并行最佳模型的可替换物理层进行单变量对照；若速度或真实数据精度下降，保留 V21 为物理审计/材料代理组件，不扩大声明。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
