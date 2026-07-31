#!/usr/bin/env python3
"""Strict lint for the maintained llm-wiki contract.

The repository contains historical pages created under older schemas. This lint is
strict for core infrastructure and the NequIP/Allegro/SevenNet repair scope, while
also validating all MkDocs nav targets and prohibiting CI workflows that mutate
knowledge content.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FIELDS = {
    "id",
    "title",
    "type",
    "status",
    "project",
    "tags",
    "sources",
    "created",
    "updated",
    "confidence",
}
ALLOWED_STATUS = {"draft", "active", "verified", "superseded"}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}
ALLOWED_TYPES = {
    "source",
    "entity",
    "paper-analysis",
    "briefing",
    "lecture",
    "video",
    "article",
    "comparison",
    "query",
    "summary",
    "index",
    "log",
    "schema",
}
PROJECT = "civil-engineering-llm-wiki"

PAPER_SLUGS = [
    "batzner2022-nequip",
    "musaelian2023-allegro",
    "park2024-sevennet-parallel-gnn-ip",
]
SOURCE_PATHS = {
    "batzner2022-nequip": "raw/papers/batzner2022-nequip-source.md",
    "musaelian2023-allegro": "raw/papers/musaelian2023-allegro-source.md",
    "park2024-sevennet-parallel-gnn-ip": "raw/papers/park2024-sevennet-parallel-gnn-ip-source.md",
}
ENTITY_PATHS = [
    "entities/nequip.md",
    "entities/allegro.md",
    "entities/sevennet.md",
]
CORE_PATHS = [
    "SCHEMA.md",
    "index.md",
    "papers/index.md",
    "entities/index.md",
    "log.md",
]

MAINTAINED_PATHS: list[str] = CORE_PATHS.copy()
for slug in PAPER_SLUGS:
    MAINTAINED_PATHS.extend(
        [
            SOURCE_PATHS[slug],
            f"papers/{slug}-analysis.md",
            f"papers/{slug}-method.md",
            f"papers/{slug}-results.md",
            f"papers/{slug}-critical.md",
        ]
    )
MAINTAINED_PATHS.extend(ENTITY_PATHS)

TEMP_CITATION_PATTERNS = [
    re.compile(r"filecite"),
    re.compile(r"cite"),
    re.compile(r"\bturn\d+(?:file|search|view|fetch|news|open)\d+\b"),
]
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
PROVENANCE_RE = re.compile(r"\^\[raw/papers/[a-z0-9_.-]+\.md\]")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def parse_frontmatter(path: Path, errors: list[str]) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(errors, f"{path.relative_to(ROOT)}: missing YAML frontmatter")
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        fail(errors, f"{path.relative_to(ROOT)}: unterminated YAML frontmatter")
        return {}, text
    try:
        data = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as exc:
        fail(errors, f"{path.relative_to(ROOT)}: invalid YAML: {exc}")
        return {}, parts[2]
    if not isinstance(data, dict):
        fail(errors, f"{path.relative_to(ROOT)}: frontmatter is not a mapping")
        return {}, parts[2]
    return data, parts[2]


def build_wikilink_index() -> tuple[set[str], set[str]]:
    stems: set[str] = set()
    rels: set[str] = set()
    for path in ROOT.rglob("*.md"):
        if any(part in {"site", ".git"} for part in path.parts):
            continue
        rel = path.relative_to(ROOT).as_posix()
        rels.add(rel)
        rels.add(rel.removesuffix(".md"))
        stems.add(path.stem)
    return stems, rels


def wikilink_resolves(target: str, stems: set[str], rels: set[str]) -> bool:
    target = target.split("|", 1)[0].split("#", 1)[0].strip()
    if not target:
        return False
    target = target.removesuffix(".md")
    if "/" in target:
        return target in rels
    return target in stems


def flatten_nav(node: Any) -> list[str]:
    values: list[str] = []
    if isinstance(node, str):
        values.append(node)
    elif isinstance(node, list):
        for item in node:
            values.extend(flatten_nav(item))
    elif isinstance(node, dict):
        for value in node.values():
            values.extend(flatten_nav(value))
    return values


def main() -> int:
    errors: list[str] = []

    for rel in MAINTAINED_PATHS:
        if not (ROOT / rel).is_file():
            fail(errors, f"missing maintained file: {rel}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    schema_text = (ROOT / "SCHEMA.md").read_text(encoding="utf-8")
    stems, rels = build_wikilink_index()
    seen_ids: dict[str, str] = {}

    for rel in MAINTAINED_PATHS:
        path = ROOT / rel
        data, body = parse_frontmatter(path, errors)
        missing = REQUIRED_FIELDS - data.keys()
        if missing:
            fail(errors, f"{rel}: missing frontmatter fields {sorted(missing)}")
            continue

        page_id = str(data["id"])
        if page_id in seen_ids:
            fail(errors, f"{rel}: duplicate id {page_id!r}, first used by {seen_ids[page_id]}")
        else:
            seen_ids[page_id] = rel

        if data["status"] not in ALLOWED_STATUS:
            fail(errors, f"{rel}: invalid status {data['status']!r}")
        if data["type"] not in ALLOWED_TYPES:
            fail(errors, f"{rel}: invalid type {data['type']!r}")
        if data["project"] != PROJECT:
            fail(errors, f"{rel}: project must be {PROJECT!r}")
        if data["confidence"] not in ALLOWED_CONFIDENCE:
            fail(errors, f"{rel}: invalid confidence {data['confidence']!r}")
        if not isinstance(data["tags"], list):
            fail(errors, f"{rel}: tags must be a list")
        else:
            for tag in data["tags"]:
                if not re.search(rf"(?<![a-z0-9-]){re.escape(str(tag))}(?![a-z0-9-])", schema_text):
                    fail(errors, f"{rel}: tag {tag!r} is absent from SCHEMA taxonomy")
        if not isinstance(data["sources"], list):
            fail(errors, f"{rel}: sources must be a list")

        full_text = path.read_text(encoding="utf-8")
        for pattern in TEMP_CITATION_PATTERNS:
            if pattern.search(full_text):
                fail(errors, f"{rel}: contains temporary chat/web citation token")

        links = WIKILINK_RE.findall(body)
        if data["type"] not in {"source", "schema", "log"} and len(links) < 2:
            fail(errors, f"{rel}: fewer than two outbound wikilinks")
        for link in links:
            if not wikilink_resolves(link, stems, rels):
                fail(errors, f"{rel}: unresolved wikilink [[{link}]]")

        if rel.startswith("papers/") and rel != "papers/index.md":
            if not PROVENANCE_RE.search(body):
                fail(errors, f"{rel}: missing persistent source provenance marker")
        if rel in ENTITY_PATHS and not PROVENANCE_RE.search(body):
            fail(errors, f"{rel}: missing persistent source provenance marker")

    for slug in PAPER_SLUGS:
        analysis = (ROOT / f"papers/{slug}-analysis.md").read_text(encoding="utf-8")
        required_sections = [
            "## 1.",
            "## 2.",
            "## 3.",
            "## 4.",
            "## 5.",
            "## 6.",
            "## 7.",
            "## 8.",
            "## 9.",
            "## 10.",
            "## 11.",
            "## 12.",
        ]
        for heading in required_sections:
            if heading not in analysis:
                fail(errors, f"papers/{slug}-analysis.md: missing section prefix {heading}")
        for suffix in ("method", "results", "critical"):
            if f"[[{slug}-{suffix}]]" not in analysis:
                fail(errors, f"papers/{slug}-analysis.md: missing link to {suffix} page")

    registrations = {
        "papers/index.md": [f"[[{slug}-analysis]]" for slug in PAPER_SLUGS],
        "entities/index.md": ["[[nequip]]", "[[allegro]]", "[[sevennet]]"],
        "index.md": [
            "[[papers/index]]",
            "[[entities/index]]",
            "[[batzner2022-nequip-analysis]]",
            "[[musaelian2023-allegro-analysis]]",
            "[[park2024-sevennet-parallel-gnn-ip-analysis]]",
        ],
        "log.md": [
            "Unified llm-wiki compliance repair",
            "Batzner et al. (2022) — NequIP",
            "Musaelian et al. (2023) — Allegro",
            "Park et al. (2024) — SevenNet",
        ],
    }
    for rel, markers in registrations.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                fail(errors, f"{rel}: missing registration marker {marker!r}")

    mkdocs_path = ROOT / "mkdocs.yml"
    try:
        mkdocs = yaml.safe_load(mkdocs_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        fail(errors, f"mkdocs.yml: invalid YAML: {exc}")
        mkdocs = {}
    for target in flatten_nav(mkdocs.get("nav", [])):
        if target.endswith(".md") and not (ROOT / target).is_file():
            fail(errors, f"mkdocs.yml: nav target does not exist: {target}")
    mkdocs_text = mkdocs_path.read_text(encoding="utf-8")
    for marker in (
        "Batzner 2022 NequIP",
        "Musaelian 2023 Allegro",
        "Park 2024 SevenNet",
        "entities/nequip.md",
        "entities/allegro.md",
        "entities/sevennet.md",
    ):
        if marker not in mkdocs_text:
            fail(errors, f"mkdocs.yml: missing navigation marker {marker!r}")

    workflows = ROOT / ".github" / "workflows"
    for workflow in workflows.glob("*.yml"):
        text = workflow.read_text(encoding="utf-8")
        if "git push" in text or re.search(r"contents:\s*write", text):
            fail(errors, f"{workflow.relative_to(ROOT)}: workflow mutates repository contents")
        if workflow.name.startswith(("register-", "complete-", "finalize-")):
            fail(errors, f"{workflow.relative_to(ROOT)}: one-time mutation workflow is prohibited")

    if errors:
        print(f"llm-wiki lint failed with {len(errors)} error(s):")
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"llm-wiki lint passed for {len(MAINTAINED_PATHS)} maintained files.")
    print("Verified 3 full-text paper families, 3 entities, indexes, provenance, navigation and read-only CI.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
