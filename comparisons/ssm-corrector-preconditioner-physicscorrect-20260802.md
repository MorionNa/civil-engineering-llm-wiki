---
id: comparison--ssm-corrector-preconditioner-physicscorrect-20260802
title: 长记忆 SSM、残差校正、神经预条件与 PhysicsCorrect：面向 MechConv PINN 的证据比较
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-02'
updated: '2026-08-02'
confidence: low
legacy_paper_ids:
- arXiv:2507.02227v2
- arXiv:2502.01337v2
- arXiv:2507.23428v5
- arXiv:2409.03231v2
- arXiv:2306.12047v3
legacy_download_status: all_open_access_downloaded
legacy_si_status: all_not_found
legacy_source_files:
- papers/literature_20260802_next/PhysicsCorrect_2026/manifest.json
- papers/literature_20260802_next/PhysicsCorrect_2026/PDFs/PhysicsCorrect_A_Training-Free_Approach_for_Stable_Neural_PDE_Simulations.pdf
- papers/literature_20260802_next/Neural_Preconditioning_Operator_2025/manifest.json
- papers/literature_20260802_next/Neural_Preconditioning_Operator_2025/PDFs/Neural_Preconditioning_Operator_for_Efficient_PDE_Solves.pdf
- papers/literature_20260802_next/ST_SSM_2025/manifest.json
- papers/literature_20260802_next/ST_SSM_2025/PDFs/Merging_Memory_and_Space_A_Spatiotemporal_State_Space_Neural_Operator.pdf
- papers/literature_20260802_next/State_Space_Neural_Operator_2024/manifest.json
- papers/literature_20260802_next/State_Space_Neural_Operator_2024/PDFs/State-space_models_are_accurate_and_efficient_neural_operators_for_dynamical_systems.pdf
- papers/literature_20260802_next/Residual_Error_Corrector_2024/manifest.json
- papers/literature_20260802_next/Residual_Error_Corrector_2024/PDFs/Residual-Based_Error_Corrector_Operator_to_Enhance_Accuracy_and_Reliability_of_Neural_Operator_Surrogates_of_Nonlinear_Variational_Boundary-.pdf
legacy_github_status: clone_failed_no_code_retrieved
legacy_github_sources:
- https://github.com/summerwine668/PhysicsCorrect
- https://github.com/zheyuanhu01/State_Space_Model_Neural_Operator
- https://github.com/neuraloperator/neuraloperator
legacy_tags:
- neural-operator
- mechconv
- state-space-model
- residual-correction
- preconditioning
- scalability
- high-frequency
---

# 长记忆 SSM、残差校正、神经预条件与 PhysicsCorrect：面向 MechConv PINN 的证据比较

## 1. 一句话结论

这 5 篇文献分别覆盖“记住长时间历史”“把残差变成误差校正”“用神经算子降低线性求解迭代数”“缓存固定 Jacobian 做训练免调修正”四类机制；对本项目最有价值的组合是 **SSM 作为非物理的长记忆表示 + MechConv/可替换本构负责边力与装配 + 预条件/残差算子用于训练或离线审计**，而不是把外部校正器或 Krylov 求解器放进默认端到端 forward。

## 2. 证据矩阵：论文直接报告了什么

