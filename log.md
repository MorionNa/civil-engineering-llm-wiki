---
id: log
title: Civil Engineering LLM Wiki Log
type: log
status: active
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-06-28'
updated: '2026-08-03'
confidence: high
---

# Wiki Log

## [2026-08-03] ingest | Li et al. (2022) — BFEMP

- Source: user-provided `1-s2.0-S0045782521006277-main.pdf`, CMAME 390 (2022) 114350, DOI 10.1016/j.cma.2021.114350.
- Preserved immutable source metadata, exact file size and SHA-256 under `raw/papers/li2022-bfemp-source.md`.
- Created canonical source note and the complete Chinese `analysis + method + results + critical` paper family.
- Created `entities/bfemp.md` and reusable concepts for particle–simplex barrier coupling and FEM-defined separable MPM boundaries.
- Recorded monolithic variational MPM–FEM integration, chain-rule contact-force transfer, projected Newton, CCD/determinant-filtered line search and lagged friction.
- Preserved evidence for exact momentum conservation, 8.57%/9.67% APIC/FLIP energy loss, non-adhesive irregular boundaries, Hertz contact, sub-0.01% friction tests, PPC=16 convergence order 2.75 and the 3D twist case.
- Explicitly retained finite-particle-support overlap, approximate surface weights, friction-lag convergence limits, MPM transfer dissipation, unchanged topology and limited 3D/engineering validation.
- Distinguished direct paper conclusions from RC-collapse, dynamic FEM-to-MPM conversion and hybrid fracture/debris migration inferences.
- Updated exhaustive paper/source/entity/concept registries, the main knowledge map and automatic web-navigation inputs.

## [2026-08-03] ingest | Li et al. (2020) — Incremental Potential Contact

- Source: user-provided `3386569.3392425.pdf`, ACM TOG 39(4), Article 49, DOI 10.1145/3386569.3392425.
- Preserved immutable source metadata, exact file size and SHA-256 under `raw/papers/li2020-incremental-potential-contact-source.md`.
- Created canonical source note and the complete Chinese `analysis + method + results + critical` paper family.
- Created `entities/incremental-potential-contact.md` and reusable concepts for local smooth contact barriers and CCD-filtered feasible line search.
- Recorded unsigned primitive distances, finite-support C2 barriers, projected Newton, adaptive barrier conditioning, CCD-aware line search and lagged variational friction.
- Preserved evidence for aligned and codimensional contact, high-speed impact, extreme compression, friction-dependent structures, time steps from 0.002 s to 2 s, and models up to 688K nodes / 2.3M tetrahedra / 498K contacts per step.
- Explicitly retained positive-gap initialization, non-inverting-energy conditions, friction-lag convergence limits, floating-point CCD boundaries, dense-contact linear-system cost and unchanged-topology assumptions.
- Distinguished direct paper conclusions from RC-collapse, fragment-contact and hybrid FEM/MPM/XPBI migration inferences.
- Updated exhaustive paper/source/entity/concept registries, the main knowledge map and automatic web-navigation inputs.

## [2026-08-02] ingest | Yu et al. (2024) — XPBI

- Source: user-provided `2405.11694v2.pdf`, arXiv:2405.11694v2 [cs.GR], version dated 2024-09-14.
- Preserved immutable source metadata, exact file size and SHA-256 under `raw/papers/yu2024-xpbi-source.md`.
- Created canonical source note and the complete Chinese `analysis + method + results + critical` paper family.
- Created `entities/xpbi.md` and reusable concepts for velocity-gradient updated-Lagrangian state tracking and plasticity-in-the-loop XPBD.
- Recorded StVK-Hencky constraints, corrected Wendland-kernel gradients, fixed-point implicit plasticity, colored Gauss–Seidel, XSPH and position correction.
- Preserved evidence for Von Mises, Drucker–Prager, NACC and Herschel–Bulkley materials, up to four million particles, scalability and the 20k-particle 30-fps interaction case.
- Explicitly retained the missing implementation code, unmonitored plastic fixed-point convergence, neighborhood-quality dependence, timestep/damping dependence and engineering-validation limitations.
- Distinguished direct paper conclusions from RC-collapse, post-failure particle conversion and hybrid FEM/MPM/XPBI migration inferences.
- Updated exhaustive paper/source/entity/concept registries, the main knowledge map and automatic web-navigation inputs.

## [2026-08-02] ingest | Pantidis et al. (2026) — PICNN-IFENN phase-field fracture

