---
id: notes--cycle40-cs-lbpc-nogo-hysteresis-2026-08-04
title: 'Cycle 40 CS-LBPC: accurate 1500-step dynamics but inactive hysteresis'
type: decision
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-04'
updated: '2026-08-04'
confidence: low
---

# Cycle 40 CS-LBPC: accurate 1500-step dynamics but inactive hysteresis

Cycle 40 used a fresh excitation-only engineering pool with eight complete records, each containing exactly 1,500 intervals. The evaluation-dt 500DOF certified Newmark solver passed the original u/v/a/F accuracy routes against a dt/4 reference: all-eight sample-mean R2 was 1.000000 / 0.999951 / 0.955890 / 0.999933, and the minimum across every sample and channel was 0.866246. All 16 block/device/dtype candidates fit the frozen inference and forward/backward memory limits. OpenSees Newton remained the fastest accurate portfolio member at a median of about 29.20 seconds over four complete selection trajectories.

The user's added requirement that nonlinear cases exhibit a clear hysteresis loop was converted into a frozen geometric validity test before force–deformation arrays were inspected. The fixed base-story test required nontrivial loading/unloading branch separation, loop work, decorrelation from a single-valued elastic line, and effective hysteretic-state displacement. All eight cases failed. Force–drift correlation remained at least 0.999959, median branch separation was only 0.111%–0.244% of force range, and effective-state separation was at most 0.388% of drift range. The response was therefore almost linear even though the Bouc–Wen plugin was active.

The likely cause is a dimensionless scale mismatch: the connected family multiplies story stiffness by N/5 while retaining unit masses, the original excitation RMS, and Bouc–Wen beta=gamma=30. At 500DOF this suppresses story drift relative to the hysteretic transition scale. Merely calling a nonlinear plugin is not evidence that nonlinearity affected the task.

Cycle 40 consequently stopped before its implemented 16-configuration timing selection and before training. Its certificate-slack teacher also showed limited reach—only 72.786% of internal steps met the alpha=0.25 target—but that was not the terminal kill. A new cycle must derive and freeze a hysteresis-demand scale, generate a new 1,500-step pool, and pass visible-loop validity before any speed or learning claim.

Primary local evidence: `docs/plans/cycle40_cs_lbpc_nogo_hysteresis_20260804.md` and `outputs/remote_cycle40_hysteresis500_pool8_1500steps_20260804a`.

## Verification Needed

This page records locally reproducible experiment evidence rather than an external publication. Re-run the frozen scripts and validate the artifact manifests before promotion from draft.

## Related Pages

- [[notes/cycle39-bapc-d0-nogo-2026-08-03]]
- [[notes/cycle39-canonical-admissibility-refrozen-2026-08-03]]
- [[notes/index]]
- [[index]]
