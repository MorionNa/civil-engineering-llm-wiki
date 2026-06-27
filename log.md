# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

## [2026-06-27] ingest | Chen et al. (2025) — AT-PINN-HC: 硬约束增强时间推进 PINN 结构振动分析

## [2026-06-27] ingest | Linka et al. (2022) — Bayesian PINNs for real-world nonlinear dynamical systems
- Source: DOI 10.1016/j.cma.2022.115346 (CMAME Vol 402, 2022), raw/papers/10_1016_j_cma_2022_115346_extracted.txt
- SCHEMA.md updated: added bayesian-inference, hamiltonian-monte-carlo, uncertainty-quantification, self-adaptive-pinn, epidemiology (Methods); damped-harmonic-oscillator (Models); jhu-covid19 (Data)
- Created: papers/linka2022-bayesian-pinn-{analysis,method,results,critical}.md (1+3)
- Created: entities/bayesian-pinn.md, entities/hamiltonian-monte-carlo.md
- Domain: physics-informed ML — BPINN: 物理残差=贝叶斯似然因子, HMC联合推断网络权重+物理参数, COVID-19 6模型系统对比
- Source: DOI 10.1016/j.cma.2024.117691 (CMAME Vol. 436, 2025), raw/papers/10_1016_j_cma_2024_117691_extracted.txt
- SCHEMA.md updated: added time-marching, auxiliary-function, hard-constraint-strategies (Methods), vibration-analysis, superscript-panel, euler-bernoulli-beam (Domain), trigonometric-auxiliary, exponential-auxiliary, polynomial-auxiliary (Physics simulation)
- Created: papers/chen2025-at-pinn-hc-{analysis,method,results,critical}.md (1+3)
- Created: entities/at-pinn-hc.md
- Domain: 物理信息机器学习 + 计算力学 — PINN 硬约束 + 时间推进 + 结构振动
- Note: 全文未提取（仅摘要+元数据），置信度 medium；正文细节待补充

## [2026-06-22] ingest | AMAP CV Lab (2026) — ABot-Earth 0.5: Generative 3D Earth Model
- Source: tech-report.pdf (AMAP CV Lab, 2026-06-08), raw/papers/amapcvlab2026-abotearth.pdf
- SCHEMA.md updated: added Remote Sensing & 3D Geospatial section (29 tags), Systems/Models section (5 tags), new datasets (8)
- Created: papers/amapcvlab2026-abotearth-{analysis,method,results,critical}.md (1+3)
- Created: entities/abot-earth.md, entities/abot-3dgs.md, entities/3d-gaussian-splatting.md, entities/from-orbit-to-ground.md, entities/clod-gs.md
- Domain: 遥感 + 生成式 AI — 3DGS 原生生成，卫星条件，<10min/km², 190+ 国家

## [2026-06-15] ingest | Maimon et al. (2026) — Sparse-to-Dense Coding (Nature)
- Source: DOI 10.1038/s41586-026-10537-0 (Nature 2026), raw/papers/10_1038_s41586-026-10537-0.pdf
- SCHEMA.md updated: added hippocampal-formation, ca3, ca1, sparse-coding, dense-coding, neural-coding, population-coding, place-cells, tetrode-recording, calcium-imaging, dimensionality-expansion, dentate-gyrus (Neuroscience section)
- Created: papers/maimon2026-sparse-dense-{analysis,method,results,critical}.md
- Created: entities/sparse-dense-coding.md

## [2026-06-15] ingest | Lee & Ham (2024) — AZ-NAS
- Source: arXiv 2403.19232, raw/papers/aznas_lee2024.pdf
- Created: papers/lee2024-aznas-{analysis,method,results,critical}.md
- Created: entities/az-nas.md

## [2026-06-15] ingest | Akhauri et al. (2022) — EZNAS
- Source: arXiv 2209.07413 (NeurIPS 2022), raw/papers/eznas_akhauri2022.pdf
- Created: papers/akhauri2022-eznas-{analysis,method,results,critical}.md
- Created: entities/eznas.md

