"""MkDocs hooks for maintaining the public wiki navigation.

The paper navigation is derived from ``docs/papers`` at build time so every
registered paper page is visible in the left sidebar without editing
``mkdocs.yml`` after each ingest.
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml


DOCS_DIR = Path(__file__).resolve().parents[1] / "docs"
PAPERS_DIR = DOCS_DIR / "papers"
PAGE_SUFFIXES = ("analysis", "method", "results", "critical")
PAGE_LABELS = {
    "analysis": "概览",
    "method": "方法",
    "results": "结果",
    "critical": "批判与迁移",
}


def _frontmatter_title(path: Path) -> str:
    """Return a page title from YAML frontmatter, with a safe fallback."""
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            data = yaml.safe_load(text[4:end]) or {}
            title = data.get("title")
            if isinstance(title, str) and title.strip():
                return title.strip()
    return path.stem.replace("-", " ")


def _family_and_kind(stem: str) -> tuple[str, str | None]:
    for kind in PAGE_SUFFIXES:
        suffix = f"-{kind}"
        if stem.endswith(suffix):
            return stem[: -len(suffix)], kind
    return stem, None


def _compact_family_title(title: str) -> str:
    """Trim repetitive page-role wording while retaining paper identity."""
    patterns = (
        r"[：:]?\s*论文分析$",
        r"[：:]?\s*方法机制(?:展开)?$",
        r"[：:]?\s*实验结果(?:与证据核查|展开)?$",
        r"[：:]?\s*结果证据(?:展开)?$",
        r"[：:]?\s*批判(?:性分析)?(?:、迁移与研究机会)?$",
        r"[—-]\s*贡献.*$",
    )
    compact = title
    for pattern in patterns:
        compact = re.sub(pattern, "", compact, flags=re.IGNORECASE).strip()
    return compact or title


def _paper_navigation() -> list[dict[str, Any]]:
    if not PAPERS_DIR.exists():
        return [{"论文索引": "papers/index.md"}]

    families: dict[str, dict[str | None, Path]] = defaultdict(dict)
    for path in sorted(PAPERS_DIR.glob("*.md")):
        if path.name == "index.md":
            continue
        family, kind = _family_and_kind(path.stem)
        families[family][kind] = path

    entries: list[tuple[str, dict[str, Any]]] = []
    for family, pages in families.items():
        preferred = pages.get("analysis") or next(iter(pages.values()))
        family_title = _compact_family_title(_frontmatter_title(preferred))

        if len(pages) == 1:
            relative = preferred.relative_to(DOCS_DIR).as_posix()
            nav_entry: dict[str, Any] = {family_title: relative}
        else:
            children: list[dict[str, str]] = []
            for kind in PAGE_SUFFIXES:
                page = pages.get(kind)
                if page is not None:
                    children.append(
                        {PAGE_LABELS[kind]: page.relative_to(DOCS_DIR).as_posix()}
                    )
            for kind, page in sorted(pages.items(), key=lambda item: str(item[0])):
                if kind not in PAGE_SUFFIXES:
                    children.append(
                        {_frontmatter_title(page): page.relative_to(DOCS_DIR).as_posix()}
                    )
            nav_entry = {family_title: children}

        entries.append((family_title.casefold(), nav_entry))

    entries.sort(key=lambda item: item[0])
    return [{"论文索引": "papers/index.md"}, *[entry for _, entry in entries]]


def on_config(config: Any) -> Any:
    """Replace the curated Papers block with a complete generated block."""
    nav = config.get("nav") or []
    for item in nav:
        if isinstance(item, dict) and "Papers" in item:
            item["Papers"] = _paper_navigation()
            break
    else:
        nav.insert(1, {"Papers": _paper_navigation()})

    config["nav"] = nav
    return config
