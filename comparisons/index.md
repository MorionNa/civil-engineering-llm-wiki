---
id: comparisons--index
title: Comparisons
type: index
status: active
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-07-31'
updated: '2026-08-03'
confidence: high
---

# Comparisons

- [[mtp-mechconv-v2-mdof50-galerkin-pivot]] — 50DOF 运动学瓶颈、独立因果本构回放与 Galerkin 矩阵粗层转向
- [[mtp-mechconv-v2-experiment-ledger]] — 独立物理复评、矩阵块自由度、因果本构和稀疏多层实现账本
- [[mtp-mechconv-v2-evidence]] — 五篇全文对时间并行、reach、粗层、halo、本构与速度的采用/拒绝矩阵
- [[mtp-mechconv-v2-grill-audit]] — 反方审查后 v2.1 的物理独立审计、数据锁定和可证伪门槛
- [[project-scheme-ingest-manifest-2026-08-03]] — 133 份方案/结果文档与 9 个复现家族的全量入库清单
- [[current-structural-pinn-ranking-2026-08-03]] — 当前性能排名及用户六项目标的逐项判定
- [[baseline-unified-r2-reassessment-2026-08-03]] — PhyLSTM3 与 CM-PINN 的统一 R² 复算
- [[inference-speed-evidence-2026-08-03]] — 5DOF、50kDOF、物理 oracle 与 OpenSeesPy 的速度证据边界
- [[one-structure-one-model-contract-2026-08-03]] — 一结构一模型与同结构加载泛化合同
- [[fixed-mdof5-mtp-strict-label-free-v1-nogo-20260803]] - Strict label-free MTP negative result for one fixed 5DOF structure and one random model

对比分析：并排比较不同方法、模型的性能与适用场景。

- [[scan-vs-hash-sparse-mpm]] — CPU 扫描式与 GPU 哈希式活跃网格构造的架构适配对比
- [[seisgpt-vs-phylstm-cm-pinns]] — 三类物理信息结构响应预测范式的机制、数据、泛化和选型对比

<!-- AUTO-REGISTRY:START -->

## Complete Registry

- [[comparisons/baseline-unified-r2-reassessment-2026-08-03]] — PhyLSTM3 与 CM-PINN 的统一 R² 复算
- [[comparisons/current-structural-pinn-ranking-2026-08-03]] — 当前结构动力学 PINN 排名与六项目标差距（2026-08-03）
- [[comparisons/inference-speed-evidence-2026-08-03]] — 推理效率证据：学习模型、物理 oracle 与 OpenSeesPy 缺口
- [[comparisons/one-structure-one-model-contract-2026-08-03]] — 一结构一模型：当前结构动力学 PINN 的适用边界
- [[comparisons/project-scheme-ingest-manifest-2026-08-03]] — nonlinear-pinn 全量方案与复现入库清单（2026-08-03）

