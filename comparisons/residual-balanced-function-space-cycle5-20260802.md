---
id: comparison--residual-balanced-function-space-cycle5-20260802
title: Cycle 5：残差平衡 + 函数空间尺度 + 变形/频带分层
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 5：残差平衡 + 函数空间尺度 + 变形/频带分层

## 结论

上一轮所有“在线修正器”都触碰了本项目的核心矛盾：硬 EOM 可以在一次 forward 内成立，但独立的 `D_BDF2(v)-a_EOM` 仍然偏大；额外逆、Newton 或 state replay 要么超速，要么与 learned constitutive correction 不兼容。因此下一候选应只改变训练表示/损失/采样，不改变部署 forward。

## 本轮证据转移

1. BRDR/残差衰减率工作支持按慢收敛残差提高训练权重，但不能直接把点权重当作物理证明；本项目应对 `r_a`、`r_F`、低/高频、大小变形分组做有界 EMA 权重，权重均值固定为 1。
2. 变分 residual adaptivity 将残差倾斜解释为目标范数/采样分布的选择，因此候选必须用固定的 `dt`、节点/边质量尺度和频带积分权重，避免训练 loss 与最终 RMS/R² 指标不一致。
3. 函数空间算子原则支持 quadrature-aware loss 和 discretization-agnostic interface；对本项目的具体含义是 owned-node/owned-edge 的 MechConv 贡献、halo=6 拼接和 full/subgraph 误差都用同一物理测度审计。
4. 结构保持图求解器和 SGNO 支持“局部守恒/受控生成器/高频稳定”的动机，但不能直接移植其 PDE flux 或 Fourier operator；现有矩阵边 MechConv 和 pole-residue 分支必须保留。

## 允许的候选形态

候选只能是现有 `TemporalParallelMatrixMechConv` 的训练协议 successor：

- hard trapezoid `u=I(v)`、MechConv 矩阵边力、可替换 constitutive plugin、两次 constitutive call、`required_halo_hops=6` 全部不变；
- 训练期计算 `r_a`、`r_F`、constitutive、kinematic 和 low/mid/high residual，使用物理尺度归一化和 bounded residual-decay weights；
- 预注册小/大变形 strata，指标至少包含 edge relative deformation、层间 drift、hysteretic state/energy，不允许用单一 `max|u|` 事后命名；
- 小/大变形和线性/双线性/Bouc–Wen 先做本地接口与短 smoke，再考虑远程单 GPU；
- 若 response R²、独立 physics RMS、频带、halo、速度任一硬门失败，冻结该 successor，parent 不变。

## 负知识

不再尝试：CMEJ² 额外动力逆、TR-PCGrad 终端 readout、CGERC 大修正头、固定 parent state 的 CHaRT、stateful Newton replay、在线 FFT/Fourier correction。这些分支没有同时满足精度、状态一致性和速度。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
