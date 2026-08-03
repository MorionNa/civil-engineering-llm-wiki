---
id: comparison--cycle34_variational_impulse_mechconv_20260803
title: 'Cycle 34: Variational and Symplectic Impulse Operators for MechConv (2026-08-03)'
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
legacy_source_files:
- literature/cycle34_variational_edge_integrator_20260803/PDFs/Variational_Integrator_Graph_Networks_for_Learning_Energy_Conserving_Dynamical_Systems.pdf
- literature/cycle34_variational_edge_integrator_20260803/PDFs/Symplectic_Momentum_Neural_Networks_--_Using_Discrete_Variational_Mechanics_as_a_prior_in_Deep_Learning.pdf
- literature/cycle34_variational_edge_integrator_20260803/PDFs/SPINI_a_structure-preserving_neural_integrator_for_hamiltonian_dynamics_and_parametric_perturbation.pdf
- docs/plans/seal_exmechconv_result_20260803.md
- docs/plans/ecaso_mechconv_result_20260803.md
- docs/plans/v28_block_causal_state_flow_result_20260803.md
- docs/plans/v30_lfct_frequency_conditioned_parent_result_20260803.md
legacy_evidence_scope: The bibliographic, local-file, hash, page-count, and retrieval-status
  facts below are verified metadata. Transfer proposals and project gates are engineering
  hypotheses; they are not claims that the cited papers validated this project's Bouc-Wen
  second-order graph contract. The Birkhoffian paper is abstract-only.
legacy_tags:
- variational-integrator
- symplectic
- momentum-network
- structure-preserving
- forced-damped-dynamics
- bouc-wen
- matrix-edge
- halo
evidence_scope: The bibliographic, local-file, hash, page-count, and retrieval-status
  facts below are verified metadata. Transfer proposals and project gates are engineering
  hypotheses; they are not claims that the cited papers validated this project's Bouc-Wen
  second-order graph contract. The Birkhoffian paper is abstract-only.
---

# Cycle 34: 变分/辛冲量算子迁移审查

## 已核验文献事实

### Variational Integrator Graph Networks

- 标题：*Variational Integrator Graph Networks for Learning Energy Conserving Dynamical Systems*。
- 版本：arXiv `2004.13688v2`。
- 本地 PDF：`literature/cycle34_variational_edge_integrator_20260803/PDFs/Variational_Integrator_Graph_Networks_for_Learning_Energy_Conserving_Dynamical_Systems.pdf`。
- SHA256：`6ccc4aee84c9bb6baaeccafb87deee32c80ab8a68eaa39775afb5e01a6a85f5d`。
- 页数：27 pages；SI：requested / not_found。

### Symplectic Momentum Neural Networks

- 标题：*Symplectic Momentum Neural Networks*。
- 版本：arXiv `2201.08281v4`。
- 本地 PDF：`literature/cycle34_variational_edge_integrator_20260803/PDFs/Symplectic_Momentum_Neural_Networks_--_Using_Discrete_Variational_Mechanics_as_a_prior_in_Deep_Learning.pdf`。
- SHA256：`d61a72e2b21c914cdfecf758450c2042bd82bc0c6084d2b290059395ffbf4b0d`。
- 页数：12 pages；SI：requested / not_found。

### SPINI

- 标题：SPINI。
- DOI：`10.1038/s41598-025-28710-2`。
- 本地 PDF：`literature/cycle34_variational_edge_integrator_20260803/PDFs/SPINI_a_structure-preserving_neural_integrator_for_hamiltonian_dynamics_and_parametric_perturbation.pdf`。
- SHA256：`11b3daa1302fa179d979be572b681c35d3e7acf7a39065d565e72e0959a23f78`。
- 页数：13 pages；SI：requested but fetch_failed due CDP proxy。

### Birkhoffian forced/damped paper

- DOI：`10.1016/j.compstruc.2026.108210`。
- OA status：`oa_not_found`。
- 本轮只有 abstract；不得把摘要当作正文强证据，也不记录未核验的算法细节。

## 可迁移启示

### 1. 离散变分/辛结构可作为长时间行为的候选先验

把离散作用量、离散动量或辛更新放入 proposal，可作为长 rollout 中结构保持的设计方向。它适合约束已知保守部分的离散几何，而不是自动证明有载荷、阻尼和材料记忆时的能量性质。

对本项目而言，最安全的迁移形式是：让变分/辛分支只生成候选端点 `u_p, v_p` 或线性参考流，随后仍由唯一边本构产生 `f_constitutive`，并由

```text
M a_next = p_next - C v_p - B.T @ f_constitutive
```

得到权威加速度。

### 2. 强迫/阻尼情形必须改用能量收支，而非保守能量不变量