## [2026-06-15] ingest | Ru et al. (2020) — NAGO
- Source: arXiv 2004.01395 (NeurIPS 2020), raw/papers/nago_ru2020.pdf
- Created: papers/ru2020-nago-{analysis,method,results,critical}.md
- Created: entities/nago.md

## [2026-06-15] ingest | Real et al. (2020) — AutoML-Zero
- Source: arXiv 2003.03384 (ICML 2020), raw/papers/automl_zero_real2020.pdf
- Created: papers/real2020-automl-zero-{analysis,method,results,critical}.md
- Created: entities/automl-zero.md

## [2026-06-14] ingest | So et al. (2021) — Primer
- Source: arXiv 2109.08668 (NeurIPS 2021), raw/papers/primer2021_efficient_transformers.pdf
- SCHEMA.md updated: added sq-tc-search, mdha, squared-relu (NAS section)
- Created: papers/so2021-primer-analysis.md (overview)
- Created: papers/so2021-primer-method.md (method details)
- Created: papers/so2021-primer-results.md (results details)
- Created: papers/so2021-primer-critical.md (contribution/knowledge/negative/transferable/opportunities)
- Created: entities/primer.md (entity page)
- Updated: index.md, mkdocs.yml (124 pages total)

## [2026-06-14] ingest | Li et al. (2021) — BossNAS
- Source: arXiv 2103.12424 (ICLR 2021), raw/papers/bossnas2021_iclr.pdf
- SCHEMA.md updated: added ensemble-bootstrapping, block-wise-search, self-supervised-nas, hybrid-cnn-transformer, hybrid-search-space (NAS section)
- Created: papers/li2021-bossnas-analysis.md (overview)
- Created: papers/li2021-bossnas-method.md (method details)
- Created: papers/li2021-bossnas-results.md (results details)
- Created: papers/li2021-bossnas-critical.md (contribution/knowledge/negative/transferable/opportunities)
- Created: entities/bossnas.md (entity page)

## [2026-06-14] ingest | Zhao et al. (2021) — Memory-Efficient DNAS
- Source: arXiv 2105.14669 (ACL-IJCNLP 2021 Findings), raw/papers/memory_efficient_dnas2021.pdf
- SCHEMA.md updated: added differentiable-nas, memory-efficient-nas, multi-split-reversible (NAS section)
- Created: papers/zhao2021-memory-efficient-dnas-analysis.md (overview)
- Created: papers/zhao2021-memory-efficient-dnas-method.md (method details)
- Created: papers/zhao2021-memory-efficient-dnas-results.md (results details)
- Created: papers/zhao2021-memory-efficient-dnas-critical.md (contribution/knowledge/negative/transferable/opportunities)
- Created: entities/memory-efficient-dnas.md (entity page)

## [2026-06-14] ingest | Serianni et al. (2023) — Training-free NAS for RNNs/Transformers
- Source: arXiv 2306.00288, raw/papers/training_free_nas2023.pdf
- SCHEMA.md updated: added hidden-covariance, linear-regions-count (NAS section)
- Created: papers/serianni2023-training-free-nas-rnn-transformers-analysis.md (overview)
- Created: papers/serianni2023-training-free-nas-rnn-transformers-method.md (method details)
- Created: papers/serianni2023-training-free-nas-rnn-transformers-results.md (results details)
- Created: papers/serianni2023-training-free-nas-rnn-transformers-critical.md (contribution/knowledge/negative/transferable/opportunities)
- Created: entities/training-free-nas-transformers.md (entity page)

## [2026-06-13] ingest | Chen et al. (2021) — AutoFormer
- Source: DOI 10.1109/iccv48922.2021.01205 (ICCV 2021, CCF-A), raw/papers/chen2021_autoformer.md
- SCHEMA.md updated: added one-shot-nas, weight-entanglement, evolutionary-search (NAS section); autoformer (Models); imagenet, cifar-10, cifar-100 (Datasets); transfer-learning (Meta)
- Created: papers/chen2021-autoformer-analysis.md (overview)
- Created: papers/chen2021-autoformer-method.md (method details)
- Created: papers/chen2021-autoformer-results.md (results details)
- Created: papers/chen2021-autoformer-critical.md (contribution/knowledge/negative/transferable/opportunities)
- Updated: index.md (74 pages total)

