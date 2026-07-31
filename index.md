# Civil Engineering LLM Wiki

> 面向物理信息机器学习、结构动力学、计算力学、建筑图纸解析、AI4S 与生成式三维的中文科研知识库。
>
> Last updated: 2026-07-31

## 知识库入口

- [[papers/index]] — 论文知识页索引；每篇全文论文按 `analysis + method + results + critical` 组织。
- [[entities/index]] — 模型、算法、数据集与组织实体索引。
- [[notes/index]] — 讲座、视频、汇报和文章笔记。
- [[comparisons/index]] — 方法横向比较与失败模式总结。
- [[SCHEMA]] — 文件结构、frontmatter、标签和 ingest 规范。
- [[log]] — 追加式知识库操作记录。

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
- [[musaelian2023-allegro-results]] — QM9、revMD-17、Li$_3$PO$_4$ 与超大规模模拟。
- [[musaelian2023-allegro-critical]] — 局部性、长程项、显存和结构图迁移。
- [[allegro]] — Allegro 实体页。

### SevenNet：分布式消息传递并行

- [[park2024-sevennet-parallel-gnn-ip-analysis]] — NequIP 类 GNN 原子势空间分解并行概览。
- [[park2024-sevennet-parallel-gnn-ip-method]] — ghost atoms、正向节点特征和反向梯度通信。
- [[park2024-sevennet-parallel-gnn-ip-results]] — 32 GPU 扩展与 112,000 原子 Si$_3$N$_4$ 模拟。
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
- [[zhang2026-legonet-analysis]] — LegONet：可组合结构保持 PDE 算子块。
- [[goswami2022-variational-deeponet-analysis]] — V-DeepONet：变分能量约束神经算子。

## 计算力学与倒塌模拟

- [[giles2025-avbd-analysis]] — AVBD：增广拉格朗日硬约束物理仿真。
- [[lu2013-collapse-rc-highrise-analysis]] — RC 高层建筑极端地震倒塌模拟。
- [[physics-constrained-training-failure-modes]] — 物理约束训练失败模式总结。

## 建筑图纸解析与计算机视觉

- [[ronneberger2015-unet-analysis]] — U-Net。
- [[zhao2017-pspnet-analysis]] — PSPNet。
- [[chen2018-deeplabv3plus-analysis]] — DeepLabv3+。
- [[sun2019-hrnetv2-analysis]] — HRNet。
- [[xie2021-segformer-analysis]] — SegFormer。

## 遥感、生成式三维与数字地球

- [[lee2026-skyfall-gs-analysis]] — Skyfall-GS：卫星 3DGS 重建与扩散式视角扩展。
- [[amapcvlab2026-abotearth-analysis]] — ABot-Earth：生成式三维地球模型。
- [[skyfall-gs-vs-abot-earth]] — 两类城市三维路线比较。

## 大模型、NAS 与训练系统

- [[li2025-functional-scaling-laws-analysis]] — Functional Scaling Laws。
- [[wang2024-nas-pinn-analysis]] — NAS-PINN。
- [[chen2021-tenas-analysis]] — TE-NAS。
- [[chen2021-autoformer-analysis]] — AutoFormer。
- [[fedus2021-switch-transformer-analysis]] — Switch Transformer。
- [[dai2024-deepseek-moe-analysis]] — DeepSeekMoE。

## 使用方式

1. 从本页或各分类索引定位主题；
2. 优先阅读论文 `analysis` 页面建立全局认识；
3. 需要公式、架构和训练细节时进入 `method`；
4. 需要量化证据时进入 `results`；
5. 设计新研究前重点阅读 `critical` 中的 Negative Knowledge 与可迁移机会；
6. 通过页面间 `[[wikilinks]]` 沿知识链继续检索。
