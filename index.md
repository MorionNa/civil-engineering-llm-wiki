---
id: index
title: Civil Engineering LLM Wiki Index
type: index
status: active
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-07-16'
updated: '2026-08-04'
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

## 最新知识链：高鲁棒接触、异构耦合、约束粒子与高效 MPM

- [[li2022-bfemp-analysis]] — BFEMP：以粒子–FEM 边界障碍势单体耦合隐式 MPM 与 FEM。
- [[li2022-bfemp-method]] — 链式接触力传递、投影 Newton、CCD/行列式过滤与 lagged 摩擦。
- [[li2022-bfemp-results]] — 动量、Hertz 接触、临界摩擦、细化收敛、屈曲和三维扭转证据。
- [[li2022-bfemp-critical]] — 有限粒子域重叠、表面权重、摩擦收敛和动态转换边界。
- [[bfemp]] — BFEMP 实体页。
- [[li2020-incremental-potential-contact-analysis]] — IPC：在每个非线性迭代中保持无交叉、无反转的接触可行路径。
- [[li2020-incremental-potential-contact-method]] — 无符号距离障碍势、Projected Newton、CCD 线搜索和滞后变分摩擦。
- [[li2020-incremental-potential-contact-results]] — 高速、尖锐障碍、极端压缩、摩擦结构与 2.3M 四面体规模证据。
- [[li2020-incremental-potential-contact-critical]] — 摩擦 lagging、正间隙初始化、线性系统成本与断裂拓扑边界。
- [[incremental-potential-contact]] — IPC 实体页。
- [[yu2024-xpbi-analysis]] — XPBI：以速度梯度、更新拉格朗日状态和 XPBD 内循环塑性处理连续介质非弹性。
- [[yu2024-xpbi-method]] — 修正 Wendland 核、逐粒子能量约束、塑性固定点和着色 Gauss–Seidel。
- [[yu2024-xpbi-results]] — Von Mises、Drucker–Prager、NACC、Herschel–Bulkley 与百万粒子证据。
- [[yu2024-xpbi-critical]] — 塑性收敛、邻域依赖、耗散和工程迁移边界。
- [[xpbi]] — XPBI 实体页。
- [[pantidis2026-ifenn-phase-field-analysis]] — PICNN-IFENN：用两个传播增量训练相场 PDE 代理，FEM 保持机械平衡。
- [[pantidis2026-ifenn-phase-field-method]] — 无时序空间耦合、对称卷积核、固定 Laplacian 残差和交错求解。
- [[pantidis2026-ifenn-phase-field-results]] — 跨载荷步、网格密度、双裂纹方向与矩形域泛化。
- [[pantidis2026-ifenn-phase-field-critical]] — 起裂阶段、长度尺度、Gaussian 残余刚度和工程迁移边界。
- [[picnn-ifenn-phase-field]] — PICNN-IFENN 实体页。
- [[liu2025-incompressible-crack-mpm-analysis]] — 不可压缩裂纹 MPM：部分损伤软化、完全损伤碎屑转换与体积历史。
- [[liu2025-incompressible-crack-mpm-method]] — 压缩感知状态转换、非关联 Drucker–Prager 回映射和额外体积变形梯度。
- [[liu2025-incompressible-crack-mpm-critical]] — 网格相关裂纹增厚、视觉验证边界及 RC 倒塌迁移推论。
- [[zhao2026-unified-sparse-mpm-analysis]] — Unified Sparse MPM：把大范围空域压缩为活跃节点集合与紧凑索引。
- [[feng2026-mpm-lite-analysis]] — MPM Lite：固定网格积分与 PPC 无关的隐式求解阶段。
- [[juel2026-stabilized-fractional-step-mpm-analysis]] — 稳定化分步双相 MPM：固–液大变形与压力稳定化。

## 结构动力学与物理信息机器学习

- [[meng2026-seisgpt-analysis]] — SeisGPT。
- [[wu2025-cm-pinn-analysis]] — CM-PINNs。
- [[zhang2020-phylstm-analysis]] — PhyLSTM2/3。
- [[du2026-hcff-pinn-analysis]] — HCFF-PINN。
- [[rathore2024-pinn-loss-landscape-analysis]] — PINN 损失景观与二阶优化。
- [[mandl2025-separable-pi-deeponet-analysis]] — 可分离物理信息 DeepONet。

### nonlinear-pinn 项目证据（2026-08-03）

- [[project-scheme-ingest-manifest-2026-08-03]] — 133 份方案/结果文档与 9 个复现家族的全量覆盖清单。
- [[current-structural-pinn-ranking-2026-08-03]] — 当前最接近六项目标的方案、硬门通过情况与未完成项。
- [[baseline-unified-r2-reassessment-2026-08-03]] — PhyLSTM3 与 CM-PINN 的 pooled/macro/worst-case R² 统一复算。
- [[inference-speed-evidence-2026-08-03]] — 5DOF 批量、大规模 50kDOF 与 OpenSeesPy 证据缺口。
- [[one-structure-one-model-contract-2026-08-03]] — 一个结构对应一个模型，不要求跨结构零样本泛化。
- [[notes/cycle41-hn-cs-lbpc-nogo-m1-2026-08-04]] - Cycle 41 normalized Bouc-Wen equivalence failed the frozen M1 gate before validation or training.
- [[notes/cycle42-exact-bilinear-nogo-h1-2026-08-04]] - Cycle 42 exact bilinear passed H0 but only two of four development histories passed visible-loop validity.
- [[fixed-mdof5-mtp-strict-label-free-v1-nogo-20260803]] - Strict label-free fixed-structure MTP fails official-90 accuracy, independent physics, and inference speed.
- [[reproduction-schemes-inventory-2026-08-03]] — CM-PINN、PhyLSTM、HCFF-PINN、图网络与时间积分复现总览。

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

## Local Workspace Merge (2026-08-03)

- [[papers/list2025-unrolled-training-analysis]] — 非线性结构动力学的展开训练与长期积分稳定性。
- [[papers/brandstetter2022-mp-pde-analysis]] — Message Passing Neural PDE Solvers。
- [[papers/moseley2023-fbpinn-analysis]] — FBPINN 的时空分解与局部归一化。
- [[entities/mtp-mechconv-v2]] — 项目主线 MTP-MechConv 实体。
- [[entities/message-passing-reach-contract]] — 消息传递可达域与 halo 合同。
- [[comparisons/mtp-mechconv-v2-evidence]] — 时间并行、reach、粗层、halo 与本构证据矩阵。
- [[comparisons/cycle36_pdps_mco_literature_20260803]] — PDPS/MCO 文献证据与 M0 边界。
- [[notes/ingest-v20-rk4z-2026-08-01]] — V20-RK4Z 项目证据入口。

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
