---
id: comparison--cycle12_v24_psg-evidence-and-contract-20260802
title: Cycle 12：V24-PSG-MechConv 证据与契约
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 12：V24-PSG-MechConv 证据与契约

## 新证据

- Liang et al., *SPINI: a structure-preserving neural integrator for Hamiltonian dynamics and parametric perturbation*, Scientific Reports 15, 43842 (2025), DOI `10.1038/s41598-025-28710-2`。其方法将 Hamiltonian 学习与 Yoshida 辛积分分离，适用于无耗散 Hamilton 系统；不能直接证明阻尼、外力、约束或滞回本构下的工程结构预测。
- Duruisseaux et al., *Approximation of nearly-periodic symplectic maps via structure-preserving neural networks*, Scientific Reports 13, 8351 (2023), DOI `10.1038/s41598-023-34862-w`。Hénon/gyroceptron 说明辛映射表达力和长期几何稳定性，但文中目标为 purely Hamiltonian dynamics。
- Sharma & Fink, *A physics-informed graph neural network conserving linear and angular momentum for dynamical systems*, Nature Communications 17, 1045 (2026), DOI `10.1038/s41467-025-67802-5`。边局部 frame 可硬编码 action-reaction 和守恒量，复杂度随边/点线性；该证据仍不覆盖本项目的 path-dependent constitutive replay、独立 EOM 审计或 partition-invariant halo force。
- Fabiani et al., *Enabling local neural operators to perform equation-free system-level analysis*, Nature Machine Intelligence 8, 1127–1141 (2026), DOI `10.1038/s42256-026-01265-1`。local-in-space/time 与 patch/projective 思路支持局部上下文和多尺度复用，但不等于任意历史本构都存在可并行的时间前缀。

本轮 OA 下载器尝试了 SPINI、nearly-periodic symplectic maps 和 DYNAMI-CAL GraphNet 的确定清单；因当前环境未配置机构/浏览器 OA 路由，两次运行分别记录为 `failed_after_retry`/超时，没有把错误响应当作 PDF。前两篇以及 local neural operator、multi-level structural PINN 的合法全文/本地抽取证据已在 cycle 11 目录保留。

## V24 最小契约

V24 只验证边局部 passive scattering + replaceable constitutive state + `B^T f_e` + hard `a=M^{-1}(F-Cv-B^Tf_e)`。粗层只能提供 context；不能写 edge force/state/material。预检阈值和停止规则见 `docs/plans/v24_psg_mechconv_design_20260802.md`。

## Grill 结论

Conditional GO 仅意味着值得做一次无训练证伪。若高频稳定性需要超过两次子步、passive projection 需要 Newton/Krylov、构成本构不能保持精确 temporal prefix、或 halo 通信抹去线性边复杂度，则直接推理速度目标不可守；任一失败都停止，不启动远程训练。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