- Source: user-provided `1-s2.0-S0045782525007571-main.pdf`, CMAME 448 (2026) 118485, DOI 10.1016/j.cma.2025.118485.
- Preserved immutable source metadata, exact file size and SHA-256 under `raw/papers/pantidis2026-ifenn-phase-field-source.md`.
- Created canonical source note and the complete Chinese `analysis + method + results + critical` paper family.
- Created `entities/picnn-ifenn-phase-field.md` and reusable concepts for history-variable spatial coupling and physics-informed Laplacian convolution.
- Recorded the two-increment, approximately five-minute training setup, fully convolutional input-size generalization, multi-pass convergence reduction, and multi-crack/rectangular-domain evidence.
- Preserved limitations concerning FEM-based initiation, structured meshes, Gaussian-filter residual stiffness, characteristic-length ratio dependence, and incomplete damage at asymmetric crack coalescence.
- Distinguished direct paper conclusions from concrete-fracture, structural-collapse and MPM-coupling migration inferences.
- Updated exhaustive paper/source/entity/concept registries, the main knowledge map and automatic web-navigation inputs.

## [2026-08-02] ingest | Liu et al. (2025) — Incompressible Crack MPM

- Source: user-provided `3728298.pdf`, PACMCGIT 8(1), Article 6, DOI 10.1145/3728298.
- Preserved immutable source metadata, exact file size and SHA-256 under `raw/papers/liu2025-incompressible-crack-mpm-source.md`.
- Created canonical source note and the complete Chinese `analysis + method + results + critical` paper family.
- Created `entities/incompressible-crack-mpm.md` and reusable concepts for compression-aware damage transition and volume-preserving debris plasticity.
- Recorded Weibull particle strength, tensile-only damage softening, complete-damage state conversion, non-associated Drucker–Prager return mapping and the additional true-volume deformation gradient.
- Preserved visual and performance evidence for Brazilian-disc compression, complex meshes, tensile loading, repeated debris compression and the reported 3.2%/7.9% runtime overheads.
- Explicitly retained the local-damage grid dependence, crack-thickening, low-resolution fluidization, missing engineering calibration and non-equivalent baseline limitations.
- Distinguished paper conclusions from RC-collapse, concrete crushing and high-fidelity fragmentation migration inferences.
- Updated exhaustive paper/source/entity/concept registries, the main knowledge map and automatic web-navigation inputs.

## [2026-08-02] ingest | Zhao et al. (2026) — Unified Sparse MPM

- Source: user-provided `2605.28525v3.pdf`, arXiv:2605.28525v3 [cs.CE], version dated 2026-07-28.
- Preserved immutable source metadata, exact file size and SHA-256 under `raw/papers/zhao2026-unified-sparse-mpm-source.md`.
- Created canonical source note and the complete Chinese `analysis + method + results + critical` paper family.
- Created `entities/unified-sparse-mpm.md`, `concepts/active-node-compact-indexing.md`, and `comparisons/scan-vs-hash-sparse-mpm.md`.
- Recorded the active-node-set/compact-index abstraction, block-level CPU prefix scan, GPU 64-bit-key hashing, atomic insertion and overflow rebuilding.
- Preserved numerical evidence for the sliding box, granular collapse and Blatten landslide, including sparsity ratios, single-GPU memory boundary and architecture-specific performance.
- Distinguished computational scalability evidence from physical landslide validation and marked multi-GPU, implicit, multiphase and structural-collapse extensions as research opportunities.
- Updated exhaustive paper/source/entity/concept/comparison registries, the main knowledge map and automatic web-navigation inputs.

## [2026-08-02] ingest | Feng et al. (2026) — MPM Lite

- Source: user-provided `3811294(1).pdf`, ACM TOG 45(4), Article 152, DOI 10.1145/3811294.
- Preserved immutable source metadata, file size and SHA-256 under `raw/papers/feng2026-mpm-lite-source.md`.
- Created canonical source note and the complete Chinese `analysis + method + results + critical` paper family.
- Created `entities/mpm-lite.md` and reusable concepts for particle-independent grid integration and rotation-free stretch reconstruction.
- Recorded linear-kernel two-hop transfer, extensive Kirchhoff-stress resampling, FEM-style incremental-potential integration, explicit/implicit performance and material-versatility evidence.
- Explicitly separated paper conclusions from structural-collapse migration inferences and retained anisotropy, reduced-integration, thin-structure and particle-scaling limitations.
- Updated exhaustive paper/source/entity/concept registries, the main knowledge map and automatic web navigation inputs.

## [2026-08-01] ingest | Chen et al. (2026) — EMPM

