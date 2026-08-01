---
id: log
title: Civil Engineering LLM Wiki Log
type: log
status: active
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-06-28'
updated: '2026-08-01'
confidence: high
---

# Wiki Log

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
