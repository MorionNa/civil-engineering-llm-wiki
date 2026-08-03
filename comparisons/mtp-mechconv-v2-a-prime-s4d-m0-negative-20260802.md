---
id: comparison--mtp-mechconv-v2-a-prime-s4d-m0-negative-20260802
title: A-prime S4D residual M0 negative result
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
legacy_date: 2026-08-02
---

# Conclusion

The selected temporal-parallel matrix-edge MechConv received one authorized
candidate addition: a zero-initialized, stable real-pole causal S4D residual
inside the existing dynamic-projection slot.  Local tests verified stable
poles, causal prefix invariance, zero-init identity, matrix-edge/halo smoke,
replaceable linear and Bouc-Wen plugins, and exactly two constitutive calls.

The single remote official90 screen failed the independent physics gates:

- independent acceleration relative RMS: `0.0340205` versus the `0.030` gate;
- independent force relative RMS: `0.0494444` versus the `0.045` gate.

Pooled and worst-case response R² and forward timing passed their floors, so
the failure is specifically a lack of independent physics contraction, not a
general response or speed collapse.  The branch is frozen; no sweep,
backbone unfreeze, or second screen is authorized by this result.

# Evidence

- Local targeted pytest: 4 passed.
- Remote run: `outputs/remote_a_prime_s4d_m0_20260802b`.
- Candidate checkpoint SHA256:
  `4cd08653c689265bdbc8a1191aa920f07903e06dc248406e215408f6233b7afa`.
- Full mandatory audit fields not emitted by the runner remain unverified and
  are not counted as passes.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
