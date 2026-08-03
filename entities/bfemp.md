---
id: entity--bfemp
title: "BFEMP — Barrier Finite Element Material Point Coupling"
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- entity/model
keywords:
- bfemp
- mpm-fem
- barrier-contact
- implicit-coupling
sources:
- sources/papers/li2022-bfemp.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
---

# BFEMP

## Definition

BFEMP is a monolithic implicit coupling framework for a Material Point Method domain and a finite-element domain. It couples the two through particle-to-FEM-boundary barrier contact and variational friction while preserving their separate discretizations. ^[sources/papers/li2022-bfemp.md]

## Core Components

- unified incremental-potential time integration;
- MPM particle–FEM simplex barrier contact;
- chain-rule contact-force transfer to MPM grid degrees of freedom;
- projected Newton nonlinear solve;
- CCD and deformation-gradient filtered line search;
- lagged variational Coulomb friction;
- FEM-defined separable irregular boundaries for MPM.

## Inputs and Outputs

Inputs include an FEM mesh, an MPM particle/grid discretization, material energies, masses, time-integration settings and contact/friction parameters. Outputs are the next-step FEM nodal states and MPM particle states.

## Supported Scope

The paper demonstrates hyperelastic FEM/MPM coupling with APIC, PIC and FLIP transfers, two-dimensional and three-dimensional contact, moving boundaries and friction-dependent instability.

## Limitations

- no dynamic conversion between FEM and MPM;
- no cutting or fracture-topology update;
- particle-center nonpenetration does not eliminate finite-support overlap;
- friction lagging lacks arbitrary-step convergence guarantees;
- public code is not identified in the supplied paper.

## Relations

- extends [[entities/incremental-potential-contact]] to heterogeneous MPM–FEM coupling;
- complements [[entities/unified-sparse-mpm]] for large sparse MPM domains;
- may combine with [[entities/incompressible-crack-mpm]] for post-damage debris, as a migration proposal;
- differs from [[entities/xpbi]], which is a pure-particle XPBD formulation rather than MPM–FEM coupling.

## Evidence By Source

Li et al. (2022) provide the formulation, seven numerical examples and explicit limitations. See [[li2022-bfemp-analysis]] and [[li2022-bfemp-critical]].
