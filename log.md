# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

## [2026-07-31] update | Publish scalable Wiki index and stable MkDocs navigation
- Reorganized `index.md` as a section-based research entry page with direct links to paper, entity, note and comparison indexes
- Published the complete NequIP → Allegro → SevenNet paper/entity chain on the homepage
- Simplified `mkdocs.yml` to a stable compact navigation; unlisted pages remain built, searchable and reachable through section indexes and wikilinks
- Removed temporary registration workflow and temporary registration note

## [2026-07-31] ingest | Batzner et al. (2022) — NequIP
- Source: user-provided `s41467-022-29939-5.pdf` (Nature Communications 13, 2453; DOI 10.1038/s41467-022-29939-5)
- Created: raw/papers/batzner2022-nequip-source.md
- Created: papers/batzner2022-nequip-{analysis,method,results,critical}.md
- Created: entities/nequip.md
- Updated: papers/index.md, entities/index.md, index.md, mkdocs.yml and log.md
- Core: E(3) equivariance, spherical harmonics, Clebsch–Gordan tensor products, energy-conserving forces and data efficiency

## [2026-07-31] update | Register Allegro and SevenNet graph-learning chain
- Registered the existing Allegro and SevenNet paper/entity pages in the paper and entity indexes
- Added Allegro and SevenNet to the homepage and public MkDocs navigation
- Knowledge chain: NequIP → Allegro → SevenNet → large-scale structural graph learning

## [2026-07-30] ingest | Wang & Zhong (2024) — NAS-PINN: Neural architecture search-guided PINN
- Source: user-provided `1-s2.0-S0021999123006988-main.pdf` (Journal of Computational Physics 496, 112603)
- Created: papers/wang2024-nas-pinn-{analysis,method,results,critical}.md
- Created: entities/neural-architecture-search.md
- Updated: papers/index.md
- Domain: physics-informed learning + neural architecture search
- Core: differentiable NAS + mask-based width search + bi-level optimization for automatic PINN architecture design

## [2026-06-28] ingest | Zhao et al. (2026) — Causal Attention: 自适应因果性时空加权 PINN
- Source: DOI 10.1016/j.jcp.2026.115071 (JCP 2026), raw/papers/10_1016_j_jcp_2026_115071.xml
