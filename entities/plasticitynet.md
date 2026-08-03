---
id: entity--plasticitynet
title: PlasticityNet
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- domain/physics-informed-learning
- entity/model
keywords:
- elastoplasticity
- neural-energy
- constitutive-model
sources:
- sources/papers/plasticitynet-2022.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
---

# PlasticityNet

## Definition

PlasticityNet is a neural-network-based elastoplastic constitutive modeling framework proposed for optimization time integration.

## Key Ideas

- Learn local potential energy representations of elastoplastic forces.
- Preserve compatibility with optimization-based implicit integration.
- Support MPM and FEM discretizations.
- Separate constitutive modeling from the simulation framework.

## Relation to Research

The method is relevant to learned constitutive models and physics-based simulation, but the paper does not demonstrate large-scale structural earthquake simulation.

## Related Pages

- [[sources/papers/plasticitynet-2022]]
