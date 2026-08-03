---
id: comparison--cdno-d-full-nonlinear-teacher-remote-failclosed-20260802
title: CDNO-D full nonlinear teacher — 2026-08-02 comparison entry
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# CDNO-D full nonlinear teacher — 2026-08-02 comparison entry

CDNO-D passed the local oracle and student expressivity gates, but has no formal model result. The remote training phase was fail-closed before optimizer construction because the config supplied the teacher dataset hash in a field that requires the immutable parent checkpoint hash. This is an execution/configuration failure, not evidence for or against the architecture. No remote checkpoint or official90 metrics were produced; do not cite this candidate as an improvement over the production parent until a separately authorized run completes.

Evidence paths:

- `outputs/local_cdno_d_oracle_probe_v1_count10/metrics.json`
- `outputs/local_cdno_d_student_smoke_v1/metrics.json`
- `outputs/remote_cdno_d_formal_v1_attempt/failure_manifest.json`
- `docs/plans/cdno_d_full_nonlinear_oracle_local_result_20260802.md`

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