- [[comparisons/cdno-d-corrected-remote-code-failclosed-20260802]] ? CDNO-D corrected remote attempt — code-interface failure (2026-08-02)
- [[comparisons/cdno-d-formal-v2-parent-source-sync-result-20260802]] ? CDNO-D formal v2: parent-source-sync result (2026-08-02)
- [[comparisons/cdno-d-full-nonlinear-teacher-remote-failclosed-20260802]] ? CDNO-D full nonlinear teacher — 2026-08-02 comparison entry
- [[comparisons/cgerc-v3-m0-negative-20260802]] ? CGERC-v3 M0 negative result（2026-08-02）
- [[comparisons/chart-cnr-o0-audit-20260802]] ? CHaRT-CNR-O0 audit: conditional stability is not nonlinear validity — 2026-08-02
- [[comparisons/chart-fold-m0-hold-20260802]] ? CHaRT-Fold-M0: design hold, not a training result — 2026-08-02
- [[comparisons/chart-sr-n0-audit-20260802]] ? CHaRT-SR-N0 stateful replay audit
- [[comparisons/cmej2-m0-negative-20260802]] ? CMEJ²-M0 negative result — 2026-08-02
- [[comparisons/cycle10_v22_causal-proposal-sensitivity-20260802]] ? Cycle 10 — V22 causal proposal sensitivity audit (2026-08-02)
- [[comparisons/cycle11_v23_pact-evidence-and-contract-20260802]] ? Cycle 11 — V23 PACT-MechConv evidence and contract (2026-08-02)
- [[comparisons/cycle11_v23_pact-result-20260802]] ? Cycle 11 — V23-PACT result (2026-08-02)
- [[comparisons/cycle12_v24_psg-evidence-and-contract-20260802]] ? Cycle 12：V24-PSG-MechConv 证据与契约
- [[comparisons/cycle12_v24_psg-result-20260802]] ? Cycle 12：V24-PSG-MechConv 实测结果
- [[comparisons/cycle13_v25_cclro-evidence-20260802]] ? Cycle 13：V25-CCLRO-MechConv 证据与裁决
- [[comparisons/cycle13_v25_cclro-result-20260802]] ? Cycle 13：V25-CCLRO-MechConv 证据与裁决（2026-08-02）
- [[comparisons/cycle14_v26-literature-evidence-20260803]] ? Cycle14 V26 文献证据卡：NPO / Jha corrector / NOEM
- [[comparisons/cycle14_v26_rcpp-result-20260803]] ? Cycle 14：V26-RCPP-MechConv 结果
- [[comparisons/cycle15_v27_cdno-d-evidence-20260803]] ? Cycle 15：V27-CDNO-D Teacher-Compiled MechConv 证据卡
- [[comparisons/cycle15_v27_cdno-d-result-20260803]] ? Cycle 15：V27-CDNO-D 结果与否证
- [[comparisons/cycle16_v28-block-causal-state-flow-result-20260803]] ? Cycle 16 — V28 Block-Causal State-Flow result (2026-08-03)
- [[comparisons/cycle17_v29-pimc-sol-grill-result-20260803]] ? Cycle 17 — V29 PIMC Sol grill result (2026-08-03)
- [[comparisons/cycle18_v30-lfct-remote-result-20260803]] ? Cycle 18 — V30 LFCT remote result (2026-08-03)
- [[comparisons/cycle19_ceic_m0_20260803]] ? CEIC M0：守恒边冲量坐标（2026-08-03）
- [[comparisons/cycle19_ceic_m0_integration_result_20260803]] ? CEIC M0 集成结果（2026-08-03）
- [[comparisons/cycle19_ceic_remote_screen_result_20260803]] ? CEIC 远程 screen 结果（2026-08-03）
- [[comparisons/cycle20_dhkr_design_20260803]] ? DHKR：离散谐波运动残差设计（2026-08-03）
- [[comparisons/cycle20_dhkr_formal_result_20260803]] ? Cycle 20 DHKR formal result
- [[comparisons/cycle20_dhkr_m0_integration_result_20260803]] ? DHKR M0 集成结果（2026-08-03）
- [[comparisons/cycle20_dhkr_remote_screen_result_20260803]] ? Cycle 20 DHKR remote screen status
- [[comparisons/cycle21_egtp_sol_nogo_20260804]] ? Cycle 21 EGTP review: NO-GO
- [[comparisons/cycle21_literature_evidence_20260804]] ? Cycle 21 literature evidence
- [[comparisons/cycle22_pcil_design_20260804]] ? Cycle 22 PCIL design
- [[comparisons/cycle22_pcil_sol_nogo_20260804]] ? Cycle 22 PCIL review: NO-GO
- [[comparisons/cycle23_literature_evidence_20260803]] ? Cycle 23 evidence note: shared local physical representations
- [[comparisons/cycle23_scfp_m0_nogo_20260803]] ? Cycle 23 SCFP M0 audit: rejected
- [[comparisons/cycle24_dpsm_real_gate_nogo_20260803]] ? Cycle 24 DPSM audit: rejected
- [[comparisons/cycle25_galerkin_coarse_sol_nogo_20260803]] ? Cycle 25 Galerkin coarse transport: rejected
- [[comparisons/cycle26_eces_p_evidence_nogo_20260803]] ? Cycle 26 ECES-P audit: rejected for insufficient evidence
- [[comparisons/cycle27_parent_feasibility_audit_nogo_20260803]] ? Cycle 27 feasibility audit: parent Pareto conflict
- [[comparisons/cycle28_independent_parent_baseline_nogo_20260803]] ? Cycle 28 — independent parent baseline NO-GO
- [[comparisons/cycle29_bcpa_m0_nogo_20260803]] ? BCPA M0 decision record — 2026-08-03
- [[comparisons/cycle3-energy-conservation-corrector-20260802]] ? Cycle 3 evidence note: energy consistency, exact invariants, and residual correctors
- [[comparisons/cycle32_endpoint_sparse_operator_20260803]] ? Cycle 32 evidence refresh: endpoint mechanics and sparse temporal operators
- [[comparisons/cycle33_stiff_split_exponential_20260803]] ? Cycle 33: Stiff Split and Exponential Methods — Transfer Audit (2026-08-03)
- [[comparisons/cycle34_variational_impulse_mechconv_20260803]] ? Cycle 34: Variational and Symplectic Impulse Operators for MechConv (2026-08-03)
- [[comparisons/cycle35_github_prnn_pignn_refresh_20260803]] ? Cycle 35 GitHub refresh: PRNN and physics-informed GNN
- [[comparisons/cycle35_lco_rk8_state_space_20260803]] ? Cycle 35: LCO-RK8(4)-MechConv and causal state-space evidence
- [[comparisons/cycle35_rk84_addendum_20260803]] ? Cycle 35 addendum: eight-stage pseudo-symplectic RK(4,8)
- [[comparisons/cycle36_pdps_mco_literature_20260803]] ? Cycle 36: PDPS-MCO literature and GitHub evidence
- [[comparisons/cycle4-preconditioner-corrector-20260802]] ? Cycle 4 evidence: preconditioners, residual correctors, and state-space operators — 2026-08-02
- [[comparisons/cycle6_nature_github_evidence_20260802]] ? Cycle 6 evidence refresh — 2026-08-02
- [[comparisons/cycle7_conservation_local_operator_refresh_20260802]] ? Cycle 7 evidence refresh — conservation, local operators, and reusable elements (2026-08-02)
- [[comparisons/cycle8_power_flow_phase_operator_refresh_20260802]] ? Cycle 8 evidence refresh: power-flow phase carriers and function-space interfaces (2026-08-02)
- [[comparisons/cycle9_causal_consistency_physics_operator_refresh_20260802]] ? Cycle 9 evidence refresh: causal path consistency and physics-constrained operators (2026-08-02)
- [[comparisons/ecaso_m0_nogo_20260803]] ? ECASO M0 — NO-GO record
- [[comparisons/fbpinn-xpinn-structgraph-pignn-transfer-boundaries]] ? FBPINN / XPINN / StructGraph-Dyna / PI-GNN：对 MTP-MechConv 的迁移边界
- [[comparisons/fdvi_m0_nogo_20260803]] ? FDVI-MechConv M0 NO-GO (2026-08-03)
- [[comparisons/fixed-mdof5-mtp-strict-label-free-v1-nogo-20260803]] - Fixed 5DOF MTP strict label-free V1 NO-GO (2026-08-03)
- [[comparisons/independent_boucwen_split_contract_v1_20260803]] ? Independent Bouc–Wen truth split v1 — evidence card
- [[comparisons/lco_rk48_shared_m0_nogo_20260803]] ? LCO-RK48 Shared-MechConv M0 NO-GO (2026-08-03)
- [[comparisons/lco_rk8_m0_nogo_20260803]] ? LCO-RK8(4)-MechConv M0 NO-GO (2026-08-03)
- [[comparisons/lco_rk8_sol_audit_20260803]] ? LCO-RK8(4)-MechConv Sol audit addendum
- [[comparisons/md-pnop-laplace-matrix-pimo-scalepinn-20260802]] ? MD-PNOP、PILNO、矩阵预条件、PIMIONet 与 Scale-PINN：面向失败 MechConv 方案的可执行比较
- [[comparisons/mtp-mechconv-v2-a-prime-s4d-m0-negative-20260802]] ? A-prime S4D residual M0 negative result
- [[comparisons/mtp-mechconv-v2-evidence]] ? MTP-MechConv v2：时间并行、消息可达性与多层子图证据对照
- [[comparisons/mtp-mechconv-v2-experiment-ledger]] ? MTP-MechConv v2 独立物理实验账本
- [[comparisons/mtp-mechconv-v2-grill-audit]] ? MTP-MechConv v2 grill 审计：从候选到 v2.1 可证伪协议
- [[comparisons/mtp-mechconv-v2-impulse-bridge-negative-20260802]] ? MTP-MechConv v2：硬冲量桥接 screen 的负知识
- [[comparisons/mtp-mechconv-v2-mdof50-galerkin-pivot]] ? MTP-MechConv v2：50DOF 运动学瓶颈与 Galerkin 粗层转向
- [[comparisons/mtp-mechconv-v2-selected-kkt-projection-m0-negative-20260802]] ? Selected MechConv output KKT projection M0 — negative result
- [[comparisons/mtp-mechconv-v2-selected-nonintegrated-adapter-screen-v4-negative-20260802]] ? MTP-MechConv v2 selected checkpoint non-integrated adapter screen (negative)
- [[comparisons/mtp-mechconv-v2-v18-v19-negative-knowledge]] ? MTP-MechConv v2：V18–V19 长时载体证伪与退化边界
- [[comparisons/mtp-mechconv-v2-v19-scalability-and-correctness-correction]] ? MTP-MechConv v2：V19 可扩展性口径修正与 M0-B 正确性否决
- [[comparisons/mtp-mechconv-v2-v20-rk4z-design-evidence]] ? MTP-MechConv v2：V20-RK4Z 设计证据与限制
- [[comparisons/mtp-mechconv-v2-v21-m0-causal-audit]] ? MTP-MechConv v2 V21-M0：顺序因果本构与硬平衡审计
- [[comparisons/opsf_m0_nogo_20260803]] ? OPSF M0 review — 2026-08-03
- [[comparisons/optimizer-for-ai4s-and-physics-models]] ? AdamW vs Adafactor vs Lion vs Shampoo vs SOAP vs Muon：AI4S 与物理模型优化器选型
- [[comparisons/oracle-evidence-cycle-20260802]] ? Offline oracle evidence for MechConv structural dynamics — 2026-08-02
- [[comparisons/pdps_mco_m0_nogo_20260803]] ? PDPS-MCO M0 comparison record — NO-GO — 2026-08-03
- [[comparisons/pfnet-mhpinn-hrpinn-mechconv-20260802]] ? PFNet、MH-PINN 与 HRPINN/PHRPINN：硬物理、可迁移性与 MechConv 边界
- [[comparisons/phylstm2-vs-phylstm3-vs-lstm]] ? PhyLSTM2 vs PhyLSTM3 vs LSTM — Performance Comparison
- [[comparisons/physics-constrained-training-failure-modes]] ? 物理约束训练的失败模式对比 — PhyLSTM vs PINN
- [[comparisons/reproduction-failure-prevention-contract-2026-08-03]] ? 复现失败预防合同：从源码到可引用结论的准入门
- [[comparisons/reproduction-schemes-inventory-2026-08-03]] ? 2026 当前复现方案总览：证据、优势与边界
- [[comparisons/residual-balanced-function-space-cycle5-20260802]] ? Cycle 5：残差平衡 + 函数空间尺度 + 变形/频带分层
- [[comparisons/rpsl_literature_design_20260803]] ? RPSL literature and design evidence — 2026-08-03
- [[comparisons/rpsl_m0_nogo_20260803]] ? RPSL M0 NO-GO record — 2026-08-03
- [[comparisons/scan-vs-hash-sparse-mpm]] ? 扫描式与哈希式稀疏 MPM 实现比较
- [[comparisons/seal_m0_nogo_20260803]] ? SEAL/ExMechConv M0 NO-GO (2026-08-03)
- [[comparisons/seisgpt-vs-phylstm-cm-pinns]] ? SeisGPT vs PhyLSTM vs CM-PINNs：三类物理信息结构响应预测范式
- [[comparisons/skyfall-gs-vs-abot-earth]] ? Skyfall-GS vs ABot-Earth：卫星条件 3D 城市的精修路线与前向生成路线
- [[comparisons/smpf_ocm_m0_nogo_20260803]] ? SMPF-OCM M0 comparison record — NO-GO — 2026-08-03
- [[comparisons/ssm-corrector-preconditioner-physicscorrect-20260802]] ? 长记忆 SSM、残差校正、神经预条件与 PhysicsCorrect：面向 MechConv PINN 的证据比较
- [[comparisons/structure-preserving-candidates-20260802]] ? Structure-Preserving Candidates for MechConv: SPON, PNO, SP-NODE and Port-Hamiltonian (2026-08-02)
- [[comparisons/temporal-parallel-bemci-m0-negative-20260802]] ? Temporal-parallel BEMCI-M0 negative result (2026-08-02)
- [[comparisons/temporal-parallel-dstr-cvar-negative-20260802]] ? DSTR-CVaR local screen result — 2026-08-02
- [[comparisons/temporal-parallel-ppec-m0-negative-20260802]] ? Temporal-parallel PPEC-M0 negative result (2026-08-02)
- [[comparisons/temporal-parallel-tddm-m0-negative-20260802]] ? TDDM-M0 negative result
- [[comparisons/trpcgrad-crt-m0-negative-20260802]] ? TR-PCGrad-CRT-M0 negative result (2026-08-02)

<!-- AUTO-REGISTRY:END -->
