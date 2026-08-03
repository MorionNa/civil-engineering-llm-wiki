---
id: comparison--md-pnop-laplace-matrix-pimo-scalepinn-20260802
title: MD-PNOP、PILNO、矩阵预条件、PIMIONet 与 Scale-PINN：面向失败 MechConv 方案的可执行比较
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-02'
updated: '2026-08-02'
confidence: low
legacy_paper_ids:
- arXiv:2509.01416v1
- arXiv:2602.12706
- arXiv:2508.03421
- arXiv:2505.07090
- arXiv:2602.19475
legacy_download_status: five_local_pdfs_verified
legacy_si_status: manifest_complete_only_for_md_pnop
legacy_source_files:
- literature/github_20260802_next/manifest.json
- literature/github_20260802_next/PDFs/Accelerating_PDE_Solvers_with_Equation-Recast_Neural_Operator_Preconditioning.pdf
- literature/github_20260802_next/PDFs/Physics-Informed_Laplace_Neural_Operator_for_Solving_Partial_Differential_Equations.pdf
- literature/github_20260802_next/PDFs/A_matrix_preconditioning_framework_for_physics-informed_neural_networks_based_on_adjoint_method.pdf
- literature/github_20260802_next/PDFs/Physics-informed_Multiple-Input_Operators_for_efficient_dynamic_response_prediction_of_structures.pdf
- literature/github_20260802_next/PDFs/Scale-PINN_Learning_Efficient_Physics-Informed_Neural_Networks_Through_Sequential_Correction.pdf
legacy_github_status: four_repositories_cloned_and_checked
legacy_tags:
- mechconv
- structural-dynamics
- residual-target
- equation-recast
- causal-weighting
- preconditioning
- high-frequency
- replaceable-constitutive
---

# 面向当前失败方案的证据比较

## 1. 当前问题边界

上一轮 A′ 的 causal S4D residual head 已经满足速度、响应和两次本构调用/推理速度门，但独立加速度 RMS 约 `0.03402`、独立力 RMS 约 `0.04944`，仍高于 `0.030/0.045`。因此本轮最重要的问题不是继续增加记忆容量，而是让网络学习**可审计的残差目标**，并改善多尺度/高频残差的优化条件，同时保持：

- matrix-edge MechConv 是最终边力装配器；
- constitutive plugin 可替换且不改变主干契约；
- `a` 由硬 EOM 构造，最终输出满足 `kx+cv+ma=F`；
- 单次端到端推理不引入 KKT、Krylov、Newmark 或外部校正器；
- owned-node/halo 子图输出可拼接。

## 2. 证据到动作的矩阵

| 来源 | 直接方法证据 | 下一轮可执行动作 | 不能直接承诺 |
|---|---|---|---|
| MD-PNOP | 将参数偏离残差重写为源项；神经算子提供改进候选，传统求解器最终恢复物理；报告约 50% 求解时间下降 | 以 proposal 的 `r_F` 为输入，构造真实 `delta_v*`/`delta_a*` 监督 target；校正后只重新走一次 MechConv + EOM | 原论文物理保证依赖迭代 PDE solver；不是单次结构推理、不是可替换本构证明 |
| PILNO | pole-residue 瞬态 + Fourier 稳态；virtual broadband inputs；时间因果残差加权 | 训练期加入随机相位/频带/初值的 virtual excitation；按早期瞬态、共振峰、高频相位给 `r_F` 与 `a` 加权 | LNO/PILNO 没有矩阵边权、halo 子图或结构本构历史；非因果 FFT 不能直接用于 inference |
| Matrix preconditioning PINN | AD + matrix coloring 得 Jacobian；ILU 缩放 PDE residual；adjoint 解决梯度兼容 | 用 edge/node/time block 的近似 Jacobian 作为训练期 residual/gradient preconditioner；先不把 ILU solve 放入 inference | 改善条件数不等于硬 EOM；动态非线性本构 Jacobian 不能固定；没有 MechConv 扩展证明 |
| PIMIONet | 第二 trunk 编码时间；连续空间/时间查询；预计算 M/C/K 动力平衡；Schur reduced domain | 增加独立 time/frequency query 与 reduced-graph 训练组织，之后用全图 MechConv/EOM 审计 | 固定 M/C/K 不覆盖 Bouc–Wen/大变形；reduced domain 不自动等于 halo 等价；FEM/亚秒结果不可直接转成项目门 |
| Scale-PINN | 将序贯 residual correction 纳入 PINN 训练，强调训练效率 | 用低频→高频→独立力的 curriculum；每阶段更新 residual target/权重，保持同一个硬物理 forward | 训练加速不等于推理加速；本轮 GitHub commit 无 Python 源码，不能据代码复现 |

