---
id: index
title: Civil Engineering LLM Wiki Index
type: index
status: active
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-07-16'
updated: '2026-08-02'
confidence: high
---

# Civil Engineering LLM Wiki

> 面向物理信息机器学习、结构动力学、计算力学、建筑图纸解析、AI4S 与生成式三维的中文科研知识库。

## Dashboard

- **论文知识页：** [[papers/index]]
- **模型、算法与数据实体：** [[entities/index]]
- **概念与机制：** [[concepts/index]]
- **规范来源记录：** [[sources/index]]
- **讲座、视频、汇报与文章笔记：** [[notes/index]]
- **横向比较：** [[comparisons/index]]
- **知识库规范：** [[SCHEMA]]
- **操作记录：** [[log]]

所有页面通过上述分区索引、wikilink 和站内搜索可达。`mkdocs.yml` 保持精选导航，完整侧栏由构建 hook 自动生成。

## 最新知识链：大规模、高效、断裂与双相 MPM

- [[liu2025-incompressible-crack-mpm-analysis]] — 不可压缩裂纹 MPM：部分损伤软化、完全损伤碎屑转换与体积历史。
- [[liu2025-incompressible-crack-mpm-method]] — 压缩感知状态转换、非关联 Drucker–Prager 回映射和额外体积变形梯度。
- [[liu2025-incompressible-crack-mpm-critical]] — 网格相关裂纹增厚、视觉验证边界及 RC 倒塌迁移推论。
- [[zhao2026-unified-sparse-mpm-analysis]] — Unified Sparse MPM：把大范围空域压缩为活跃节点集合与紧凑索引。
- [[zhao2026-unified-sparse-mpm-method]] — CPU 块级 prefix scan、GPU 哈希原子插入与架构专用实现。
- [[zhao2026-unified-sparse-mpm-results]] — Blatten 强稀疏案例的一至两个数量级时间/内存收益。
- [[zhao2026-unified-sparse-mpm-critical]] — 低稀疏度、块内浪费、哈希竞争与单节点验证边界。
- [[unified-sparse-mpm]] — Unified Sparse MPM 实体页。
- [[feng2026-mpm-lite-analysis]] — MPM Lite：固定网格积分与 PPC 无关的隐式求解阶段。
- [[juel2026-stabilized-fractional-step-mpm-analysis]] — 稳定化分步双相 MPM：固–液大变形与压力稳定化。

## 结构动力学与物理信息机器学习

- [[meng2026-seisgpt-analysis]] — SeisGPT。
- [[wu2025-cm-pinn-analysis]] — CM-PINNs。
- [[zhang2020-phylstm-analysis]] — PhyLSTM2/3。
- [[du2026-hcff-pinn-analysis]] — HCFF-PINN。
- [[rathore2024-pinn-loss-landscape-analysis]] — PINN 损失景观与二阶优化。
- [[mandl2025-separable-pi-deeponet-analysis]] — 可分离物理信息 DeepONet。

## 等变图学习与神经算子

- [[batzner2022-nequip-analysis]] — NequIP。
- [[musaelian2023-allegro-analysis]] — Allegro。
- [[park2024-sevennet-parallel-gnn-ip-analysis]] — SevenNet。
- [[li2025-node-onet-analysis]] — NODE-ONet。
- [[li2026-sgno-analysis]] — SGNO。
- [[zeraatkar2026-pgt-analysis]] — PGT。

## 建筑图纸、生成式三维与大模型

- [[ronneberger2015-unet-analysis]] — U-Net。
- [[chen2018-deeplabv3plus-analysis]] — DeepLabv3+。
- [[xie2021-segformer-analysis]] — SegFormer。
- [[lee2026-skyfall-gs-analysis]] — Skyfall-GS。
- [[amapcvlab2026-abotearth-analysis]] — ABot-Earth。
- [[jiang2024-mixtral-of-experts-analysis]] — Mixtral。

## Maintenance Rules

1. 新论文先创建 raw source record 与 canonical source note，再完成中文 1+3 页面并创建/更新实体与概念。
2. 只使用持久化 provenance marker；禁止提交临时 `filecite` 或 `turnNfileM`。
3. 新页面必须进入对应分区索引；侧栏由 `scripts/mkdocs_hooks.py` 扫描全部页面生成。
4. 每次 ingest/revise/verify/lint/deploy 均追加 [[log]]。
5. 合并前运行严格 lint 和 MkDocs build；GitHub Actions 只验证与部署，不修改知识内容。

## Complete Knowledge Map

- [[papers/index]]
- [[entities/index]]
- [[concepts/index]]
- [[sources/index]]
- [[notes/index]]
- [[comparisons/index]]
- [[SCHEMA]]
- [[log]]
