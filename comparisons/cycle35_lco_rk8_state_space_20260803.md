---
id: comparison--cycle35_lco_rk8_state_space_20260803
title: 'Cycle 35: LCO-RK8(4)-MechConv and causal state-space evidence'
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
legacy_evidence_scope: Verified local PDF metadata/extraction, public primary metadata,
  prior project gates, and Sol design review. The proposed architecture is an unverified
  local M0 hypothesis.
legacy_tags:
- rk8
- explicit-composition
- phase-accuracy
- causal-state-space
- mechconv
- halo
- constitutive
evidence_scope: Verified local PDF metadata/extraction, public primary metadata, prior
  project gates, and Sol design review. The proposed architecture is an unverified
  local M0 hypothesis.
---

# Cycle 35：LCO-RK8(4)-MechConv 证据与设计边界

## 本轮检索与下载

### 直接相关的开放全文

1. *Non-linear mechanical field reconstruction coupling recurrent neural networks with physics-informed graph neural networks*, arXiv `2606.10909v1`, submitted 2026-06-09. Local PDF SHA256 `2ce81e5652c5e95e9992e1834d43a4c1081dc09a5d0a36044aa13eb7b533ef79`, 37 pages, SI not found. The paper reports an LSTM hidden state for path-dependent constitutive response, a physics-informed GNN stress reconstruction, a discrete divergence equilibrium penalty, mesh-agnostic connectivity, and a claimed 3-order FE speedup on its own microstructure task. These are transfer hypotheses only; it does not establish this project's second-order hard EOM, Bouc-Wen contract, or halo equivalence.
2. *A hybrid numerical methodology coupling Reduced Order Modeling and Graph Neural Networks for non-parametric geometries: applications to structural dynamics problems*, arXiv `2406.02615v1` / DOI `10.1016/j.cma.2024.117243`. Local PDF SHA256 `23498b783bdcac5f614818c2b62d90bf96ce6bd790cdc6cb562400e0a24eadd6`, 28 pages, SI not found. It supports heterogeneous discretization and ROM/GNN acceleration as a geometry-transfer direction, but does not prove nonlinear history constitutive replacement or exact dynamic balance.
3. *Symplectic Neural Networks in Taylor Series Form for Hamiltonian Systems*, arXiv `2005.04986v4` / DOI `10.1016/j.jcp.2021.110325`. Local PDF SHA256 `755cd092299fc1798bce1ae6183bbdb783ec09b74d4a46b335ab624b64450a70`, 35 pages, SI not found. Its fourth-order symplectic composition is relevant to phase/long-rollout design, but its evidence is Hamiltonian and not a forced, damped, history-dependent structural graph contract.

### OA retrieval blockers recorded

The lawful OA downloader was also given the definite DOI list `10.1016/j.cma.2019.112594`, `10.1016/j.jmps.2021.104697`, `10.1126/sciadv.abf3658`, `10.1111/mice.13292`, and `10.1016/j.cma.2024.117243`. Their typed status was `oa_not_found` in the configured OA-only route; no login or institutional fallback was attempted. The SciAdv record exposed PMC metadata but its guessed OA PDF endpoint returned 404 and was not mislabeled as a paper.

## Transferable evidence

- The 2026 LSTM-GNN preprint motivates a causal, local history state coupled to graph spatial reconstruction and a scale-aware equilibrium penalty.
- The self-consistency paper in *Scientific Reports* (DOI `10.1038/s41598-026-49661-2`) explicitly separates truncation (future inputs cannot change past outputs) from approximate consistency under different discretizations. It motivates a causal state contract, but its heuristic transition is not a proof of structural dynamic phase accuracy.
- Taylor/symplectic neural work motivates a high-order explicit composition for phase fidelity, but conservative Hamiltonian evidence cannot be promoted to damping, external work, Bouc-Wen memory, or general matrix-edge balance.

## Proposed local M0: LCO-RK8(4)-MechConv

Let `Y=(u,v,z_e)` and let the replaceable edge plugin expose a pure stage trial and a finite-dimensional Markov state rate. For an eight-stage explicit tableau `(A,b)`, use

```text
Yhat_i = Y_n + h * sum_{j<i} A[i,j] G(Yhat_j)
         + chi_i * S(h Omega)^4 * tanh(N_theta(F_i))
G(Y_i) = [ v_i,
           M^-1(F_i - C v_i - endpoint_scatter(f_e)),
           g_e(u_i,v_i,z_i) ]
Y_{n+1} = Y_n + h * sum_i b_i G(Yhat_i)
```

The linear path is locked to `P8(z)=sum_{k=0}^8 z^k/k!`; the neural stage defect is bounded and order-scaled. For linear plugins `chi=0` is required, so the phase certificate cannot be silently changed by the neural path. The intended linear phase error is `O((omega h)^8)` and the general nonlinear consistency target is order four.

This is a fixed explicit composition, not a global solve: no Newton iteration, tolerance loop, tangent inverse, or post-hoc force projection. It must nevertheless be described honestly as a numerical integrator inside the forward pass. If fixed explicit composition is disallowed, the full objective is logically incompatible with the requested direct speed/phase combination and this candidate must stop.

## Non-negotiable contracts

- Each physical owner edge is trialed exactly eight times and committed once per macro-step.
- Endpoint force tensors are general `[B,E,2,D]`; no scalar `(-f,+f)` shortcut is allowed.
- Every stage performs owner-only constitutive evaluation, global-ID endpoint reduction, and node-to-ghost stage-state synchronization before the next stage.
- The final acceleration is recomputed from the authoritative final constitutive force and mass equation; the EOM identity must not be the only physics evidence.
- Replacing linear, bilinear, and Bouc-Wen plugins must not alter the graph/composition code. Non-Markov or unbounded memory is outside the proof domain.

## Hard M0 gates and stop rule

1. Linear oscillator `omega*h={0.02,0.2,0.5,1.0}`: analytic `P8` agreement, phase error `<=0.5%` for `<=0.5`, no amplitude growth.
2. Ten-thousand-step low/high rollout: cumulative phase `<=0.5%` and conservative energy/amplitude drift `<=2%`.
3. Damped nonlinear work balance must converge at fourth order under `h -> h/2`; damping dissipation must be nonnegative.
4. Bouc-Wen reversal/zero-crossing/large-loop cases: pure trials, one commit, finite state, positive loop dissipation, and agreement with an independent same-tableau reference.
5. Full-vs-halo equivalence for scalar, 2DOF, and general matrix endpoint edges: `u/v/a/z/f`, loss, and gradients within `1e-10` in float64.
6. Cross-constitutive and orientation-permutation tests share the same composition; negative controls must fail when a stage synchronization or owner uniqueness rule is removed.
7. No hidden calls beyond `8` trials + `1` commit + `8` sparse assemblies per owner edge per macro-step.

Any hard-gate failure is **NO-GO** with no remote run. If the candidate passes local physics but its fixed eight-call cost cannot beat the same-device Newton/Newmark/FEM comparator in a large-deformation benchmark, it is downgraded to a physical RK8 baseline rather than claimed as a learned fast surrogate.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
