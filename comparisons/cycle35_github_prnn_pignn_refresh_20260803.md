---
id: comparison--cycle35_github_prnn_pignn_refresh_20260803
title: 'Cycle 35 GitHub refresh: PRNN and physics-informed GNN'
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
legacy_tags:
- github
- constitutive
- recurrent
- pignn
- mesh-agnostic
---

# GitHub refresh

## Repositories and pinned commits

- `SLIMM-Lab/pyprnn` at `5d2aca4211c4a783b9e6964fd34f2b611f2e2c15` (2025-09-15): embeds intact constitutive models in a physically recurrent neural network and explicitly advertises path dependence and step-size behavior. The code is a constitutive/material surrogate demo, not a graph-level structural dynamics solver.
- `dodaltuin/soft-tissue-pignn` at `7623b2eae4e203ae933c05f1f251ff9fb0d74574` (2026-03-02): provides a physics-informed graph emulator with potential-energy utilities and FEniCS-generated data. It is useful for graph/potential-loss scaffolding, but does not establish the project's second-order hard EOM, Bouc-Wen state ownership, or full/halo equivalence.

## Transfer decision

Use PRNN's intact-plugin idea only as evidence for a causal constitutive adapter and step-size audit. Use the PIGNN repository only as an implementation reference for mesh graph data and energy diagnostics. Do not import either repository as the LCO-RK8 numerical authority; the local composition must be independently tested against the RK(4,8) tableau, matrix endpoint assembly, and project-specific dynamic contracts.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
