---
id: comparison--cdno-d-corrected-remote-code-failclosed-20260802
title: CDNO-D corrected remote attempt — code-interface failure (2026-08-02)
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# CDNO-D corrected remote attempt — code-interface failure (2026-08-02)

The previous hash-field error was corrected and the dataset loader contract passed locally. The fresh remote run nevertheless failed before optimizer construction because the remote model source was stale relative to the locked parent checkpoint: `power_phase_edge_carrier` was not accepted by `TemporalParallelMatrixMechConv.__init__`. This produces no scientific score and no learned artifact. The candidate remains frozen under fail-closed rules until a new user-authorized cycle can synchronize the exact parent-compatible source.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