## [2026-06-13] ingest | Xu et al. (2021) — NAS-BERT
- Source: DOI 10.1145/3447548.3467262 (KDD 2021), raw/papers/xu2021_nas_bert.md
- SCHEMA.md updated: added Model Compression tag category (knowledge-distillation, bert-compression, task-agnostic-compression, block-wise-training, progressive-shrinking, separable-convolution, supernet, model-compression) + datasets (glu-e, squad)
- Created: papers/xu2021-nas-bert-analysis.md (overview)
- Created: papers/xu2021-nas-bert-method.md (method details)
- Created: papers/xu2021-nas-bert-results.md (results details)
- Created: papers/xu2021-nas-bert-critical.md (contribution/knowledge/negative/transferable/opportunities)
- Updated: index.md (70 pages total)

## [2026-06-13] ingest | Jiang et al. (2024) — Mixtral of Experts
- Source: arXiv 2401.04088, raw/papers/jiang2024_mixtral_of_experts.md
- SCHEMA.md updated: added LLM/MoE tag categories (mixture-of-experts, sparse-moe, gating-network, top-k-routing, swiglu, decoder-only-transformer, large-language-model, efficient-inference, load-balancing, router-analysis, instruction-tuning, supervised-fine-tuning, direct-preference-optimization, multilingual-data, llm-benchmark, code-generation-benchmark, math-benchmark, commonsense-reasoning, long-context-modeling, bias-evaluation, mixtral-8x7b, mistral-7b, llama-2, gpt-3.5-turbo, the-pile, passkey-retrieval, mt-bench, bbq-bias, bold-bias, humaneval, gsm8k, mbpp, mmlu, hellaswag)
- Created: papers/jiang2024-mixtral-of-experts-analysis.md (overview)
- Created: papers/jiang2024-mixtral-of-experts-method.md (method details)
- Created: papers/jiang2024-mixtral-of-experts-results.md (results details)
- Created: papers/jiang2024-mixtral-of-experts-critical.md (contribution/knowledge/negative/transferable/opportunities)
- Updated: index.md (54 pages total)

## [2026-06-10] create | Wiki initialized
- Domain: Physics-informed machine learning and computational mechanics
- Structure created with SCHEMA.md, index.md, log.md

## [2026-06-10] ingest | Zhang et al. (2020) — PhyLSTM
- Source: DOI 10.1016/j.cma.2020.113226, SHA256 61904aed...
- Raw captured: raw/papers/zhang2020-phylstm.md
- SCHEMA.md created with 12-dimension paper analysis framework + tag taxonomy
- Created: papers/zhang2020-phylstm-analysis.md (overview)
- Created: papers/zhang2020-phylstm-method.md (method details)
- Created: papers/zhang2020-phylstm-results.md (results details)
- Created: papers/zhang2020-phylstm-critical.md (contribution/knowledge/negative/transferable/opportunities)
- Created: entities/phylstm2.md
- Created: entities/phylstm3.md
- Created: entities/bouc-wen-model.md
- Created: entities/peer-strong-motion-database.md
- Created: comparisons/phylstm2-vs-phylstm3-vs-lstm.md
- Updated: index.md (9 pages total)

## [2026-06-10] ingest | Wang et al. (2023) — When PINNs Go Wrong
- Source: DOI, SHA256 a9173427...
- Raw captured: raw/papers/wang2023-pinn-spurious.md
- Created: papers/wang2023-pinn-spurious-analysis.md (overview)
- Created: papers/wang2023-pinn-spurious-method.md
- Created: papers/wang2023-pinn-spurious-results.md
- Created: papers/wang2023-pinn-spurious-critical.md
- Created: entities/pseudo-time-stepping.md
- Created: comparisons/physics-constrained-training-failure-modes.md
- Back-linked: PhyLSTM overview + critical pages with PINN cross-references
- Updated: index.md (15 pages total)

## [2026-06-10] ingest | Agentic Engineering 22 条技巧 (Matt Van Horn, Datawhale)
- Source: X/@mvanhorn, OCR via RapidOCR (avg confidence 0.98)
- Raw captured: raw/articles/agentic-engineering-tips-2026.md
- Created: papers/agentic-engineering-22-tips.md (single page, non-paper format)
- Updated: index.md (16 pages total)

