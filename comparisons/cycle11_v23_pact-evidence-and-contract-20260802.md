---
id: comparison--cycle11_v23_pact-evidence-and-contract-20260802
title: Cycle 11 — V23 PACT-MechConv evidence and contract (2026-08-02)
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 11 — V23 PACT-MechConv evidence and contract (2026-08-02)

## Literature retrieval

The Nature retrieval shortlist targeted local time stepping, subdomain/coarse
communication, and structural lower-order physics decomposition.

| Candidate | Local status | Transfer decision |
|---|---|---|
| Local neural operators / equation-free system-level analysis | OA PDF verified; SHA256 `751c8b0826ad939e9361563d66dbaad619d78784549de4dfc239fc14fabbeb82` | Adopt short-time/local-in-space composition as a design hint; reject its PDE-only claims as structural proof |
| Multi-level physics-informed deep learning for computational structural mechanics | OA PDF verified; SHA256 `6903471e6dad98fb1a92aab928acec41e9be77290b84001d69b957a98d46dd20` | Adopt separation of geometry/constitutive/equilibrium roles; retain MechConv and hard EOM |
| NOEM | Metadata and Zenodo code archive identified; direct arXiv and Nature PDF downloads failed with typed statuses | Adopt subdomain/operator-element interface as inspiration only; no full-text or performance claim |

The local operator repository was fetched at commit
`b412095644ae2bce2f23ca321d729fc9c2fbc75e`; the official neuraloperator
repository was fetched at `86a8bc7812a31b42c4f7895693cf4ac11521c066`.

## Sol grill result

Sol's V23-PACT-MechConv design is conditional GO only for a no-training
falsification slice. It is NO-GO for remote training until the registered
perturbation, constitutive-transfer, owner/ghost, expressivity, and speed
gates pass.

The critical change from V22 is to make `u` and `v` a single constrained
discrete trajectory and to keep constitutive history outside the learned
latent state. The coarse hierarchy can only modulate displacement decoding;
all physical force remains `B^T f_e` from an owned replaceable plugin.

## Known limitations

Associativity of constitutive state maps is exact for affine linear maps but
not automatically available for bilinear or Bouc–Wen updates. Therefore no
parallel-prefix speed claim is allowed for those plugins until numerical
agreement and convergence gates pass. Energy/passivity bounds restrict error
growth but do not establish R² accuracy.

The two downloaded papers support the conceptual ingredients but do not prove
the requested irregular matrix-edge structural-dynamics contract. The V22
real-motion kill gate remains the decisive prior failure.

## Next action

Implement only a read-only V23 constrained-trajectory sensitivity preflight
and its tests. If any pre-training gate fails, preserve the immutable parent,
use V21 as a physical oracle, and stop before remote training.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
