---
id: comparison--cycle33_stiff_split_exponential_20260803
title: 'Cycle 33: Stiff Split and Exponential Methods — Transfer Audit (2026-08-03)'
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
legacy_source_files:
- literature/cycle33_stiff_structure_preserving_20260803/PDFs/Structure-Preserving_Neural_Ordinary_Differential_Equations_for_Stiff_Systems.pdf
- literature/cycle33_stiff_structure_preserving_20260803/PDFs/MENO_Hybrid_Matrix_Exponential-based_Neural_Operator_for_Stiff_ODEs._Application_to_Thermochemical_Kinetics.pdf
- docs/plans/v28_block_causal_state_flow_result_20260803.md
- docs/plans/v30_lfct_frequency_conditioned_parent_result_20260803.md
- docs/plans/ecaso_mechconv_result_20260803.md
legacy_evidence_scope: PDF metadata and project experiment records are recorded as
  verified facts. Transfer proposals and hard counterexamples below are engineering
  hypotheses or project gates, not claims that the papers validated structural dynamics.
  PeTIGN has no downloaded body text in this audit.
legacy_tags:
- stiff-dynamics
- exponential-integrator
- operator-learning
- sparse-graph-operator
- structure-preserving
- second-order-eom
- constitutive-state
evidence_scope: PDF metadata and project experiment records are recorded as verified
  facts. Transfer proposals and hard counterexamples below are engineering hypotheses
  or project gates, not claims that the papers validated structural dynamics. PeTIGN
  has no downloaded body text in this audit.
---

# Cycle 33: 刚性拆分与指数方法迁移审查

## 结论先行

本轮文献支持三类待验证设计方向：

1. 将可知的线性/刚性部分与待学习的非线性部分拆分；
2. 用指数积分或其他稳定化离散处理刚性线性部分；
3. 用稀疏图算子承载局部空间耦合。

这些方向不能直接替代本项目的结构动力学合同。项目仍必须显式保留二阶 EOM、材料/边状态、矩阵边权、边力的稀疏装配以及子图 halo/owner 语义。任何新候选都要先通过本地合同和稳定性反例，再讨论训练收益；不能假设它会自动改善高频响应。

## 已核验文献与证据边界

### PDF 1

- 标题：*Structure-Preserving Neural Ordinary Differential Equations for Stiff Systems*。
- 版本：arXiv `2503.01775v4`。
- 本地 PDF：`literature/cycle33_stiff_structure_preserving_20260803/PDFs/Structure-Preserving_Neural_Ordinary_Differential_Equations_for_Stiff_Systems.pdf`。
- SHA256：`142b87a8277b6b6172d92bc18ac08a7dbcde7f721809f7cc3f13d27f6823ab10`。
- 页数：19 pages。
- SI：requested / not_found。

### PDF 2

- 标题：*MENO: Hybrid Matrix Exponential-based Neural Operator for Stiff ODEs. Application to Thermochemical Kinetics*。
- 版本：arXiv `2507.14341v1`。
- 本地 PDF：`literature/cycle33_stiff_structure_preserving_20260803/PDFs/MENO_Hybrid_Matrix_Exponential-based_Neural_Operator_for_Stiff_ODEs._Application_to_Thermochemical_Kinetics.pdf`。
- SHA256：`9f703bdd8e325ff560523cd808b80c0cc3ade4d5183a4ef591fd57a59f9bf5b1`。
- 页数：52 pages。
- SI：requested / not_found。

### PeTIGN

- 标题信息：PeTIGN。
- DOI：`10.1016/j.engstruct.2026.123094`。
- OA route status：`oa_not_found`。
- 正文未下载。本轮不得把摘要内容当作强证据，也不从 PeTIGN 推导具体实现结论。

## 可迁移启示：只能作为候选假设

### 1. 线性/非线性拆分

可把已知的质量、阻尼、名义刚度或其他可组装线性算子作为受控分支，把 Bouc-Wen 等材料历史和非线性边力留给权威本构插件。这样做的可检验目标是：刚性线性部分负责稳定传播，非线性部分仍保留边状态、端点运动学和唯一边力来源。

迁移限制是，拆分后的线性分支不能偷偷成为第二力头，不能绕过 `M a = p - C v - B.T @ f_edge`，也不能用名义线性切线代替全过程材料切线。

### 2. 指数积分与稳定化

指数或稳定化时间推进可作为高刚度线性子算子的候选处理方式。当前证据只支持把它作为“可能降低刚性离散误差/放宽稳定限制”的假设；不支持声称结构动力学高频成功。

最低要求是比较同一时间步、同一材料状态和同一矩阵边权下的线性振子、Bouc-Wen 短 rollout 与 RK4/Newmark/FEM 参考，并报告稳定窗口、低/高频误差、EOM 残差和本构调用数。

### 3. 稀疏图算子

稀疏图算子适合保留局部边消息、矩阵边权和 `B.T @ f_edge` 的两端点装配。迁移实现必须使用 edge gather/scatter 或等价稀疏算子，不能创建 `E x N` dense incidence；还必须在 full graph 与 edge-partition/halo 图之间保持力和状态的一致性。

## 不能直接转移到本项目的内容

