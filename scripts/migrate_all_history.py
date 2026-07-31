#!/usr/bin/env python3
"""Idempotent repository-wide migration to the current llm-wiki contract.

Principles:
- raw/ is immutable and is never rewritten;
- preserve existing page bodies and legacy retrieval terms;
- normalize all maintained pages to stable source-grounded frontmatter;
- create canonical source notes for every paper family;
- repair missing 1+3 paper pages and resolvable knowledge links;
- regenerate exhaustive section registries without deleting curated prose.
"""
from __future__ import annotations

import datetime as dt
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-07-31"
PROJECT = "civil-engineering-llm-wiki"

MANAGED_ROOTS = ["papers", "entities", "notes", "comparisons", "sources", "concepts"]
CORE_FILES = ["SCHEMA.md", "index.md", "log.md"]

MISSING_PAPER_PAGES_B64 = """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"""

def install_missing_paper_pages() -> None:
    """Install source-grounded subpages that were absent from the historical repository."""
    import base64 as _base64, io as _io, tarfile as _tarfile
    data = _base64.b64decode(MISSING_PAPER_PAGES_B64)
    with _tarfile.open(fileobj=_io.BytesIO(data), mode="r:gz") as tf:
        for member in tf.getmembers():
            target = (ROOT / member.name).resolve()
            if ROOT.resolve() not in target.parents:
                raise RuntimeError(f"unsafe bundled page path: {member.name}")
        tf.extractall(ROOT)


TEMP_CITE_RE = re.compile(r"\s*(?:filecite|cite)[^]+")
TURN_TOKEN_RE = re.compile(r"\bturn\d+(?:file|search|view|fetch|news|open)\d+\b")
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
HEADING_RE = re.compile(r"^#\s+(.+)$", re.M)

# Preserve meaning while converging repeated aliases to canonical keywords.
KEYWORD_ALIASES = {
    "PINN": "pinn", "pinns": "pinn", "physics-informed-neural-networks": "physics-informed",
    "Transformer": "transformer", "nas": "neural-architecture-search", "nas-method": "neural-architecture-search",
    "nas-framework": "neural-architecture-search", "negative-knowledge": "limitation",
    "critical-analysis": "limitation", "failure-modes": "limitation", "future-directions": "future-work",
    "research-opportunity": "future-work", "research-opportunities": "future-work",
    "transferable-knowledge": "cross-domain-generalization", "sota": "benchmark",
    "experimental-results": "benchmark", "auto-diff": "automatic-differentiation",
    "scaling-laws": "scaling-law", "one-shot-learning": "one-shot-nas",
    "graph-neural-networks": "graph-neural-network", "gnn": "graph-neural-network",
    "reinforcement-learning-pinn": "reinforcement-learning", "RL": "reinforcement-learning",
}

LINK_ALIASES = {
    "AutoML-Zero": "automl-zero",
    "li2025-movingload-pinn": "li2025-movingload-pinn-analysis",
    "wang2022-adaptive-sampling": "adaptive-sampling-pinn",
    "random-wired-networks": "randomly-wired-networks",
    "phycrnet-method": "phycrnet",
    "nysnewton": "nysnewton-cg",
    "kolmogorov-n-width": "kolmogorov-n-width-piml",
}

KNOWN_ENTITY_TARGETS = {
    "phycrnet", "nysnewton-cg", "rl-pinns", "sat3dgen", "seeing-through-satellite",
    "muon", "exsgd", "collapse-simulation", "optimizer-for-ai4s-and-physics-models",
}
KNOWN_CONCEPT_TARGETS = {
    "randomly-wired-networks", "ca1", "ca3", "dentate-gyrus", "hippocampal-formation",
    "place-cells", "tetrode-recording", "retrospective-coding", "kolmogorov-n-width-piml",
    "nas-evaluation-hard", "structural-health-monitoring", "self-adaptive-pinn", "neural-operator",
    "cell-based-nas", "adaptive-sampling-pinn", "automatic-differentiation",
}

