---
id: comparison--cycle7_conservation_local_operator_refresh_20260802
title: Cycle 7 evidence refresh — conservation, local operators, and reusable elements
  (2026-08-02)
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 7 evidence refresh — conservation, local operators, and reusable elements (2026-08-02)

## Retrieved shortlist

The authoritative-venue ranker retained five records. Three Nature OA PDFs were downloaded and verified as `%PDF` artifacts; two Springer Nature records were retained as `credentials_missing` because no local publisher API credential or institutional browser route is configured. Supporting Information was requested by default; the three OA records report SI fetch failure because the CDP proxy was unavailable.

1. Sharma & Fink, “A physics-informed graph neural network conserving linear and angular momentum for dynamical systems,” Nature Communications, DOI `10.1038/s41467-025-67802-5`. OA PDF SHA256 `7bca261e...`.
2. Ouyang et al., “NOEM: efficient and scalable finite element method enabled by reusable neural operators,” Nature Computational Science, DOI `10.1038/s43588-026-00974-2`. Publisher full text unavailable locally (`credentials_missing`).
3. Fabiani et al., “Enabling local neural operators to perform equation-free system-level analysis,” Nature Machine Intelligence, DOI `10.1038/s42256-026-01265-1`. Publisher full text unavailable locally (`credentials_missing`); GitHub head was refreshed.
4. Toscano et al., “A variational framework for residual-based adaptivity in neural PDE solvers and operator learning,” npj Artificial Intelligence, DOI `10.1038/s44387-026-00084-4`. OA PDF SHA256 `bd48a65a...`.
5. Xiong & Zhao, “Attaining physics-driven convolutional operators by architecture design,” Communications Physics, DOI `10.1038/s42005-026-02613-8`. OA PDF SHA256 `76dbd16a...`.

GitHub refresh manifest: `literature/github_20260802_cycle7/manifest_combined_20260802.json`; ranked candidates: `literature/github_20260802_cycle7/ranked.json`.

## Transferable ideas and exclusions

- DYNAMI-CAL GRAPHNET provides a strong architectural clue: internal interactions can be represented as antisymmetric edge-local contributions, while edge embeddings carry temporal memory. For this project, the safe transfer is an *antisymmetric training/readout audit around the existing MechConv force assembly*, not replacing MechConv or adding a new forward rollout.
- NOEM supports reusable local operators at element/subdomain level. The safe transfer is a constitutive/operator adapter contract that can be tested on subgraphs; importing FEM/NOEM hybrid assembly into inference would violate the current direct end-to-end requirement.
- Local neural operators support local-in-time and local-in-space computation, but their published workflow uses Krylov/Newton/continuation for system-level analysis. Those online iterative methods are explicitly excluded from the deployment forward path here.
- Residual adaptivity gives a principled route to allocation of training signal, but the rejected DSTR-CVaR screen shows that truth-only deformation/frequency weighting alone did not improve high-frequency physics. Any successor must couple adaptivity to a physically meaningful force decomposition or gradient constraint.
- Physics-driven convolutional operators reinforce multiscale convolutional representations, but the current parent already has multiscale temporal poles and high-frequency heads; simply adding another convolutional branch is not justified without a zero-forward-change local proof.

## Next-candidate boundary

The next viable candidate should be a **force-decomposition-consistent antisymmetric MechConv training constraint** or a mathematically bounded constitutive/force interface, with no online corrector, no FFT deployment stage, no change to the two constitutive calls, and no change to `required_halo_hops=6`. It must be tested first on cross-constitutive local smoke and nontrivial halo truncation before any remote screen.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
