---
id: comparison--lco_rk8_sol_audit_20260803
title: LCO-RK8(4)-MechConv Sol audit addendum
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
legacy_tags:
- lco-rk8
- no-go
- butcher-tableau
- bouc-wen
- halo
---

# Independent Sol audit

Sol confirmed **NO-GO**. The draft's linear hand-coded `P8` recurrence and nonlinear two-half-step RK4 path have different stability functions, so the candidate has no single shared eight-stage tableau. The necessary conditions for a true shared method include one strict-lower-triangular `A`, weights `b`, `c=A1`, the eight linear coefficients `b^T A^(k-1) 1 = 1/k!`, and all fourth-order rooted-tree conditions; none were witnessed by the draft.

Independent physical blockers in the draft:

- the neural stage modifier is not order-scaled and can destroy the claimed fourth order;
- Bouc-Wen stage state is not propagated through later RK stages;
- final acceleration/force is taken from an internal stage rather than the final composed state;
- time-varying loads are not stage-sampled;
- owner/halo synchronization helpers are not called by the step path;
- stability checks are edge-local rather than global-modal;
- work/energy bookkeeping omits stage quadrature, internal storage, and hysteresis closure.

No pytest, compileall, training, remote, dev, or sealed run was authorized for this candidate.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