| 机制 | 论文直接证据 | 成本/边界 | 与本项目的直接关系 |
|---|---|---|---|
| 长记忆 SSM（SS-NO） | S4D/SSM 以线性递推或因果卷积建模时空依赖；可学习阻尼、频率，双向空间扫描；KS、Navier–Stokes、Euler 上报告相对 L2 优势（SS-NO PDF pp.3–13） | 长序列训练的梯度内存仍增长；扫描有方向偏置；不规则网格原生扩展未解决（p.38） | 可作为 MechConv 前的历史编码器，但不自动满足 EOM 或子图接口守恒 |
| Mamba 动力算子 | Mamba 用选择性 SSM 学习 ODE 长时积分；序列长度 32,768 时仍可训练，标准 Transformer 在较长长度 OOM；部分无阻尼/高频案例 LNO 更好（Mamba PDF pp.15–18） | 结果主要是 ODE/PK-PD；训练线性成本不等于一次推理成本；physics-only 在 PK-PD 失败（p.30） | 适合作为 causal history channel；必须把力闭合留在 MechConv/EOM |
| Residual-Based Error Corrector | 对 \(R(m,u)=0\) 解一次 \(\delta_uR(e_C)=-R\)，在局部可获得二次误差界；SVD reduced space 降低网络维度；reaction–diffusion/拓扑优化误差显著下降（PDF pp.5–7、10–27） | 外部线性变分求解，不是一次网络输出；局部可逆/小误差假设；换本构需重建 Jacobian | 适合训练期残差监督、局部 Jacobian 审计，不适合作为默认实时矫正器 |
| Neural Preconditioning/NAMG | 学习 \(M\approx A^{-1}\)，以 condition/residual/data loss 作为 Krylov 预条件；多重网格分担高/低频误差；在 128 训练、4096 测试中保持较温和迭代增长（PDF pp.3–12） | 求解阶段仍需 CG/GMRES 迭代；理论依赖 SPD、多重网格 approximation property 等假设；实验非结构动力学 rollout | 可用于训练 teacher、固定次数子图 refinement 或离线 coarse operator；不能直接等同端到端推理 |
| PhysicsCorrect | 用 PDE 残差线性化求 \(J^\dagger b\)，缓存 Jacobian/伪逆；报告 200 步修正仅 `0.90 vs 0.69 s`，但网格时间/显存二次增长（PDF pp.3–7） | 线性化需 proposal 足够好；离散残差零点与参考解有差异；高分辨率 Jacobian 是瓶颈 | 可做固定线性 EOM 的离线诊断/监督；上一轮项目 KKT 投影约 33 s，说明默认推理路径不可接受 |

## 3. 适配当前 MechConv 架构的分层职责（项目推论）

```text
节点状态/外力/本构历史
        │
        ▼
SSM/Mamba causal history encoder（只产生时序特征）
        │
        ├── 可替换 constitutive plugin：linear / bilinear / Bouc–Wen ...
        │       └── edge deformation, edge velocity, internal state → edge force
        ▼
matrix-edge MechConv：按 owned-edge/halo 计算矩阵消息并以 Bᵀ 装配
        │
        ▼
硬 EOM 构造：a = M⁻¹(F_ext − C v − f_edge)，或等价的结构动力学头
        │
        └── residual/Jacobian/preconditioner 仅用于训练诊断或离线审计
```

这里的职责划分是本项目推论，不是任何一篇论文的直接结论。关键不变量是：换本构只替换 plugin；MechConv 仍是最终边力装配；SSM 不得绕过 `kx+cv+ma=F` 生成未经装配的力；子图只交换 halo，owned-edge 计数和接口装配规则不变。

## 4. 长记忆、高频与跨分辨率的综合判断

### 长记忆

SS-NO 的 Appendix K 以 Mori–Zwanzig 直觉解释粗网格动力学为何需要历史记忆；Mamba 的长时间摆实验也显示线性序列成本与更温和的误差增长。**项目推论**：对当前结构动力学，SSM 可能帮助表示未解析的历史本构、外力相位和低分辨率 aliasing，但它应接收明确的时间方向和初始状态，并保留 causal 版本作为默认审计对象。

### 高频

SS-NO 的可学习频率和阻尼、PhysicsCorrect 对波动方程改用二阶时间差分，都提示高频需要与动力学阶数/谱结构匹配。另一方面，Mamba 论文明确报告了无阻尼或高频/混沌案例中 LNO 有时更优。**项目推论**：任何 SSM 候选都必须同时审计高频 `u/v/a/edge_force`、相位漂移、Nyquist 附近能量和独立 EOM，而不能只看 pooled R² 或相对 L2。

