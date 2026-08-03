---
id: comparison--cycle20_dhkr_design_20260803
title: DHKR：离散谐波运动残差设计（2026-08-03）
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# DHKR：离散谐波运动残差设计（2026-08-03）

## 方案选择

Sol high 否决了下游 CRFC 力残差头：它不能直接改善位移/速度，且会把残差
变成第二本构模型。新候选为 DHKR（Discrete-Harmonic Kinematic Residual）。

## 核心机制

对固定的无量纲频率 `theta_r = omega_r * dt`（要求小于 `0.8*pi`），节点头
从时间池化 hidden 预测 `A_ir,D_ir`。速度修正为

`delta_v_i,n = gamma * sum_r omega_tilde_r *
[-A_ir sin(n theta_r) + D_ir cos(n theta_r)]`，

其中 `omega_tilde_r = 2/dt * tan(theta_r/2)`。修正放在第一次本构调用之前，
由 parent 的 hard trapezoid 直接得到位移，因此每个固定系数对严格满足离散
梯形运动学关系。本构插件仍是唯一力来源，原 dynamic projection 仍负责 EOM。

## 证据边界

已合法下载并验证 Springer Nature OA 论文
`10.1186/s40323-026-00324-x`，其支持自然频率嵌入以减轻频谱偏置，但没有证明
DHKR 的图规模、halo 或非线性跨本构结论。SI 因本地 CDP proxy 不可用而失败，
主 PDF 已验证。

ModalGNN_Time_Domain 与 neuraloperator 的 GitHub 直连分别出现 reset/timeout，
没有把未拉取的代码当作证据。

## 必须通过的本地闸门

zero-init parent 等价、梯形恒等式、两次本构调用、三种本构有限梯度、五步 clipped
Adam 稳定下降、full/halo 和 500-node smoke，以及频率上限检查。全部通过后才允许
一次串行远程 Adam screen。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
