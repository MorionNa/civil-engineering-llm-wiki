---
id: comparison--chart-cnr-o0-audit-20260802
title: 'CHaRT-CNR-O0 audit: conditional stability is not nonlinear validity — 2026-08-02'
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# CHaRT-CNR-O0 audit: conditional stability is not nonlinear validity — 2026-08-02

The first real parent audit is stored in `outputs/local_chart_oracle_audit_20260802/metrics.json`. It is a useful interface result, not a model-improvement result.

The parent’s raw edge-state input was captured from the constitutive pre-hook, so the zero-correction replay exactly reproduced force/state histories. A fixed-state central finite-difference JVP was also numerically stable. However, the state held fixed is precisely the missing path-dependent variable in Bouc–Wen hysteresis. A finite and stable conditional tangent therefore cannot be interpreted as a full nonlinear constitutive tangent.

The random small recheck slightly increased strict residual RMS, which is consistent with a direction that is stable but not a solved Newton direction. The next and only permitted oracle must use a causal step law that evolves state from `z_{t-1}` and solve the current-time residual, with no future residual, global normal equations, or deployment-side correction.

The new user requirement for both small and large deformation is not yet met. The audited `max |u|=1.710943` case is only a high-amplitude stress case; deformation strata must use pre-registered edge/layer deformation and hysteretic-state/energy measures. Until stateful replay, halo, frequency, and stratified gates pass, the parent remains the production default and no student or remote training is allowed.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
