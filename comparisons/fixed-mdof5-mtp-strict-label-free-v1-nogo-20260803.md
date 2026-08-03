---
id: comparison--fixed-mdof5-mtp-strict-label-free-v1-nogo-20260803
title: Fixed 5DOF MTP strict label-free V1 NO-GO (2026-08-03)
type: comparison
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/ai4s
- method/pinn
- method/evaluation
- evidence/report
keywords:
- strict-label-free
- one-structure-one-model
- MTP
- Bouc-Wen
- causal constitutive scan
- independent equilibrium
- negative result
sources:
- ../../../docs/experiments/fixed_mdof5_mtp_strict_label_free_v1_20260803.md
- ../../../outputs/fixed_mdof5_mtp_strict_label_free_v1b_20260803/training_summary.json
- ../../../outputs/fixed_mdof5_mtp_strict_label_free_v1b_20260803/evaluation_best/metrics_official90_spectral.json
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
failure_modes:
- long-horizon-residual-optimization
- independent-equilibrium-failure
- causal-scan-latency-regression
---

# Fixed 5DOF MTP strict label-free V1: NO-GO (2026-08-03)

## Decision

Within the [[one-structure-one-model-contract-2026-08-03]], a dedicated MTP model was randomly initialized for one fixed 5DOF Bouc-Wen structure. The training path used no response labels and no teacher trajectories. It ran successfully, but prediction accuracy, independent physics, and inference efficiency all failed. The route is **NO-GO**.

This is not a cross-structure transfer failure. No weights from another structure were loaded or fine-tuned. The failure occurred while learning the excitation-to-response map for the same fixed structure.

## Strict data contract

- Structure/model count: 1 / 1.
- Random initialization: seed 0.
- Allowed information: mass, stiffness, topology, zero damping, Bouc-Wen parameters, zero initial conditions, the first 10 training excitations, and excitation-only augmentation to 40 histories.
- Response labels: 0.
- Teacher trajectories: 0.
- Pretrained checkpoints: none.
- Held-out excitations used by optimization: none.
- The MATLAB loader requested only time and input_tf; response arrays were not deserialized.

## Official-90 evidence

| Metric | Result |
|---|---:|
| pooled R2: u / v / a / F | -0.129127 / 0.000772 / 0.091187 / -0.234775 |
| worst-case R2: u / v / a / F | -2.360659 / -0.182225 / -0.568384 / -0.742052 |
| independent force relative RMS | 1.158799 |
| independent acceleration relative RMS | 0.797319 |
| 90-history GPU forward | 4.30499 s |
| training time | 673.183 s / 120 epochs |

All four channels fail both the pooled R2 > 0.90 route and the worst-case R2 > 0.80 route. Low-modal and high-modal spectral errors are both large, so this is not only a very-high-frequency failure.

## Failure mechanism

1. Acceleration is constructed with a hard EOM, making the internal residual about 4.34e-8. The independent BDF2 residual is 1.159. A hard identity is not external correctness evidence.
2. The response is not exactly zero. Predicted u/v RMS is 0.200/0.204, while truth RMS is 0.509/0.613. The model found a nonzero trajectory with incorrect amplitude and phase.
3. Exact causal Bouc-Wen state advancement removes the free constitutive-state ambiguity, but full 30-second residual optimization remains ill-conditioned. At the best full-history epoch 115, the pre-clip gradient norm is about 3.90e3.
4. The 1,501-step causal constitutive scan makes 90-history inference 12.36 times slower than supervised MTP-bu. This also fails [[inference-speed-evidence-2026-08-03]].

## Decision impact

- MTP-bu remains the closest learned candidate in [[current-structural-pinn-ranking-2026-08-03]], but it uses real labels and teacher distillation.
- Known constitutive physics plus hard EOM plus an independent residual is insufficient to guarantee correct strict label-free training.
- Do not continue this exact route by only increasing epochs or changing loss weights. A next attempt must change the numerical formulation, such as window-local multiple shooting, continuity constraints, or an implicit/adjoint long-horizon optimizer.
- If a physics solver generates trajectories for student distillation, those trajectories must be reported as synthetic labels. The result is no longer strictly label-free.

## Related pages

- [[one-structure-one-model-contract-2026-08-03]]
- [[physics-constrained-training-failure-modes]]
- [[mtp-mechconv-v2-evidence]]
- [[current-structural-pinn-ranking-2026-08-03]]
- [[inference-speed-evidence-2026-08-03]]

## Provenance

^[../../../docs/experiments/fixed_mdof5_mtp_strict_label_free_v1_20260803.md]
^[../../../outputs/fixed_mdof5_mtp_strict_label_free_v1b_20260803/training_summary.json]
^[../../../outputs/fixed_mdof5_mtp_strict_label_free_v1b_20260803/evaluation_best/metrics_official90_spectral.json]
