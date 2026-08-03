---
id: comparison--cmej2-m0-negative-20260802
title: CMEJ²-M0 negative result — 2026-08-02
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# CMEJ²-M0 negative result — 2026-08-02

## Summary

CMEJ²-M0 was a bounded, frozen-parent correction using two additional causal diagonal dynamic inverses and sparse matrix-edge tangent actions. It passed local identity, explicit matrix oracle, causality, constitutive-call, hard EOM/kinematic, halo, teacher-isolation, and tiny-training gates. The single serialized remote official90 screen was rejected.

## Evidence

Run record: `docs/plans/temporal_parallel_cmej2_m0_remote_result_20260802.md`
Raw metrics: `outputs/remote_temporal_parallel_cmej2_m0_20260802b/metrics_official90_spectral.json`
Artifact hashes: `outputs/remote_temporal_parallel_cmej2_m0_20260802b/artifact_sha256_final.txt`

The candidate improved independent acceleration RMS from `0.034003` to `0.032463` and independent force RMS from `0.049418` to `0.047181`, but failed the hard limits `0.030` and `0.045`. Its total official90 forward time increased from `0.4549 s` for the parent to `1.0245 s`, exceeding the `0.634345 s` cap. Response R², independent force-balance R² (`0.997774`), constructed EOM, kinematics, exactly two constitutive calls, and high-modal spectral gates passed.

## Transferable conclusion

Sparse matrix-edge residual correction can reduce the independent physics defect without damaging the response contract, but fixed extra causal inverses are not inference-efficient enough here and do not close the residual gap. This branch is frozen. The parent remains the default; CMEJ² is retained only as an offline diagnostic reference.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
