---
id: comparison--cycle32_endpoint_sparse_operator_20260803
title: 'Cycle 32 evidence refresh: endpoint mechanics and sparse temporal operators'
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 32 evidence refresh: endpoint mechanics and sparse temporal operators

Date: 2026-08-03

## Retrieved sources

The lawful OA retrieval workflow downloaded the following main PDFs into
`literature/cycle32_endpoint_sparse_operator_20260803_si/`:

| Paper | DOI | Main PDF SHA-256 | SI |
|---|---|---|---|
| A physics-informed graph neural network conserving linear and angular momentum for dynamical systems | `10.1038/s41467-025-67802-5` | `7bca261e4bef1ef0e3d3378af2ebf414d6d5f07539cf9db0903bfd194023dab1` | requested; unavailable because the local CDP proxy was not reachable |
| Temporal neural operator for modeling time-dependent physical phenomena | `10.1038/s41598-025-16922-5` | `a5f77eb9435b56c80ac54a5ad513ab1db183100b9552c03c4805769f4b1f572c` | requested; unavailable because the local CDP proxy was not reachable |

The manifest records `open_access_downloaded` for both main PDFs and a typed `fetch_failed` SI status. No abstract or HTML response was mislabeled as a PDF.

## Transferable evidence

### DYNAMI-CAL GRAPHNET

The 2026 Nature Communications paper uses edge-local antisymmetric reference frames and decodes pairwise internal interactions so equal-and-opposite exchanges are built into the architecture. It also uses shared spatiotemporal message passing/sub-time stepping and reports stable long rollouts on a granular benchmark with more than 2,000 particles. This supports an edge-owned interaction state, sparse scatter, and explicit conservation as the correct scalability direction.

It is not a solution to the present problem by itself: its learned pairwise impulses are not a replaceable structural constitutive law, and the paper does not establish the required endpoint `kx+cv+ma=F` residual for nonlinear frame structures. Its particle benchmark therefore cannot be used as evidence for structural high-frequency accuracy or Newton-iteration speedup.

### Temporal Neural Operator

The TNO paper formalizes a time-evolution operator with Markov or finite-history inputs and temporal bundling. The paper explicitly discusses the tradeoff: bundling can reduce operator calls, but predicting the whole available horizon can weaken temporal-dynamics learning and long-horizon extrapolation. This supports bounded short bundles with pushforward training, not an unqualified one-shot long-horizon decoder.

TNO has no hard mechanical force balance and does not replace the endpoint constitutive/EOM contract. It is useful only for temporal training curriculum and frequency coverage.

### Hybrid-operator caution

The refreshed npj Computational Materials review/experiment reports that pure learned operators accumulate long-term error and uses a direct numerical solver as a correction/intervention mechanism. This is evidence against claiming a solver-free speedup without a stability and endpoint-residual gate.

## GitHub refresh

- `neuraloperator/neuraloperator`: the public repository page reports 883 commits and an update on 2026-07-07. The current library still exposes GINO/GNO-style irregular-geometry operator blocks and resolution-invariant operator tooling; these are relevant spatial components, not a structural constitutive solver.
- `neuraloperator/graph-pde`: the organization page reports the repository last updated 2025-06-02. It remains useful as historical graph-PDE reference code but is not evidence of a current maintained production path.

## Design consequence for the next candidate

The next candidate must combine the useful edge-local antisymmetry and sparse scatter with a strict endpoint sequence:

`(u_n,v_n,z_n) -> causal proposal (u_{n+1},v_{n+1}) -> exactly one endpoint constitutive advance -> sparse B^T f_{n+1} -> authoritative a_{n+1}`.

The proposal may not be called a physically valid step until the final endpoint EOM is returned. Matrix plugins must expose edge force/state ownership; a global node-force escape hatch is not acceptable. A temporal bundle is admissible only if every bundled endpoint preserves that same contract.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