## [2026-06-10] ingest | AVBD SIGGRAPH 2025 — B站视频 (Kimi转录)
- Source: https://www.bilibili.com/video/BV1QpKNzeEqq
- Transcribed via Kimi ReadMediaFile (纯视觉分析，视频无语音)
- Raw captured: raw/articles/avbd-siggraph2025-bilibili.md
- Created: papers/avbd-siggraph2025-video.md (single page, non-paper format)

## [2026-06-11] ingest | AI4S第二讲：扩散生成模型（B站视频，Kimi ReadMediaFile）
- Source: https://www.bilibili.com/video/BV15t5m68E3w
- 94MB 完整视频一次通过 Kimi ReadMediaFile（无需拆分）
- Speaker: 章敏（浙江大学 × Datawhale × 魔搭社区）
- Raw captured: raw/articles/diffusion-models-ai4s-lecture2-bilibili.md
- Created: papers/ai4s/diffusion-models-ai4s-lecture2.md (single page, non-paper format)
- Updated: SCHEMA.md (新增 Generative models + AI4S tag taxonomy)
- Updated: index.md (18 pages total)

## [2026-06-11] ingest | Giles et al. (2025) AVBD paper (DOI: 10.1145/3731195)
- Full-text PDF (14MB) saved: raw/papers/giles2025-avbd.pdf
- Extracted text saved: raw/papers/giles2025-avbd.md (65,670 chars)
- Created: papers/giles2025-avbd-analysis.md (overview, 11 dimensions)
- Created: papers/giles2025-avbd-method.md (augmented Lagrangian, inequality, friction, stiffness ramping)
- Created: papers/giles2025-avbd-results.md (9 experiments, performance table)
- Created: papers/giles2025-avbd-critical.md (contributions, 6 negative knowledge items, 6 transferable, 6 research opportunities)
- Updated: SCHEMA.md (added Physics simulation tag taxonomy)
- Updated: index.md (22 pages total)

## [2026-06-11] ingest | Lu et al. (2013) EESD collapse simulation paper (DOI: 10.1002/eqe.2240)
- Downloaded via Wiley TDM API: raw/papers/10_1002_eqe_2240.pdf (19 pages)
- Extracted text: raw/papers/lu2013-collapse-rc-highrise.md (47,190 chars)
- Configured: WILEY_TDM_TOKEN in ~/.bashrc (was missing, paper-download Wiley API now works)
- Created: papers/lu2013-collapse-rc-highrise-analysis.md (overview, 11 dimensions)
- Created: papers/lu2013-collapse-rc-highrise-method.md (fiber-beam, multilayer shell, elemental deactivation)
- Created: papers/lu2013-collapse-rc-highrise-results.md (3 case studies, failure criteria sensitivity)
- Created: papers/lu2013-collapse-rc-highrise-critical.md (6 contributions/NK/TK, 5 research opportunities)
- Updated: SCHEMA.md (added Structural engineering tag taxonomy)
- Updated: index.md (26 pages total)

## [2026-06-11] ingest | Ronneberger et al. (2015) U-Net paper (DOI: 10.1007/978-3-319-24574-4_28)
- Downloaded via Crossref OA: raw/papers/10_1007_978-3-319-24574-4_28.pdf (8 pages)
- Extracted text: raw/papers/ronneberger2015-unet.md (19,739 chars)
- Created: papers/ronneberger2015-unet-analysis.md (overview, 11 dimensions)
- Created: papers/ronneberger2015-unet-method.md (overlap-tile, elastic augmentation, weighted loss)
- Created: papers/ronneberger2015-unet-results.md (ISBI EM/cell tracking challenge results)
- Created: papers/ronneberger2015-unet-critical.md (contributions, 5 NK, 5 TK, 4 opportunities)
- Updated: SCHEMA.md (added Computer vision tag taxonomy)
## [2026-06-11] ingest | Zhao et al. (2017) PSPNet paper (arXiv: 1612.01105)
- Raw PDF: raw/papers/1612.01105v2.pdf (4.5MB, arxiv pre-print)
- Text extracted via pymupdf (8 pages)
- Created: papers/zhao2017-pspnet-analysis.md (overview, 11 dimensions)
- Created: papers/zhao2017-pspnet-method.md (Pyramid Pooling Module + Deep Supervision)
- Created: papers/zhao2017-pspnet-results.md (ADE20K/VOC/Cityscapes SOTA + ablation)
- Created: papers/zhao2017-pspnet-critical.md (3 contributions, 7 NK, 6 TK, 6 opportunities — includes U-Net cross-ref)
- Updated: SCHEMA.md (added CV tags: scene-parsing, pyramid-pooling, etc.)
- Updated: index.md (34 pages total)
- Note: PSPNet complements U-Net — global context (pyramid pooling) vs local fusion (skip connections)
- Updated: index.md (34 pages total)

