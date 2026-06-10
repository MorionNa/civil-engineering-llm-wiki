# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

## [2026-06-10] create | Wiki initialized
- Domain: Physics-informed machine learning and computational mechanics
- Structure created with SCHEMA.md, index.md, log.md

## [2026-06-10] ingest | Zhang et al. (2020) — PhyLSTM
- Source: DOI 10.1016/j.cma.2020.113226, SHA256 61904aed...
- Raw captured: raw/papers/zhang2020-phylstm.md
- SCHEMA.md created with 12-dimension paper analysis framework + tag taxonomy
- Created: concepts/zhang2020-phylstm-analysis.md (overview)
- Created: concepts/zhang2020-phylstm-method.md (method details)
- Created: concepts/zhang2020-phylstm-results.md (results details)
- Created: concepts/zhang2020-phylstm-critical.md (contribution/knowledge/negative/transferable/opportunities)
- Created: entities/phylstm2.md
- Created: entities/phylstm3.md
- Created: entities/bouc-wen-model.md
- Created: entities/peer-strong-motion-database.md
- Created: comparisons/phylstm2-vs-phylstm3-vs-lstm.md
- Updated: index.md (9 pages total)

## [2026-06-10] ingest | Müller et al. (2023) — When PINNs Go Wrong
- Source: DOI, SHA256 a9173427...
- Raw captured: raw/papers/muller2023-pinn-spurious.md
- Created: concepts/muller2023-pinn-spurious-analysis.md (overview)
- Created: concepts/muller2023-pinn-spurious-method.md
- Created: concepts/muller2023-pinn-spurious-results.md
- Created: concepts/muller2023-pinn-spurious-critical.md
- Created: entities/pseudo-time-stepping.md
- Created: comparisons/physics-constrained-training-failure-modes.md
- Back-linked: PhyLSTM overview + critical pages with PINN cross-references
- Updated: index.md (15 pages total)

## [2026-06-10] ingest | Agentic Engineering 22 条技巧 (Matt Van Horn, Datawhale)
- Source: X/@mvanhorn, OCR via RapidOCR (avg confidence 0.98)
- Raw captured: raw/articles/agentic-engineering-tips-2026.md
- Created: concepts/agentic-engineering-22-tips.md (single page, non-paper format)
- Updated: index.md (16 pages total)

## [2026-06-10] ingest | AVBD SIGGRAPH 2025 — B站视频 (Kimi转录)
- Source: https://www.bilibili.com/video/BV1QpKNzeEqq
- Transcribed via Kimi ReadMediaFile (纯视觉分析，视频无语音)
- Raw captured: raw/articles/avbd-siggraph2025-bilibili.md
- Created: concepts/avbd-siggraph2025-video.md (single page, non-paper format)
- Updated: index.md (17 pages total)
