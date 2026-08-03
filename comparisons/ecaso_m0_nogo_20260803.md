---
id: comparison--ecaso_m0_nogo_20260803
title: ECASO M0 — NO-GO record
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# ECASO M0 — NO-GO record

**Decision: NO-GO; candidate stopped.**

Remote run:
`/home/senna/nonlinear-pinn-next/outputs/remote_ecaso_calibration_m0_20260803_retry1`

Local artifact:
`artifacts/ecaso_calibration_m0/remote_20260803_retry1`

The run completed on the independent calibration split only. Dataset SHA256
is `40b3fa29006bf01366724f25d40ffa4b53455978f810439b90914eae6ca25ca1`; root
SHA256 is `692ea2933f56e798ca01832d402b0a67e1ee55509c0de74f1f79fc0987796e6f`.
No dev, sealed, or official90 data were accessed. The structural M0 gate passed
(`m0_preflight_pass=true`), with 80/160/80 constitutive calls before/training/
after and 80 expected after calls.

The strict common-descent gate failed. Before -> after pooled R2 was:

| u | v | a | edge force |
|---:|---:|---:|---:|
| .9686507363 -> .9654346647 | .9771272961 -> .9781063848 | .9999440146 -> .9999353409 | .9731957343 -> .9693531987 |

High-band acceleration R2 was `.9999704009 -> .9999699584`; high-band
edge-force R2 was `.9798333482 -> .9799080923`. Active EOM maximum residual was
`1.4551915e-11 -> 1.1641532e-10`. These are diagnostic values, not evidence of
accuracy or high-frequency success.

Retain the contract-correct ECASO scaffold only. Use the V21 physical oracle,
RK4/Newmark/FEM references, and the frozen parent as initial guess/error
indicator. The checkpoint SHA256 is
`189d83542d0c898381c59ad6de068297e676b3deb332cfceaa66ac471206bfbe`; the
prediction SHA256 is
`b92d370da77bbb2e2400d010dfc783941bd4670cb31e6595592022d40a9b3bfd`.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