## [2026-06-11] ingest | Chen et al. (2018) DeepLabv3+ paper (arXiv: 1802.02611v3)
- Raw PDF: raw/papers/deepLabv3plus.pdf (4.0MB, 18 pages)
- Created: papers/chen2018-deeplabv3plus-analysis.md (overview, 11 dimensions)
- Created: papers/chen2018-deeplabv3plus-method.md (ASPP + Simple Decoder + Atrous Separable Conv + Xception)
- Created: papers/chen2018-deeplabv3plus-results.md (VOC/Cityscapes SOTA + decoder design ablation + trimap)
- Created: papers/chen2018-deeplabv3plus-critical.md (5 contributions, 9 NK, 6 TK, 6 opportunities)
- Updated: SCHEMA.md (added CV tags: atrous-convolution, depthwise-separable-convolution, etc.)
- Updated: index.md (38 pages total)
- Note: DeepLabv3+ completes the semantic segmentation trilogy — U-Net (local fusion), PSPNet (global pooling), DeepLabv3+ (ASPP + decoder, best accuracy)

## [2026-06-11] ingest | Sun et al. (2019) HRNetV2 paper (arXiv: 1904.04514)
- Raw PDF: raw/papers/arxiv_1904.04514.pdf (13 pages)
- Created: papers/sun2019-hrnetv2-analysis.md (overview, 11 dimensions)
- Created: papers/sun2019-hrnetv2-method.md (multi-resolution parallel + fusion + HRNetV2 aggregation)
- Created: papers/sun2019-hrnetv2-results.md (Cityscapes/PASCAL Context/LIP/face/COSO multi-task SOTA + HRNetV1 vs V2)
- Created: papers/sun2019-hrnetv2-critical.md (5 contributions, 9 NK, 5 TK, 6 opportunities)
- Updated: SCHEMA.md (added CV tags: high-resolution-representation, multi-resolution-fusion, etc.)
- Updated: index.md (42 pages total)
- Note: HRNet opens a 4th paradigm — maintain high resolution throughout (vs U-Net recovery, PSPNet pooling, DeepLabv3+ dilation+decoder). 3× more efficient than PSPNet at same accuracy.

## [2026-06-11] ingest | Xie et al. (2021) SegFormer paper (arXiv: 2105.15203, NeurIPS 2021)
- Raw PDF: raw/papers/segformer.pdf (5.6MB, 18 pages)
- Created: papers/xie2021-segformer-analysis.md (overview, 11 dimensions)
- Created: papers/xie2021-segformer-method.md (MiT encoder + Mix-FFN + Eff-SA + All-MLP decoder)
- Created: papers/xie2021-segformer-results.md (ADE/Cityscapes/COCO-Stuff SOTA + Cityscapes-C robustness)
- Created: papers/xie2021-segformer-critical.md (5 contributions, 9 NK, 5 TK, 6 opportunities)
- Updated: SCHEMA.md (added Transformer tags: vision-transformer, mix-ffn, etc.)
- Updated: index.md (46 pages total)
- Note: SegFormer opens the 5th paradigm — Transformer-based segmentation. No positional encoding, no complex decoder, no context modules. ERF analysis explains why MLP decoder works on Transformer but not CNN.2026-06-12 | ingest | TE-NAS (Chen et al. 2021) — ICLR 2021, 4 pages: analysis/method/results/critical. Training-free NAS via NTK + linear regions

