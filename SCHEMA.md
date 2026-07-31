---
id: schema
title: "Civil Engineering LLM Wiki Schema"
type: schema
status: active
project: civil-engineering-llm-wiki
tags: []
sources: []
created: 2026-07-16
updated: 2026-07-31
confidence: high
---

# Wiki Schema

## Domain

Physics-informed machine learning and computational mechanics, with emphasis on structural dynamics, nonlinear system identification, scientific machine learning, engineering computer vision, AI4S, large language models, and remote-sensing / generative 3D knowledge.

## Architecture

```text
wiki/
├── SCHEMA.md
├── index.md
├── log.md
├── raw/                    # immutable source material or source metadata
│   ├── articles/
│   ├── papers/
│   ├── transcripts/
│   ├── videos/
│   └── assets/
├── papers/                 # full-text paper analyses: 1 overview + 3 sub-pages
├── notes/                  # non-paper notes
│   ├── briefings/
│   ├── lectures/
│   ├── videos/
│   └── articles/
├── entities/               # models, methods, datasets, tools, organizations, people
├── comparisons/
├── queries/
└── scripts/                # validation and maintenance scripts
```

## Ingest Rules

| Source type | Target | Required output |
|---|---|---|
| Full-text academic paper | `raw/papers/`, `papers/`, `entities/` | Source metadata + analysis/method/results/critical + ≥1 entity |
| Abstract-only paper | `papers/` | One overview with `evidence_scope: abstract-only` |
| PPT / meeting | `notes/briefings/` | One source-grounded note |
| Lecture / tutorial | `notes/lectures/` | One source-grounded note |
| Video | `notes/videos/` | One source-grounded note |
| Article / blog | `notes/articles/` | One source-grounded note |

Raw source material is immutable after ingest. A source metadata note may be revised only to correct metadata or add provenance; it must never silently replace or rewrite the original source.

## Strict Frontmatter Contract

Every maintained knowledge page and section index starts with:

```yaml
---
id: short-stable-id
title: Human-readable title
type: source | entity | paper-analysis | briefing | lecture | video | article | comparison | query | summary | index | log | schema
status: draft | active | verified | superseded
project: civil-engineering-llm-wiki
tags: []
sources: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: low | medium | high
---
```

Optional structured fields:

```yaml
evidence_scope: abstract-only
methods: []
results: []
failure_modes: []
datasets: []
reproducibility: low | medium | high
code_url: []
dataset_url: []
contested: true
contradictions: []
```

Rules:

- `id` is stable and unique.
- `status: verified` means checked against the listed source, not independently reproduced.
- `project` is fixed to `civil-engineering-llm-wiki`.
- `sources` explicitly reference source metadata or raw paths.
- Bump `updated` whenever content changes.
- A replaced page uses `status: superseded` and links the replacement.

## Provenance And Evidence

- Use `sources` for page-level provenance.
- Use persistent paragraph markers such as `^[raw/papers/source-file.md]` for source-derived evidence.
- State page, section, figure or table positions in prose when useful.
- Never commit temporary ChatGPT tokens such as `filecite...`, `turnNfileM`, `turnNsearchM` or web reference IDs.
- Do not claim independent reproduction unless experiments were actually rerun.
- Label cross-domain transfer as inference, migration or research proposal rather than a paper conclusion.
- Preserve conflicting evidence in a `Conflict` or `Counterevidence` section; do not silently overwrite it.

## Wikilinks

- Use bare `[[wikilinks]]`; never wrap them in backticks.
- Maintained knowledge pages have at least two outbound links unless they are terminal source records.
- Wikilinks must resolve to an existing Markdown page or recognized section-index path.
- Prefer existing entities over near-duplicate entity names.

## Index And Navigation Contract

- Register pages in the relevant section index.
- `index.md` is the global dashboard and links every section index plus high-priority knowledge chains.
- Exhaustive page lists may live in section indexes; every page must remain reachable through a finite index path.
- `mkdocs.yml` may remain curated, while unlisted pages remain searchable and reachable through indexes/wikilinks.
- Append every meaningful create, ingest, revise, verify, lint or deployment repair to `log.md`.

## CI/CD Contract

GitHub Actions may lint, build, upload and deploy. GitHub Actions must not edit knowledge pages, create commits, push branches or self-delete workflows. All repository mutations occur before PR validation.

