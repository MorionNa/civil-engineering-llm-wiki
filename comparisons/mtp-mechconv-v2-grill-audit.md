---
id: comparison--mtp-mechconv-v2-grill-audit
title: MTP-MechConv v2 grill 审计：从候选到 v2.1 可证伪协议
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-07-31'
updated: '2026-07-31'
confidence: low
legacy_tags:
- neural-operator
- message-passing
- structural-dynamics
- equation-of-motion
- hard-constraints
- limitation
- future-work
legacy_sources:
- raw/papers/10_1016_j_cma_2024_117441.pdf
- raw/papers/10_1016_j_cma_2025_118476.pdf
- raw/papers/10_1016_j_cma_2024_117116.pdf
- raw/papers/arxiv_2202_03376.pdf
- raw/papers/10_1007_s10444_023_10065_9.pdf
---

# MTP-MechConv v2 grill 审计

## 审计结论
当前 5DOF 时间并行模型只证明了一个开发基线。硬 EOM 使 balance residual 达机器精度，但不能独立证明 \(u,v,a,f_e\) 正确；已有 6-block 开发结果的 `acceleration_kinematic_relative_rms=0.119` 也说明，严格 EOM 与真实运动学必须分开审核。

## v2.1 的六项重构
1. `linspace(0,1,T)` 改为固定尺度物理时间，新增后缀扰动前缀不变测试。
2. 方程统一为 \(Ma+Cv+f_\mathrm{int}(u,z)=F_\mathrm{eff}\)，仅线性插件使用 \(Ku\)。
3. 最终本构状态改为插件因果推进；状态头不能自由吸收恢复力误差。
4. 认证范围明确为 block-diagonal lumped mass；一般一致质量另立全局路线。
5. 实现 3DOF/6DOF block-MechConv；5DOF 全图 halo 不再作为规模证据。
6. 粗层只提供稀疏 latent context，不直接生成构件恢复力或隐式全图 gather。

## 指标纠偏

| 类别 | 指标 |
|---|---|
| 预测 | \(R^2_{u,v,a,f_e}\)、NRMSE、峰值、相位、per-sample p05 |
| 构造 | EOM nRMS \(\le10^{-6}\)，balance R² 只标记 constructed |
| 独立物理 | \(D_tu-v\)、\(D_tv-a\)、独立 EOM nRMS \(\le0.05\) |
| 本构 | 独立 replay、恢复力 R² \(\ge0.95\)、耗能误差 \(\le5\%\) |
| 扩展 | stitching/interface RMS \(\le10^{-4}\) |
| 速度 | \(N\ge500\)、batch=1、公平基线至少 10× |

## 数据与终测
Official90 降级为开发集；所有当前训练和高频头选择只能使用 dev。架构冻结后建立无同源地震动/裁剪/缩放/频域变体泄漏的新 locked test，并只打开一次。

## 论文边界回写
[[unrolled-training]] 与 [[mp-pde]] 主要支持自回归分布训练，不能证明整段算子需要 solver-in-loop。[[message-passing-reach-contract]] 是设计启发，不是 FFT 整段算子的 CFL 定理。[[fbpinn]] 和 [[multilevel-fbpinn]] 支持局部尺度化与粗层通信，但不能替代矩阵边、滞回状态和 halo 等价实验。

## 关联页面
- [[mtp-mechconv-v2-evidence]]
- [[mtp-mechconv-v2]]
- [[message-passing-reach-contract]]
- [[multilevel-fbpinn]]

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.