## [2026-06-13] ingest | Fedus et al. (2021) Switch Transformer — JMLR 2022
- Source: arXiv: 2101.03961, raw/papers/fedus2021_switch_transformer.md (40 pages, 101K chars)
- Created: papers/fedus2021-switch-transformer-analysis.md (overview, 137 lines)
- Created: papers/fedus2021-switch-transformer-method.md (method dim 5 expanded, 187 lines)
- Created: papers/fedus2021-switch-transformer-results.md (results dim 6 expanded, 185 lines)
- Created: papers/fedus2021-switch-transformer-critical.md (dims 7-12 combined, 134 lines)
- Updated: index.md (58 pages total)

## [2026-06-13] ingest | Lepikhin et al. (2020) GShard — ICLR 2021
- Source: arXiv: 2006.16668, raw/papers/lepikhin2021_gshard.md (35 pages, ~123K chars)
- Created: papers/lepikhin2021-gshard-analysis.md (overview, 12 dimensions)
- Created: papers/lepikhin2021-gshard-method.md (MoE gating + GShard API + SPMD Partitioner + Einsum partitioning)
- Created: papers/lepikhin2021-gshard-results.md (Translation quality BLEU + Training efficiency + Memory/runtime scaling)
- Created: papers/lepikhin2021-gshard-critical.md (5 contributions, 9 NK, 7 TK, 10 research opportunities)
- Updated: SCHEMA.md (added distributed-training tags: conditional-computation, spmd, automatic-sharding, etc.)
- Updated: index.md (62 pages total)
- Note: GShard is the foundational MoE+distributed-training systems paper. Automatic sharding via annotations + XLA SPMD Partitioner. 600B MoE Transformer trained in 4 days on 2048 TPU v3. Every-other-layer MoE design + top-2 gating with expert capacity/auxiliary loss/random routing.

## [2026-06-13] ingest | Dai et al. (2024) — DeepSeekMoE (DOI: 10.18653/v1/2024.acl-long.70)
- Source: ACL 2024, PDF downloaded via paper-download crossref_oa
- Raw captured: raw/papers/dai2024_deepseek_moe.pdf + .md
- Created: papers/dai2024-deepseek-moe-analysis.md (overview, 12 dimensions)
- Created: papers/dai2024-deepseek-moe-method.md (fine-grained segmentation + shared isolation + balance loss + 2B/16B configs)
- Created: papers/dai2024-deepseek-moe-results.md (5 experiments: vs GShard/Switch, upper-bound, ablation, specialization analysis, 16B scaling)
- Created: papers/dai2024-deepseek-moe-critical.md (4 contributions, 6 NK, 7 TK, 8 research opportunities, reproducibility 🟢 high)
- Updated: index.md (66 pages total)
- Note: DeepSeekMoE completes the MoE quartet with Switch Transformer (routing simplification) → GShard (distributed systems) → Mixtral (open-source application) → DeepSeekMoE (expert specialization). Two novel strategies: fine-grained expert segmentation + shared expert isolation. 16B model matches 7B dense with 40% compute.

## [2026-06-13] ingest | Wang et al. (2020) — HAT: Hardware-Aware Transformers
- Source: ACL 2020, DOI 10.18653/v1/2020.acl-main.686, raw/papers/wang2020_hat.md
- Created: papers/wang2020-hat-analysis.md (overview)
- Created: papers/wang2020-hat-method.md (SuperTransformer + latency predictor + evolutionary search)
- Created: papers/wang2020-hat-results.md (4 tasks × 3 hardware experiments)
- Created: papers/wang2020-hat-critical.md (3 contributions, 5 NK, 6 TK, 7 research opportunities)
- SCHEMA.md updated: added NAS tags (hardware-aware-nas, latency-prediction, evolutionary-search, weight-sharing-supernet, hardware-specialization, latency-constraint), NLP tags (machine-translation, heterogeneous-transformer, encoder-decoder-attention, edge-inference), dataset tags (wmt14, wmt19, iwslt14)
- Updated: index.md (74 pages total)
- Note: HAT is the first hardware-aware NAS for NLP. SuperTransformer weight sharing reduces search cost 12,041× vs Evolved Transformer. Key insight: GPU prefers shallow-wide, ARM CPU prefers deep-thin.