## 3. 最值得立即实施的组合

### 3.1 监督 residual target，而非更大 SSM

对冻结或轻微可训练的 selected proposal，先计算：

\[
r_F^{(p)}=F_{ext}-\{f_{int}(u^{(p)},z^{(p)})+Cv^{(p)}+Ma^{(p)}\}.
\]

从真实轨迹构造与 proposal 对齐的 `delta_v*`、`delta_a*`，或用局部线性化得到受限的 `delta_v*`。新 head 只预测状态/速度校正，不直接生成 `f_int`。校正后必须由同一个 constitutive plugin、MechConv 和硬 EOM 重算；这样监督信号能降低独立加速度/力 RMS，却不破坏力的来源。

这与 MD-PNOP 的“残差重写为源项”同构，但把传统 solver 的在线迭代改成**离线 teacher target + 单步 neural correction**。必须在数据切分上避免未来时间或真实答案泄漏；virtual input 只能提供 physics-only residual，不能被当作测试标签。

### 3.2 因果宽频训练

借用 PILNO 的 virtual-input 与 causal weighting：

1. 低频、结构正常高频、随机窄带、宽带 chirp、随机相位和不同初值分层采样；
2. 对早期瞬态、共振邻域、Nyquist 前最后一段频带分别统计 `u/v/a/edge_force` 与 `r_F`；
3. 让早期时间残差权重较大并逐步退火，避免直接用全时段均匀权重掩盖相位错误；
4. 加入 PIMIONet 式 time/frequency query，但 query 只能调制 proposal/history，不可跳过边力装配。

### 3.3 训练期预条件，不增加推理求解器

用 Matrix-preconditioning PINN 的思想，根据 MechConv 的稀疏矩阵边结构构造轻量 block 预条件。候选是节点块、边块和时间块的对角/低秩近似，作用在 residual loss 或梯度上；Jacobian coloring/ILU 只在训练期或离线审计使用。若它需要每个推理样本求解三角系统、Krylov 或 KKT，则不属于默认方案。

### 3.4 序贯课程

Scale-PINN 的可迁移部分是训练顺序而不是额外 inference solver：

```text
proposal/低频监督
        ↓
宽频与初值 virtual residual
        ↓
监督 delta_v/delta_a + 独立力 residual
        ↓
冻结主干审计：本构、MechConv、硬 EOM、子图、速度
```

每个阶段都要保留同一个两次本构调用契约；若阶段性校正只在训练后处理脚本中有效，不能进入候选。

## 4. 不能直接满足项目要求的共性原因

- **物理一致性层级不同**：PILNO/Scale-PINN 的 PDE residual loss 是软约束；MD-PNOP/PIMIONet 的“物理”来自求解器或预计算线性矩阵；都不能替代本项目的硬 EOM。
- **结构图接口缺失**：五篇论文都没有同时证明矩阵边权、owned-node/halo 拼接和任意规模子图训练/推理。
- **本构不可替换**：固定 M/C/K、线性 PDE Jacobian 或频响数据不能直接覆盖带内部状态的 Bouc–Wen、双线性和大变形。
- **推理速度证据不等价**：论文的 solver iteration reduction、亚秒 FEM surrogate 或训练时间下降，不等于 90 条序列上的单次 forward median/P95 门。
- **频域/因果风险**：pole-residue/Fourier 能改善频谱表示，但非因果操作可能让未来扰动影响当前输出；必须保留 prefix perturbation 审计。

## 5. 下一候选的硬契约

候选可以叫作“Residual-Targeted Causal MechConv（RT-Causal-MechConv）”，但只有在实现后才可使用该名称。候选至少要满足：

1. correction target 由已保存 proposal/真值生成并可复核；
2. correction head 不直接输出边力，不拥有 constitutive state；
3. 同一 forward 最多两次 constitutive call，最终边力由 MechConv 装配；
4. `r_F`、`u-v`、EOM、causal prefix、halo stitching 和 plugin read-only 均有本地测试；
5. remote single-screen 才能检验独立 acceleration `≤0.030`、independent force `≤0.045`、高频和速度；
6. 任意外部 refinement 只能作为离线审计，不可用来包装失败结果。

## 6. 裁决

本轮文献支持的新方向是“**监督 residual target + 因果宽频训练 + 训练期残差预条件 + 序贯课程**”。它比继续扩大 A′ 的 SSM 更直接地针对失败门，但尚未证明可行；在用户允许进入下一轮实验前，不应宣称满足全部目标。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
