---
id: comparison--independent_boucwen_split_contract_v1_20260803
title: Independent Bouc–Wen truth split v1 — evidence card
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Independent Bouc–Wen truth split v1 — evidence card

## Decision

The legacy `official90` pool remains development evidence. It is not an independent test set because it was repeatedly inspected during parent/candidate selection and is assembled from the same `input_tf`/`input_pred_tf` source file.

## Locked replacement

The new split is independent of `data_boucwen.mat` and uses a fixed five-DOF shear chain, fixed Bouc–Wen parameters, new PCG64DXSM excitation streams, and a float64 RK4 truth solver with internal step `0.0025 s` and released step `0.02 s`.

| role | cases | public seed/commitment | permitted use |
|---|---:|---|---|
| calibration | 64 | `2026080301` | calibration and local diagnostics |
| dev | 32 | `2026080302` | candidate/threshold selection |
| held-out | 64 | commitment only: `0fac14ad79564d4eb03f5a0ba6adca865e23a5b6a4113703de08f1b6ec85cb5e` | one final evaluation after checkpoint freeze |

## Remote evidence

Run directory: `outputs/remote_independent_boucwen_split_v1_20260803` on the configured GPU host. The retrieved artifacts are under `artifacts/independent_boucwen_split_v1/remote_20260803/`.

- calibration SHA-256: `40b3fa29006bf01366724f25d40ffa4b53455978f810439b90914eae6ca25ca1`
- dev SHA-256: `29976c3326e8381bbd60c9c586f21866553d10240467a95add43825892027680`
- sealed held-out SHA-256: `745b5640096ce0395ada10e5c4030363180275a4a10efca8cc0c9b3562cffaa0`
- cross-split excitation hashes: disjoint in the retrieved manifests
- finite/shape audit: passed locally after retrieval

No model was trained or selected using the held-out split. The frozen temporal-parallel parent remains the fallback until a separate evaluator is implemented and a candidate is explicitly authorized.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
