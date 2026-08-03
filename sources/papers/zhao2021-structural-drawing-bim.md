---
id: source--zhao2021-structural-drawing-bim
title: Zhao et al. (2021) — Reconstructing BIM from 2D structural drawings
 type: source
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/computer-vision
- evidence/paper
keywords:
- structural-drawing
- bim-reconstruction
- faster-r-cnn
- ocr
- ifc
sources:
- raw/papers/zhao2021-structural-drawing-bim-source.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
evidence_scope: full-text
---

# Source Note

## Bibliographic Record

- Zhao, Y.; Deng, X.; Lai, H. (2021). *Reconstructing BIM from 2D structural drawings for existing buildings*.
- *Automation in Construction*, 128, 103750.
- DOI: 10.1016/j.autcon.2021.103750.
- Original material: `raw/papers/zhao2021-structural-drawing-bim-source.md`.

## Evidence Scope

Full-text review of a 17-page journal paper. The paper proposes a four-stage raster structural-drawing-to-IFC workflow: object detection, OCR-based annotation extraction and matching, drawing-coordinate reconstruction, and IFC creation. It evaluates object detection on 100 framing plans and demonstrates one real-building floor reconstruction.

## Evidence Map

- **Problem and motivation:** pp. 1–3.
- **Four-phase workflow:** Fig. 2 and Section 3, pp. 3–4.
- **Faster R-CNN, preprocessing and augmentation:** Sections 3.1.1–3.1.3, pp. 3–6.
- **OCR and attribute matching constraints:** Sections 3.2.1–3.2.2, pp. 5–7.
- **Drawing coordinate system and pixel-to-drawing transformation:** Section 3.3, pp. 7–8.
- **XML/IFC organization:** Sections 3.3.2–3.4, pp. 8–9.
- **Dataset, training and object-detection results:** Sections 4.1–4.3, pp. 8–11.
- **Case study and generated IFC:** Section 4.4, pp. 11–13.
- **Accuracy factors and limitations:** Sections 5.1–5.3, pp. 12–14.
- **Conclusions and future work:** pp. 14–15.

## Directly Supported Claims

1. The method detects grid heads, columns, horizontal beams, vertical beams and sloped beams using Faster R-CNN.
2. OCR extracts dimensions and object attributes; matching uses proximity, mixed alphanumeric content and orientation consistency.
3. Grid heads and dimension annotations define a drawing coordinate system used to correct bounding-box location and infer beam length.
4. The augmented 4000-image dataset produced mAP 90.41% and wmAP 91.28%.
5. Height/elevation information was not reliably obtained from framing plans and was assigned default values during IFC creation.

## Evidence Boundaries

- Only beams, columns and grids are reconstructed; reinforcement, slabs, walls, foundations and detailed connections are outside scope.
- The case study reconstructs a floor of one school building; project-wide or cross-standard generalization is not established.
- Beam length is assumed equal to the grid distance without deducting column dimensions.
- Bounding-box object detection does not itself yield precise geometry.
- OCR performance depends on font-specific retraining.
- The full pipeline code and labeled drawing dataset are not released in the supplied paper.

## Related Pages

- [[zhao2021-structural-drawing-bim-analysis]]
- [[zhao2021-structural-drawing-bim-method]]
- [[zhao2021-structural-drawing-bim-results]]
- [[zhao2021-structural-drawing-bim-critical]]
- [[entities/hybrid-structural-drawing-to-ifc]]
- [[concepts/grid-anchored-drawing-coordinate-system]]
- [[concepts/constrained-annotation-object-matching]]
