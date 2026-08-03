---
id: comparison--lco_rk48_shared_m0_nogo_20260803
title: LCO-RK48 Shared-MechConv M0 NO-GO (2026-08-03)
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
legacy_source_files:
- src/nonlinear_pinn/models/lco_rk48_shared_mechconv.py
- tests/test_lco_rk48_shared_mechconv.py
legacy_evidence_scope: Local focused test evidence plus Sol read-only audit; no remote
  execution in this action.
legacy_tags:
- lco
- rk48
- pseudo-symplectic
- constitutive-rate
- halo
- no-go
evidence_scope: Local focused test evidence plus Sol read-only audit; no remote execution
  in this action.
---

# LCO-RK48 Shared-MechConv M0 NO-GO

## Recorded local result

The focused suite reported **7 passed**, including the 10000-step rollout, and compileall passed. These results are preserved as smoke evidence only and do not override the contract audit.

## Fatal audit findings

- Commit performs a second Bouc-Wen and bilinear edge-state advancement after the RK-weighted state.
- Bilinear trial is a return-map increment divided by `dt`, not a uniform local state-rate interface, so general RK4 claims across laws are invalid.
- The halo check duplicates an edge within one graph; the step has no stage-by-stage cross-subgraph owner/ghost synchronization.
- EOM residual is obtained by defining acceleration through back-substitution, not by an independent endpoint check.
- The fixed eight-stage computation is a solver-in-forward physical baseline, not a learned fast surrogate.

## Decision and fallback

**NO-GO.** Stop this candidate and do not run it remotely. Keep the added code as fail-closed diagnostic material without modification. The fallback is the V21 physical oracle or vectorized RK4/Newmark/FEM physical baseline.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