## [2026-06-13] ingest | NAS for Transformers — HAT + AutoFormer + NAS-BERT + Survey (13 pages)
- Source: ACL 2020 / ICCV 2021 / KDD 2021 / IEEE Access 2022
- PDFs: wang2020_hat.pdf (14p), chen2021_autoformer.pdf (11p), xu2021_nas_bert.pdf (11p)
- Survey full-text not obtained (IEEE paywall), single overview page from abstract
- Created: papers/wang2020-hat-*.md (4 pages) — Hardware-Aware NAS for NLP Transformer, CCF-A
- Created: papers/chen2021-autoformer-*.md (4 pages) — Weight Entanglement one-shot NAS for ViT
- Created: papers/xu2021-nas-bert-*.md (4 pages) — Task-agnostic BERT compression NAS, CCF-A
- Created: papers/chittyvenkata2022-nas-transformers-survey.md (1 page) — Survey overview
- Updated: SCHEMA.md (NAS tags: hardware-aware-nas, latency-prediction, one-shot-nas, weight-entanglement, evolutionary-search, etc.)
- Updated: index.md (75 pages total)
- Updated: mkdocs.yml (4 new nav groups)
- Note: NAS for Transformers quartet complete — HAT (hardware-aware, RL+evolutionary) → AutoFormer (one-shot, weight entanglement) → NAS-BERT (compression, progressive shrinking) → Survey (taxonomy). With earlier TE-NAS (training-free), wiki now covers 5 NAS paradigms.

## [2026-06-13] ingest | GLM 水利水电行业大模型汇报笔记
- Source: GLM 汇报 PPT 照片 (20+ slides, vision recognition)
- Created: papers/glm-hydropower-llm-2026-report.md (single page, 76 pages total)
- Note: GLM-5.0 → HydroGLM vertical LLM for hydropower. 60-person team (Zhipu AI + Tsinghua + Guoneng + Daduhe). 231GB domain corpus, A/B evaluation, Skill Agent platform.

## [2026-06-13] restructure | Wiki 架构重构：新增 notes/ 层，迁移非论文内容
- Moved: papers/{glm-hydropower, avbd-siggraph2025-video, agentic-engineering-22-tips} → notes/
- Moved: papers/ai4s/{ai4s-pinn-deepxde-tutorial, diffusion-models-ai4s-lecture2} → notes/lectures/
- Created: notes/{briefings, lectures, videos, articles}/ directory structure
- Updated: SCHEMA.md — ingest rules table + entity creation mandate
- Updated: index.md — added Notes section, removed 5 entries from Concepts
- Updated: mkdocs.yml — added Notes nav section
- Created: notes/index.md, docs/notes/ symlinks
- Fixed: 18 cross-references across 7 files

## [2026-06-13] ingest | Entities 系统性重建：28 个实体页面
- Created 23 new entity pages: models (6 LLM + 5 vision + 3 NAS), algorithms (2), orgs (4), datasets (3)
- Updated 5 existing entity pages: PhyLSTM2/3, Bouc-Wen, Pseudo-time-stepping, PEER
- Updated: entities/index.md, main index.md (new Entities structure), mkdocs.yml nav
- Entities now: 28 total (was 5), organized in 6 categories
- Wiki total: 99 pages (was 76)

## [2026-06-13] rename | concepts/ → papers/ — 语义澄清
- Renamed: concepts/ → papers/ (69 files moved)
- Updated: SCHEMA.md, README.md, index.md, mkdocs.yml
- Updated: frontmatter type: concept → paper-analysis (69 files)

