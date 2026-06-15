# Wiki Schema

## Domain
Physics-informed machine learning and computational mechanics — with a focus on deep learning methods for metamodeling, structural dynamics, and nonlinear system identification. Expanding into semantic segmentation for structural engineering (scan-to-BIM), large language models (NAS/MoE/LLM推理), and AI4S.

## Architecture

```
wiki/
├── SCHEMA.md              # This file: conventions, rules, tag taxonomy
├── index.md                # Content catalog with one-line summaries
├── log.md                  # Chronological action log (append-only)
├── raw/                    # L1: Immutable source material (never modified)
│   ├── articles/           #   Web articles, clippings
│   ├── papers/             #   PDFs, arxiv papers
│   ├── transcripts/        #   Meeting/interview transcripts
│   ├── videos/             #   Raw video files
│   └── assets/             #   Images, diagrams
├── papers/               # L2: Deep paper analyses (1+3 structure only)
│   └── <paper-slug>-{analysis,method,results,critical}.md
├── notes/                  # L2: Derivative single-page notes (NON-PAPER ingest)
│   ├── briefings/          #   PPT meetings, 汇报笔记, 会议纪要
│   ├── lectures/           #   讲座, 教程笔记
│   ├── videos/             #   视频内容笔记
│   └── articles/           #   文章/博客摘录
├── entities/               # L2: Entity pages (people, orgs, models, algorithms, datasets)
├── comparisons/            # L2: Side-by-side comparative analyses
└── queries/                # L2: Filed query results worth keeping
```

## Ingest Rules

| Source type | Target directory | Format |
|-------------|-----------------|--------|
| Academic paper (full text available) | `papers/` | 1+3 (analysis + method + results + critical) |
| Academic paper (survey/abstract only) | `papers/` | Single overview page |
| PPT/会议汇报 | `notes/briefings/` | Single page |
| 讲座/教程视频 | `notes/lectures/` | Single page |
| B站/YouTube 视频 | `notes/videos/` | Single page |
| 文章/博客 | `notes/articles/` | Single page |

