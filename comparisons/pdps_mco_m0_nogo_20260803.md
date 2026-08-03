---
id: comparison--pdps_mco_m0_nogo_20260803
title: PDPS-MCO M0 comparison record — NO-GO — 2026-08-03
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# PDPS-MCO M0 comparison record — NO-GO — 2026-08-03

PDPS-MCO was implemented only as a local direct causal pole-state graph
operator and then stopped after strict Sol audit. The local evidence was
`tests/test_pdps_mco.py`: **8 passed, 1 warning**; focused `compileall` also
passed. No remote screen, training, dev/sealed access, or held-out evaluation
was performed.

The scaffold did demonstrate pole direct readout, an independently formed EOM
residual, sparse endpoint scatter, and a future-hidden path from edge force and
edge state. Those facts are insufficient for candidate acceptance.

The decisive hard blockers were:

- Bouc-Wen used fixed Euler state evolution and had incorrect beta/gamma signs;
- fixed DOF and `fixed_mask` were not enforced;
- encoded initial conditions did not guarantee exact `u0/v0/a0`;
- the halo helper still sourced the full global hidden state and applied a
  global update, rather than implementing true owner/ghost evolution;
- `initial_state` was hard-coded to batch size one.

Therefore PDPS-MCO is **NO-GO** and remote execution is prohibited. Preserve the
module and tests as diagnostic scaffolding only. The fallback is GraphPhyGRU as
the current direct baseline subject to its existing final gates, V21 as the
physical oracle, or an explicitly documented traditional solver/teacher.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