## Tag Taxonomy

Tags are reusable retrieval keywords, not section headings. Add a tag only when it is expected to recur.

### Methods

neural-network, lstm, physics-informed, metamodeling, deep-learning, sequence-modeling, finite-difference, tensor-differentiator, multi-lstm, physics-constrained-loss, soft-constraint, adam-lbfgs, two-phase-optimization, collocation-strategy, conditional-computation, automatic-sharding, spmd, model-parallelism, pipeline-parallelism, distributed-training, sublinear-scaling, compiler-optimization, xla-compiler, transformer, machine-translation, heterogeneous-transformer, encoder-decoder-attention, edge-inference, bayesian-inference, hamiltonian-monte-carlo, uncertainty-quantification, self-adaptive-pinn, epidemiology, time-marching, auxiliary-function, hard-constraint-strategies, causal-attention-weighting, temporal-causality, adaptive-weighting

### Architecture And Domain

phylstm2, phylstm3, structural-dynamics, nonlinear-systems, hysteresis, seismic-response, equation-of-motion, restoring-force, data-scarcity, unobservable-variables, extrapolation-ability, vibration-analysis, superscript-panel, euler-bernoulli-beam, collapse-simulation, rc-structures, fiber-beam-element, multilayer-shell, elemental-deactivation, finite-element, high-rise-building, progressive-collapse, material-failure-criteria

### Data, Models, Failure Modes And Meta

dataset, benchmark, ground-motion, synthetic-data, ida, peer-database, blwn, jhu-covid19, bouc-wen, rate-independent, rate-dependent, mrfs, sdof, damped-harmonic-oscillator, architecture-mismatch-failure, finite-difference-error, physics-constraint-weight-tuning, comparison, review, future-work, limitation, cross-domain-generalization, architecture-selection, transfer-learning

### Physics Simulation

rigid-body-dynamics, contact-mechanics, real-time-simulation, gpu-computing, constraint-solver, primal-method, dual-method, augmented-lagrangian, gauss-seidel, jacobi, high-stiffness-ratio, hard-constraints, mass-spring, frictional-contact, substep, information-propagation-limit, trigonometric-auxiliary, exponential-auxiliary, polynomial-auxiliary

### Mathematical Physics

statistical-mechanics, kinetic-theory, entropy, irreversibility, boltzmann-equation, hilbert-sixth-problem, hard-sphere-dynamics, boltzmann-grad-limit

### Computer Vision

semantic-segmentation, encoder-decoder, skip-connections, fully-convolutional, u-net, data-augmentation, small-dataset, overlap-tile, biomedical-imaging, scene-parsing, pyramid-pooling, multi-scale-context, auxiliary-loss, deep-supervision, resnet, dilated-convolution, bilinear-upsample, atrous-convolution, atrous-separable-convolution, depthwise-separable-convolution, xception, aspp, output-stride, aligned-xception, spatial-pyramid-pooling, high-resolution-representation, multi-resolution-fusion, parallel-convolutions, hrnet, hrnetv2, hrnetv2p, multi-resolution-block, vision-transformer, hierarchical-transformer, mlp-decoder, mix-ffn, efficient-self-attention, positional-encoding-free, mit-encoder, overlap-patch-merging, sequence-reduction, segformer

### Neural Architecture Search

neural-architecture-search, training-free-nas, ntk, neural-tangent-kernel, linear-regions, expressivity, trainability, weight-sharing-nas, pruning-based-nas, nas-bench-201, one-shot-nas, weight-entanglement, evolutionary-search, hardware-aware-nas, latency-prediction, weight-sharing-supernet, hardware-specialization, latency-constraint, differentiable-nas, block-wise-search, self-supervised-nas, ensemble-bootstrapping, hybrid-cnn-transformer, hybrid-search-space, memory-efficient-nas, multi-split-reversible, hidden-covariance, linear-regions-count, sq-tc-search, mdha, squared-relu

### Generative Models And Equivariance

diffusion-models, ddpm, ddim, stable-diffusion, latent-diffusion, score-based-models, langevin-dynamics, classifier-free-guidance, lora, dpo, controlnet, dreambooth, textual-inversion, image-generation, molecule-generation, protein-design, rfdiffusion, protpainter, alphafold3, se3-equivariance

