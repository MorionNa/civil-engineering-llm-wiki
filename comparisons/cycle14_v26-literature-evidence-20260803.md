---
id: comparison--cycle14_v26-literature-evidence-20260803
title: Cycle14 V26 文献证据卡：NPO / Jha corrector / NOEM
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle14 V26 文献证据卡：NPO / Jha corrector / NOEM

## 给后续 Sol 设计的短结论

这三组证据都支持“学习算子可以改善残差处理、局部表示或变分组装效率”，但没有一组证明 V26 所需的结构动力学硬 EOM、硬运动学、历史本构一致性、子图边界合同，或一次 direct forward 的免迭代闭合。

| 证据 | 可借鉴 | 明确不能声称 |
|---|---|---|
| NPO，arXiv `2502.01337v2` | 残差条件化预处理、高/低频误差分工、局部图/粗化表示；适合作为训练期 teacher/诊断或固定次数 refinement 候选 | 不能声称替代 Krylov/CG/GMRES；不能声称一次 forward 直接解出结构动力学；理论有 SPD/平滑/粗空间假设 |
| Jha corrector，DOI `10.1016/j.cma.2023.116595`，arXiv `2306.12047v3` | 变分残差 + 线性化 Jacobian 的误差诊断、teacher target、验收门 | corrector 要额外解线性变分问题；与 Newton 步相关，不能声称免迭代、硬 EOM 或部署零成本 |
| NOEM，DOI `10.1038/s43588-026-00974-2`，arXiv `2506.18427` | 可复用局部 operator/constitutive adapter、子域接口合同、operator 与 FE 的离线组装思路 | 变分 `arg min`/全局组装不是硬 EOM；未证明结构动力学时间推进、历史状态一致、halo 拼接或 direct no-iteration closure |

## Sol 设计边界

- 可以进入候选池：残差作为训练信号/teacher、固定开销的局部表示变换、离线局部 operator adapter、接口/halo 一致性审计。
- 不可以从这些论文直接推出：硬 EOM 恒等式、硬运动学恒等式、任意本构替换后的稳定性、无 Newton/Krylov/线性求解步骤、或“结构动力学目标已被论文证明”。
- 任何后续候选仍须单独通过 V26 的本地 identity/shape/halo/频率检查，再决定是否进行远程实验；本卡不授权写模型代码或训练。

## 证据定位

- 论文与 SHA256：`docs/plans/v26_literature_evidence_20260803.md`。
- 既有对照：`entities/neural-preconditioning-operator-2025.md`、`entities/residual-error-corrector-2024.md`、`comparisons/cycle4-preconditioner-corrector-20260802.md`、`comparisons/cycle7_conservation_local_operator_refresh_20260802.md`。
- GitHub 快照：`literature/github_20260802_cycle4/repos/neuraloperator__physics_informed` 当前 commit `3b6bc307c63c64057d0496753bf1af5f44ac5108`；`literature/github_20260802_cycle11/repos/neuraloperator` 当前 commit `86a8bc7812a31b42c4f7895693cf4ac11521c066`，本轮 fetch 成功。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