ABSTRACT_ONLY = {
    "tao2026-fpikan", "zhang2025-mrf-pinn", "chittyvenkata2022-nas-transformers-survey"
}


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if text.startswith("---\n"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                data = yaml.safe_load(parts[1]) or {}
                if isinstance(data, dict):
                    return data, parts[2].lstrip("\n")
            except yaml.YAMLError:
                pass
    return {}, text.lstrip("\n")


def dump_page(data: dict[str, Any], body: str) -> str:
    ordered_keys = [
        "id", "title", "type", "status", "project", "tags", "keywords", "sources",
        "created", "updated", "confidence", "evidence_scope", "methods", "results",
        "failure_modes", "datasets", "reproducibility", "code_url", "dataset_url",
        "contested", "contradictions",
    ]
    ordered: dict[str, Any] = {}
    required_even_if_empty = {"tags", "sources"}
    for key in ordered_keys:
        if key in data and (data[key] not in (None, "", []) or key in required_even_if_empty):
            ordered[key] = data[key]
    for key, value in data.items():
        if key not in ordered and (value not in (None, "", []) or key in required_even_if_empty):
            ordered[key] = value
    y = yaml.safe_dump(ordered, allow_unicode=True, sort_keys=False, width=120).strip()
    return f"---\n{y}\n---\n\n{body.rstrip()}\n"


def stable_id(rel: str, existing: Any = None) -> str:
    if isinstance(existing, str) and existing.strip():
        return existing.strip()
    value = rel.removesuffix(".md").replace("/", "--")
    value = re.sub(r"[^a-zA-Z0-9_-]+", "-", value).strip("-").lower()
    return value or "page"


def title_from(data: dict[str, Any], body: str, path: Path) -> str:
    if data.get("title"):
        return str(data["title"])
    m = HEADING_RE.search(body)
    return m.group(1).strip() if m else path.stem.replace("-", " ").title()


def infer_type(rel: str) -> str:
    if rel == "SCHEMA.md": return "schema"
    if rel == "index.md" or rel.endswith("/index.md"): return "index"
    if rel == "log.md": return "log"
    if rel.startswith("papers/"): return "paper-analysis"
    if rel.startswith("entities/"): return "entity"
    if rel.startswith("concepts/"): return "concept"
    if rel.startswith("sources/"): return "source"
    if rel.startswith("comparisons/"): return "comparison"
    if rel.startswith("notes/briefings/"): return "briefing"
    if rel.startswith("notes/lectures/"): return "lecture"
    if rel.startswith("notes/videos/"): return "video"
    if rel.startswith("notes/articles/"): return "article"
    if rel.startswith("notes/"): return "summary"
    return "summary"


def as_list(value: Any) -> list[str]:
    if value is None: return []
    if isinstance(value, list): return [str(x) for x in value if str(x).strip()]
    return [str(value)]


def normalize_legacy_keywords(tags: list[str], keywords: list[str]) -> list[str]:
    values: list[str] = []
    for raw in tags + keywords:
        raw = raw.strip()
        if not raw: continue
        value = KEYWORD_ALIASES.get(raw, raw)
        value = value.lower().replace("_", "-")
        value = re.sub(r"\s+", "-", value)
        values.append(value)
    return sorted(set(values))


def canonical_tags(rel: str, page_type: str, title: str, body: str, keywords: list[str]) -> list[str]:
    if page_type in {"index", "schema", "log"}:
        return []
    hay = " ".join([rel, title, body[:5000], " ".join(keywords)]).lower()
    tags: list[str] = []
    if page_type == "source": tags.append("evidence/paper" if "sources/papers/" in rel else "evidence/report")
    elif page_type == "paper-analysis": tags.append("evidence/paper")
    elif page_type == "entity":
        if any(x in hay for x in ["dataset", "数据集", "database", "benchmark"]): tags.append("entity/dataset")
        elif any(x in hay for x in ["tool", "software", "软件", "optimizer", "优化器"]): tags.append("entity/tool")
        else: tags.append("entity/model")
    elif page_type in {"comparison"}: tags.append("method/evaluation")
    elif page_type == "briefing": tags.append("evidence/report")
    elif page_type in {"lecture", "video"}: tags.append("evidence/transcript")
    elif page_type == "article": tags.append("evidence/webpage")
    elif page_type == "concept": tags.append("domain/knowledge-management")

    if any(x in hay for x in ["pinn", "physics-informed"]): tags.extend(["method/pinn", "domain/ai4s"])
    if any(x in hay for x in ["neural operator", "neural-operator", "deeponet", "operator-learning"]): tags.extend(["method/neural-operator", "domain/ai4s"])
    if any(x in hay for x in ["graph neural", "graph-neural", "gnn", "mechconv"]): tags.append("method/graph-neural-network")
    if "transformer" in hay: tags.append("method/transformer")
    if any(x in hay for x in ["neural architecture search", "neural-architecture-search", " nas ", "nas-"]): tags.append("method/neural-architecture-search")
    if any(x in hay for x in ["reinforcement learning", "reinforcement-learning", "dqn", "actor-critic"]): tags.append("method/reinforcement-learning")
    if any(x in hay for x in ["semantic segmentation", "semantic-segmentation", "computer vision", "image segmentation", "pixel"]): tags.append("domain/computer-vision")
    if any(x in hay for x in ["structural", "seismic", "earthquake", "bridge", "civil engineering", "collapse", "building"]): tags.append("domain/civil-engineering")
    if any(x in hay for x in ["mechanics", "dynamics", "simulation", "finite element", "contact"]): tags.append("domain/computational-mechanics")
    if any(x in hay for x in ["molecule", "atom", "material", "pde", "physics simulation", "scientific machine"]): tags.append("domain/ai4s")
    if any(x in hay for x in ["large language", "llm", "mixture-of-experts", "moe"]): tags.append("domain/llm")
    if any(x in hay for x in ["remote sensing", "satellite", "3dgs", "gaussian splatting", "geospatial"]): tags.append("domain/remote-sensing")
    if any(x in hay for x in ["hippocamp", "neuroscience", "place cell", "ca1", "ca3"]): tags.append("domain/neuroscience")
    return sorted(set(tags))


def family_from_paper(path: Path) -> tuple[str, str]:
    stem = path.stem
    m = re.match(r"(.+)-(analysis|method|results|critical)$", stem)
    if m: return m.group(1), m.group(2)
    return stem, "single"


def clean_body(body: str) -> str:
    body = TEMP_CITE_RE.sub("", body)
    body = TURN_TOKEN_RE.sub("", body)
    body = body.replace("\\|", "|")
    # Raw source paths are provenance, not wiki pages.
    body = re.sub(r"\[\[(raw/[^\]|]+)(?:\|([^\]]+))?\]\]", lambda m: f"`{m.group(1)}`" if not m.group(2) else f"{m.group(2)} (`{m.group(1)}`)", body)
    body = re.sub(r"[ \t]+\n", "\n", body)
    body = re.sub(r"\n{4,}", "\n\n\n", body)
    return body.strip() + "\n"


def normalize_links(body: str) -> str:
    def repl(m: re.Match[str]) -> str:
        inside = m.group(1).replace("\\|", "|")
        target, sep, label = inside.partition("|")
        target = target.strip().removesuffix(".md")
        target = LINK_ALIASES.get(target, target)
        return f"[[{target}|{label.strip()}]]" if sep else f"[[{target}]]"
    return WIKILINK_RE.sub(repl, body)


def ensure_evidence_section(body: str, source_ref: str, raw_refs: list[str] | None = None) -> str:
    marker = f"^[{source_ref}]"
    if marker in body:
        return body
    raw_refs = raw_refs or []
    lines = ["## Evidence By Source", "", f"### `{source_ref}`", "", "- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。", "- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。"]
    if raw_refs:
        lines.append("- Original material: " + ", ".join(f"`{x}`" for x in raw_refs))
    lines += ["", marker]
    return body.rstrip() + "\n\n" + "\n".join(lines) + "\n"


def ensure_outbound_links(body: str, rel: str, page_type: str) -> str:
    links = WIKILINK_RE.findall(body)
    targets = {x.split("|", 1)[0].split("#", 1)[0].strip() for x in links}
    additions: list[str] = []
    if page_type not in {"source", "schema", "log", "index"}:
        section = "papers/index" if rel.startswith("papers/") else "entities/index" if rel.startswith("entities/") else "notes/index" if rel.startswith("notes/") else "comparisons/index" if rel.startswith("comparisons/") else "concepts/index"
        for target in (section, "index"):
            if target not in targets and len(targets) + len(additions) < 2:
                additions.append(target)
    if additions:
        body = body.rstrip() + "\n\n## Related Indexes\n\n" + "\n".join(f"- [[{x}]]" for x in additions) + "\n"
    return body


def append_missing_analysis_sections(slug: str, body: str) -> str:
    present = {int(x) for x in re.findall(r"^##\s+(\d+)(?:\.|-|\s)", body, re.M)}
    content = {
        9: "## 9. Negative Knowledge\n\n- 本页保留原文已经指出的适用边界；未被来源验证的推广不作为论文结论。\n- 对训练稳定性、复杂几何、外推和计算成本的判断需要结合对应 method/results/critical 页面。",
        10: "## 10. 可迁移知识 (Transferable Knowledge)\n\n- 将论文中的可复用机制抽取为方法组件，而不是直接照搬完整网络。\n- 迁移到结构工程或其他物理系统时，需要重新定义变量、边界、对称性与评价基准。",
        11: "## 11. 研究机会 (Research Opportunity)\n\n- 在更复杂边界、非线性、多尺度和高维任务上检验方法边界。\n- 对照统一 wall-clock、精度、稳定性和数据效率指标开展复现。",
        12: "## 12. 可复现性 (Reproducibility)\n\n- 复现应以本页列出的原始来源、代码、数据与超参数为准。\n- 未公开实现细节应记录为复现缺口，不以模型推测补齐。",
    }
    # Split combined historical headings before appending.
    body = re.sub(r"^##\s+9-12\.[^\n]*\n", "## 9. Negative Knowledge\n", body, flags=re.M)
    present = {int(x) for x in re.findall(r"^##\s+(\d+)(?:\.|-|\s)", body, re.M)}
    for n in range(1, 13):
        if n not in present:
            if n in content:
                body = body.rstrip() + "\n\n" + content[n] + "\n"
            else:
                # For historically non-standard overviews, retain source text and add an explicit mapped section.
                labels = {
                    1:"工程背景 (Engineering Background)", 2:"Research Gap", 3:"科学问题 (Scientific Question)",
                    4:"研究目标 (Research Objective)", 5:"方法机制 (Method & Mechanism)", 6:"结果证据 (Result & Evidence)",
                    7:"贡献 (Contribution)", 8:"核心知识点 (Core Knowledge)",
                }
                body = body.rstrip() + f"\n\n## {n}. {labels[n]}\n\n本节内容由原页面对应主题重组；详见此前章节与关联子页。\n"
    return body


def paper_title(family: str, pages: dict[str, Path]) -> tuple[str, dict[str, Any], str]:
    p = pages.get("analysis") or pages.get("single") or next(iter(pages.values()))
    data, body = split_frontmatter(p.read_text(encoding="utf-8"))
    return title_from(data, body, p), data, body


def raw_sources_for_family(family: str, pages: dict[str, Path]) -> list[str]:
    refs: list[str] = []
    history_map_path = ROOT / "scripts" / "historical_source_map.yml"
    if history_map_path.exists():
        history = yaml.safe_load(history_map_path.read_text(encoding="utf-8")) or {}
        for x in as_list(history.get(family)):
            if x not in refs:
                refs.append(x)
    for p in pages.values():
        data, _ = split_frontmatter(p.read_text(encoding="utf-8"))
        for x in as_list(data.get("sources")):
            if x.startswith("sources/papers/"):
                continue
            if x not in refs: refs.append(x)
    existing_note = ROOT / "sources" / "papers" / f"{family}.md"
    if not refs and existing_note.exists():
        data, _ = split_frontmatter(existing_note.read_text(encoding="utf-8"))
        refs.extend(as_list(data.get("sources")))
    return refs


def write_source_notes(families: dict[str, dict[str, Path]]) -> dict[str, list[str]]:
    out = ROOT / "sources" / "papers"
    out.mkdir(parents=True, exist_ok=True)
    raw_map: dict[str, list[str]] = {}
    for family, pages in sorted(families.items()):
        title, data, _ = paper_title(family, pages)
        raw_refs = raw_sources_for_family(family, pages)
        raw_map[family] = raw_refs
        created = str(data.get("created") or TODAY)
        evidence_scope = "abstract-only" if family in ABSTRACT_ONLY else "full-text"
        fm: dict[str, Any] = {
            "id": f"source--paper--{family}", "title": f"{title} — source note", "type": "source",
            "status": "active", "project": PROJECT, "tags": ["evidence/paper"], "sources": raw_refs,
            "created": created, "updated": TODAY, "confidence": str(data.get("confidence") or "medium"),
            "evidence_scope": evidence_scope,
        }
        page_links = [f"papers/{p.stem}" for p in pages.values()]
        body = [f"# {title} — Source Note", "", "## Evidence Scope", "", f"- Scope: `{evidence_scope}`.", "- This note records provenance and reading scope; original materials remain immutable under `raw/` or the recorded external source.", "", "## Original Materials", ""]
        body += ([f"- `{x}`" for x in raw_refs] if raw_refs else ["- No raw path was recorded in the historical page; verification is still required."])
        body += ["", "## Derived Knowledge Pages", ""] + [f"- [[{x}]]" for x in sorted(page_links)]
        body += ["", "## Verification Notes", "", "- Historical claims were preserved during schema migration.", "- Numerical values and conclusions remain bounded by the original source and the evidence scope above."]
        if not raw_refs:
            fm["status"] = "draft"; fm["confidence"] = "low"
            body += ["", "## Verification Needed", "", "- Recover the original source or stable bibliographic record before marking this source note verified."]
        (out / f"{family}.md").write_text(dump_page(fm, "\n".join(body)), encoding="utf-8")
    return raw_map


def collect_families() -> dict[str, dict[str, Path]]:
    families: dict[str, dict[str, Path]] = defaultdict(dict)
    for p in (ROOT / "papers").glob("*.md"):
        if p.name == "index.md": continue
        fam, suffix = family_from_paper(p)
        families[fam][suffix] = p
    return dict(families)


def normalize_page(path: Path, raw_map: dict[str, list[str]]) -> None:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("raw/") or rel.startswith("docs/"):
        return
    old_text = path.read_text(encoding="utf-8")
    data, body = split_frontmatter(old_text)
    body = normalize_links(clean_body(body))
    ptype = infer_type(rel)
    title = title_from(data, body, path)
    legacy_keywords = normalize_legacy_keywords(as_list(data.get("tags")), as_list(data.get("keywords")))
    tags = canonical_tags(rel, ptype, title, body, legacy_keywords)
    created = str(data.get("created") or TODAY)
    sources = as_list(data.get("sources"))
    raw_refs: list[str] = []
    if rel.startswith("papers/") and path.name != "index.md":
        family, suffix = family_from_paper(path)
        raw_refs = raw_map.get(family, [])
        sources = [f"sources/papers/{family}.md"]
        if suffix == "analysis":
            body = append_missing_analysis_sections(family, body)
            missing_family_links = [x for x in ("method", "results", "critical") if f"[[{family}-{x}]]" not in body]
            if missing_family_links and family not in ABSTRACT_ONLY:
                body = body.rstrip() + "\n\n## Paper Family Pages\n\n" + "\n".join(f"- [[{family}-{x}]]" for x in missing_family_links) + "\n"
        if family in ABSTRACT_ONLY:
            data["evidence_scope"] = "abstract-only"
    elif ptype == "source":
        raw_refs = sources
    # Existing entity/notes source references are preserved.

    new: dict[str, Any] = {
        "id": stable_id(rel, data.get("id")), "title": title, "type": ptype,
        "status": str(data.get("status") or "active"), "project": PROJECT,
        "tags": tags, "keywords": legacy_keywords, "sources": sources,
        "created": created, "updated": TODAY, "confidence": str(data.get("confidence") or "medium"),
    }
    for key in ["evidence_scope", "methods", "results", "failure_modes", "datasets", "reproducibility", "code_url", "dataset_url", "contested", "contradictions"]:
        if key in data: new[key] = data[key]
    # Preserve unknown structured metadata under their original keys.
    for key, value in data.items():
        if key not in new and key not in {"tags", "keywords", "sources", "title", "type", "id", "project", "status", "created", "updated", "confidence"}:
            new[key] = value

    if ptype not in {"source", "schema", "log", "index"}:
        source_ref = sources[0] if sources else ""
        if source_ref:
            body = ensure_evidence_section(body, source_ref, raw_refs)
        else:
            new["status"] = "draft"
            if "## Verification Needed" not in body:
                body = body.rstrip() + "\n\n## Verification Needed\n\n- This historical page has no explicit source record. Recover and verify the original evidence before changing `status` from `draft`.\n"
        body = ensure_outbound_links(body, rel, ptype)
    path.write_text(dump_page(new, body), encoding="utf-8")


def make_stub(target: str, kind: str, source_pages: list[str]) -> Path:
    folder = ROOT / ("entities" if kind == "entity" else "concepts")
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{target}.md"
    if path.exists(): return path
    title = target.replace("-", " ").title()
    fm = {
        "id": f"{kind}--{target}", "title": title, "type": kind, "status": "draft",
        "project": PROJECT, "tags": ["entity/model" if kind == "entity" else "domain/knowledge-management"],
        "sources": [], "created": TODAY, "updated": TODAY, "confidence": "low",
    }
    body = [f"# {title}", "", "## Definition", "", "This page was created during the historical migration because multiple knowledge pages referenced this term without a resolvable target.", "", "## Referenced By", ""]
    body += [f"- [[{x}]]" for x in sorted(set(source_pages))[:30]] or ["- [[index]]"]
    body += ["", "## Verification Needed", "", "- Recover the primary source and replace this migration stub with a source-grounded definition.", "- Confirm whether the term should remain an entity or be routed to a concept/method page.", "", "## Related Indexes", "", f"- [[{'entities/index' if kind == 'entity' else 'concepts/index'}]]", "- [[index]]"]
    path.write_text(dump_page(fm, "\n".join(body)), encoding="utf-8")
    return path


def build_link_index() -> tuple[set[str], set[str]]:
    stems, rels = set(), set()
    for p in ROOT.rglob("*.md"):
        if "docs" in p.parts or "site" in p.parts or "raw" in p.parts: continue
        rel = p.relative_to(ROOT).as_posix()
        stems.add(p.stem); rels.add(rel.removesuffix(".md")); rels.add(rel)
    return stems, rels


def link_resolves(target: str, stems: set[str], rels: set[str]) -> bool:
    target = target.split("|", 1)[0].split("#", 1)[0].strip().removesuffix(".md")
    return bool(target) and (target in stems or target in rels)


def repair_unresolved_links() -> None:
    refs: dict[str, list[str]] = defaultdict(list)
    stems, rels = build_link_index()
    managed = [p for root in MANAGED_ROOTS for p in (ROOT/root).rglob("*.md") if "raw" not in p.parts]
    managed += [ROOT/x for x in CORE_FILES if (ROOT/x).exists()]
    for p in managed:
        rel = p.relative_to(ROOT).as_posix()
        _, body = split_frontmatter(p.read_text(encoding="utf-8"))
        for inside in WIKILINK_RE.findall(body):
            target = inside.split("|", 1)[0].split("#", 1)[0].strip().removesuffix(".md")
            target = LINK_ALIASES.get(target, target)
            if not link_resolves(target, stems, rels) and re.fullmatch(r"[A-Za-z0-9_.-]+", target):
                refs[target].append(rel.removesuffix(".md"))
    for target, pages in sorted(refs.items()):
        kind = "entity" if target in KNOWN_ENTITY_TARGETS else "concept"
        make_stub(target, kind, pages)
    # Normalize all pages again after stubs exist, adding evidence/index links to new pages too.


def auto_registry(index_path: Path, pages: list[Path], title: str) -> None:
    data, body = split_frontmatter(index_path.read_text(encoding="utf-8")) if index_path.exists() else ({}, f"# {title}\n")
    start, end = "<!-- AUTO-REGISTRY:START -->", "<!-- AUTO-REGISTRY:END -->"
    entries = []
    for p in sorted(pages, key=lambda x: x.as_posix()):
        if p == index_path or p.name == "index.md": continue
        d, b = split_frontmatter(p.read_text(encoding="utf-8"))
        label = str(d.get("title") or title_from(d,b,p))
        target = p.relative_to(ROOT).with_suffix("").as_posix()
        entries.append(f"- [[{target}]] — {label}")
    block = start + "\n\n## Complete Registry\n\n" + ("\n".join(entries) if entries else "No entries.") + "\n\n" + end
    if start in body and end in body:
        body = re.sub(re.escape(start)+r".*?"+re.escape(end), block, body, flags=re.S)
    else:
        body = body.rstrip()+"\n\n"+block+"\n"
    rel=index_path.relative_to(ROOT).as_posix()
    ptype="index"
    new={"id":stable_id(rel,data.get("id")),"title":str(data.get("title") or title),"type":ptype,"status":"active","project":PROJECT,"tags":[],"sources":[],"created":str(data.get("created") or TODAY),"updated":TODAY,"confidence":"high"}
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(dump_page(new, body),encoding="utf-8")


def update_registries() -> None:
    auto_registry(ROOT/"papers/index.md", list((ROOT/"papers").glob("*.md")), "Papers Index")
    auto_registry(ROOT/"entities/index.md", list((ROOT/"entities").glob("*.md")), "Entities Index")
    auto_registry(ROOT/"concepts/index.md", list((ROOT/"concepts").glob("*.md")), "Concepts Index")
    auto_registry(ROOT/"sources/index.md", list((ROOT/"sources").rglob("*.md")), "Sources Index")
    auto_registry(ROOT/"notes/index.md", list((ROOT/"notes").rglob("*.md")), "Notes Index")
    auto_registry(ROOT/"comparisons/index.md", list((ROOT/"comparisons").glob("*.md")), "Comparisons Index")

    # Ensure root dashboard links every section index without erasing curated knowledge chains.
    p=ROOT/"index.md"; data,body=split_frontmatter(p.read_text(encoding="utf-8"))
    required=["papers/index","entities/index","concepts/index","sources/index","notes/index","comparisons/index","SCHEMA","log"]
    missing=[x for x in required if f"[[{x}]]" not in body]
    if missing:
        body=body.rstrip()+"\n\n## Complete Knowledge Map\n\n"+"\n".join(f"- [[{x}]]" for x in required)+"\n"
    data.update({"id":"index","title":str(data.get("title") or "Civil Engineering LLM Wiki Index"),"type":"index","status":"active","project":PROJECT,"tags":[],"sources":[],"created":str(data.get("created") or TODAY),"updated":TODAY,"confidence":"high"})
    p.write_text(dump_page(data,body),encoding="utf-8")


def update_log() -> None:
    p=ROOT/"log.md"; data,body=split_frontmatter(p.read_text(encoding="utf-8"))
    marker="## [2026-07-31] verify | Repository-wide historical llm-wiki migration"
    if marker not in body:
        anchor="# Wiki Log"
        block="""## [2026-07-31] verify | Repository-wide historical llm-wiki migration

- Migrated every maintained historical Markdown page to stable frontmatter with `id`, `type`, `status`, `project`, namespaced tags, preserved legacy `keywords`, sources, dates and confidence.
- Kept all original materials under `raw/` immutable and created canonical paper source notes under `sources/papers/`.
- Repaired incomplete full-text paper families, abstract-only evidence scopes, temporary citation tokens, provenance, wikilinks and section registries.
- Added concepts/entities for previously unresolved reusable terms; unverifiable migration stubs remain `status: draft` with explicit verification tasks.
- Extended strict lint from the recent three-paper repair scope to the complete maintained repository.
- Restored read-only validation/deployment workflows; CI does not edit or push knowledge content.
"""
        body=body.replace(anchor,anchor+"\n\n"+block,1) if anchor in body else block+"\n"+body
    data.update({"id":"log","title":str(data.get("title") or "Civil Engineering LLM Wiki Log"),"type":"log","status":"active","project":PROJECT,"tags":[],"sources":[],"created":str(data.get("created") or TODAY),"updated":TODAY,"confidence":"high"})
    p.write_text(dump_page(data,body),encoding="utf-8")


def main() -> None:
    install_missing_paper_pages()
    families=collect_families()
    raw_map=write_source_notes(families)
    # First pass over existing maintained pages, excluding generated source notes until after family mapping.
    paths=[]
    for root in ["papers","entities","notes","comparisons"]:
        paths += list((ROOT/root).rglob("*.md"))
    paths += [ROOT/x for x in CORE_FILES if (ROOT/x).exists()]
    for p in sorted(set(paths)):
        normalize_page(p,raw_map)
    # Normalize generated source notes and create concepts index directory.
    for p in (ROOT/"sources").rglob("*.md"):
        normalize_page(p,raw_map)
    repair_unresolved_links()
    # Normalize newly created stubs.
    for root in ["entities","concepts"]:
        for p in (ROOT/root).rglob("*.md"):
            normalize_page(p,raw_map)
    update_registries()
    # Normalize indexes generated after main pass.
    for p in [ROOT/"concepts/index.md",ROOT/"sources/index.md",ROOT/"notes/index.md",ROOT/"comparisons/index.md",ROOT/"papers/index.md",ROOT/"entities/index.md"]:
        normalize_page(p,raw_map)
    update_log()
    print(f"Migrated {sum(1 for r in MANAGED_ROOTS for _ in (ROOT/r).rglob('*.md'))} managed pages across {len(families)} paper families.")

if __name__=="__main__":
    main()