**Entity creation rule**: Every paper ingest MUST create or update ≥1 entity page in `entities/`. Non-paper ingest SHOULD create entities when introducing new models/organizations/people.

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `zhang2020-phylstm-analysis.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use backtick-wrapped wikilinks show as code: `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- **Provenance markers:** On pages that synthesize 3+ sources, append `^[raw/papers/source-file.md]` at the end of paragraphs whose claims come from a specific source.

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | paper-analysis | briefing | lecture | video | article | comparison | query | summary
tags: [from taxonomy below]
sources: [raw/papers/source-name.md]
confidence: high | medium | low
contested: true
contradictions: [other-page-slug]
---
```

## Tag Taxonomy

⚠️ Tags are **content keywords for cross-paper retrieval**, NOT section titles.
The 11 analysis dimensions (engineering-background, research-gap, etc.) live in the
markdown headings — tagging pages with them is redundant and gives zero filtering power.

Tags should be searchable across papers: a good tag appears on 3-15 pages.

### 技术标签 (Content-based, domain-specific)
- **Methods:** neural-network, lstm, physics-informed, metamodeling, deep-learning, 
  sequence-modeling, finite-difference, tensor-differentiator, multi-lstm,
  physics-constrained-loss, soft-constraint, adam-lbfgs, two-phase-optimization,
  collocation-strategy, conditional-computation, automatic-sharding, spmd,
  model-parallelism, pipeline-parallelism, distributed-training, sublinear-scaling,
  compiler-optimization, xla-compiler, transformer, machine-translation,
  heterogeneous-transformer, encoder-decoder-attention, edge-inference
- **Architecture:** phylstm2, phylstm3
- **Domain:** structural-dynamics, nonlinear-systems, hysteresis, seismic-response, 
  equation-of-motion, restoring-force, data-scarcity, unobservable-variables,
  extrapolation-ability
- **Data:** dataset, benchmark, ground-motion, synthetic-data, ida, peer-database, blwn
- **Models:** bouc-wen, rate-independent, rate-dependent, mrfs, sdof
- **Failure modes:** architecture-mismatch-failure, finite-difference-error,
  physics-constraint-weight-tuning
- **Structural engineering:** collapse-simulation, rc-structures, fiber-beam-element,
  multilayer-shell, elemental-deactivation, finite-element, high-rise-building,
  progressive-collapse, material-failure-criteria
- **Physics simulation:** rigid-body-dynamics, contact-mechanics, real-time-simulation,
  gpu-computing, constraint-solver, primal-method, dual-method, augmented-lagrangian,
  gauss-seidel, jacobi, high-stiffness-ratio, hard-constraints, mass-spring,
  frictional-contact, substep, information-propagation-limit
- **Meta:** comparison, review, future-work, limitation, cross-domain-generalization,
  architecture-selection, transfer-learning
- **Computer vision:** semantic-segmentation, encoder-decoder, skip-connections,
  fully-convolutional, u-net, data-augmentation, small-dataset, overlap-tile,
  biomedical-imaging, scene-parsing, pyramid-pooling, multi-scale-context,
  auxiliary-loss, deep-supervision, resnet, dilated-convolution, bilinear-upsample,
  atrous-convolution, atrous-separable-convolution, depthwise-separable-convolution,
  xception, aspp, output-stride, aligned-xception, spatial-pyramid-pooling,
  high-resolution-representation, multi-resolution-fusion, parallel-convolutions,
  hrnet, hrnetv2, hrnetv2p, multi-resolution-block,
  vision-transformer, hierarchical-transformer, mlp-decoder, mix-ffn,
  efficient-self-attention, positional-encoding-free, mit-encoder,
  overlap-patch-merging, sequence-reduction, segformer
- **Neural Architecture Search:** neural-architecture-search, training-free-nas,
  ntk, neural-tangent-kernel, linear-regions, expressivity, trainability,
  weight-sharing-nas, pruning-based-nas, nas-bench-201, one-shot-nas,
  weight-entanglement, evolutionary-search,
  hardware-aware-nas, latency-prediction, evolutionary-search,
  weight-sharing-supernet, hardware-specialization, latency-constraint,
  differentiable-nas, block-wise-search, self-supervised-nas,
  ensemble-bootstrapping, hybrid-cnn-transformer, hybrid-search-space,
  memory-efficient-nas, multi-split-reversible, hidden-covariance,
  linear-regions-count, sq-tc-search, mdha, squared-relu
- **Generative models:** diffusion-models, ddpm, ddim, stable-diffusion, latent-diffusion,
  score-based-models, langevin-dynamics, classifier-free-guidance, lora, dpo,
  controlnet, dreambooth, textual-inversion, image-generation, molecule-generation,
  protein-design, rfdiffusion, protpainter, alphafold3, se3-equivariance
- **AI4S:** ai4s, scientific-discovery, inverse-problem, pinn, deepxde,
  physics-simulation, material-design, weather-prediction
- **Large Language Models:** mixture-of-experts, sparse-moe, gating-network,
  top-k-routing, swiglu, decoder-only-transformer, large-language-model,
  efficient-inference, load-balancing, router-analysis, instruction-tuning,
  supervised-fine-tuning, direct-preference-optimization, multilingual-data,
  llm-benchmark, code-generation-benchmark, math-benchmark,
  commonsense-reasoning, long-context-modeling, bias-evaluation
- **Models/Architectures:** mixtral-8x7b, mistral-7b, llama-2, gpt-3.5-turbo, autoformer
- **Neuroscience:** hippocampal-formation, ca3, ca1, sparse-coding, dense-coding, neural-coding, population-coding, place-cells, tetrode-recording, calcium-imaging, dimensionality-expansion, dentate-gyrus
- **Model Compression:** knowledge-distillation, bert-compression,
  task-agnostic-compression, block-wise-training, progressive-shrinking,
  separable-convolution, supernet, model-compression
- **Datasets:** the-pile, passkey-retrieval, mt-bench, bbq-bias, bold-bias,
  humaneval, gsm8k, mbpp, mmlu, hellaswag, wmt14,
  wmt19, iwslt14, glu-e, squad, imagenet, cifar-10, cifar-100

Rule: every tag must appear in this taxonomy. Add new tags here BEFORE using them.

## Paper Analysis Page Structure

Every ingested paper produces a **1 overview + 3 sub-page** structure under `papers/`:

```
papers/<author-year>-<keyword>-analysis.md    ← Overview (~80 lines)
papers/<author-year>-<keyword>-method.md      ← Dimension 5 expanded
papers/<author-year>-<keyword>-results.md     ← Dimension 6 expanded
papers/<author-year>-<keyword>-critical.md    ← Dimensions 7-11 combined
```

- **Overview:** All 11 dimensions in 2-3 sentences each, with `→ [[sub-page]]` links.
  Dimensions 1-4 (engineering-background, research-gap, scientific-question, research-objective)
  live ONLY in the overview.
- **Method sub-page:** Architecture diagrams, loss function tables, training strategy.
- **Results sub-page:** Experiment tables with numerical values, per-example conclusions.
- **Critical sub-page:** Contribution, core knowledge, negative knowledge (limitations + unsolved +
  don't-copy), transferable knowledge (what → how table), research opportunities.
- **Overview exempt from 200-line split rule.** Sub-pages split at ~100 lines.

### Paper Analysis Page Template (Overview)

```markdown
---
title: "<Author> (<Year>) — <Short Title>: 论文分析"
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: paper-analysis
tags: [<content-keywords-from-taxonomy>]
sources: [raw/papers/<source-file>.md]
# Dimension fields — categorize keywords for structured filtering:
methods: [<method-keywords>]
results: [<result-keywords>]
failure_modes: [<failure-keywords>]
datasets: [<dataset-names>]
reproducibility: high | medium | low
code_url:
  - <official-repo-url>
