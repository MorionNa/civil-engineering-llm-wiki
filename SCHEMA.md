---
id: schema
title: Civil Engineering LLM Wiki Schema
type: schema
status: active
project: civil-engineering-llm-wiki
tags: []
keywords:
- entity-first
- llm-wiki
- source-grounded
sources: []
created: '2026-07-16'
updated: '2026-07-31'
confidence: high
---

# Civil Engineering LLM Wiki Schema

## Core Principle

This wiki is **entity-first and source-grounded**. Evidence from a source should normally be written into the reusable page whose subject will matter later: an entity, concept, method, claim, comparison, decision or baseline. A standalone source note is created when a long or complex source supports multiple pages, needs independent review, or would otherwise require repeated rereading.

The repository retains a compatibility extension for deep academic-paper reading: a full-text paper may be represented by an `analysis + method + results + critical` family. These pages are still subject-oriented knowledge pages; the canonical source record lives under `sources/papers/` and the original material remains immutable under `raw/` or at the recorded external location.

## Architecture

```text
wiki/
├── SCHEMA.md
├── index.md
├── log.md
├── raw/                       # immutable original materials; never rewritten by migration
│   ├── articles/
│   ├── papers/
│   ├── transcripts/
│   ├── webpages/
│   ├── assets/
│   └── misc/
├── sources/                   # optional standalone source notes
│   ├── index.md
│   └── papers/
├── entities/                  # named models, datasets, tools, people and organizations
├── concepts/                  # reusable ideas, mechanisms, metrics, assumptions and limitations
├── papers/                    # compatibility extension for deep full-text paper families
├── methods/                   # reusable procedures or algorithms when separated from paper pages
├── claims/                    # evidence/confidence/counterevidence records
├── baselines/                 # reference methods and reproducibility settings
├── comparisons/               # structured trade-off analyses
├── decisions/                 # project decisions and revisit conditions
├── notes/                     # briefings, lectures, videos and articles
├── queries/                   # reusable research questions
└── scripts/                   # migration, lint and maintenance utilities
```

Directories may be introduced when the first qualifying page is created. Do not create empty topical pages merely to mirror this diagram.

## Routing Rule

Choose a page location by the **subject of the note**, not by where the information came from:

- `entities/`: named model, dataset, tool, benchmark, person, organization or venue.
- `concepts/`: reusable idea, definition, mechanism, metric, assumption or limitation.
- `methods/`: reusable procedure, algorithm, protocol or implementation pattern.
- `claims/`: statement requiring explicit evidence, confidence, scope and counterevidence.
- `comparisons/`: two-or-more-option trade-off analysis.
- `decisions/`: selected option, rationale, alternatives and revisit conditions.
- `baselines/`: reference configuration, metrics and comparability risks.
- `sources/`: independent reading/provenance record for a long, complex or multi-page source.
- `papers/`: the project-specific deep-reading extension for a full-text academic paper.

Do not use `entities/` as a generic location for source summaries unless the source is primarily about one named entity.

## Ingest Rules

| Source | Required handling |
|---|---|
| Full-text academic paper | Preserve original under `raw/` or record a stable external source; create `sources/papers/<slug>.md`; create/update reusable entity/concept/method pages; when deep paper review is needed, create `analysis + method + results + critical` |
| Abstract-only academic paper | One overview is allowed with `evidence_scope: abstract-only`; do not invent method/results detail absent from the abstract |
| PPT / meeting | Source-grounded briefing or reusable subject pages; record source and scope |
| Lecture / tutorial / video | Transcript/source note when available, then reusable concept/method/entity pages |
| Article / blog / webpage | Preserve URL or raw capture; separate author claims from verified facts |

### Source Note Policy

Create a standalone source note when at least one condition holds:

- one source supports multiple reusable pages;
- the source is long, complex or likely to be revisited;
- the source contains many claims requiring traceability;
- the reading record itself needs review;
- the project uses the 1+3 paper extension.

A source note records evidence scope and original-material locations. It does not replace the original source.

## Raw Immutability

Files under `raw/` are immutable after ingest. Migration and lint scripts must not overwrite, normalize, rename or delete raw source files. Metadata corrections are recorded in a source note or a new versioned raw record rather than silently changing the original.

## Strict Frontmatter Contract

Every maintained Markdown page outside `raw/` starts with:

```yaml
---
id: short-stable-id
title: Human-readable title
type: source | entity | concept | method | claim | baseline | comparison | decision | query | paper-analysis | briefing | lecture | video | article | summary | index | log | schema
status: draft | active | verified | superseded
project: civil-engineering-llm-wiki
tags: []
keywords: []
sources: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: low | medium | high
---
```

`keywords` is optional for new pages but is retained during historical migration so legacy retrieval terms are not lost. Optional structured fields include:

```yaml
evidence_scope: full-text | abstract-only | transcript | webpage | secondary-synthesis
methods: []
results: []
failure_modes: []
datasets: []
reproducibility: low | medium | high
code_url: []
dataset_url: []
contested: true
contradictions: []
```

Rules:

