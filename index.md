---
id: index
title: "Civil Engineering LLM Wiki Index"
type: index
status: active
project: civil-engineering-llm-wiki
tags: []
sources: []
created: 2026-07-16
updated: 2026-07-31
confidence: high
---

# Civil Engineering LLM Wiki

> 面向物理信息机器学习、结构动力学、计算力学、建筑图纸解析、AI4S 与生成式三维的中文科研知识库。

## Dashboard

- **论文知识页：** [[papers/index]]
- **模型、算法与数据实体：** [[entities/index]]
- **讲座、视频、汇报与文章笔记：** [[notes/index]]
- **横向比较：** [[comparisons/index]]
- **知识库规范：** [[SCHEMA]]
- **操作记录：** [[log]]

所有页面通过上述分区索引、wikilink 和站内搜索可达。`mkdocs.yml` 保持精选导航，不承担完整页面清单职责。

## 最新知识链：NequIP → Allegro → SevenNet

这三项工作分别处理等变表示、严格局部扩展和分布式消息传递并行，构成迁移到大规模结构图学习的重要技术链。

### NequIP：等变表示与数据效率

- [[batzner2022-nequip-analysis]] — 论文概览：E(3) 等变图神经网络原子势。
- [[batzner2022-nequip-method]] — O(3) 不可约表示、球谐方向基和 Clebsch–Gordan 张量积。
- [[batzner2022-nequip-results]] — MD-17、水/冰、反应界面与离子输运结果。
- [[batzner2022-nequip-critical]] — 长程作用、解释性、扩展瓶颈与结构动力迁移。
- [[nequip]] — NequIP 实体页。

### Allegro：严格局部高阶等变表示

- [[musaelian2023-allegro-analysis]] — 严格局部 pair-centered 等变原子势概览。
- [[musaelian2023-allegro-method]] — 双潜空间、局部环境嵌入与迭代张量积。
- [[musaelian2023-allegro-results]] — QM9、revised MD-17、Li$_3$PO$_4$ 与超大规模模拟。
- [[musaelian2023-allegro-critical]] — 局部性、长程项、显存和结构图迁移。
- [[allegro]] — Allegro 实体页。

### SevenNet：分布式消息传递并行

- [[park2024-sevennet-parallel-gnn-ip-analysis]] — NequIP 类 GNN 原子势空间分解并行概览。
- [[park2024-sevennet-parallel-gnn-ip-method]] — ghost atoms、正向节点特征和反向梯度通信。
- [[park2024-sevennet-parallel-gnn-ip-results]] — 32 GPU 弱扩展与约 112,000 原子 Si$_3$N$_4$ 模拟。
- [[park2024-sevennet-parallel-gnn-ip-critical]] — GPU 利用率、通信成本与子结构并行迁移。
- [[sevennet]] — SevenNet 实体页。

## 结构动力学与物理信息机器学习

- [[meng2026-seisgpt-analysis]] — SeisGPT：面向大规模建筑结构的物理信息基础模型。
- [[wu2025-cm-pinn-analysis]] — CM-PINNs：本构模型约束的非线性结构响应预测。
- [[zhang2020-phylstm-analysis]] — PhyLSTM2/3：物理约束时序模型。
- [[du2026-hcff-pinn-analysis]] — HCFF-PINN：结构频率先验与初值硬约束。
- [[liu2025-site-response-pinn-analysis]] — 地震场地反应 PINN。
- [[gao2025-adaptive-loss-pinn-analysis]] — 自适应损失权重 PINN。
- [[rathore2024-pinn-loss-landscape-analysis]] — PINN 损失景观与二阶优化。
- [[penwarden2024-kolmogorov-n-width-piml-analysis]] — 多任务 PIML 的最坏情形泛化度量。
- [[mandl2025-separable-pi-deeponet-analysis]] — 可分离物理信息 DeepONet。

## 神经算子与长时动力学

- [[li2025-node-onet-analysis]] — NODE-ONet：物理编码 Neural ODE 算子网络。
- [[li2026-sgno-analysis]] — SGNO：谱生成神经算子与长时稳定性。
- [[zeraatkar2026-pgt-analysis]] — PGT：Green 函数物理偏置注意力。
- [[goswami2022-variational-deeponet-analysis]] — V-DeepONet：变分能量约束算子学习。

## 计算力学与倒塌模拟

- [[giles2025-avbd-analysis]] — AVBD：增广拉格朗日硬约束物理仿真。
- [[lu2013-collapse-rc-highrise-analysis]] — RC 高层建筑极端地震倒塌模拟。
- [[physics-constrained-training-failure-modes]] — 物理约束训练失败模式比较。

## 建筑图纸解析与计算机视觉

- [[ronneberger2015-unet-analysis]] — U-Net。
- [[zhao2017-pspnet-analysis]] — PSPNet。
- [[chen2018-deeplabv3plus-analysis]] — DeepLabv3+。
- [[sun2019-hrnetv2-analysis]] — HRNetV2。
- [[xie2021-segformer-analysis]] — SegFormer。

## 生成式三维与遥感

- [[lee2026-skyfall-gs-analysis]] — Skyfall-GS。
- [[amapcvlab2026-abotearth-analysis]] — ABot-Earth。
- [[skyfall-gs-vs-abot-earth]] — 两类城市三维生成路线比较。

## 大语言模型与架构搜索

- [[fedus2021-switch-transformer-analysis]] — Switch Transformer。
- [[lepikhin2021-gshard-analysis]] — GShard。
- [[jiang2024-mixtral-of-experts-analysis]] — Mixtral。
- [[dai2024-deepseek-moe-analysis]] — DeepSeekMoE。
- [[wang2024-nas-pinn-analysis]] — NAS-PINN。
- [[chen2021-tenas-analysis]] — TE-NAS。

## Maintenance Rules

1. 新论文先创建 source metadata，再完成 1+3 页面并创建/更新实体。
2. 只使用持久化 provenance marker；禁止提交临时 `filecite` 或 `turnNfileM`。
3. 新页面必须进入对应分区索引，并在必要时进入本页高优先级知识链。
4. 每次 ingest/revise/verify/lint 均追加 [[log]]。
5. 合并前运行严格 lint 和 MkDocs build；GitHub Actions 只验证与部署，不修改仓库。
