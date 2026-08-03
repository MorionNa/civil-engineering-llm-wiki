---
id: notes--cycle38-drc-nc-nogo-2026-08-03
title: 'Cycle 38 DRC-NC: certified accuracy but no net speed benefit'
type: decision
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 38 DRC-NC: certified accuracy but no net speed benefit

Cycle 38 tested a 450-parameter Dedicated Residual-Conditioned Newton Corrector (DRC-NC) inside a transactional, full-order Newmark solver. Each learned proposal was checked against the actual constitutive plugin and independently replayed; rejected proposals fell back to the canonical nonlinear solve. This preserved the exact discrete dynamics contract and the frozen displacement, velocity, acceleration, and restoring-force R2 metrics.

The strongest fair OpenSeesPy opponent used OpenSees 3.7.1 with Newton, NewtonLineSearch, KrylovNewton, and ModifiedNewton in a preregistered portfolio. The timed path included per-case reset and host-memory output, with one batched analysis call and binary node/element recorders. At 500 DOFs, Newton was fastest: four 1500-step cases took a five-repeat median of 4.476126 seconds, minimum sample-by-channel R2 was 0.999662, and the maximum scaled dynamics residual was 7.31e-10.

An oracle economic screen paid the actual per-step feature construction, 450-parameter network forward, proposal, plugin, certification, replay, and output costs, while substituting the exact same-branch root for the learned prediction. At 500 DOFs it took a median of 3.787834 seconds, 15.38% faster than OpenSeesPy, with zero fallback and zero post-proposal Newton updates. The same screen had no useful headroom at 5 or 50 DOFs, so subsequent training was restricted to the preregistered 500-DOF scene.

The trained 500-DOF model reduced canonical Newton updates from 11,722 to 11,578 but took 6.096718 seconds. A frozen causal benefit gate called the learned corrector on only 202 of 6,000 steps and reduced updates to 11,679. It retained exact u/v/a/F R2 of 1.0 and passed the dynamics certificate, but its 4.066689-second median remained 3.35% slower than the 3.934708-second exact canonical backbone. It was 9.15% faster than OpenSeesPy only because the backbone was already faster.

The candidate is therefore NO-GO: it meets accuracy and physics requirements but creates no net economic benefit over its own certified backbone. This does not show that the overall research target is unreasonable. The oracle establishes useful 500-DOF proposal headroom, while the trained path shows that invoking even a very small neural module every step consumes it. The next falsifiable direction is a block-amortized proposal compiler called once per bounded known-load block, with all packing, device transfer, certification, invalidation, fallback, and output costs included in the timer.

Primary local evidence: `docs/plans/cycle38_drc_nc_nogo_20260803.md`, `outputs/remote_cycle38_opensees_binaryrec500_dev4_r5_20260803a`, `outputs/remote_cycle38_d0_scale500_dev4_r5_20260803a`, `outputs/remote_cycle38_d2_drc_500dof_20260803a`, and `outputs/remote_cycle38_d2_benefit_gate500_20260803a`.

## Verification Needed

This page records locally reproducible experiment evidence rather than an externally published source. Re-run the frozen scripts from the listed artifact manifests before promoting the page from draft or treating its timing values as independently verified.

## Related Pages

- [[notes/index]]
- [[index]]
