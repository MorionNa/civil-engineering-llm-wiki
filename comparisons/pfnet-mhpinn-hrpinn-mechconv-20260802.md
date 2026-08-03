---
id: comparison--pfnet-mhpinn-hrpinn-mechconv-20260802
title: PFNet、MH-PINN 与 HRPINN/PHRPINN：硬物理、可迁移性与 MechConv 边界
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-02'
updated: '2026-08-02'
confidence: low
legacy_paper_ids:
- arXiv:2605.07279
- arXiv:2604.19843
- arXiv:2511.23307
- arXiv:2509.01416
- arXiv:2602.12706
- arXiv:2602.19475
legacy_download_status: three_round2_pdfs_sha_verified
legacy_si_status: manifest_v2_audited_no_separate_si
legacy_source_files:
- literature/github_20260802_round2/manifest_combined_20260802_v2.json
- literature/github_20260802_round2/PDFs/Physics-informed_operator_learning_for_transferable_energy-dissipative_microstructure_dynamics.pdf
- literature/github_20260802_round2/PDFs/Mapping-based_Hard-constrained_Physics-Informed_Neural_Networks_for_unbounded_wave_problems.pdf
- literature/github_20260802_round2/PDFs/Hard-Constrained_Neural_Networks_with_Physics-Embedded_Architecture_for_Residual_Dynamics_Learning_and_Invariant_Enforcement_in_Cyber-Physic.pdf
- knowledge/civil-engineering-llm-wiki/comparisons/md-pnop-laplace-matrix-pimo-scalepinn-20260802.md
- knowledge/civil-engineering-llm-wiki/comparisons/mtp-mechconv-v2-a-prime-s4d-m0-negative-20260802.md
- knowledge/civil-engineering-llm-wiki/comparisons/cgerc-v3-m0-negative-20260802.md
- knowledge/civil-engineering-llm-wiki/comparisons/mtp-mechconv-v2-selected-nonintegrated-adapter-screen-v4-negative-20260802.md
legacy_tags:
- physics-informed
- neural-operator
- operator-learning
- hard-constraint-strategies
- boundary-condition
- temporal-causality
- long-horizon-rollout
- autoregressive-rollout
- dissipative-dynamics
- equation-of-motion
- structural-dynamics
- spectral-bias
- pde
---

# 一句话裁决

三篇新论文分别提供了**物理结构化状态推进（PFNet）**、**解析硬边界/远场约束（MH-PINN）**和**硬编码已知动力学加残差学习（HRPINN）**的证据，但没有一篇同时覆盖矩阵边权 MechConv、owned-node/halo 子图、可替换历史本构、独立 `kx+cv+ma=F` 审计和单次快速推理。对当前项目最有价值的不是直接移植网络，而是把“可验证的物理结构”放在 forward 契约中，并把残差校正限制为训练目标或可证伪的内部模块。

## 1. 三篇论文的直接证据

| 论文 | 直接方法证据 | 直接结果/边界 | 对当前 MechConv 的可迁移判断 |
|---|---|---|---|
| PFNet（arXiv:2605.07279） | 以统一变分形式描述 Allen-Cahn/Cahn-Hilliard：正半定 Onsager 算子驱动自由能耗散；用扩散风格 U-Net、循环 padding、状态熵条件和 κ 的 FiLM 调制学习一步演化算子；四通道马氏体任务只扩展输入输出通道（PDF pp. 5-8, 18-22）。 | CH 单步误差约 `1e-5` 量级，长时自回归能保持主要粗化路径；误差主要在弥散界面和拓扑变化区域。模型约 86M 参数，训练是单步监督，推理通过反复自回归；论文没有给出结构动力学四通道 R² 或硬 `kx+cv+ma=F`（PDF pp. 9, 18-22）。 | 可借鉴“通用状态推进器 + 可替换物理/参数条件”的职责分离，以及对界面/突变区域做分层审计；不能把 U-Net 或能量耗散条件当作矩阵边力装配器，也不能据此证明任意图规模或本构历史可替换。^[literature/github_20260802_round2/PDFs/Physics-informed_operator_learning_for_transferable_energy-dissipative_microstructure_dynamics.pdf]
| MH-PINN（arXiv:2604.19843） | 用代数坐标映射把半无限域压缩到有限域；用远场渐近因子、精确距离函数和 envelope 在输出结构中硬编码 Dirichlet/Neumann 与 Sommerfeld 条件，训练损失只保留映射后的 PDE 残差（PDF pp. 6-11）。 | 在声学辐射 `k=1..10` 上相对误差报告为 `7.97e-5..7.46e-4`，`k=20` 为 `2.54e-6`；SH 波峡谷算例采用硬 Neumann，结果与 Null-field BIEM 一致（PDF pp. 13-16, 25-26）。单一全局映射对多体散射不直接适用，作者把域分解列为后续工作（PDF pp. 28-30）。 | 可迁移的是“已知解析结构应进入 forward，而非只进 loss”，以及对高频相位/边界的单独审计；不能把频域波数高频结果等同于结构时域高频，不能直接解决矩阵边权、子图 halo 或本构内部状态。^[literature/github_20260802_round2/PDFs/Mapping-based_Hard-constrained_Physics-Informed_Neural_Networks_for_unbounded_wave_problems.pdf]
| HRPINN/PHRPINN（arXiv:2511.23307） | HRPINN 在递归积分器中硬编码 `f_phys`，网络只学习 `f_unk`；PHRPINN 每步先 predict 再把状态投影到 `g(x)=0` 流形，可用鲁棒非线性 KKT 或快速切空间投影（PDF pp. 8-16）。 | 电池 DAE 中 HRPINN-Large 的 MAE 为 `0.0377`，HRPINN-Small 仅 68 个参数且优于约 10k 参数 NODE；PHRPINN 约束违反可达 `1e-7` 量级，但鲁棒投影可能耗时数小时，刚性算例出现 NaN，且大规模稠密 KKT 为瓶颈（PDF pp. 24-30）。 | 最接近当前“硬动力学 + 学残差”的思想，但必须把投影求解代价纳入推理契约；它支持“本构/未知项作为 plugin”的概念，不支持把 KKT/外部求解器塞进快速端到端 MechConv。^[literature/github_20260802_round2/PDFs/Hard-Constrained_Neural_Networks_with_Physics-Embedded_Architecture_for_Residual_Dynamics_Learning_and_Invariant_Enforcement_in_Cyber-Physic.pdf] |

