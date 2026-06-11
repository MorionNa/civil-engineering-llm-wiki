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

## [2026-06-10] ingest | Wang et al. (2023) — When PINNs Go Wrong
- Source: DOI, SHA256 a9173427...
- Raw captured: raw/papers/wang2023-pinn-spurious.md
- Created: concepts/wang2023-pinn-spurious-analysis.md (overview)
- Created: concepts/wang2023-pinn-spurious-method.md
- Created: concepts/wang2023-pinn-spurious-results.md
- Created: concepts/wang2023-pinn-spurious-critical.md
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

## [2026-06-11] ingest | AI4S第二讲：扩散生成模型（B站视频，Kimi ReadMediaFile）
- Source: https://www.bilibili.com/video/BV15t5m68E3w
- 94MB 完整视频一次通过 Kimi ReadMediaFile（无需拆分）
- Speaker: 章敏（浙江大学 × Datawhale × 魔搭社区）
- Raw captured: raw/articles/diffusion-models-ai4s-lecture2-bilibili.md
- Created: concepts/ai4s/diffusion-models-ai4s-lecture2.md (single page, non-paper format)
- Updated: SCHEMA.md (新增 Generative models + AI4S tag taxonomy)
- Updated: index.md (18 pages total)

## [2026-06-11] ingest | Giles et al. (2025) AVBD paper (DOI: 10.1145/3731195)
- Full-text PDF (14MB) saved: raw/papers/giles2025-avbd.pdf
- Extracted text saved: raw/papers/giles2025-avbd.md (65,670 chars)
- Created: concepts/giles2025-avbd-analysis.md (overview, 11 dimensions)
- Created: concepts/giles2025-avbd-method.md (augmented Lagrangian, inequality, friction, stiffness ramping)
- Created: concepts/giles2025-avbd-results.md (9 experiments, performance table)
- Created: concepts/giles2025-avbd-critical.md (contributions, 6 negative knowledge items, 6 transferable, 6 research opportunities)
- Updated: SCHEMA.md (added Physics simulation tag taxonomy)
- Updated: index.md (22 pages total)

## [2026-06-11] ingest | Lu et al. (2013) EESD collapse simulation paper (DOI: 10.1002/eqe.2240)
- Downloaded via Wiley TDM API: raw/papers/10_1002_eqe_2240.pdf (19 pages)
- Extracted text: raw/papers/lu2013-collapse-rc-highrise.md (47,190 chars)
- Configured: WILEY_TDM_TOKEN in ~/.bashrc (was missing, paper-download Wiley API now works)
- Created: concepts/lu2013-collapse-rc-highrise-analysis.md (overview, 11 dimensions)
- Created: concepts/lu2013-collapse-rc-highrise-method.md (fiber-beam, multilayer shell, elemental deactivation)
- Created: concepts/lu2013-collapse-rc-highrise-results.md (3 case studies, failure criteria sensitivity)
- Created: concepts/lu2013-collapse-rc-highrise-critical.md (6 contributions/NK/TK, 5 research opportunities)
- Updated: SCHEMA.md (added Structural engineering tag taxonomy)
- Updated: index.md (26 pages total)

## [2026-06-11] ingest | Ronneberger et al. (2015) U-Net paper (DOI: 10.1007/978-3-319-24574-4_28)
- Downloaded via Crossref OA: raw/papers/10_1007_978-3-319-24574-4_28.pdf (8 pages)
- Extracted text: raw/papers/ronneberger2015-unet.md (19,739 chars)
- Created: concepts/ronneberger2015-unet-analysis.md (overview, 11 dimensions)
- Created: concepts/ronneberger2015-unet-method.md (overlap-tile, elastic augmentation, weighted loss)
- Created: concepts/ronneberger2015-unet-results.md (ISBI EM/cell tracking challenge results)
- Created: concepts/ronneberger2015-unet-critical.md (contributions, 5 NK, 5 TK, 4 opportunities)
- Updated: SCHEMA.md (added Computer vision tag taxonomy)
- Updated: index.md (30 pages total)
