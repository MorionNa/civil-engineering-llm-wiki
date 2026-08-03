---
id: notes--cycle42-exact-bilinear-nogo-h1-2026-08-04
title: 'Cycle 42 exact bilinear: qualified return map but only 2/4 visible loops'
type: decision
status: draft
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- method/evaluation
- decision/implementation
sources: []
created: '2026-08-04'
updated: '2026-08-04'
confidence: low
---

# Cycle 42 exact bilinear: qualified return map but only 2/4 visible loops

Cycle 42 replaced the ill-conditioned normalized/physical Bouc--Wen equivalence in [[notes/cycle41-hn-cs-lbpc-nogo-m1-2026-08-04]] with a thermodynamically explicit bilinear kinematic-hardening return map. After correcting a story-coordinate error in the audit itself without changing any threshold or model parameter, H0 passed analytic loading, an independent high-precision scalar reference, KKT/complementarity, nonnegative dissipation, reversal, algorithmic tangents, strong monotonicity, multi-story yielding, stale-token rejection, batch isolation, and serialization/restart.

H1 then ran four development excitations, each with exactly 1,500 host intervals, at 500DOF and internal dt 0.0025. Certified dynamics passed with maximum DOF-scaled residual `8.67e-10`. Cases 0 and 1 clearly passed the frozen visible-loop contract. Case 2 failed the p90 loading/unloading separation (`0.0549<0.08`) and normalized loop work (`0.0965<0.10`); case 3 failed p90 separation (`0.0699<0.08`). H1 therefore failed 2/4 despite active plasticity.

The reusable mechanism lesson differs from the inactive nonlinearity in [[notes/cycle40-cs-lbpc-nogo-hysteresis-2026-08-04]]. Here large excursions activate plasticity strongly, but a constant positive post-yield slope makes the total force range grow with drift while the yield-offset loop width remains comparatively bounded. Normalized branch separation can therefore shrink for the largest histories.

Cycle 42 stopped before dt/4 H2, validation generation, speed screening, or training. Parameters and samples were not adjusted. A justified successor is a fresh-split exact elastic-perfectly-plastic anchor with zero post-yield material tangent; positive mass in the Newmark effective Jacobian can still provide a unique discrete root. That is a new mechanism and must be frozen and grilled before response access.

Primary local evidence: `docs/plans/cycle42_erm_bilinear_cs_lbpc_nogo_h1_20260804.md` and `outputs/remote_cycle42_h1_selection4_bilinear500_1500steps_20260804a`.

## Verification Needed

This page records locally reproducible experiment evidence rather than an external publication. Re-run the frozen H0/H1 scripts and inspect artifact hashes before promotion from draft.

## Related Pages

- [[notes/cycle41-hn-cs-lbpc-nogo-m1-2026-08-04]]
- [[notes/cycle40-cs-lbpc-nogo-hysteresis-2026-08-04]]
- [[comparisons/structure-preserving-candidates-20260802]]
- [[notes/index]]
