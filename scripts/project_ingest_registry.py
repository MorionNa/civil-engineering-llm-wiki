"""Generate the exhaustive nonlinear-pinn project ingest registry."""

from __future__ import annotations

import re
from pathlib import Path

import yaml


WIKI = Path(__file__).resolve().parents[1]
PROJECT = WIKI.parents[1]
MANIFEST = WIKI / "comparisons" / "project-scheme-ingest-manifest-2026-08-03.md"
COMPARISONS = WIKI / "comparisons"

ALIASES = {
    "cdno-d-formal-v2-result-20260802": "cdno-d-formal-v2-parent-source-sync-result-20260802",
    "chart-cnr-o0-audit-result-20260802": "chart-cnr-o0-audit-20260802",
    "chart-sr-n0-audit-result-20260802": "chart-sr-n0-audit-20260802",
    "cycle19-ceic-m0-design-20260803": "cycle19_ceic_m0_20260803",
    "independent-boucwen-split-contract-v1": "independent_boucwen_split_contract_v1_20260803",
    "lco-rk48-shared-mechconv-result-20260803": "lco_rk48_shared_m0_nogo_20260803",
    "rpsl-mechconv-design-20260803": "rpsl_literature_design_20260803",
    "selected-kkt-projection-m0-result-20260802": "mtp-mechconv-v2-selected-kkt-projection-m0-negative-20260802",
    "temporal-parallel-a-prime-m0-result-20260802": "mtp-mechconv-v2-a-prime-s4d-m0-negative-20260802",
    "temporal-parallel-bemci-m0-local-result-20260802": "temporal-parallel-bemci-m0-negative-20260802",
    "temporal-parallel-cgerc-v3-m0-result-20260802": "cgerc-v3-m0-negative-20260802",
    "temporal-parallel-cmej2-m0-result-20260802": "cmej2-m0-negative-20260802",
    "temporal-parallel-dstr-cvar-local-result-20260802": "temporal-parallel-dstr-cvar-negative-20260802",
    "temporal-parallel-impulse-bridge-screen-20260802": "mtp-mechconv-v2-impulse-bridge-negative-20260802",
    "temporal-parallel-ppec-m0-local-result-20260802": "temporal-parallel-ppec-m0-negative-20260802",
    "temporal-parallel-selected-velocityadapter-screen-v4-20260802": "mtp-mechconv-v2-selected-nonintegrated-adapter-screen-v4-negative-20260802",
    "temporal-parallel-tddm-m0-remote-result-20260802": "temporal-parallel-tddm-m0-negative-20260802",
    "v22-causal-proposal-sensitivity-result-20260802": "cycle10_v22_causal-proposal-sensitivity-20260802",
    "v23-pact-mechconv-result-20260802": "cycle11_v23_pact-result-20260802",
    "v25-cclro-mechconv-result-20260802": "cycle13_v25_cclro-result-20260802",
    "v26-literature-evidence-20260803": "cycle14_v26-literature-evidence-20260803",
    "v26-rcpp-mechconv-result-20260803": "cycle14_v26_rcpp-result-20260803",
    "v27-cdno-d-teacher-compiled-mechconv-result-20260803": "cycle15_v27_cdno-d-result-20260803",
    "v28-block-causal-state-flow-result-20260803": "cycle16_v28-block-causal-state-flow-result-20260803",
    "v30-lfct-frequency-conditioned-parent-result-20260803": "cycle18_v30-lfct-remote-result-20260803",
}


def replace_block(text: str, marker: str, body: str) -> str:
    start = f"<!-- {marker}:START -->"
    end = f"<!-- {marker}:END -->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    replacement = f"{start}\n{body.rstrip()}\n{end}"
    updated, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError(f"missing marker block: {marker}")
    return updated


def page_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"(?m)^#\s+(.+?)\s*$", text)
    return match.group(1).strip() if match else path.stem


