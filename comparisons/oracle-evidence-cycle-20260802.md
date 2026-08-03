---
id: comparison--oracle-evidence-cycle-20260802
title: Offline oracle evidence for MechConv structural dynamics — 2026-08-02
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Offline oracle evidence for MechConv structural dynamics — 2026-08-02

## New evidence

The verified local bundle is `literature/github_20260802_oracle/manifest_combined_20260802.json`. The three papers were downloaded through the lawful open-access route and checked as real PDFs with nonzero page counts and SHA-256 hashes.

- NOEM combines reusable neural-operator elements with a variational finite-element interface. The transferable idea is a reusable local subdomain interface; for this project, the interface must remain the existing MechConv matrix-edge force assembly and halo contract.
- FE-MAD differentiates through a constitutive model inside a nonlinear finite-element pipeline. The transferable idea is a constitutive-plugin tangent oracle. It does not justify assuming every replaceable plugin is differentiable, so an oracle must support automatic differentiation when available and a causal finite-difference fallback otherwise.
- HFS applies high-frequency scaling in latent space rather than using Fourier correction. The safe local test is to reuse the existing high-frequency head and measure low/mid/high residual bands; it must not become an online FFT or post-hoc corrector.

## Architectural implication

The parent’s independent defect is

`r_a = D_BDF2(v) - a_EOM(v,z)`,

with force defect `r_F = M r_a`. The deployed model already has one diagonal-dynamics projection and two constitutive calls. Therefore a credible improvement must either change the training representation or use an offline teacher; adding another deployed inverse has already failed the speed gate.

The current evidence supports only an oracle-only experiment: perturb the parent trajectory with a strictly causal halo-limited tangent or finite-difference direction, re-run the actual nonlinear constitutive plugin, and test whether the resulting velocity correction improves both residuals before any student training. The oracle must also pass prefix causality, halo stitching, bounded displacement drift, and frequency-band checks. This is empirical evidence, not a mathematical proof of learnability.

## Reusable constitutive contract

The constitutive interface should expose restoring force, internal state, and residual as it does now. Optional tangent support may expose a local Jacobian-vector product; if absent, use a causal finite-difference perturbation with a plugin-specific step-size audit. The MechConv backbone and hard acceleration construction remain unchanged when switching plugins.

## Decision

CHaRT-Fold-M0 remains held. No GPU training is authorized until the oracle has at least 20% improvement in both independent acceleration and force RMS after nonlinear recomputation, at least 10% improvement in low and high bands, and passes all causality/halo/bounded-drift gates. The new evidence informs this gate but does not satisfy it.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
