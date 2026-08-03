---
id: comparison--fbpinn-xpinn-structgraph-pignn-transfer-boundaries
title: FBPINN / XPINN / StructGraph-Dyna / PI-GNN：对 MTP-MechConv 的迁移边界
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-01'
updated: '2026-08-01'
confidence: low
legacy_tags:
- comparison
- architecture-selection
- transfer-learning
- limitation
- physics-informed
- pinn
- spatial-partitioning
- message-passing
- structural-dynamics
- parallel-computing
legacy_sources:
- papers/literature_20260801/FBPINN_2107.07871/manifest.json
- papers/literature_20260801/FBPINN_2107.07871/PDFs/FBPINN_Scalable_Domain_Decomposition.pdf.pdf
- papers/literature_20260729/01_multilevel_fbpinn/manifest.json
- papers/literature_20260729/01_multilevel_fbpinn/PDFs/Multilevel_domain_decomposition-based_architectures_for_physics-informed_neural_networks.pdf
- papers/literature_20260729/02_enforced_interface_dpin/manifest.json
- papers/literature_20260729/02_enforced_interface_dpin/PDFs/Enforced_Interface_Constraints_for_Domain_Decomposition_Method_of_Discrete_Physics-Informed_Neural_Networks.pdf
- literature/github/StructGraph-Dyna/README.md
- literature/github/StructGraph-Dyna/main.py
- literature/github/StructGraph-Dyna/configs/design_space_result.yaml
- literature/github/soft-tissue-pignn/README.md
- literature/github/soft-tissue-pignn/models.py
- papers/literature_20260729/04_modular_elastoplasticity/manifest.json
- papers/literature_20260729/04_modular_elastoplasticity/PDFs/Modular_machine_learning-based_elastoplasticity_generalization_in_the_context_of_limited_data.pdf
---

# 迁移结论

本页只把文献和仓库中已经观察到的机制迁移到本项目的结构动力学图网络语境；它不把 PDE 坐标域、固定几何软组织、门框图或一维/单轴材料试验的结果外推成 MTP-MechConv 已经验证的结果。FBPINN 的下载 manifest 记录的实际文件名是重复 `.pdf` 的路径；用户给出的无重复后缀路径不存在，因此以下 FBPINN 证据以实际文件和 manifest 为准。^[papers/literature_20260801/FBPINN_2107.07871/manifest.json]

| 方法 | 可迁移点 | 不能外推点 | 对本项目的失败边界 |
|---|---|---|---|
| FBPINN | 重叠局部网络、局部归一化、窗口加和；用局部计算缓解高频/多尺度训练困难；多层版本用粗层补全远距离通信。 | 它的基函数定义在坐标子域，不能直接替代结构图的矩阵边、质量/刚度语义或状态拼接；多层扩展的 scaling 证据来自 PDE/子域实验，不等于任意结构图可扩展。 | 粗层若抹平高频，或 pooling/prolongation 改变边界与状态含义，局部高频和动力学守恒会丢失；不能把单 GPU 或规则子域结果写成通用大图证明。 |
| XPINN / 接口约束 dPINN | 把子域接口连续性、位移/能量耦合写成显式契约；接口约束应独立于局部网络优化，并可成为门控。 | XPINN 的弱接口损失不等于离散结构图上的精确矩阵装配；EIC-dPINN 依赖有限元式离散、Gaussian quadrature 与位移接口，不能直接证明速度/加速度/内部力的全状态连续。 | 只惩罚或只预测接口位移，会留下速度、加速度、内力和本构状态的接口断层；接口 loss 下降也不能证明全局动力学闭合。 |
| StructGraph-Dyna | 使用 PyG/GraphGym 的模块化图训练管线；节点/边特征、消息传递、图级回归和配置化实验可作为工程骨架；固定图上的边消息可承载局部结构上下文。 | README 的门框示例依赖外部数据集；`main.py` 只是 GraphGym 通用训练入口，配置中 `add_pinn: false`，不能据此声称已验证 PINN 物理约束、跨拓扑泛化或本项目的 RK4Z 接口。 | 仅用 MSE 图级回归或通用 message passing，可能学到输出拟合而非 EOM/本构/边界闭合；固定数据集、固定拓扑和未公开的训练数据不足以支撑大规模结构迁移。 |
| PI-GNN（soft-tissue-pignn） | `models.py` 的 primal graph emulator 提供 encoder–processor–decoder 分解；消息的反向符号聚合显式编码局部动量守恒；固定几何时可缓存 latent，再按全局参数解码。 | README 明确固定几何假设；数据是软组织/梁等特定几何，输入输出和 constitutive law 不能直接换成 MTP 的结构动力学状态；缓存 latent 不能处理拓扑、边界或本构插件变化。 | 只在固定几何和训练分布内使用 latent decoder；几何、边界、材料或载荷路径变化时，必须重新验证消息守恒、边界调整和状态可观测性，不能把“物理感知”当成通用稳定性证明。 |

## 对下一架构的可执行取舍

1. 保留 FBPINN/多层 FBPINN 的“局部计算 + 粗层通信”思想，但将窗口/子域替换成不改变矩阵边、owner/separator 和 halo 语义的图分块；粗层只提供上下文，不替代细层的边力和本构计算。^[papers/literature_20260729/01_multilevel_fbpinn/PDFs/Multilevel_domain_decomposition-based_architectures_for_physics-informed_neural_networks.pdf]
2. 采用 XPINN/EIC 的接口契约思想，但接口对象必须至少区分位移、速度、加速度、内力和本构状态；硬装配/确定性 carrier 优先于把接口一致性全部交给一个软 loss。^[papers/literature_20260729/02_enforced_interface_dpin/PDFs/Enforced_Interface_Constraints_for_Domain_Decomposition_Method_of_Discrete_Physics-Informed_Neural_Networks.pdf]
3. 借用 StructGraph-Dyna 的配置化 GraphGym 工程结构和 PI-GNN 的反向边消息，但不能照搬其 MSE 训练目标或固定几何 latent 缓存；本项目的验收必须单列独立的运动学、EOM、接口和本构门。^[literature/github/StructGraph-Dyna/configs/design_space_result.yaml]
4. 将模块化弹塑性中的“可替换本构组件 + 热力学硬约束”作为插件边界：数据不足时保留解析组件，学习组件只承担证据支持的部分；它在单轴/循环材料数据上的外推不等于多自由度结构响应外推。^[papers/literature_20260729/04_modular_elastoplasticity/PDFs/Modular_machine_learning-based_elastoplasticity_generalization_in_the_context_of_limited_data.pdf]

## 未获取状态

本批资料中 PPINN / Parallel-PINN 仅作为待获取的相关路线记录；没有把它们写成已下载全文、已复核实现或已验证基线，因此不据此作数值、速度或稳定性结论。^[papers/literature_20260729/02_enforced_interface_dpin/PDFs/Enforced_Interface_Constraints_for_Domain_Decomposition_Method_of_Discrete_Physics-Informed_Neural_Networks.pdf]

## 关联页面

- [[fbpinn]]：FBPINN 的局部窗口、频谱偏差和图迁移边界
- [[multilevel-fbpinn]]：多层粗细通信与 pooling/prolongation 约束
- [[mtp-mechconv-v2-v20-rk4z-design-evidence]]：V20 carrier 与确定性最终平衡
- [[mtp-v20-v19-negative-knowledge-architecture]]：V19/V20.2 负知识对架构的直接约束

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.
