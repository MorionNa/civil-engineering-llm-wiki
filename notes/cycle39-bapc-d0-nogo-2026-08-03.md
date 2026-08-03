---
id: notes--cycle39-bapc-d0-nogo-2026-08-03
title: 'Cycle 39 BAPC D0: accurate and faster than OpenSees, but no robust backbone gain'
type: decision
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 39 BAPC D0: accurate and faster than OpenSees, but no robust backbone gain

Cycle 39 tested a Block-Amortized Proposal Compiler after refreezing the 500DOF internal step to `dt=0.0025`. The 1,030-parameter local-plus-eight-mode compiler was called once per bounded known-load block. Neural output remained only an initial iterate: every internal step used the full transactional Newmark constitutive plugin, global and per-DOF residual certificates, independent replay, atomic commit, and canonical fallback.

The legal D0 oracle charged the actual same-shape network forward, block packing, dtype/device transfer, modal-plus-local encode/decode, proposal, certification, replay, invalidation/fallback state machine, load refinement, and u/v/a/F host output. Only offline same-branch root generation was excluded. It had zero fallback, clipping and invalidation and retained u/v/a/F sample-mean R2 of 1.000000 / 0.999941 / 0.976579 / 0.999922 against a `dt=0.000625` reference; the all-sample/all-channel minimum was 0.967326.

Five randomized repeats gave oracle median 23.1138 seconds, exact canonical median 23.2635 seconds, and fastest accurate OpenSees Newton median 28.9374 seconds. The oracle was 20.12% faster than OpenSees and paired-faster than canonical in every repeat, but only 0.643% faster than canonical by medians. It therefore failed the preregistered robust headroom condition `oracle/canonical <= 0.98` and no training was authorized.

The failure exposed two mechanism details. The calibration pilot's actual fastest configuration was B=128/CUDA/float64 at 5.3473 seconds, but the frozen rule preferred a smaller block when candidates were within 1%; it selected B=16/CPU/float64 at 5.3964 seconds. Formal validation then paid 3,000 block forwards and about 0.945 seconds of network time. In addition, same-tolerance teacher roots sat close to the `1e-9` certificate boundary, so legal float64 encoding perturbations caused 39,814 Newton updates even though maximum accepted-root difference remained below 4.8e-10.

Cycle 39 is consequently a candidate NO-GO, not a failure of the user objective. A new cycle may preregister a large-block economic selection rule and an offline certificate-slack root target, while preserving the online certificate, sequential state machine, data isolation, fair timing, O(NB) memory and unchanged user metrics.

Primary local evidence: `docs/plans/cycle39_bapc_d0_nogo_20260803.md`, `outputs/remote_cycle39_opensees_refrozen500_dev4_r5_20260803b`, and `outputs/remote_cycle39_bapc_d0_500_dev4_r5_20260803a`.

## Verification Needed

This page records locally reproducible experiment evidence rather than an externally published source. Re-run the frozen scripts and validate the listed artifact manifests before promoting it from draft or treating its timing values as independently verified.

## Related Pages

- [[notes/cycle39-canonical-admissibility-refrozen-2026-08-03]]
- [[notes/cycle38-drc-nc-nogo-2026-08-03]]
- [[notes/index]]
- [[index]]