- Source: user-provided `2601.17251v1.pdf` (arXiv:2601.17251v1).
- Created canonical source note and full 1+3 paper family.
- Created `entities/empm.md`.
- Core: differentiable MPM, RGB-D reconstruction, Gaussian Splatting, offline/online material identification and embodied deformable-object simulation.
- Verified numerical evidence from Tables 1–3 and recorded tracking, homogeneity and quasi-static-update limitations.

## [2026-08-01] revise | 自动生成完整论文侧边导航

- Replaced the manually curated three-paper MkDocs sidebar with a read-only build hook that scans every Markdown page under `docs/papers/`.
- Groups the standard `analysis + method + results + critical` family under one collapsible paper entry and also exposes single-page paper records.
- Keeps `papers/index.md` as the first paper-navigation item and sorts paper families deterministically by title.
- Removed global `navigation.expand` so the much larger complete registry remains collapsed and usable by default.
- Future paper ingests require no manual `mkdocs.yml` edit: the next site build automatically includes the new pages.

## [2026-08-01] ingest | 深蓝（2026）— 从 CFD 到 Transolver：物理世界的 Token

- Source: user-provided 7-page Zhihu PDF capture; technical body reviewed on pages 1-5.
- Preserved immutable source metadata and SHA-256 under `raw/webpages/shenlan2026-physical-token-transolver-source.md`.
- Created `notes/articles/shenlan2026-physical-token-transolver.md` and registered it in the notes index and MkDocs navigation.
- Core: node-level full-attention bottleneck, POD/DMD compact-representation analogy, feature-space Dynamic Slicing, learned physical Token and Physics Attention.
- Added an explicitly labelled structural-dynamics/MechConv migration inference; it is not presented as an article conclusion.
- Evidence boundary: secondary technical article, not the Transolver primary paper or an independent reproduction.

## [2026-07-31] verify | Repository-wide historical llm-wiki migration

- Migrated every maintained historical Markdown page to stable frontmatter with `id`, `type`, `status`, `project`, namespaced tags, preserved legacy `keywords`, sources, dates and confidence.
- Kept all original materials under `raw/` immutable and created canonical paper source notes under `sources/papers/`.
- Repaired incomplete full-text paper families, abstract-only evidence scopes, temporary citation tokens, provenance, wikilinks and section registries.
- Added concepts/entities for previously unresolved reusable terms; unverifiable migration stubs remain `status: draft` with explicit verification tasks.
- Extended strict lint from the recent three-paper repair scope to the complete maintained repository.
- Restored read-only validation/deployment workflows; CI does not edit or push knowledge content.

> Chronological record of meaningful wiki actions. Append-only; newest entries first.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: create, ingest, revise, verify, lint, deploy, query, archive, delete.

## [2026-08-03] ingest | nonlinear-pinn 全量方案、复现与当前性能证据

- 登记 `docs/plans/` 下 133/133 份方案、设计、正式结果、NO-GO 与 fail-closed 文档。
- 登记 `reproductions/` 下 9/9 个顶层复现家族；保留指标、训练历史、预测和 checkpoint 的项目原路径。
- 新增当前性能排名：MTP-bu 是学习模型中最接近要求的候选，但仅能证明 5DOF 核心 R² 门通过。
- 新增 PhyLSTM3 与 CM-PINN 的统一 pooled/macro/worst-case R² 复算，明确 MTP-bu 不是所有通道全面领先。
- 新增推理速度证据页；记录 50kDOF 相对优化向量化 RK4 的 0.088× 负结果，并把 OpenSeesPy 对比保持为未完成门。
- 固化“一结构一模型”边界：不要求跨结构零样本泛化，但仍要求同结构跨加载、高低频、独立物理和公平速度测试。
- 训练时间按可核验性报告：MTP-bu 为 1434.685 s/150 epochs；历史 checkpoint 或基线缺失值明确标为不可核验。
- 未创建新论文实体：本次工作是项目方案与实验结果的证据整合，现有模型/方法实体足以承接。
- 修复 Windows 物化构建中的 6 个 MkDocs 导航告警；全库严格构建通过。

## [2026-07-31] verify | Unified llm-wiki compliance repair for NequIP, Allegro and SevenNet

