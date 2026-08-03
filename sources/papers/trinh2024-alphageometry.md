---
id: source--trinh2024-alphageometry
title: Trinh et al. (2024) — AlphaGeometry source note
type: source
status: active
project: civil-engineering-llm-wiki
tags:
- domain/automated-reasoning
- domain/ai4s
- evidence/paper
keywords:
- alphageometry
- neuro-symbolic-theorem-proving
- synthetic-proofs
- auxiliary-construction
- traceback
sources:
- raw/papers/trinh2024-alphageometry-source.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---

# Trinh et al. (2024) — AlphaGeometry

## Bibliographic Record

- **Title:** Solving olympiad geometry without human demonstrations
- **Authors:** Trieu H. Trinh, Yuhuai Wu, Quoc V. Le, He He, Thang Luong
- **Venue:** Nature 625, 476–482 (2024)
- **DOI:** 10.1038/s41586-023-06747-5
- **Code:** the article states that code and a model checkpoint are available in the `google-deepmind/alphageometry` repository.

## Evidence Scope

Full-text review of the article, Methods and Extended Data. The source covers random geometry-premise sampling, symbolic deduction with deductive database plus algebraic reasoning, traceback and proof pruning, dependency-difference extraction of auxiliary constructions, transformer pretraining/fine-tuning, alternating language-model/symbolic proof search, IMO-AG-30 evaluation, larger-set evaluation, compute, limitations and code availability.

## Evidence Map

- **pp. 1–3:** motivation, 100 million synthetic theorem–proof pairs, neuro-symbolic loop, dependency difference.
- **pp. 4–6:** benchmark construction, baselines, main and ablation results, expert evaluation, proof readability.
- **pp. 8–10:** representation language, DD+AR, traceback, pruning, data generation, model architecture, training and beam search.
- **pp. 10–11:** cross-domain framework requirements, data/code availability.
- **Extended Data:** runtime parallelism, human-proof comparisons, unsolved cases, ablations and construction/action tables.

## Directly Supported Claims

1. AlphaGeometry trains without human proof demonstrations by generating synthetic geometry problems and proofs from random premises.
2. The symbolic engine combines deductive database rules with algebraic reasoning, while the language model proposes auxiliary constructions.
3. Traceback extracts minimal dependencies; dependency difference identifies construction steps that are moved into the proof sequence for model learning.
4. The final system solves 25 of 30 translated olympiad-level geometry problems, versus 10 for the previous stated best method and 18 for the strongest hand-designed-heuristic baseline.
5. On a separate 231-problem set, the paper reports 98.7% solved.
6. The code and model checkpoint are stated to be public.

## Evidence Boundaries

- The formal language is geometry-specific rather than Lean or another general-purpose proof language.
- Only about 75% of eligible non-combinatorial IMO geometry problems since 2000 can be represented in the adopted environment; inequalities and combinatorial geometry are excluded.
- Human comparison is approximate because machines receive domain-specific translations and binary scoring.
- Proofs can be long, low-level and less readable than human solutions using complex numbers, barycentrics or high-level theorems.
- Training and search require very large compute: 100,000 CPU workers for data generation, TPUv3 slices for training, and thousands of CPU workers plus multiple GPUs for the reported search configuration.
- The article's framework does not remove the need to build domain objects, a premise sampler, symbolic engines and traceback procedures for each new domain.

## Related Pages

- [[trinh2024-alphageometry-analysis]]
- [[trinh2024-alphageometry-method]]
- [[trinh2024-alphageometry-results]]
- [[trinh2024-alphageometry-critical]]
- [[entities/alphageometry]]
- [[concepts/dependency-difference-auxiliary-construction]]
- [[concepts/traceback-synthetic-theorem-generation]]
- [[concepts/alternating-neural-symbolic-proof-search]]

## Persistent Provenance

^[raw/papers/trinh2024-alphageometry-source.md]
