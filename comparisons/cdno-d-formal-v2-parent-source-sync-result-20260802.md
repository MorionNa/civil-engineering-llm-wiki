---
id: comparison--cdno-d-formal-v2-parent-source-sync-result-20260802
title: 'CDNO-D formal v2: parent-source-sync result (2026-08-02)'
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# CDNO-D formal v2: parent-source-sync result (2026-08-02)

## Verdict

The only approved post-sync remote rerun completed successfully, but CDNO-D is rejected as a promoted model. The immutable temporal matrix-MechConv parent remains the production baseline.

## Evidence

- Run: `outputs/remote_cdno_d_formal_v2_parent_source_sync`
- Seed 0, 40 epochs, CUDA, 2 real subgraphs, required halo 6 hops.
- Local and remote source manifests match for all 231 non-cache files.
- Pooled official90 R²: `u=0.91515`, `v=0.95764`, `a=0.91615`, edge force `0.96327`.
- Worst displacement R²: `0.70617`.
- High-modal scores: `u=0.83384`, `v=0.82986`, `a=0.81956`, edge force `0.74611`.
- Independent acceleration relative RMS: `0.03811`; independent force-balance relative RMS: `0.05540`.
- Model forward time: `0.59096 s / 90 cases`.

The constructed force balance passes (`R²=1.0`, residual `5.92e-8`), while the independent force audit fails the `0.05` RMS gate. The formal candidate gate is `qualified=false`; no promotion or downstream scale claim is justified.

## Research consequence

This run is useful as a provenance repair and negative result, not as evidence that the CDNO-D teacher improves deployment. Keep the parent checkpoint immutable. Any future attempt should address high-modal and worst-case displacement behavior first, and must receive a new single-run approval before remote training.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