dataset_url:
  - <dataset-url>
confidence: high
---

# <Paper Title>

## 1. 工程背景 (Engineering Background)
> 为什么这个问题在工程上重要？不解决会怎样？

## 2. Research Gap
> 已有研究缺了什么？核心矛盾是什么？为什么现有方法不行？

## 3. 科学问题 (Scientific Question)
> 现有理论/模型/方法中的核心难题是什么？（不是研究对象，不是方法名）

## 4. 研究目标 (Research Objective)
> 本文想实现什么？（不是性能目标，是研究层面要达成什么）

## 5. 方法机制 (Method & Mechanism)
> 本文方法如何工作？输入→输出是什么？为什么这样设计？机制图/公式关键点。

## 6. 结果证据 (Result & Evidence)
> 什么结果支撑结论？关键指标、对比方法、数值。

## 7. 贡献 (Contribution)
> 本文新增了什么？（与方法机制的区别：贡献是"多了什么"，方法是"怎么做的"）

## 8. 核心知识点 (Core Knowledge)
> 读完这篇论文应该记住什么？

## 9. Negative Knowledge
> 论文暴露了什么风险、失败边界或不该照搬的做法？
> - 方法的适用范围/前提假设是什么？
> - 什么场景下会失效？
> - 有什么未解决的问题？

## 10. 可迁移知识 (Transferable Knowledge)
> 哪些经验可用于其他研究？具体怎么迁移？

## 11. 研究机会 (Research Opportunity)
> 下一步可以研究什么？具体方向和建议。

## 12. 可复现性 (Reproducibility)
> 代码和数据是否公开？能否独立复现论文结果？
> - 🟢 高：源码 + 数据 + 预训练权重完全公开
> - 🟡 中：无源码但论文表述详细，大概率可复现
> - 🔴 低：关键细节缺失，难以独立复现

| 项目 | 说明 |
|------|------|
| **等级** | 🟢/🟡/🔴 |
| **官方代码** | `<repo-url>` |
| **数据集** | `<dataset-names + 是否公开>` |
| **协议** | `<license>` |
| **复现要点** | `<关键注意事项，如预训练依赖、已知坑>` |

## 关联页面
- `[[entity-page-1]]` — 说明
- `[[entity-page-2]]` — 说明
```

Dimensions 3 (scientific-question) and 7 (contribution) are the hardest to get right — always verify:
- Scientific question ≠ research object, ≠ method name, ≠ performance goal
- Contribution ≠ routine combination, ≠ "we applied X to Y"

## Entity Pages
One page per notable entity (model, dataset, method, person). Include: overview, key facts/dates, relationships, source references.

## Paper Pages
One page per topic. Include: definition, current knowledge state, open questions, related papers.

## Comparison Pages
Side-by-side analyses with comparison dimensions (table format preferred), verdict/synthesis, sources.

## Page Thresholds
- **Overview page:** exempt from 200-line split rule — completeness of all 12 dimensions in one file is the priority
- **Sub-pages:** split when exceeding ~100 lines
- **Create entity pages** when a model/dataset/method appears in 2+ sources OR is central to one source
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions, minor details, or things outside the domain
- **Archive a page** when its content is fully superseded — move to `_archive/`, remove from index

## Update Policy
When new information conflicts with existing content:
1. Check dates — newer sources generally supersede older ones
2. If genuinely contradictory, note both positions with dates and sources
3. Mark contradiction in frontmatter: `contradictions: [page-name]`
4. Flag for user review in the lint report
