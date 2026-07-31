#!/usr/bin/env python3
"""Repository-wide strict lint for the civil-engineering llm-wiki.

The lint covers every maintained Markdown page outside immutable raw materials and
the generated docs/site copies. It validates schema, sources, provenance, links,
paper-family completeness, exhaustive indexes, navigation, raw immutability
policy, and read-only CI.
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROJECT = "civil-engineering-llm-wiki"
MANAGED_ROOTS = ["papers", "entities", "concepts", "sources", "notes", "comparisons"]
CORE_PATHS = ["SCHEMA.md", "index.md", "log.md"]
REQUIRED_FIELDS = {"id", "title", "type", "status", "project", "tags", "sources", "created", "updated", "confidence"}
ALLOWED_STATUS = {"draft", "active", "verified", "superseded"}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}
ALLOWED_TYPES = {
    "source", "entity", "concept", "method", "claim", "baseline", "comparison", "decision", "query",
    "paper-analysis", "briefing", "lecture", "video", "article", "summary", "index", "log", "schema",
}
ABSTRACT_ONLY = {"tao2026-fpikan", "zhang2025-mrf-pinn", "chittyvenkata2022-nas-transformers-survey"}
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
TEMP_RE = re.compile(r"(?:filecite|cite)|\bturn\d+(?:file|search|view|fetch|news|open)\d+\b")
PROVENANCE_RE = re.compile(r"\^\[[^\]]+\]")


def managed_files() -> list[Path]:
    pages: list[Path] = []
    for root in MANAGED_ROOTS:
        base = ROOT / root
        if base.exists():
            pages.extend(base.rglob("*.md"))
    pages.extend(ROOT / p for p in CORE_PATHS)
    return sorted(set(pages))


def parse_page(path: Path, errors: list[str]) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        errors.append(f"{path.relative_to(ROOT)}: unterminated YAML frontmatter")
        return {}, text
    try:
        data = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid YAML: {exc}")
        return {}, parts[2]
    if not isinstance(data, dict):
        errors.append(f"{path.relative_to(ROOT)}: frontmatter is not a mapping")
        return {}, parts[2]
    return data, parts[2]


def build_link_index(paths: list[Path]) -> tuple[set[str], set[str]]:
    stems: set[str] = set(); rels: set[str] = set()
    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        stems.add(path.stem)
        rels.add(rel); rels.add(rel.removesuffix(".md"))
    return stems, rels


def normalize_target(value: str) -> str:
    return value.split("|", 1)[0].split("#", 1)[0].strip().removesuffix(".md")


def resolves(target: str, stems: set[str], rels: set[str]) -> bool:
    return bool(target) and (target in stems or target in rels)


def flatten_nav(node: Any) -> list[str]:
    if isinstance(node, str): return [node]
    if isinstance(node, list):
        out: list[str] = []
        for item in node: out.extend(flatten_nav(item))
        return out
    if isinstance(node, dict):
        out: list[str] = []
        for item in node.values(): out.extend(flatten_nav(item))
        return out
    return []


def family_inventory() -> dict[str, set[str]]:
    families: dict[str, set[str]] = defaultdict(set)
    for path in (ROOT / "papers").glob("*.md"):
        if path.name == "index.md": continue
        m = re.match(r"(.+)-(analysis|method|results|critical)$", path.stem)
        if m: families[m.group(1)].add(m.group(2))
        else: families[path.stem].add("single")
    return dict(families)


def registry_contains(index_path: Path, target: str) -> bool:
    return f"[[{target}]]" in index_path.read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []
    paths = managed_files()
    for core in CORE_PATHS:
        if not (ROOT / core).is_file(): errors.append(f"missing core file: {core}")
    for required_index in ["papers/index.md", "entities/index.md", "concepts/index.md", "sources/index.md", "notes/index.md", "comparisons/index.md"]:
        if not (ROOT / required_index).is_file(): errors.append(f"missing section index: {required_index}")
    if errors:
        print("\n".join("ERROR: " + x for x in errors)); return 1

    schema_text = (ROOT / "SCHEMA.md").read_text(encoding="utf-8")
    allowed_tags = set(re.findall(r"`([a-z0-9]+/[a-z0-9-]+)`", schema_text))
    stems, rels = build_link_index(paths)
    ids: dict[str, str] = {}
    page_data: dict[str, dict[str, Any]] = {}

    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        data, body = parse_page(path, errors)
        page_data[rel] = data
        missing = REQUIRED_FIELDS - set(data)
        if missing: errors.append(f"{rel}: missing frontmatter fields {sorted(missing)}")
        if not missing:
            page_id = str(data["id"])
            if page_id in ids: errors.append(f"{rel}: duplicate id {page_id!r}; first used by {ids[page_id]}")
            else: ids[page_id] = rel
            if data["status"] not in ALLOWED_STATUS: errors.append(f"{rel}: invalid status {data['status']!r}")
            if data["confidence"] not in ALLOWED_CONFIDENCE: errors.append(f"{rel}: invalid confidence {data['confidence']!r}")
            if data["type"] not in ALLOWED_TYPES: errors.append(f"{rel}: invalid type {data['type']!r}")
            if data["project"] != PROJECT: errors.append(f"{rel}: project must be {PROJECT!r}")
            if not isinstance(data["tags"], list): errors.append(f"{rel}: tags must be a list")
            else:
                for tag in data["tags"]:
                    if str(tag) not in allowed_tags: errors.append(f"{rel}: tag {tag!r} is absent from namespaced taxonomy")
            if not isinstance(data["sources"], list): errors.append(f"{rel}: sources must be a list")

        full_text = path.read_text(encoding="utf-8")
        if TEMP_RE.search(full_text): errors.append(f"{rel}: contains temporary assistant citation token")
        if "\\|" in full_text and "[[" in full_text: errors.append(f"{rel}: contains escaped wikilink separator")

        links = [normalize_target(x) for x in WIKILINK_RE.findall(body)]
        for link in links:
            if not resolves(link, stems, rels): errors.append(f"{rel}: unresolved wikilink [[{link}]]")
        ptype = data.get("type")
        if ptype not in {"source", "schema", "log", "index"} and len(set(links)) < 2:
            errors.append(f"{rel}: fewer than two outbound wikilinks")

        sources = data.get("sources", []) if isinstance(data.get("sources", []), list) else []
        if ptype not in {"source", "schema", "log", "index"}:
            if sources:
                if not PROVENANCE_RE.search(body): errors.append(f"{rel}: sources listed but no persistent provenance marker")
            elif data.get("status") != "draft" or "## Verification Needed" not in body:
                errors.append(f"{rel}: no source; must be draft with Verification Needed")
        for source in sources:
            source = str(source)
            if source.startswith("sources/") and source.endswith(".md") and not (ROOT / source).is_file():
                errors.append(f"{rel}: canonical source note does not exist: {source}")

    # raw/ is immutable and excluded from normalization. Ensure workflows do not target it for write operations.
    raw_files = list((ROOT / "raw").rglob("*")) if (ROOT / "raw").exists() else []
    if not any(p.is_file() for p in raw_files): errors.append("raw/: no immutable source records found")

    families = family_inventory()
    for family, suffixes in sorted(families.items()):
        source_note = ROOT / "sources" / "papers" / f"{family}.md"
        if not source_note.is_file(): errors.append(f"{family}: missing canonical paper source note")
        if family in ABSTRACT_ONLY:
            if suffixes != {"single"}: errors.append(f"{family}: abstract-only paper must remain a single overview")
            path = ROOT / "papers" / f"{family}.md"
            data = page_data.get(path.relative_to(ROOT).as_posix(), {})
            if data.get("evidence_scope") != "abstract-only": errors.append(f"{family}: missing evidence_scope: abstract-only")
            continue
        expected = {"analysis", "method", "results", "critical"}
        if suffixes != expected: errors.append(f"{family}: incomplete 1+3 family; found {sorted(suffixes)}")
        analysis = ROOT / "papers" / f"{family}-analysis.md"
        text = analysis.read_text(encoding="utf-8") if analysis.exists() else ""
        sections = {int(x) for x in re.findall(r"^##\s+(\d+)(?:\.|-|\s)", text, re.M)}
        missing_sections = set(range(1, 13)) - sections
        if missing_sections: errors.append(f"{analysis.relative_to(ROOT)}: missing overview sections {sorted(missing_sections)}")
        for suffix in ["method", "results", "critical"]:
            if f"[[{family}-{suffix}]]" not in text: errors.append(f"{analysis.relative_to(ROOT)}: missing link to {suffix} page")

    # Every page must be reachable from its exhaustive section registry.
    index_map = {
        "papers": ROOT / "papers/index.md", "entities": ROOT / "entities/index.md",
        "concepts": ROOT / "concepts/index.md", "sources": ROOT / "sources/index.md",
        "notes": ROOT / "notes/index.md", "comparisons": ROOT / "comparisons/index.md",
    }
    for root, index_path in index_map.items():
        for path in (ROOT / root).rglob("*.md"):
            if path.name == "index.md": continue
            target = path.relative_to(ROOT).with_suffix("").as_posix()
            if not registry_contains(index_path, target): errors.append(f"{index_path.relative_to(ROOT)}: missing registry entry [[{target}]]")

    root_index = (ROOT / "index.md").read_text(encoding="utf-8")
    for target in ["papers/index", "entities/index", "concepts/index", "sources/index", "notes/index", "comparisons/index", "SCHEMA", "log"]:
        if f"[[{target}]]" not in root_index: errors.append(f"index.md: missing section link [[{target}]]")

    # Navigation must parse and point to existing pages.
    try:
        mkdocs = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        errors.append(f"mkdocs.yml: invalid YAML: {exc}"); mkdocs = {}
    for target in flatten_nav(mkdocs.get("nav", [])):
        if target.endswith(".md") and not (ROOT / target).is_file(): errors.append(f"mkdocs.yml: missing nav target {target}")

    # Read-only workflow contract.
    for workflow in (ROOT / ".github/workflows").glob("*.yml"):
        text = workflow.read_text(encoding="utf-8")
        rel = workflow.relative_to(ROOT)
        if re.search(r"contents:\s*write", text): errors.append(f"{rel}: contents: write is prohibited")
        for token in ["git push", "git commit", "create-pull-request", "peter-evans/create-pull-request"]:
            if token in text: errors.append(f"{rel}: repository mutation token {token!r} is prohibited")
        if workflow.name.startswith(("register-", "complete-", "finalize-")): errors.append(f"{rel}: one-time mutation workflow is prohibited")

    # Migration artifacts are prohibited from final PR.
    forbidden_names = {"tree-api-test.txt", "dummy", "test-branch-file", "test"}
    for path in ROOT.rglob("*"):
        if path.is_file() and path.name in forbidden_names:
            errors.append(f"forbidden migration artifact: {path.relative_to(ROOT)}")
    for forbidden in ["wiki-repository-snapshot", "Upload repository snapshot"]:
        for workflow in (ROOT / ".github/workflows").glob("*.yml"):
            if forbidden in workflow.read_text(encoding="utf-8"):
                errors.append(f"{workflow.relative_to(ROOT)}: contains temporary migration artifact marker {forbidden!r}")

    if errors:
        print(f"Repository-wide llm-wiki lint failed with {len(errors)} error(s):")
        for error in errors: print("ERROR:", error)
        return 1
    print(f"Repository-wide llm-wiki lint passed for {len(paths)} maintained Markdown pages.")
    print(f"Verified {len(families)} paper families, canonical sources, exhaustive indexes, provenance, links and read-only CI.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
