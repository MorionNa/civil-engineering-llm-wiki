---
id: comparison--cycle11_v23_pact-result-20260802
title: Cycle 11 — V23-PACT result (2026-08-02)
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 11 — V23-PACT result (2026-08-02)

## Final gate result

V23-PACT-MechConv was rejected before training. The candidate replaced V22's
independent velocity proposal with a smooth causal velocity-knot trajectory,
endpoint-locked displacement, and shared discrete trapezoid reconstruction.
It retained the V21 physical plugin and did not add a learned constitutive
state, force bypass, or EOM corrector.

The contract itself passed, including exact prefix invariance, 2/4 owner-force
partition equivalence, finite/deterministic replay, and trapezoid residual near
machine precision. The 1% physical sensitivity gate failed:

| kind | 65-step force RMS | 1501-step force RMS | G65/G17 |
| --- | ---: | ---: | ---: |
| DC | 0.0643 | 0.0224 | 3.996 |
| normal-range high frequency | 0.4613 | 0.0362 | 0.966 |
| smooth random | 0.4638 | 0.0779 | 2.683 |

The failure means endpoint locking and removal of the trapezoid alternating
null mode are insufficient to make the proposed learned trajectory channel
well-conditioned. It is not justified to spend remote training compute on
this candidate.

## Implementation audit trail

- V1: implementation bug—bubble inner-product projection did not enforce zero
  integral; its focused tests failed.
- V2: corrected projection and focused tests passed, but its direct artifact
  exposed a nonfinite random long-horizon path.
- V3: strict JSON writer converted undefined ratios to `null`.
- V4: smooth velocity-knot construction removed the alternating null mode.
- V5: final endpoint/mean contract passed; the real physical gate still failed.

The final artifact is
`outputs/local_v23_pact_trajectory_sensitivity_v5/metrics.json`. The v5 tests
are in `tests/test_probe_v23_pact_trajectory_sensitivity_v5.py`.

## Research consequence

The next viable architecture cannot be another unconstrained trajectory
proposal or local residual head. It would need a mathematically contractive
or passive propagator—likely a discrete port-Hamiltonian/generalized-material
map—with a separately proven coarse communication interface. Until that
candidate has a no-training gate, retain the selected parent for 5DOF and use
strict physical solvers for larger structures.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
