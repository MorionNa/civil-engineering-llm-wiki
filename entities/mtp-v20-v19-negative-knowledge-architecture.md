---
id: entity--mtp-v20-v19-negative-knowledge-architecture
title: MTP-MechConv V20.2 / V19 负知识：下一架构约束
type: entity
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-01'
updated: '2026-08-01'
confidence: low
legacy_tags:
- structural-dynamics
- limitation
- architecture-selection
- physics-informed
- neural-operator
- hard-constraints
- message-passing
- transfer-learning
legacy_sources:
- docs/plans/rk4z_stage_head_v20_2_screen25_fail_2026-08-01.md
- docs/plans/tridiagonal_zcq_mechconv_v19_m0b_veto_2026-08-01.md
- literature/github/StructGraph-Dyna/main.py
- literature/github/soft-tissue-pignn/models.py
---

# 负知识摘要

V19 和 V20.2 的共同教训不是“网络容量不够”，而是接口与训练目标没有覆盖最终要证明的对象。V19 的频域 Thomas-ZCQ 计算本身可以与同一梯形参考保持很小误差，但连续 RK4 真值回放的加速度恢复门失败；V20.2 的最终 force-balance 是构造得到的精确量，而 stage-residual 学习仍然失败。^[docs/plans/tridiagonal_zcq_mechconv_v19_m0b_veto_2026-08-01.md]

## 已锁定的失败边界

- 不能把与某个离散参考的一致性当成与连续 RK4 真值的一致性；离散运动学关系、载荷波和高刚度模态必须使用同一时间积分语义验收。
- 不能把硬编码的最终平衡 R² 当成预测质量；必须独立检查 stage residual、运动学、EOM、构成/本构和频带指标。
- V20.2 的直接监督 stage head 在 25 个 epoch、25,192 参数的 screen 中，mean response R² 为 0.483985，stage residual R² 为 0.092992；这些数值只描述该失败 screen，不是一般性能结论。^[docs/plans/rk4z_stage_head_v20_2_screen25_fail_2026-08-01.md]
- V20.2 排除了 carrier 的训练闭环，因此没有真正施加“carrier 重构 stage state → plugin force → residual”一致性；加长同一 uncoupled head 的训练不能修复缺失的物理耦合。
- V19 的 50 DOF 速度与内存记录不能外推为通用 owner/separator、任意图规模或大规模训练已通过；当前结果只授权继续做接口替代方案的正确性审计。

## 下一架构必须改变什么

| 约束 | 架构要求 | 必须保留的否决门 |
|---|---|---|
| carrier 闭环 | 单 carrier 端到端重构 stage state，并在训练中调用 constitutive plugin；若改成 predictor-corrector，须单独声明速度/接口代价。 | stage residual、plugin consistency、response 和低/高频门同时通过 |
| 物理量分工 | 网络只预测可学习残差/边量；最终平衡、外力符号、矩阵边权和边界条件由确定性算子装配。 | 不得用 architecture-constructed balance 指标替代独立预测指标 |
| 图分块 | 采用 FBPINN 的局部/粗层通信启发，但 preserve core edge semantics、owner/separator、halo 和 state identity。 | 子图重排、halo 宽度、粗层开关后，局部与全图结果不得出现未解释的门退化 |
| 本构插件 | 采用模块化弹塑性“解析组件/学习组件可替换”原则；数据不足时不强行学习全 constitutive law。 | 载荷路径、材料状态和热力学约束必须独立审计 |
| 频率与长时域 | 训练目标显式包含低/高频或等价谱门；不能从低频平均 R² 推断高频稳定。 | 预注册的频带门和长时 rollout 门必须保留 |

## 决策含义

下一架构优先级是“carrier 内物理耦合 + 独立验收 + 可替换插件”，不是简单扩大 stage head，也不是将 FBPINN/PI-GNN 的局部消息传递直接搬进来。StructGraph-Dyna 可提供配置和 GraphGym 管线参考，soft-tissue PI-GNN 可提供反向消息守恒的实现启发，但二者都不能解除 V19/V20.2 已暴露的证据责任。^[literature/github/StructGraph-Dyna/main.py]

## 关联页面

- [[fbpinn-xpinn-structgraph-pignn-transfer-boundaries]]
- [[mtp-mechconv-v2-v19-scalability-and-correctness-correction]]
- [[mtp-mechconv-v2-v20-rk4z-design-evidence]]
- [[v20-2-rk4z-stage-head-screen25-failure-2026-08-01]]
## V20.3a screen correction

The V20.3a preregistration narrows the claim: the single carrier is only a
proposal-driven fixed-point surrogate. Bouc--Wen must replay history with
z1 = zn and a grid commit defect; a free latent z cannot be used to algebraically
match proposal force. Stage 1 and 2 suffix perturbation tests close the
interval-level causality loophole. Proposal/plugin residual and acceleration
branches use separate frozen-scale NRMSE, and high-frequency response is a
hard gate. One unseen internal set is frozen and evaluated once after model
and checkpoint freeze.

A truly plugin-driven final state is a two-carrier predictor-corrector with a
second history replay and final fixed-point defect. Matrix edges, MechConv,
owner/separator/Schur, subgraph stitching, and scale are deliberately
post-screen gates. See [[mtp-v20-3a-screen-contract]] and
[[fbpinn-xpinn-structgraph-pignn-transfer-boundaries]].

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.