def comparison_slugs() -> set[str]:
    return {path.stem for path in COMPARISONS.glob("*.md") if path.name != "index.md"}


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def infer_target(stem: str, slugs: set[str]) -> str:
    wanted = normalize(stem)
    exact = [slug for slug in slugs if normalize(slug) == wanted]
    if exact:
        return f"[[{exact[0]}]]"
    alias = ALIASES.get(wanted)
    if alias in slugs:
        return f"[[{alias}]]"
    return "[[project-scheme-ingest-manifest-2026-08-03]]"


def plan_registry() -> tuple[str, int, int]:
    plans = sorted((PROJECT / "docs" / "plans").glob("*.md"), key=lambda p: p.name.casefold())
    slugs = comparison_slugs()
    mapped = 0
    rows = ["| # | 项目源文件 | 文档标题 | 知识入口 |", "|---:|---|---|---|"]
    for index, path in enumerate(plans, 1):
        target = infer_target(path.stem, slugs)
        if target != "[[project-scheme-ingest-manifest-2026-08-03]]":
            mapped += 1
        source = f"`docs/plans/{path.name}`"
        title = page_title(path).replace("|", "\\|")
        rows.append(f"| {index} | {source} | {title} | {target} |")
    return "\n".join(rows), len(plans), mapped


def repro_registry() -> tuple[str, int, int, int]:
    root = PROJECT / "reproductions"
    families = sorted([path for path in root.iterdir() if path.is_dir()], key=lambda p: p.name.casefold())
    rows = [
        "| 复现家族 | Markdown/README | 指标文件 | 预测/模型资产 | 知识入口 |",
        "|---|---:|---:|---:|---|",
    ]
    total_metrics = 0
    total_assets = 0
    for family in families:
        files = [path for path in family.rglob("*") if path.is_file() and ".venv" not in path.parts]
        markdown = sum(path.suffix.lower() == ".md" for path in files)
        metrics = sum(path.suffix.lower() in {".json", ".csv"} and ("metric" in path.name.lower() or "history" in path.name.lower()) for path in files)
        assets = sum(path.suffix.lower() in {".pt", ".pth", ".npz", ".mat"} for path in files)
        total_metrics += metrics
        total_assets += assets
        rows.append(
            f"| `{family.name}` | {markdown} | {metrics} | {assets} | [[reproduction-schemes-inventory-2026-08-03]] |"
        )
    return "\n".join(rows), len(families), total_metrics, total_assets


def main() -> None:
    plans, plan_count, mapped_count = plan_registry()
    repros, family_count, metric_count, asset_count = repro_registry()
    summary = (
        f"- 项目方案/结果 Markdown：**{plan_count} / {plan_count} 已登记**。\n"
        f"- 其中 **{mapped_count}** 份可直接映射到独立对比/结果页；其余由本清单与综合证据页承接。\n"
        f"- 顶层复现家族：**{family_count} / {family_count} 已登记**。\n"
        f"- 复现目录内可检索的 metrics/history 文件：**{metric_count}**；预测或模型资产：**{asset_count}**。\n"
        "- 覆盖口径：排除复现目录内的私有虚拟环境；不复制二进制资产，只登记其家族和原始路径。"
    )
    text = MANIFEST.read_text(encoding="utf-8")
    text = replace_block(text, "PROJECT-INGEST-SUMMARY", summary)
    text = replace_block(text, "PROJECT-PLAN-REGISTRY", plans)
    text = replace_block(text, "PROJECT-REPRO-REGISTRY", repros)
    MANIFEST.write_text(text, encoding="utf-8", newline="\n")
    print(
        yaml.safe_dump(
            {
                "plans": plan_count,
                "plans_directly_mapped": mapped_count,
                "reproduction_families": family_count,
                "metric_or_history_files": metric_count,
                "prediction_or_model_assets": asset_count,
            },
            allow_unicode=True,
            sort_keys=False,
        ).strip()
    )


if __name__ == "__main__":
    main()
