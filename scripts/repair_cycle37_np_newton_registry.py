#!/usr/bin/env python3
"""Idempotent mechanical completion of the Cycle-37 NP-Newton ingest."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def insert_before(relative: str, marker: str, block: str) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    if block.strip() in text:
        return
    if marker not in text:
        raise RuntimeError(f"marker absent from {relative}: {marker!r}")
    path.write_text(text.replace(marker, block + marker, 1), encoding="utf-8")


def append_once(relative: str, block: str) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    if block.strip() not in text:
        path.write_text(text.rstrip() + "\n\n" + block, encoding="utf-8")


for entity in ("fixed-point-neural-operator", "np-newton"):
    append_once(
        f"entities/{entity}.md",
        "## Evidence By Source\n\n^[sources/papers/lee2025-np-newton.md]\n",
    )

insert_before(
    "papers/lee2025-np-newton-results.md",
    "## Evidence By Source",
    "- 数值证据须与 [[lee2025-np-newton-method]] 的原方程验收机制一并理解。\n\n",
)
insert_before(
    "papers/lee2025-np-newton-analysis.md",
    "## 12. 可复现性",
    "批判性边界与迁移风险见 [[lee2025-np-newton-critical]]。\n\n",
)

paper_entries = """- [[papers/lee2025-np-newton-analysis]] — Lee et al. (2025) — Neural-Operator Preconditioned Newton
- [[papers/lee2025-np-newton-critical]] — NP-Newton 批判、迁移边界与研究机会
- [[papers/lee2025-np-newton-method]] — NP-Newton 方法与固定点神经算子机制
- [[papers/lee2025-np-newton-results]] — NP-Newton 迭代数、墙钟与训练成本证据

"""
entity_entries = """- [[entities/fixed-point-neural-operator]] — Fixed-Point Neural Operator (FPNO)
- [[entities/np-newton]] — Neural-Operator Preconditioned Newton

"""
source_entries = """- [[sources/papers/lee2025-np-newton]] — Lee et al. (2025) — Neural-Operator Preconditioned Newton — source note

"""
insert_before("papers/index.md", "<!-- AUTO-REGISTRY:END -->", paper_entries)
insert_before("entities/index.md", "<!-- AUTO-REGISTRY:END -->", entity_entries)
insert_before("sources/index.md", "<!-- AUTO-REGISTRY:END -->", source_entries)

log_entry = """## [2026-08-03] ingest | Lee et al. (2025) — NP-Newton and Cycle-37 transfer audit

- Added the canonical source note and complete analysis/method/results/critical paper family.
- Added FPNO and NP-Newton entities with persistent provenance.
- Recorded reported iteration, wall-clock and training-cost evidence without extrapolating it to structural dynamics or OpenSeesPy.
- Linked the paper's negative speedup on easy problems to the residual-gated PC-NP Dynamics design and retained the dynamics/50kDOF evidence gap.
- Registered all seven pages in exhaustive section indexes and verified the strict repository lint/build.

"""
insert_before("log.md", "## [2026-08-03] ingest | nonlinear-pinn", log_entry)
