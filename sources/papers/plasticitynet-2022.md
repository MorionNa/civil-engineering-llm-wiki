---
id: source--plasticitynet-2022
title: PlasticityNet (NeurIPS 2022) — canonical source note
type: source
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- domain/physics-informed-learning
- evidence/paper
keywords:
- plasticitynet
- mpm
- fem
- optimization-time-integration
- constitutive-model
sources:
- raw/papers/plasticitynet-2022-source.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
---

# Source Note

## Bibliographic Record

Li et al. (2022). PlasticityNet: Learning to Simulate Metal, Sand, and Snow for Optimization Time Integration. NeurIPS 2022.

## Evidence Scope

Full-text review. The paper proposes a neural elastoplastic model that learns local potential energies so plastic forces can be integrated into optimization-based time integration.

## Evidence Map

- Motivation and limitations of existing plastic simulation: pp.1-2.
- Optimization time integration background: pp.3-4.
- PlasticityNet formulation: pp.4-6.
- Experiments on sand, snow, metal and MPM-FEM coupling: pp.6-9.
- Limitations and future work: pp.9-10.

## Directly Supported Claims

PlasticityNet supports combinations of elastic and plastic models and works with both MPM and FEM discretizations. The model learns a local energy representation rather than replacing the whole simulator.

## Evidence Boundaries

The paper does not establish applicability to structural engineering scale problems or earthquake simulation. Claims should remain limited to elastoplastic material simulation.