外力做功、阻尼耗散和材料内部储能会改变保守系统的长时间判据。下一候选需要报告离散功平衡、阻尼耗散、材料状态能量代理和 EOM 残差，不能把无阻尼 Hamiltonian 轨迹的稳定表现直接迁移成结构动力学准确性。

### 3. 隐式离散可能改善刚性，但 root-find 成本和调用合同必须显式化

变分或辛离散常把端点方程变成隐式关系。若采用 root-find，必须报告每区间迭代次数、Jacobian/tangent 来源、失败回退、总本构调用数和可微成本；不能把一个隐式求解器隐藏在 forward 或 post-processing 中。

## 不可直接迁移的边界

| 方向 | 本项目的不可替代对象 | 必须补齐的合同 |
|---|---|---|
| Hamiltonian/保守离散结构 | Bouc-Wen 历史、材料内部状态和非线性边力 | 当前/拟议端点、edge state owner、每边调用审计和唯一权威本构力 |
| 变分端点方程 | 二阶 hard EOM 与固定 DOF | 端点 proposal 后重新计算 `a_next`，active-DOF EOM 残差必须达标 |
| 图网络局部耦合 | 矩阵 edge weight、`B.T` 稀疏装配和 halo | matrix edge shape、action-reaction、full-vs-partition/halo 等价；禁止全局 dense incidence |
| 长时间辛性 | 强迫、阻尼、非线性储能和高频离散 | 离散功/耗散账本、刚性稳定窗口、high-band acceleration/edge-force 指标 |
| 隐式 root-find | 单次 endpoint constitutive call 和训练预算 | 明确 root-find 是否允许；若允许，逐次报告迭代、tangent、失败路径和调用数 |

## 与既有候选失败记录的对照

### SEAL

SEAL 的本地 smoke 为 `7 passed, 1 warning`，compileall 通过，但 Sol 只读审查判定硬 NO-GO：其 ETD 是截断 Taylor exp/常值 `phi1`，谱界不代表全局稳定性，矩阵边权与一般 frame edge 不匹配，owner/ghost 不能避免 halo 重复推进，残差 slope 在零残差时梯度失活，且 energy helper 不能证明高频稳定。变分/辛标签不能绕过这些合同。

### ECASO

ECASO 的结构合同 M0 通过，但独立 calibration retry 的严格 common-descent gate 失败，候选停止。其 EOM 残差很小不等于训练改进或高频成功；新候选仍需同时证明响应指标和结构合同。

### V28

V28 的 tiny hard-physics smoke 通过部分平衡与运动学检查，但在 `m=1, C=0, k=100000, dt=0.01` 的 200 步扰动中达到 `max|u| = 1.9358004941688542e179`，且没有 halo/subgraph 路径。离散变分或辛先验必须先通过同类高刚度反例。

### V30

V30 被 rejected and frozen。其局部频率 carrier 被记录为 halo-compatible，但 pooled 指标略有回退，高模态 `u/v/a` 为 `0.846559/0.840715/0.835312`，高模态 edge force 为 `0.766457`，均未达到严格高频门槛。局部结构保持标签不能替代 high-band 证据。

## 下一候选的待验证硬门

1. **离散更新合同**：先在小标量线性振子上与 Newmark/RK4/FEM 对照；证明离散 action/动量或辛结构与实际端点 state 的关系，且不能通过第二力头绕过权威 EOM。
2. **强迫/阻尼账本**：在有载荷、阻尼和 Bouc-Wen 历史的 rollout 中同时检查功平衡、耗散、材料状态、hard EOM 和 kinematic residual；不得只报告保守能量漂移。
3. **隐式成本门**：若用 root-find，固定最大迭代次数，显式记录每区间本构/tangent 调用；超过预算、不可微或静默 fallback 立即 NO-GO。
4. **矩阵边/稀疏 halo 门**：验证一般 2D matrix edge、orientation/reorder、2/4 partition、owner-to-ghost state 和 full-vs-halo force equivalence；不得只验证 central pair spring。
5. **刚性与高频门**：至少覆盖 V28 同类高刚度反例，并报告 low/high-band `u/v/a/edge-force`、稳定窗口和 EOM 残差；不能以 `dt*local_bound <= 1` 单独作为稳定证明。
6. **因果与调用门**：每个物理 edge 的 endpoint 顺序必须不同且可审计；禁止未来泄漏、重复 halo 推进、post-processing 修补和隐藏的额外本构调用。
7. **严格晋级门**：在 calibration-only 条件下，固定 parent、数据 hash 和训练预算，所有目标通过 common-descent；否则保留为诊断脚手架，不进入 remote preflight。

## 决策

Cycle34 只提供下一候选的离散几何和刚性处理假设，不构成当前项目的 GO。V21 physical oracle、向量化 Newmark/RK4/FEM 继续作为 fallback；frozen parent 仅作 legacy 初值和误差指示器。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