- Scope: 3 source metadata notes, 12 paper pages, 3 entity pages, schema, global/section indexes, validation workflow and web navigation.
- Rebuilt all three paper overviews to include the required 12 dimensions.
- Expanded method pages with architecture, equations, training/parallel procedures and assumptions.
- Expanded results pages with source-supported numerical tables and interpretation boundaries.
- Expanded critical pages with contribution, core knowledge, Negative Knowledge, do-not-copy cautions, transfer inference and research opportunities.
- Added strict frontmatter fields: `id`, `title`, `type`, `status`, `project`, `tags`, `sources`, `created`, `updated`, `confidence`.
- Replaced temporary chat citations with persistent `^[raw/papers/...-source.md]` provenance markers.
- Distinguished paper conclusions from structural-dynamics migration proposals.
- Normalized source metadata and recorded source-version boundaries.
- Registered all pages in `papers/index.md`, `entities/index.md`, `index.md` and `mkdocs.yml`.
- Added read-only lint/build CI; GitHub Actions no longer writes or commits knowledge pages.

## [2026-07-31] ingest | Batzner et al. (2022) — NequIP

- Source: user-provided `s41467-022-29939-5.pdf`.
- Journal: Nature Communications 13, 2453.
- DOI: 10.1038/s41467-022-29939-5.
- Created: `raw/papers/batzner2022-nequip-source.md`.
- Created: `papers/batzner2022-nequip-{analysis,method,results,critical}.md`.
- Created: `entities/nequip.md`.
- Core: E(3) equivariance, spherical harmonics, Clebsch–Gordan tensor products, energy-conserving forces and data efficiency.

## [2026-07-31] ingest | Musaelian et al. (2023) — Allegro

- Source: user-provided `s41467-023-36329-y.pdf`.
- Journal: Nature Communications 14, 579.
- DOI: 10.1038/s41467-023-36329-y.
- Created: `raw/papers/musaelian2023-allegro-source.md`.
- Created: `papers/musaelian2023-allegro-{analysis,method,results,critical}.md`.
- Created: `entities/allegro.md`.
- Core: strict locality, pair-centered dual latent spaces, learned environment embedding, iterative tensor products and massive scaling.

## [2026-07-31] ingest | Park et al. (2024) — SevenNet

- Source: user-provided `2402.03789v1.pdf`.
- Version: arXiv:2402.03789v1.
- Created: `raw/papers/park2024-sevennet-parallel-gnn-ip-source.md`.
- Created: `papers/park2024-sevennet-parallel-gnn-ip-{analysis,method,results,critical}.md`.
- Created: `entities/sevennet.md`.
- Core: spatial decomposition, layerwise forward feature communication, reverse gradient communication, SevenNet-0 and LAMMPS integration.

## [2026-07-31] update | Register NequIP → Allegro → SevenNet knowledge chain

- Added the three paper families to the paper index and curated MkDocs navigation.
- Added NequIP, Allegro and SevenNet to the entity index.
- Added a global-dashboard path from graph representation to strict locality and distributed parallelism.
- Linked the chain to large-scale structural graph learning as an explicitly labeled transfer direction.

## [2026-07-30] ingest | Wang & Zhong (2024) — NAS-PINN

- Source: user-provided `1-s2.0-S0021999123006988-main.pdf`.
- Created: `papers/wang2024-nas-pinn-{analysis,method,results,critical}.md`.
- Created: `entities/neural-architecture-search.md`.
- Core: differentiable NAS, mask-based width search and bi-level PINN architecture optimization.

## [2026-06-28] ingest | Zhao et al. (2026) — Causal Attention

- Source: DOI 10.1016/j.jcp.2026.115071.
- Core: adaptive causality-aware spatiotemporal weighting for PINNs.

## [2026-08-03] merge | Local MTP-MechConv v2 knowledge pages into strict wiki baseline

- Merged 180 local pages covering papers, entities, comparisons and experiment notes into the latest GitHub mainline.
- Added 14 canonical source-note stubs and registered all imported pages in the section indexes.
- Preserved local transfer audits and negative evidence; imported pages remain `draft` until canonical source verification.
- Added the message-passing, spectral-bias and parallel-computing tags to the controlled taxonomy.

## [2026-08-03] experiment ingest | Fixed 5DOF MTP strict label-free V1 NO-GO

- Ingested the completed one-structure-one-random-model physics-only experiment.
- Training used 0 response labels, 0 teacher trajectories and no checkpoint warm start; 120 remote GPU epochs took 673.183 s.
- Locked official-90 pooled R2 for u/v/a/F was -0.129127 / 0.000772 / 0.091187 / -0.234775; independent force relative RMS was 1.158799.
- Recorded the causal-scan latency regression: 4.30499 s for 90 histories, 12.36x slower than MTP-bu.
- Created: comparisons/fixed-mdof5-mtp-strict-label-free-v1-nogo-20260803.md.
- Updated: comparisons/index.md and index.md.
- Skipped entity: this is a negative experiment variant of the existing MTP-MechConv entity, not a new reusable model or dataset.
