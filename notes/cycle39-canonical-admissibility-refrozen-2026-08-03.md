---
id: notes--cycle39-canonical-admissibility-refrozen-2026-08-03
title: 'Cycle 39 C0: same-step exactness concealed acceleration discretization error'
type: decision
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 39 C0: same-step exactness concealed acceleration discretization error

Cycle 38 compared its certified hybrid solver with a canonical trajectory generated at the same Newmark step and consequently obtained u/v/a/F R2 values of 1.0. Cycle 39 introduced a canonical admissibility gate before any block compiler or training: the evaluation-step canonical trajectory had to pass the unchanged user R2 routes against an independently refined trajectory, while every internal step retained residual certification, transactional constitutive history, independent replay, and a positive effective-tangent LDL factorization.

The original 500DOF internal step `dt=0.02` failed. Against a `dt=0.005` reference, u/v/a/F sample-mean R2 was 0.999987 / 0.995839 / 0.575267 / 0.993769, and the all-sample/all-channel minimum was 0.400027. Even `dt=0.01` against `dt=0.005` failed because acceleration sample-mean R2 was 0.744072 and the overall minimum was 0.625997. Both paths satisfied their discrete residual certificates, demonstrating that discrete equation consistency alone does not establish time-discretization accuracy.

A calibration-only bounded pilot compared internal subdivisions 1, 2, 4, and 8 with subdivision 16. The smallest passing choice was subdivision 8, or internal `dt=0.0025`. On two calibration histories its u/v/a/F sample-mean R2 against `dt=0.00125` was 1.000000 / 0.999980 / 0.974787 / 0.999973, and its all-sample/all-channel minimum was 0.970908. Subdivision 4 (`dt=0.005`) still failed because acceleration sample-mean R2 was 0.827649.

At very small steps, the float64 residual floor occasionally exceeded the original per-DOF `1e-9` certificate by only a few percent and caused line-search stagnation. Frozen diagnostics located the first two events and showed that the same committed state passed independent replay after one Newton update at residuals 1.036e-9 and 2.091e-9, with positive effective-tangent LDL pivots above 2.56e6. The refined reference tolerance was therefore capped at `1e-8`; the evaluation solver remained at `1e-9`. No further loosening was allowed.

The formal four-history validation compared evaluation `dt=0.0025` with a `dt=0.000625` reference. u/v/a/F sample-mean R2 was 0.99999998 / 0.99994059 / 0.97657924 / 0.99992214, and the all-sample/all-channel minimum was 0.96732628. The intermediate `dt=0.00125` trajectory against the same reference had minimum R2 0.99838989. Every internal step passed independent replay, the evaluation maximum scaled residual was 9.994e-10, and the minimum effective-tangent LDL pivot was 6.410e5. C0 therefore passed only after the time discretization was refrozen.

The practical consequence is strict: all subsequent BAPC, canonical, and OpenSees timing must integrate at `dt=0.0025` and return the original `dt=0.02` host output grid. Cycle 38 timing at `dt=0.02` cannot support the Cycle 39 speed claim.

Primary local evidence: `outputs/remote_cycle39_c0_canonical500_dev4_refine4_20260803b`, `outputs/remote_cycle39_dt_pilot500_cal2_subdiv16_refeps1e8_20260803d`, `outputs/remote_cycle39_refinement_probe500_cal2_subdiv16_20260803a`, `outputs/remote_cycle39_refinement_probe500_cal2_subdiv16_base2_20260803b`, and `outputs/remote_cycle39_c0_refrozen500_dev4_dt0p0025_ref0p000625_20260803a`.

## Verification Needed

This page records locally reproducible experiment evidence rather than an externally published source. Re-run the frozen scripts and validate the listed artifact manifests before promoting it from draft or treating its numerical values as independently verified.

## Related Pages

- [[notes/cycle38-drc-nc-nogo-2026-08-03]]
- [[notes/index]]
- [[index]]
