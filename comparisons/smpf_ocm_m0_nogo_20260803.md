---
id: comparison--smpf_ocm_m0_nogo_20260803
title: SMPF-OCM M0 comparison record — NO-GO — 2026-08-03
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# SMPF-OCM M0 comparison record — NO-GO — 2026-08-03

SMPF-OCM was implemented as a local modal phase-flow scaffold and then
stopped after strict Sol audit. The local result was **7 passed, 1 warning**
for `tests/test_smpf_ocm.py`; focused `compileall` passed. No training,
remote work, dev/sealed access, or held-out evaluation occurred.

The scaffold passed smoke checks for `Phi^T M Phi`, exact nonzero initial
conditions, fixed DOFs, batch handling, a learned phase map, an independent
acceleration head, scalar action-reaction/index-add assembly, independently
perturbed residuals, and one constitutive call per owner edge.

The candidate is nevertheless **NO-GO**. The decisive blockers are:

- `rho*R(theta)` is the only Q/V update and has no additive input path, so
  zero initial state cannot respond to nonzero load;
- residual time levels are mismatched (`current u/v/a` with `F_next` and
  `p_current`);
- Bouc-Wen drops velocity and timestep, lacks the requested parameters and
  reversal property, while bilinear is only a clamp;
- halo parity uses complete global state and global summation rather than
  independent core/ghost partition evolution and explicit local partial
  all-reduce;
- requested frequency, long-horizon, impulse-tail, real-data, GPU, and scale
  gates remain unverified.

The candidate is stopped and must not receive a remote screen. Keep the code
and tests only as diagnostic scaffolding. Fallbacks are the current GraphPhyGRU
direct baseline, with known `u/a` limitations, and V21 MechConv as physical
oracle.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
