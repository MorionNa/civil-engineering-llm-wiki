---
id: paper--chen2026-empm-results
title: Chen et al. (2026) — EMPM 结果证据
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- domain/ai4s
- evidence/paper
keywords:
- elastoplastic
- online-correction
- phystwin
- pgnd
- quantitative-results
sources:
- sources/papers/chen2026-empm.md
created: '2026-08-01'
updated: '2026-08-01'
confidence: high
evidence_scope: full-text
---

# EMPM 结果证据

## Experimental Scope

The study uses three elastic objects—rope, soft elastic toy and cloth—and three elastoplastic objects—pita bread, bread dough and plasticine. Data are collected with three RealSense D455 cameras. Offline interaction uses human hands; online experiments use two Franka arms. Training and online optimization run on one NVIDIA A6000. ^[sources/papers/chen2026-empm.md]

## Offline Quantitative Comparison

| Category | Method | Dist ↓ | Track ↓ | IoU ↑ | PSNR ↑ | SSIM ↑ | LPIPS ↓ |
|---|---|---:|---:|---:|---:|---:|---:|
| Elastic | PGND | 0.0618 | — | 0.6898 | 21.06 | 0.8938 | 0.0977 |
| Elastic | PhysTwin | 0.0227 | 0.1467 | 0.6981 | 24.12 | 0.9312 | 0.0756 |
| Elastic | EMPM | **0.0222** | **0.1377** | **0.7095** | **24.19** | **0.9319** | **0.0711** |
| Elastoplastic | PGND | 0.0245 | — | 0.5069 | 21.26 | 0.9472 | 0.0738 |
| Elastoplastic | PhysTwin | 0.0177 | 0.1108 | 0.6918 | 27.01 | 0.9695 | 0.0353 |
| Elastoplastic | EMPM | **0.0082** | **0.1014** | **0.7768** | **27.82** | **0.9725** | **0.0291** |

Table 1 reports EMPM as best across all listed metrics, with a much larger geometric advantage for elastoplastic objects. ^[sources/papers/chen2026-empm.md]

## Qualitative Evidence

Figure 4 shows better handling of fracture in pita bread and squeezing in plasticine than the spring-mass PhysTwin baseline. The authors attribute this to continuum elastoplastic and fracture capability that a spring network does not naturally represent. Figure 5 shows Gaussian-rendered sequences aligned with observations.

## Online Correction

| Object | Mask loss without | Dist without | Mask loss with | Dist with |
|---|---:|---:|---:|---:|
| Rope | 0.0456 | 0.0057 | **0.0428** | **0.0054** |
| Bread dough | 0.0031 | 0.0060 | **0.0024** | **0.0059** |

The improvement is consistent but modest for 3D distance. The paper updates once every five streaming steps when the object is relatively steady and uses ten forward steps per correction.

## Runtime

| Method | Elastic train (s) | Elastic test (s) | Elastoplastic train (s) | Elastoplastic test (s) |
|---|---:|---:|---:|---:|
| PGND | 50675.50 | **5.06** | 48464.40 | **5.34** |
| PhysTwin | 496.84 | 11.49 | 589.51 | 15.94 |
| EMPM | **161.80** | 14.71 | **171.60** | 22.21 |

EMPM has the lowest reported training time but slower inference than PGND and somewhat slower inference than PhysTwin, especially for elastoplastic objects. ^[sources/papers/chen2026-empm.md]

## Interpretation Limits

- Metrics aggregate a small set of object classes and manipulation sequences.
- Baseline correspondence differences prevent PGND tracking-error comparison.
- Runtime includes different model classes and training procedures, so it is not a pure kernel-level simulator benchmark.
- The autonomous-control claim remains prospective; Figure 7 is a proof-of-concept rollout and tracking demonstration.

## Related Pages

- [[chen2026-empm-analysis]]
- [[chen2026-empm-method]]
- [[chen2026-empm-critical]]
- [[entities/empm]]
