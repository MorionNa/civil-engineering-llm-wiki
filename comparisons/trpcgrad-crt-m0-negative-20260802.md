---
id: comparison--trpcgrad-crt-m0-negative-20260802
title: TR-PCGrad-CRT-M0 negative result (2026-08-02)
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# TR-PCGrad-CRT-M0 negative result (2026-08-02)

TR-PCGrad-CRT-M0 fine-tuned only the selected parent's terminal readouts: the
velocity row of `node_head.2` plus the existing high-frequency node and edge
heads. Its training target was a bounded causal correction from the parent's
independent acceleration residual through the existing diagonal dynamic
inverse. Symmetric PCGrad and a 2% guard trust region were used; inference
remained the original matrix-edge MechConv path with hard kinematics, one
diagonal projection, two constitutive calls, and no online solver.

The formal remote run completed without rollback and met the speed, EOM,
kinematic, and constitutive-call constraints. It nevertheless failed the
scientific acceptance gates: pooled displacement R² decreased from 0.919638 to
0.914812, independent acceleration RMS increased to 0.037292, independent
force RMS increased to 0.054200, and independent-force R² decreased to
0.997062. The branch is therefore frozen and should not be widened or resumed.

The result supports a negative conclusion: terminal readout-only PCGrad can
reduce the guard protection loss while worsening the independent dynamic
closure that matters for the selected model. The guard loss is not a safe
surrogate for the official independent-physics metrics.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
