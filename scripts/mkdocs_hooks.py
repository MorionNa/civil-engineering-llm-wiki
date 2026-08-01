"""MkDocs hooks：在构建时为所有知识分区生成完整左侧导航。"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

DOCS_DIR = Path(__file__).resolve().parents[1] / "docs"
PAGE_SUFFIXES = ("analysis", "method", "results", "critical")
PAGE_LABELS = {
    "analysis": "概览",
    "method": "方法",
    "results": "结果",
    "critical": "批判与迁移",
}
SECTION_CONFIG = {
    "Papers": ("papers", "论文索引"),
    "Entities": ("entities", "实体索引"),
    "Concepts": ("concepts", "概念索引"),
    "Sources": ("sources", "来源索引"),
    "Notes": ("notes", "笔记索引"),
    "Comparisons": ("comparisons", "对比索引"),
}


def _frontmatter_title(path: Path) -> str:
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


def _compact_title(title: str) -> str:
    patterns = (
        r"[：:]?\s*论文分析$",
        r"[：:]?\s*方法机制(?:展开)?$",
        r"[：:]?\s*(?:实验)?结果(?:证据|与证据核查|展开)?$",
        r"[：:]?\s*批判(?:性分析)?(?:、迁移与研究机会)?$",
        r"[—-]\s*贡献.*$",
    )
    compact = title
    for pattern in patterns:
        compact = re.sub(pattern, "", compact, flags=re.IGNORECASE).strip()
    return compact or title


def _paper_navigation(section_dir: Path, index_label: str) -> list[dict[str, Any]]:
    families: dict[str, dict[str | None, Path]] = defaultdict(dict)
    for path in sorted(section_dir.glob("*.md")):
        if path.name == "index.md":
            continue
        family, kind = _family_and_kind(path.stem)
        families[family][kind] = path

    entries: list[tuple[str, dict[str, Any]]] = []
    for pages in families.values():
        preferred = pages.get("analysis") or next(iter(pages.values()))
        title = _compact_title(_frontmatter_title(preferred))
        if len(pages) == 1:
            entry: dict[str, Any] = {title: preferred.relative_to(DOCS_DIR).as_posix()}
        else:
            children: list[dict[str, str]] = []
            for kind in PAGE_SUFFIXES:
                page = pages.get(kind)
                if page is not None:
                    children.append({PAGE_LABELS[kind]: page.relative_to(DOCS_DIR).as_posix()})
            entry = {title: children}
        entries.append((title.casefold(), entry))
    entries.sort(key=lambda item: item[0])
    return [{index_label: "papers/index.md"}, *[entry for _, entry in entries]]


def _directory_navigation(directory: Path) -> list[dict[str, Any]]:
    items: list[tuple[str, dict[str, Any]]] = []
    for child in sorted(directory.iterdir()):
        if child.name == "index.md" or child.name.startswith("."):
            continue
        if child.is_dir():
            nested = _directory_navigation(child)
            if nested:
                label = child.name.replace("-", " ").title()
                items.append((label.casefold(), {label: nested}))
        elif child.suffix == ".md":
            title = _frontmatter_title(child)
            items.append((title.casefold(), {title: child.relative_to(DOCS_DIR).as_posix()}))
    items.sort(key=lambda item: item[0])
    return [entry for _, entry in items]


def _section_navigation(section: str, index_label: str) -> list[dict[str, Any]]:
    section_dir = DOCS_DIR / section
    index_path = f"{section}/index.md"
    if not section_dir.exists():
        return [{index_label: index_path}]
    if section == "papers":
        return _paper_navigation(section_dir, index_label)
    return [{index_label: index_path}, *_directory_navigation(section_dir)]


def on_config(config: Any) -> Any:
    nav = config.get("nav") or []
    existing = {next(iter(item)): item for item in nav if isinstance(item, dict) and item}

    rebuilt: list[dict[str, Any]] = []
    for item in nav:
        if not isinstance(item, dict) or not item:
            rebuilt.append(item)
            continue
        label = next(iter(item))
        if label in SECTION_CONFIG:
            section, index_label = SECTION_CONFIG[label]
            rebuilt.append({label: _section_navigation(section, index_label)})
        else:
            rebuilt.append(item)

    present = {next(iter(item)) for item in rebuilt if isinstance(item, dict) and item}
    insert_at = 1
    for label, (section, index_label) in SECTION_CONFIG.items():
        if label not in present:
            rebuilt.insert(insert_at, {label: _section_navigation(section, index_label)})
            insert_at += 1

    config["nav"] = rebuilt
    return config