### Neural Operators And Training Dynamics

neural-operator, operator-learning, neural-ode, physics-encoded-network, physics-aware-attention, fourier-operator, structure-preserving, operator-splitting, compositional-modeling, trajectory-free-training, spectral-method, boundary-condition, hamiltonian, dissipative-dynamics, long-horizon-rollout, autoregressive-rollout, exponential-time-differencing, scientific-machine-learning, pde, digital-twin, scaling-law, kernel-regression, stochastic-gradient-descent, learning-rate-schedule, intrinsic-time, compute-optimal-training

### AI4S

ai4s, scientific-discovery, inverse-problem, pinn, deepxde, physics-simulation, material-design, weather-prediction

### Cheminformatics

chemical-language-model, molecular-conformation, 3d-molecular-generation, conformation-prediction, internal-coordinates, drug-discovery, dihedral-angle, pseudo-chirality, se3-invariance, virtual-screening, shape-conditioned-generation, molecular-representation

### Large Language Models

mixture-of-experts, sparse-moe, gating-network, top-k-routing, swiglu, decoder-only-transformer, large-language-model, efficient-inference, load-balancing, router-analysis, instruction-tuning, supervised-fine-tuning, direct-preference-optimization, multilingual-data, llm-benchmark, code-generation-benchmark, math-benchmark, commonsense-reasoning, long-context-modeling, bias-evaluation, mixtral-8x7b, mistral-7b, llama-2, gpt-3.5-turbo, autoformer

### Neuroscience And Compression

hippocampal-formation, ca3, ca1, sparse-coding, dense-coding, neural-coding, population-coding, place-cells, tetrode-recording, calcium-imaging, dimensionality-expansion, dentate-gyrus, knowledge-distillation, bert-compression, task-agnostic-compression, block-wise-training, progressive-shrinking, separable-convolution, supernet, model-compression

### Datasets

the-pile, passkey-retrieval, mt-bench, bbq-bias, bold-bias, humaneval, gsm8k, mbpp, mmlu, hellaswag, wmt14, wmt19, iwslt14, glu-e, squad, imagenet, cifar-10, cifar-100, dfc-2019, urbanscene3d, urbanbis, crossloc, mill-19, uavd4l, denseuav, uc-gs

### Remote Sensing And 3D

3d-gaussian-splatting, 3dgs, gaussian-primitives, satellite-imagery, remote-sensing, geospatial, digital-earth, digital-twins, 3d-scene-generation, generative-3d-earth, 3d-reconstruction, photogrammetry, urban-modeling, multi-lod, lod-hierarchy, level-of-detail, spatial-partitioning, multi-view-rendering, data-curation, vlm-quality-assessment, embodied-ai, uav-navigation, sim-to-real, closed-loop-simulation, web-mercator, enu-coordinates, ogc-3d-tiles, bhattacharyya-distance, reconstruction-based-generation, cross-view-fusion, satellite-conditioned-generation, tile-based-rendering, cdn-streaming, abot-earth, abot-3dgs, from-orbit-to-ground, clod-gs, yunjing

Rule: every tag used in frontmatter must appear in this taxonomy.

## Paper Analysis Page Structure

Every full-text paper produces:

```text
papers/<slug>-analysis.md
papers/<slug>-method.md
papers/<slug>-results.md
papers/<slug>-critical.md
```

The overview contains all 12 sections: engineering background, research gap, scientific question, research objective, method, results, contribution, core knowledge, Negative Knowledge, transferable knowledge, research opportunities and reproducibility.

The method page includes architecture/data flow, equations, inputs/outputs, training or solution strategy, assumptions and failure boundaries.

The results page includes numerical tables where supported, comparison conditions, per-example conclusions and result interpretation boundaries.

The critical page includes contribution, core knowledge, Negative Knowledge, do-not-copy cautions, transferable knowledge, research opportunities and an explicit distinction between paper claims and cross-domain inference.

## Update Policy

1. Check dates and source versions before revising claims.
2. Record newer evidence without silently rewriting incompatible older evidence.
3. Use `contradictions` and a `Conflict`/`Counterevidence` section when needed.
4. Update section indexes, global dashboard and log after meaningful changes.
5. Run strict lint and MkDocs build before merging to `main`.