## [2026-06-24] ingest | Xiong et al. (2025) ConfSeq — 分子构象描述语言 (Nature Machine Intelligence 2026)
- Downloaded: bioRxiv PDF via cloudscraper (7.3MB, 21pp) + Nature supplementary materials (ESM1-4)
- Created: papers/xiong2025-confseq-{analysis,method,results,critical}.md (1+3 structure)
- Created: entities/confseq.md — ConfSeq entity page
- Updated: SCHEMA.md — added Cheminformatics/Drug Discovery tag category (10 new tags)
- Updated: index.md — added 4 paper pages + 1 entity (+5 pages, total 165)
- Updated: mkdocs.yml — added Xiong 2025 ConfSeq nav group
- Note: Nature version paywalled; BJUT CARSI subscription doesn't cover Nature Machine Intelligence
- Updated: docs/ symlink, papers/index.md title
- All wikilinks preserved (internal uses bare slug names, no path prefixed)

## [2026-06-27] ingest | 5 篇 PINN 结构动力计算论文批量入库
- Source: Elsevier XML (paper-download via API)
- Created: 5 papers × 4 pages = 20 paper pages
  - li2025-movingload-pinn-{analysis,method,results,critical}.md (Li YF 2025 AEI: 移动荷载桥梁动力响应)
  - li2025-girder-dynamic-pinn-{analysis,method,results,critical}.md (Li YF 2025 AEI: 斜拉桥主梁动力线形)
  - linka2022-bayesian-pinn-{analysis,method,results,critical}.md (Linka 2022 CMAME: BPINN 非线性动力系统)
  - chen2025-at-pinn-hc-{analysis,method,results,critical}.md (Chen ZL 2025 CMAME: AT-PINN-HC 硬约束振动)
  - goswami2022-variational-deeponet-{analysis,method,results,critical}.md (Goswami 2022 CMAME: V-DeepONet 裂纹)
- Created: entities/pinn.md, entities/deeponet.md, entities/cable-stayed-bridge.md
- Updated: index.md (+15 entries), mkdocs.yml (+5 paper nav + 2 entity sections), SCHEMA.md (+tags)
- Domain: PINN + structural dynamics + neural operators
- Wiki: 165→191 pages

## [2026-06-27] ingest | Wang et al. (2021) PINN NTK 失败机制分析
- Source: JCP DOI 10.1016/j.jcp.2021.110768 (Elsevier XML)
- Created: papers/wang2021-pinn-ntk-failure-{analysis,method,results,critical}.md
- Created: entities/neural-tangent-kernel.md
- Domain: PINN 训练理论 — NTK 谱偏差分析 + 自适应学习率退火
- Wiki: 191→196 pages

## [2026-06-27] ingest | Jagtap et al. (2019) 自适应激活函数加速 PINN
- Source: JCP DOI 10.1016/j.jcp.2019.109136 (Elsevier XML, 790KB)
- Created: papers/jagtap2019-adaptive-activation-{analysis,method,results,critical}.md
- Domain: PINN 训练加速 — 全局/局部可训练激活斜率 + 斜率恢复项
- Wiki: 196→200 pages

## [2026-06-27] ingest | Raissi et al. (2019) PINN 开山之作
- Source: JCP DOI 10.1016/j.jcp.2018.10.045 (Elsevier XML, 1.0MB)
- Created: papers/raissi2019-pinn-{analysis,method,results,critical}.md
- Domain: PINN 奠基 — 自动微分统一处理非线性 PDE (Burgers/Schrödinger/Allen-Cahn/N-S/KdV)
- Special focus: 非线性 PDE 的 AD 处理机制 vs 传统线性化迭代
- Wiki: 200→204 pages

## [2026-06-27] ingest | Raissi et al. (2019) PINN 开山之作
- Source: JCP DOI 10.1016/j.jcp.2018.10.045
- Created: papers/raissi2019-pinn-{analysis,method,results,critical}.md
- Wiki: 200→204 pages

## [2026-06-27] ingest | 3 篇 PINN 非线性 PDE (2024-2026) — KINN, FEDONet, Causal PINN
- Source: Elsevier XML (CMAME x2, JCP x1)
- Created: wang2024-kinn-{4p} + entity/kin, sojitra2026-fedonet-{4p} + entity/fedonet, wang2024-causal-pinn-{4p} + entity/causal-training
- Key: KAN替代MLP / Fourier嵌入DeepONet / 因果时间训练
- Wang Sifan 三部曲完整: 2021 NTK → 2023 伪解 → 2024 因果
- Wiki: 204→219 pages