| 文献方向 | 不能直接替代的项目对象 | 必须补上的合同 |
|---|---|---|
| 全局 matrix exponential | 局部边力装配、矩阵边权和子图推理 | 稀疏边算子、owner/ghost 状态同步、halo 边界闭合；不得把全局指数映射当作局部接口 |
| 通用 stiff ODE 状态 | 二阶结构 EOM 与材料内部状态 | 显式保留 `u_n, v_n, a_n`、边状态、`M/C`、端点运动学和唯一权威本构力 |
| latent/learned nonlinear flow | Bouc-Wen 等有历史依赖的本构状态 | 当前/拟议端点必须区分；边状态按物理边拥有；一次区间调用次数可审计 |
| 稳定化或指数分支 | 自动获得高频精度 | 高刚度/小时间步稳定性反例、high-band `a/edge-force` 指标、严格 common-descent gate |

特别是，全局指数传播可能破坏子图的局部性和 halo 语义；材料状态不能被无标注地压缩成全局 latent 状态；二阶 EOM 也不能由一阶 ODE 的稳定性标签替代。

## 与项目失败记录的对照

### V28 Block-Causal State-Flow

V28 的 tiny smoke 通过了标量 hard balance、Symplectic-Euler 运动学和 Bouc-Wen 边状态有限性，但在 `m=1, C=0, k=100000, dt=0.01` 的 200 步零输入扰动中，`max|u| = 1.9358004941688542e179`；较低频的 `k=10000` 才保持有界。记录还明确指出没有 halo/subgraph 执行路径，且不是 learned MechConv。结论是 NO-GO；指数/稳定化方向必须先击穿同类刚性反例。

### V30 LFCT

V30 被 rejected and frozen。其局部 `sqrt(diag(K_t)/diag(M))` carrier 被记录为物理安全且 halo-compatible，但 pooled 指标略有回退，高模态 `u/v/a` 分别为 `0.846559/0.840715/0.835312`，均低于 `0.90`；高模态 edge force 为 `0.766457`，同样未过门槛且略有回退。该记录不支持“局部频率条件化已经解决高频”的结论。

### ECASO

ECASO 的结构性 M0 通过，但严格 common-descent gate 失败，因此候选停止，只保留 contract-correct scaffold。独立 calibration retry 的 pooled `u/v/a/edge-force R2` 为：

```text
u       .9686507363 -> .9654346647
v       .9771272961 -> .9781063848
a       .9999440146 -> .9999353409
edge    .9731957343 -> .9693531987
```

高频 `a` 为 `.9999704009 -> .9999699584`，高频 edge force 为 `.9798333482 -> .9799080923`；EOM 最大残差为 `1.4551915e-11 -> 1.1641532e-10`。这组结果说明合同正确和 EOM 很小并不等于训练改进，也不等于高频成功。

## 下一候选：应验证的假设与硬反例

### 假设 H1：局部指数线性分支可以在不改本构合同的情况下改善刚性传播

候选应只对可知线性算子做指数/稳定化处理，材料边状态仍由唯一 constitutive plugin 推进，边力仍由稀疏两端点装配得到。

硬反例：若线性分支产生第二力头、绕过权威 `f_edge`，或端点加速度未重新满足 hard EOM，则立即 NO-GO。

### 假设 H2：稀疏局部指数/有理近似可以与 halo 拼接等价

在小图上先证明 full graph 与 edge-partition + owner/ghost synchronization 的 `u/v/a/edge-force/state` 一致，再考虑更大图。

硬反例：任何 dense `E x N` incidence、全局矩阵指数造成的边界泄漏、owner 重排后力不变性失败，或 full-vs-halo 不等价，均停止。

### 假设 H3：刚性稳定化能改善 high-band，而不是只改善低频或平均 R2

必须同时报告 pooled 与 high-band `a/edge-force`，并使用冻结 parent、RK4/Newmark/FEM 参考和严格 common-descent gate。

硬反例：高频指标不改善、任一关键 pooled 目标回退、或只凭 EOM 残差很小而声称成功，均不能晋级。

### 假设 H4：指数/拆分推进仍能保持因果和可审计调用预算

每个区间只能读取当前状态与当前/下一载荷约定允许的输入；必须记录本构调用数、有限梯度、材料状态和 EOM/运动学残差。

硬反例：读取未来轨迹、重复使用相同 current/proposed endpoint、调用数超过合同、或以 post-processing solver 修补端点，均为实现失败而非“训练未收敛”。

## 最小验证顺序

1. 零初始化 parent parity、矩阵边权 shape/device、唯一本构调用和 hard EOM；
2. 线性高刚度振子稳定窗口，与 RK4/Newmark/FEM 做同步对照；
3. linear/bilinear/Bouc-Wen 的有限性、因果性和边状态所有权；
4. full graph 与 partition/halo 的力、状态和端点结果等价；
5. 只有以上合同和反例通过后，才做 calibration-only common-descent M0；不假设其能通过高频或正式准确度门槛。

## 项目决策

本轮结论是“可形成下一候选假设”，不是 GO，也不是文献对结构动力学的直接验证。V28、V30 和 ECASO 的失败记录共同要求：下一候选必须同时证明刚性稳定性、稀疏/halo 等价、权威二阶 EOM、本构状态因果性和严格训练门槛；否则继续保留 V21 physical oracle、RK4/Newmark/FEM reference 与 frozen parent 作为 fallback、误差指示器和验收基线。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