## 2. 与已有文献和负结果的合并解释

| 机制来源 | 可以保留的部分 | 不能误读为 | 对上一轮失败的解释 |
|---|---|---|---|
| PFNet | 状态条件、参数调制、单步训练/长时自回归分离、跨动力学类型做迁移测试 | “只要加物理条件就能保证守恒或结构力平衡” | A-prime 的 S4D 增加了记忆容量，但独立加速度/力仍未过门；问题不一定是记忆不足，而可能是物理 target/相位条件不足。 |
| MH-PINN | 输出参数化硬编码已知边界/渐近结构；高频单独验证 | “高频波数结果等于结构动力学高频泛化” | 说明高频应显式注入可证明的结构信息；但结构本构的未知历史没有可用的解析渐近因子，不能照搬。 |
| HRPINN/PHRPINN | 已知动力学负责主更新，网络只学残差；约束应在 forward 可审计 | “投影闭合就等于快速端到端” | 与当前 KKT 投影负结果一致：闭合可能非常好，但完整推理成本不可接受；CGERC-v3 还表明高容量残差头可破坏 selected proposal。 |
| MD-PNOP / PILNO / Scale-PINN | 方程重写残差 target、virtual broadband/因果训练权重、序贯 residual curriculum | “训练期残差校正天然是部署期校正器” | A-prime、velocity-adapter 和 CGERC-v3 都支持把 correction 先限在训练 target/课程，避免再加一个不受控 inference head。 |
| 当前负文档 | constructed EOM closure 必须与 independent BDF2/constitutive audit 分离；父模型仍是 selected baseline | “构造出的 `F=kx+cv+ma` R²=1 就证明预测正确” | CGERC-v3 的 `u R²≈0.834`、独立加速度/力 RMS 显著恶化，说明硬闭合可以掩盖状态预测退化；任何新文献机制都必须接受独立物理门。 |

相关证据页：[[md-pnop-2025-equation-recast-neural-operator-preconditioning]]、[[physics-informed-laplace-neural-operator-2026]]、[[scale-pinn-2026-sequential-correction]]、[[mtp-mechconv-v2-a-prime-s4d-m0-negative-20260802]]、[[cgerc-v3-m0-negative-20260802]]、[[mtp-mechconv-v2-selected-nonintegrated-adapter-screen-v4-negative-20260802]]。

## 3. 面向项目要求的逐项裁决

| 项目要求 | 三篇论文提供的证据 | 当前仍缺的证据 |
|---|---|---|
| 矩阵边权 MechConv、子图可扩展 | MH-PINN 讨论未来域分解；PFNet 有周期卷积，但不是不规则结构图 | owned-node/halo 边力装配等价、跨子图本构历史传递、规模扩展实测 |
| 本构可替换 | PFNet 在 CH 与四通道 AC 型任务间保留 backbone；HRPINN 将已知 physics 与 residual 分开 | 线性、双线性、Bouc-Wen/大变形插件在同一 MechConv 契约下的独立测试 |
| 低频与正常结构高频 | MH-PINN 有 `k=1..20` 波动算例；PFNet 有早期/晚期相变阶段 | 结构模态频带、加速度相位、独立力残差和高频最差样本门 |
| 严格 `kx+cv+ma=F` | HRPINN/PHRPINN 对已知 ODE/代数不变量做结构约束 | 本项目的最终边力必须由 MechConv 和可替换本构产生，且独立回放仍要正确 |
| 单次快速推理 | PFNet 是一次一步 forward，MH-PINN 省去边界 penalty；HRPINN 的积分器仍承担主要成本 | 90 序列 median/P95 与 Newmark/FEM 的同口径比较；不得引入 KKT、Krylov 或外部 refinement |

## 4. 知识库级结论

1. **可迁移主原则**：把已知且可证明的结构写入 forward；把未知部分限制为 residual/plugin；把最终力平衡保留在同一个矩阵边 MechConv 装配路径。
2. **训练原则**：PFNet 的状态/参数条件、PILNO 的宽频 virtual input、Scale-PINN 的序贯 residual curriculum 可以进入训练设计，但不能作为“推理时额外校正”的许可证。
3. **负知识**：PHRPINN 的 KKT 投影、MD-PNOP 的 PDE solver、PhysicsCorrect/残差校正器都说明“残差降低”和“快速单次部署”是不同目标；当前项目应继续以 selected parent 为基线，任何新候选先证明 independent acceleration/force 不恶化，再谈精度提升。
4. **本轮不授权实现**：本文件只完成证据归档和审计合并，不改变模型代码，也不把 PFNet、MH-PINN 或 HRPINN/PHRPINN 宣称为当前 MechConv 候选。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.