### 跨分辨率与大图

NPO 的 128→4096 预条件实验、SS-NO 的固定参数量跨分辨率结果是积极证据，但两者都不是任意图子划分等价性证明。SS-NO 自己把原生 graph/mesh scan 列为未来工作；PhysicsCorrect 则报告 Jacobian 随分辨率二次增长。**项目推论**：优先把跨分辨率验证落在 MechConv 的 owned-edge/halo 契约上，再评估 SSM 的状态是否可以在子图边界以可复现方式传递。

## 5. 端到端和推理成本裁决

| 路线 | 是否默认端到端 | 是否需要额外迭代/线性解 | 当前用途裁决 |
|---|---:|---:|---|
| SS-NO/Mamba encoder + MechConv/EOM | 可以设计为是 | 否（若不加校正） | 主要候选，但需重新证明物理闭合与高频 |
| Residual corrector | 否 | 是，一次线性变分解 | 训练/审计；不作为默认 forward |
| NPO/NAMG | 否 | 是，CG/GMRES 迭代 | 训练 teacher、离线 coarse/preconditioner；不作为默认 forward |
| PhysicsCorrect | 否 | 是，残差计算和线性校正；缓存后仍有投影乘法 | 固定线性残差诊断；高分辨率需谨慎 |

本项目当前已有的外部 KKT 投影实验显示：严格闭合可以实现，但完整 forward 约 33 s，远超已有 selected 预测器的约 0.58 s。因此不能因为文献中的 PDE 校正误差下降就放宽本项目的推理速度门槛。

## 6. 推荐的知识库级候选与失效条件（项目推论）

**候选**：在冻结 selected 物理头语义的前提下，仅替换/增加一个 causal SSM history encoder；本构 plugin、矩阵边权 MechConv、硬 EOM 和输出尺度保持不变。训练目标仍同时包含四通道监督、构造力平衡和独立力平衡；SSM 只通过 latent history 改善 proposal，不直接输出 closure force。

**必须先过的证伪门**：

1. local shape/device/loss/subgraph smoke；
2. selected response pooled floor 与最差样本 floor；
3. constructed/independent force balance、kinematic consistency；
4. independent acceleration/force RMS；
5. 高频频带及跨本构（至少 linear/bilinear/Bouc–Wen）；
6. 端到端 forward median/P95 不得退化到外部求解器量级。

**至少两个可能失败原因**：SSM 记忆会把本构历史与数据集分布绑定，换本构后状态语义失配；时序扫描或频率调制会改善 pooled 位移却损伤加速度相位；子图边界若没有可复现状态协议，会破坏 MechConv 的接口等价；以及保留的硬 EOM 可能让新增 latent 只能做极小修正，无法改善独立残差。

## 7. GitHub 状态记录（本轮运行证据）

| 仓库 | 网页 URL | clone 状态 | 结论 |
|---|---|---|---|
| PhysicsCorrect | https://github.com/summerwine668/PhysicsCorrect | 连接重置/超时 | 未拉取代码 |
| State Space Model Neural Operator | https://github.com/zheyuanhu01/State_Space_Model_Neural_Operator | 连接超时/重置 | 未拉取代码 |
| neuraloperator | https://github.com/neuraloperator/neuraloperator | 连接超时/重置 | 未拉取代码 |

网页 URL 仅保留为后续更新检查入口；本轮没有任何仓库代码进入工作区，不能以仓库实现作为证据。

## 8. 结论边界

这批文献支持“长记忆、残差线性化、预条件和谱/多尺度处理值得作为模块候选”，但没有任何一篇直接证明本项目的完整目标：矩阵边权 MechConv + 任意子图可扩展 + 可替换历史本构 + 低/高频四通道 R² + 独立 `kx+cv+ma=F` + 端到端快于 Newmark/FEM。后续若进入模型实验，必须以项目现有 selected/V21 指标为基线并严格 fail-closed；本轮仅完成知识归档，没有写模型代码或跑训练。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
