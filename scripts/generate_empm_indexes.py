from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def insert_before(path, marker, lines):
    p = ROOT / path
    text = p.read_text(encoding='utf-8')
    if all(line in text for line in lines):
        return
    block = '\n'.join(lines) + '\n'
    text = text.replace(marker, block + '\n' + marker, 1)
    text = text.replace("updated: '2026-07-31'", "updated: '2026-08-01'", 1)
    p.write_text(text, encoding='utf-8')

insert_before('papers/index.md', '<!-- AUTO-REGISTRY:END -->', [
'- [[papers/chen2026-empm-analysis]] — Chen et al. (2026) — EMPM 论文分析',
'- [[papers/chen2026-empm-method]] — EMPM 方法机制：可微 MPM、离线与在线参数识别',
'- [[papers/chen2026-empm-results]] — EMPM 结果证据：弹性/弹塑性对象、在线校正与运行时间',
'- [[papers/chen2026-empm-critical]] — EMPM 批判、迁移与研究机会',
])
insert_before('sources/index.md', '<!-- AUTO-REGISTRY:END -->', [
'- [[sources/papers/chen2026-empm]] — Chen et al. (2026) — EMPM: Embodied MPM for Modeling and Simulation of Deformable Objects — source note',
])
insert_before('entities/index.md', '<!-- AUTO-REGISTRY:END -->', [
'- [[entities/empm]] — EMPM — Embodied Material Point Method',
])

log = ROOT / 'log.md'
text = log.read_text(encoding='utf-8')
entry = """## [2026-08-01] ingest | Chen et al. (2026) — EMPM\n\n- Source: user-provided `2601.17251v1.pdf` (arXiv:2601.17251v1).\n- Created canonical source note and full 1+3 paper family.\n- Created `entities/empm.md`.\n- Core: differentiable MPM, RGB-D reconstruction, Gaussian Splatting, offline/online material identification and embodied deformable-object simulation.\n- Verified numerical evidence from Tables 1–3 and recorded tracking, homogeneity and quasi-static-update limitations.\n\n"""
if entry not in text:
    text = text.replace("# Wiki Log\n\n", "# Wiki Log\n\n" + entry, 1)
    text = text.replace("updated: '2026-07-31'", "updated: '2026-08-01'", 1)
    log.write_text(text, encoding='utf-8')

out = ROOT / 'generated-empm-indexes'
out.mkdir(exist_ok=True)
for rel in ['papers/index.md','sources/index.md','entities/index.md','log.md']:
    dst = out / rel.replace('/','__')
    dst.write_text((ROOT/rel).read_text(encoding='utf-8'), encoding='utf-8')
