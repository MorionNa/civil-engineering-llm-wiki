---
id: entity--hybrid-structural-drawing-to-ifc
title: Hybrid Structural-Drawing-to-IFC Pipeline
 type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/computer-vision
- entity/model
keywords:
- structural-drawing
- faster-r-cnn
- ocr
- dcs
- ifc
sources:
- sources/papers/zhao2021-structural-drawing-bim.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
---

# Hybrid Structural-Drawing-to-IFC Pipeline

## Definition

A hybrid raster-drawing reconstruction pipeline proposed by Zhao et al. (2021). It combines Faster R-CNN object detection, OCR-based annotation extraction, rule-based attribute matching, grid-anchored coordinate recovery and IFC entity generation.^[sources/papers/zhao2021-structural-drawing-bim.md]

## Components

- Image preprocessing and augmentation;
- five-class structural object detection;
- OCR extraction of dimensions and attributes;
- constrained object–annotation matching;
- drawing coordinate system reconstruction;
- XML intermediate representation;
- IfcBeam / IfcColumn generation.

## Inputs and Outputs

- **Input:** scanned structural framing plans containing grids, dimensions, beam/column graphics and labels.
- **Output:** a floor-level IFC model with beam and column geometry, partial attributes and spatial relationships.

## Evidence

The paper reports mAP 90.41% and wmAP 91.28% on 100 test drawings after training on 4000 augmented images, and demonstrates one school-building floor reconstruction.

## Limitations

The method does not recover true elevations, reinforcement, slabs, walls, foundations or detailed connections. Beam length is inferred from grid spacing, and complete code/data are not released.

## Project Role

This pipeline is a historical baseline for raster structural-drawing understanding. Its most reusable contributions are the staged architecture, grid-coordinate recovery and error-correcting engineering rules rather than the specific Faster R-CNN detector.

## Related Pages

- [[zhao2021-structural-drawing-bim-analysis]]
- [[concepts/grid-anchored-drawing-coordinate-system]]
- [[concepts/constrained-annotation-object-matching]]
