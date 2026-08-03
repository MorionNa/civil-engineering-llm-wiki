---
id: comparison--cycle22_pcil_design_20260804
title: Cycle 22 PCIL design
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 22 PCIL design

PCIL is a pre-first-MechConv port-characteristic feature lift. It derives a
causal, impedance-normalized local edge representation from the applied
inertial proxy, nominal matrix stiffness/damping, and endpoint kinematics.
Signed/absolute port scatters feed the node path and endpoint port features
feed the edge-state path. This is distinct from the rejected DHKR, LFCT,
PPEC, CMEJ², and EGTP correction families because it does not alter predicted
velocity, displacement, force, or projection after a constitutive evaluation.

The parent remains responsible for the replaceable constitutive plugin and
hard MechConv equilibrium. PCIL is currently scalar M0 only and is authorized
for one remote screen only after its 10-test local gate, including common
descent of worst-u and high-tail edge-force proxies, passes.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