- `id` is stable and unique across the repository.
- `status: verified` means checked against listed evidence, not independently reproduced.
- `status: draft` is required when no explicit source is available; include `## Verification Needed`.
- `sources` points to a canonical source note, raw path or stable external source.
- `created` is preserved; `updated` changes on meaningful revision.
- Replaced pages use `status: superseded` and link to the replacement.
- Conflicting evidence is retained under `Conflict` or `Counterevidence`; never silently reconciled.

## Namespaced Tag Taxonomy

`tags` is a deliberately small, stable routing/filtering set. Detailed historical terminology belongs in `keywords`.

### Domain

- `domain/civil-engineering`
- `domain/computational-mechanics`
- `domain/ai4s`
- `domain/computer-vision`
- `domain/remote-sensing`
- `domain/llm`
- `domain/neuroscience`
- `domain/knowledge-management`

### Method

- `method/pinn`
- `method/neural-operator`
- `method/graph-neural-network`
- `method/transformer`
- `method/neural-architecture-search`
- `method/reinforcement-learning`
- `method/evaluation`
- `method/workflow`

### Evidence

- `evidence/paper`
- `evidence/code`
- `evidence/report`
- `evidence/webpage`
- `evidence/transcript`

### Entity / Decision / Status / Risk

- `entity/model`
- `entity/dataset`
- `entity/tool`
- `entity/person`
- `entity/organization`
- `decision/architecture`
- `decision/implementation`
- `status/draft`
- `status/verified`
- `risk/uncertain`

New namespaced tags are added only when they will recur. Do not promote every one-off paper term to a tag.

## Provenance And Evidence

- Use frontmatter `sources` for page-level provenance.
- Use an `Evidence By Source` section for reusable notes that synthesize source evidence.
- A persistent marker may reference either a canonical source note or original material, for example `^[sources/papers/example.md]` or `^[raw/papers/example.pdf]`.
- State page, section, equation, figure or table positions in prose when useful.
- Never commit temporary conversation citation controls, `turn...` IDs or assistant-only reference tokens.
- Do not claim independent reproduction unless code/experiments were actually rerun.
- Mark cross-domain applications as **migration inference**, **design proposal** or **research opportunity**, not as a paper conclusion.
- Crossref metadata, abstracts and memory records do not count as full-text evidence unless the full text was actually read.

## Page Creation Threshold

Create a dedicated reusable page when at least one condition is true:

- the subject appears in two or more sources;
- it affects a research, implementation or evaluation decision;
- it is likely to be reused later;
- it contains a claim needing evidence tracking;
- multiple existing pages already reference it.

One-off details remain in the relevant page’s `Evidence By Source` section. Historical unresolved references may be migrated to `status: draft` stubs only when the references demonstrate likely reuse; such stubs must contain `Verification Needed` and must not masquerade as verified knowledge.

## Paper Deep-Reading Extension

Every full-text paper selected for deep review produces:

```text
sources/papers/<slug>.md
papers/<slug>-analysis.md
papers/<slug>-method.md
papers/<slug>-results.md
papers/<slug>-critical.md
```

The overview contains 12 explicit sections:

1. engineering background;
2. research gap;
3. scientific question;
4. research objective;
5. method and mechanism;
6. result and evidence;
7. contribution;
8. core knowledge;
9. Negative Knowledge;
10. transferable knowledge;
11. research opportunities;
12. reproducibility.

The method page includes architecture/data flow, equations, inputs/outputs, training/solution strategy, assumptions and failure boundaries. The results page records numerical evidence only when supported, together with comparison conditions and interpretation limits. The critical page includes contribution, Negative Knowledge, do-not-copy cautions, transfer opportunities and an explicit paper-claim versus migration-inference distinction.

Abstract-only pages are exempt from 1+3, but must carry `evidence_scope: abstract-only` and clearly identify what requires full-text verification.

## Wikilinks

- Use bare double-bracket wikilinks; do not wrap them in backticks.
- Non-terminal knowledge pages have at least two outbound links.
- Every link resolves to a maintained Markdown page or section index.
- Prefer canonical pages over aliases or near-duplicates.
- Raw paths and external URLs are provenance, not wikilinks.

## Index And Navigation Contract

- Register every maintained page in its section index.
- `index.md` links every section index and high-priority knowledge chain.
- Section indexes provide exhaustive finite reachability; curated prose may coexist with an auto-generated registry.
- `mkdocs.yml` may remain curated because unlisted pages remain searchable and reachable through indexes.
- Append every meaningful create, ingest, revise, verify, lint, migration or deployment repair to `log.md`.

## CI/CD Contract

GitHub Actions may checkout, lint, build, upload artifacts and deploy. It must not edit knowledge pages, create commits, push branches or self-delete workflows. Repository mutations happen before PR validation. Validation and deployment use read-only `contents` permission.

## Historical Migration Policy

The repository-wide migration preserves existing page bodies and legacy retrieval terms, normalizes frontmatter, creates canonical source notes, removes temporary citation controls, repairs links and indexes, and fills objectively incomplete 1+3 families. It does **not** silently fabricate missing source evidence. Pages whose provenance cannot be recovered remain `status: draft` with explicit verification tasks.

## Update Policy

1. Check source version and date before revising claims.
2. Preserve incompatible older evidence and record contradictions.
3. Update affected source/subject pages, indexes and log together.
4. Run repository-wide lint and MkDocs build before merging to `main`.
5. Keep `raw/` immutable and workflows read-only.
