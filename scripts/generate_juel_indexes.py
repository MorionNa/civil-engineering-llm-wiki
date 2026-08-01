from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'generated-juel-indexes'
OUT.mkdir(exist_ok=True)

TARGETS = {
    'papers': ROOT / 'papers/index.md',
    'sources': ROOT / 'sources/index.md',
    'entities': ROOT / 'entities/index.md',
    'concepts': ROOT / 'concepts/index.md',
}

def title(path: Path) -> str:
    text = path.read_text(encoding='utf-8')
    if text.startswith('---\n'):
        data = yaml.safe_load(text.split('---', 2)[1]) or {}
        return str(data.get('title') or path.stem)
    return path.stem

def replace_registry(text: str, lines: list[str]) -> str:
    block = '<!-- AUTO-REGISTRY:START -->\n\n## Complete Registry\n\n' + '\n'.join(lines) + '\n\n<!-- AUTO-REGISTRY:END -->'
    return re.sub(r'<!-- AUTO-REGISTRY:START -->.*?<!-- AUTO-REGISTRY:END -->', block, text, flags=re.S)

for root_name, index in TARGETS.items():
    pages = []
    for path in sorted((ROOT / root_name).rglob('*.md')):
        if path.name == 'index.md':
            continue
        rel = path.relative_to(ROOT).with_suffix('').as_posix()
        pages.append(f'- [[{rel}]] — {title(path)}')
    updated = replace_registry(index.read_text(encoding='utf-8'), pages)
    updated = re.sub(r"updated: '[0-9-]+'", "updated: '2026-08-01'", updated, count=1)
    (OUT / f'{root_name}-index.md').write_text(updated, encoding='utf-8')

log = (ROOT / 'log.md').read_text(encoding='utf-8')
entry = '''## [2026-08-01] ingest | Juel et al. (2026) — 稳定化分步双相 MPM

- Source: user-provided `1-s2.0-S0045782526004135-main.pdf`, CMAME 461 (2026) 119140, DOI 10.1016/j.cma.2026.119140.
- Created canonical source note, complete 1+3 paper family, one model entity and two reusable concept pages.
- Core: incremental fractional-step two-phase double-point MPM, SPGP pressure stabilization, TPIC pressure mapping, permeability-independent timestepping and matrix-free GPU pressure solve.
- Verified evidence from consolidation, free-surface flow, dam-break, porous-media interception and 8.6-million-particle 3D impact benchmarks.
- Recorded Negative Knowledge, reproducibility limits and explicitly labelled geotechnical/structural migration inferences.

'''
log = log.replace('# Wiki Log\n\n', '# Wiki Log\n\n' + entry, 1)
log = re.sub(r"updated: '[0-9-]+'", "updated: '2026-08-01'", log, count=1)
(OUT / 'log.md').write_text(log, encoding='utf-8')
