# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Last updated: 2026-06-15 | Total pages: 150 (Papers: 105, Notes: 5, Entities: 37, Comparisons: 2)

## Papers
- [[giles2025-avbd-analysis]] — Giles et al. (2025) AVBD 论文分析：augmented Lagrangian 扩展 VBD，支持硬约束 + 高刚度比
- [[giles2025-avbd-method]] — AVBD 方法展开：硬约束、不等式约束、摩擦接触、渐进刚度递增
- [[giles2025-avbd-results]] — AVBD 实验结果：vs VBD/XPBD/Seq Imp 在刚度比、质量比、碰撞堆叠上的量化对比
- [[giles2025-avbd-critical]] — AVBD 贡献+Negative+可迁移+研究机会：含 PINN 软约束失效的平行参照
- [[lu2013-collapse-rc-highrise-analysis]] — Lu et al. (2013) RC 高层建筑极端地震倒塌模拟：纤维梁+多层壳+单元去激活
- [[lu2013-collapse-rc-highrise-method]] — 倒塌模拟方法：纤维梁单元、多层壳单元、应变失效准则/去激活机制
- [[lu2013-collapse-rc-highrise-results]] — 三组倒塌算例：10层框架/18层框筒/20层框筒双地震动对比
- [[lu2013-collapse-rc-highrise-critical]] — 贡献+Negative（无足尺验证/准则敏感）+可迁移+ML 交叉机会
- [[ronneberger2015-unet-analysis]] — Ronneberger et al. (2015) U-Net：encoder-decoder + skip connections，小样本语义分割范式
- [[ronneberger2015-unet-method]] — U-Net 方法：overlap-tile 任意大图推理 + 弹性变形增强 + 加权分离 loss
- [[ronneberger2015-unet-results]] — 三组 ISBI 挑战赛结果：EM 神经元 + 细胞分割，碾压前方法
- [[ronneberger2015-unet-critical]] — 贡献+Negative（valid conv/镜像伪影）+可迁移（→结构图纸）+ 机会
- [[zhao2017-pspnet-analysis]] — Zhao et al. (2017) PSPNet：金字塔池化 + 辅助监督，ImageNet 2016 场景解析冠军
- [[zhao2017-pspnet-method]] — PSPNet 方法：Pyramid Pooling Module 四级池化 + Deeply Supervised ResNet
- [[zhao2017-pspnet-results]] — PSPNet 实验结果：ADE20K/VOC/Cityscapes SOTA + 组件 ablation
- [[zhao2017-pspnet-critical]] — PSPNet 贡献+Negative（bin size 固定/α 需搜索）+可迁移（PPM 通用模块）+ 机会
- [[chen2018-deeplabv3plus-analysis]] — Chen et al. (2018) DeepLabv3+：ASPP encoder + 简洁 decoder，VOC 89.0% SOTA
- [[chen2018-deeplabv3plus-method]] — DeepLabv3+ 方法：Atrous Separable Conv + Simple Decoder + Modified Xception
- [[chen2018-deeplabv3plus-results]] — DeepLabv3+ 结果：VOC/Cityscapes SOTA + decoder ablation + trimap 边界分析
- [[chen2018-deeplabv3plus-critical]] — DeepLabv3+ 贡献+Negative（decoder 超参经验化/JFT 不可复现）+可迁移+机会
- [[sun2019-hrnetv2-analysis]] — Sun et al. (2019) HRNetV2：全程高分辨率并行卷积 + 全分辨率聚合，Cityscapes 81.6%
- [[sun2019-hrnetv2-method]] — HRNet 方法：4 阶段多分辨率并行 + 跨分辨率全连接融合 + HRNetV2 聚合
- [[sun2019-hrnetv2-results]] — HRNet 结果：Cityscapes/PASCAL Context/LIP/面部关键点/COCO 多任务 SOTA
- [[sun2019-hrnetv2-critical]] — HRNet 贡献+Negative（大模型边际递减/无显式上下文）+可迁移+机会
- [[xie2021-segformer-analysis]] — Xie et al. (2021) SegFormer：层级化 Transformer + All-MLP decoder，ADE20K 51.8% SOTA
- [[xie2021-segformer-method]] — SegFormer 方法：MiT encoder (Mix-FFN/Eff-SA) + 纯 MLP decoder + overlap patch
- [[xie2021-segformer-results]] — SegFormer 结果：ADE/Cityscapes/COCO-Stuff SOTA + Cityscapes-C 零样本鲁棒性
- [[xie2021-segformer-critical]] — SegFormer 贡献+Negative（MLP decoder 不兼容 CNN）+可迁移+机会
- [[chen2021-tenas-analysis]] — Chen et al. (2021) TE-NAS：训练-free NAS via NTK 条件数 + 线性区域数，ImageNet 仅 4 GPU 小时
- [[chen2021-tenas-method]] — TE-NAS 方法：NTK κN + 线性区域 ˆRN + Pruning-by-Importance 搜索
- [[chen2021-tenas-results]] — TE-NAS 结果：NAS-Bench-201 / DARTS CIFAR-10 / ImageNet mobile SOTA 级零训练搜索
- [[chen2021-tenas-critical]] — TE-NAS 贡献+Negative（rank corr ~0.5-0.7）+可迁移+机会
- [[chen2021-autoformer-analysis]] — Chen et al. (2021) AutoFormer：首个 ViT 专用 NAS，Weight Entanglement 实现 once-for-all supernet
- [[chen2021-autoformer-method]] — AutoFormer 方法：Weight Entanglement + 五维弹性搜索空间 + 进化搜索 pipeline
- [[chen2021-autoformer-results]] — AutoFormer 结果：ImageNet T/S/B 74.7/81.7/82.4% + 迁移学习 + 蒸馏
- [[chen2021-autoformer-critical]] — AutoFormer 贡献+Negative（homogeneous only/CNN gap）+可迁移+7 项研究机会
- [[xu2021-nas-bert-analysis]] — Xu et al. (2021) NAS-BERT：NAS 搜 BERT 压缩，block-wise + progressive shrinking，输出 5M-60M 多尺寸 task-agnostic 模型
- [[xu2021-nas-bert-method]] — NAS-BERT 方法：搜索空间设计 + Block-wise 蒸馏 + Progressive shrinking + Model selection
- [[xu2021-nas-bert-results]] — NAS-BERT 结果：GLUE AVG 84.2 (60M) / SQuAD F1 88.4 / 多尺寸验证 / Progressive shrinking ablation
- [[xu2021-nas-bert-critical]] — NAS-BERT 贡献+Negative（block-wise isolation/supernet收敛）+可迁移（bin-based shrinking 范式）+6 项研究机会

- [[chittyvenkata2022-nas-transformers-survey]] — Chitty-Venkata et al. (2022) NAS for Transformers 综述：RL/Evolutionary/One-Shot/Training-Free 四维分类

- [[so2021-primer-analysis]] — So et al. (2021) Primer：进化搜索高效 Transformer，Squared ReLU + MDHA，T5 537M 加速 4.2×
- [[so2021-primer-method]] — Primer 方法：DNA 编码搜索空间 + CC 进化 + weight sharing supernet
- [[so2021-primer-results]] — Primer 结果：C4/LM1B perplexity + T5 加速 4.2× + GPT-3 1.9B 加速 3×
- [[so2021-primer-critical]] — Primer 贡献+Negative（decoder-only 限制/encoder-decoder 退化）+可迁移+机会
- [[li2021-bossnas-analysis]] — Li et al. (2021) BossNAS：块级自监督 NAS，Ensemble Bootstrapping 探索 hybrid CNN-Transformer
- [[li2021-bossnas-method]] — BossNAS 方法：块级分解 + Siamese Supernet + 种群中心无监督评估
- [[li2021-bossnas-results]] — BossNAS 结果：HyTra ImageNet SOTA + NATS-Bench SS 评分反超有监督（τ=0.65）
- [[li2021-bossnas-critical]] — BossNAS 贡献+Negative（块间独立性未理论分析）+可迁移+5 项研究机会
- [[zhao2021-memory-efficient-dnas-analysis]] — Zhao et al. (2021) DNAS：多分割可逆网络实现内存高效 Transformer 可微搜索
- [[zhao2021-memory-efficient-dnas-method]] — DNAS 方法：Multi-Split Reversible + BP-with-Reconstruction + Gₖ 设计
- [[zhao2021-memory-efficient-dnas-results]] — DNAS 结果：WMT14 28.4 BLEU / 120× 成本降低 超 Evolved Transformer
- [[zhao2021-memory-efficient-dnas-critical]] — DNAS 贡献+Negative（搜索隐藏层必须匹配目标）+可迁移+机会
- [[serianni2023-training-free-nas-rnn-transformers-analysis]] — Serianni et al. (2023) Training-free NAS：Hidden Covariance 代理用于 RNN/Transformer 搜索
- [[serianni2023-training-free-nas-rnn-transformers-method]] — Training-free NAS 方法：Expressivity/Trainability 跨架构代理
- [[serianni2023-training-free-nas-rnn-transformers-results]] — Training-free NAS 结果：NAS-Bench-NLP τ=0.37 / FlexiBERT 全指标被参数计数打败
- [[serianni2023-training-free-nas-rnn-transformers-critical]] — Training-free NAS 贡献+Negative（Transformer 全指标失败）+可迁移+机会

- [[jiang2024-mixtral-of-experts-analysis]]
- [[jiang2024-mixtral-of-experts-method]] — Mixtral 方法展开：8 专家 Top-2 路由 + SwiGLU + Megablocks 稀疏 MM
- [[jiang2024-mixtral-of-experts-results]] — Mixtral 实验结果：vs Llama/GPT-3.5 全面对比 + 多语言 + 长上下文 + 路由分析
- [[jiang2024-mixtral-of-experts-critical]] — Mixtral 贡献+Negative（专家不自动特化/训练细节未公开）+可迁移（密集→MoE改造）+机会
- [[wang2023-pinn-spurious-analysis]] — Wang et al. (2023) PINN 伪解问题概述：PDE 残差 loss 的缺陷 + 伪时间步进方案
- [[wang2023-pinn-spurious-method]] — 伪时间步进 + 自适应步长方法展开
- [[wang2023-pinn-spurious-results]] — Helmholtz/Klein-Gordon/Navier-Stokes/Rayleigh-Taylor 实验结果
- [[wang2023-pinn-spurious-critical]] — 贡献 + 知识点 + Negative + 可迁移 + 研究机会
- [[zhang2020-phylstm-analysis]] — Zhang et al. (2020) PhyLSTM 概述：12 维度论文分析总览
- [[zhang2020-phylstm-method]] — PhyLSTM2/3 方法机制展开：架构数据流图、损失函数详解、训练策略
- [[zhang2020-phylstm-results]] — 两个验证案例结果展开：MRF 和 Bouc-Wen
- [[zhang2020-phylstm-critical]] — 贡献 + 知识点 + Negative + 可迁移 + 研究机会。**含 PINN 失败模式关联**
- [[fedus2021-switch-transformer-analysis]] — Fedus et al. (2021) Switch Transformer 概述：简化 MoE to k=1 routing，万亿参数 4× speedup over T5-XXL
- [[fedus2021-switch-transformer-method]] — Switch 方法：Switch Routing (k=1) + 负载均衡损失 + 选择性精度 + Expert Dropout + 三维并行
- [[fedus2021-switch-transformer-results]] — Switch 结果：7× speedup over T5-Base，全 101 语言提升，蒸馏 99% 压缩 30% 保留
- [[fedus2021-switch-transformer-critical]] — Switch 贡献+Negative（训练不稳定/上游→下游断层）+可迁移+5 项研究机会
- [[lepikhin2021-gshard-analysis]] — Lepikhin et al. (2020) GShard 概述：自动分片+条件计算实现 600B 参数 MoE Transformer 4天训练
- [[lepikhin2021-gshard-method]] — GShard 方法：三层系统（MoE 门控 + 标注 API + SPMD 分区器）+ Einsum 分区模式
- [[lepikhin2021-gshard-results]] — GShard 结果：100语言翻译 ∆BLEU +13.5, 600B 训练 4天, 亚线性计算/显存缩放
- [[lepikhin2021-gshard-critical]] — GShard 贡献+Negative（bfloat16不稳定/容量固定）+可迁移（SPMD范式）+10项研究机会

- [[dai2024-deepseek-moe-analysis]] — Dai et al. (2024) DeepSeekMoE 概述：细粒度专家分割+共享专家隔离，40% 计算量达 7B 密集水平
- [[dai2024-deepseek-moe-method]] — DeepSeekMoE 方法：m× 专家分割 + Ks 共享专家 + Balance Loss + 2B/16B 双规模配置
- [[dai2024-deepseek-moe-results]] — DeepSeekMoE 结果：vs GShard/密集上限/Switch，2B 逼近理论上限，16B 仅 40% 计算量
- [[dai2024-deepseek-moe-critical]] — DeepSeekMoE 贡献+Negative（注意力瓶颈/MCQ弱点）+可迁移（细粒度范式）+8项研究机会
- [[wang2020-hat-analysis]] — Wang et al. (2020) HAT 概述：硬件感知 NAS + SuperTransformer 权重共享，为不同硬件搜索专用高效 Transformer
- [[wang2020-hat-method]] — HAT 方法：SuperTransformer + 延迟预测器 + 进化搜索 + 任意 encoder-decoder attention
- [[wang2020-hat-results]] — HAT 结果：四任务×三硬件 BLEU-Latency 对比，3× 加速 3.7× 压缩，搜索成本 1/12,041 of Evolved Transformer
- [[wang2020-hat-critical]] — HAT 贡献+Negative（预测器数据依赖/设计空间固定）+可迁移+7 项研究机会

- [[real2020-automl-zero-analysis]] — Real et al. (2020) AutoML-Zero：从零进化搜索 ML 算法，重新发现反向传播、梯度下降等核心技术
- [[real2020-automl-zero-method]] — AutoML-Zero 方法：三组件程序表示 + 65 操作集 + 小种群正则化进化 + FEC
- [[real2020-automl-zero-results]] — AutoML-Zero 结果：三阶段实验（线性/非线性/从头学），涌现反向传播、学习率衰减
- [[real2020-automl-zero-critical]] — AutoML-Zero 贡献+Negative（计算开销巨大/大规模未验证）+可迁移+机会

- [[ru2020-nago-analysis]] — Ru et al. (2020) NAGO：搜索架构生成器而非架构本身，8 维超参数编码 >4.58×10⁵⁶ 种架构
- [[ru2020-nago-method]] — NAGO 方法：HNAG 三级层次图 + BOHB 多保真度 + 异方差 BNN + Pareto 前沿
- [[ru2020-nago-results]] — NAGO 结果：CIFAR-10 96.6% + ImageNet 76.8% (5.7M) + Pareto 前沿胜 RNAG-D
- [[ru2020-nago-critical]] — NAGO 贡献+Negative（~15 GPU-day/高维度 BO 失效）+可迁移+机会

- [[akhauri2022-eznas-analysis]] — Akhauri et al. (2022) EZNAS：遗传编程自动发现零成本 NAS 代理，跨空间泛化 SOTA
- [[akhauri2022-eznas-method]] — EZNAS 方法：表达式树 + 34 操作集 + 抗过拟合三通路评估 + 进化搜索
- [[akhauri2022-eznas-results]] — EZNAS 结果：NAS-Bench-201 τ 超越 NASWOT/synflow，跨 NDS/NATS-Bench 全 SOTA
- [[akhauri2022-eznas-critical]] — EZNAS 贡献+Negative（无法区分 top 10%/丢失拓扑）+可迁移+机会

- [[lee2024-aznas-analysis]] — Lee & Ham (2024) AZ-NAS：组装四个互补零成本代理（sE/sP/sT/sC），NAS-Bench-201 τ=0.741
- [[lee2024-aznas-method]] — AZ-NAS 方法：灵敏度/参数/拓扑/综合四代理 + 非线性 log-Rank 聚合
- [[lee2024-aznas-results]] — AZ-NAS 结果：NAS-Bench-201 + MobileNetV2 + AutoFormer 三空间均 SOTA
- [[lee2024-aznas-critical]] — AZ-NAS 贡献+Negative（代理数固定/耦合黑盒）+可迁移+6 个研究机会

- [[maimon2026-sparse-dense-analysis]] — Maimon et al. (2026) Sparse→Dense Coding：Nature 论文，发现海马 CA3→CA1 的稀疏到密集编码变换
- [[maimon2026-sparse-dense-method]] — 方法：无线 tetrode + 钙成像双记录，位置场检测 + 群体解码 + 学习模拟
- [[maimon2026-sparse-dense-results]] — 结果：CA3 稀疏 (~2% 活跃) → CA1 密集 (~25% 活跃)，维度膨胀 5-10×
- [[maimon2026-sparse-dense-critical]] — 贡献+Negative（蝙蝠模型泛化限制/因果性未验证）+可迁移+机会

## Entities
### 大语言模型
- [[switch-transformer]] — Switch Transformer: MoE k=1 routing, 万亿参数
- [[gshard]] — GShard: 自动分片+条件计算, 600B MoE
- [[mixtral-8x7b]] — Mixtral 8×7B: 首个开源实用级 MoE LLM
- [[deepseek-moe]] — DeepSeekMoE: 细粒度专家分割+共享专家
- [[glm-5]] — GLM-5.0: 全球第四/开源第一
- [[hydroglm]] — HydroGLM: 水利水电行业大模型, 88.6 分

### 语义分割模型
- [[u-net]] — U-Net: skip-connections 小样本分割
- [[pspnet]] — PSPNet: 金字塔池化场景解析
- [[deeplabv3plus]] — DeepLabv3+: ASPP + decoder
- [[hrnet]] — HRNet: 高分辨率并行卷积
- [[segformer]] — SegFormer: Transformer + MLP decoder

### NAS 模型
- [[hat]] — HAT: Hardware-Aware NAS for Transformer
- [[autoformer]] — AutoFormer: ViT one-shot NAS
- [[nas-bert]] — NAS-BERT: BERT 压缩 NAS
- [[primer]] — Primer: Google 进化搜索高效 Transformer，Squared ReLU + MDHA
- [[bossnas]] — BossNAS: 块级自监督搜索 hybrid CNN-Transformer
- [[memory-efficient-dnas]] — Memory-Efficient DNAS: 多分割可逆可微 Transformer 搜索
- [[training-free-nas-transformers]] — Training-free NAS for RNN/Transformer: Hidden Covariance
- [[automl-zero]] — AutoML-Zero: Google 从零进化搜索 ML 算法框架
- [[nago]] — NAGO: Neural Architecture Generator Optimization，搜索架构生成器
- [[eznas]] — EZNAS: 遗传编程自动发现零成本 NAS 代理，跨空间泛化
- [[az-nas]] — AZ-NAS: 四互补代理组装方案，NAS-Bench-201 τ=0.741 SOTA

### 算法
- [[te-nas]] — TE-NAS: Training-free NAS
- [[avbd]] — AVBD: 硬约束物理仿真
- [[phylstm2]] — PhyLSTM2: 双 LSTM 滞回元模型
- [[phylstm3]] — PhyLSTM3: 三 LSTM 增强
- [[bouc-wen-model]] — Bouc-Wen 滞回模型
- [[pseudo-time-stepping]] — 伪时间步进

### 组织
- [[zhipu-ai]] — 智谱AI
- [[guoneng-bigdata]] — 国能大数据
- [[daduhe-company]] — 大渡河公司
- [[tsinghua-dhe]] — 清华大学水利系

### 神经科学
- [[sparse-dense-coding]] — Sparse→Dense Coding: 海马 DG→CA3→CA1 编码梯度变换，Maimon et al. (2026) Nature

### 数据集
- [[nasbench201]] — NAS-Bench-201
- [[ade20k]] — ADE20K
- [[cityscapes]] — Cityscapes
- [[peer-strong-motion-database]] — PEER 强震数据库

## Notes
- [[notes/briefings/glm-hydropower-2026]] — GLM 水利水电行业大模型汇报笔记：GLM-5.0 → HydroGLM → 智能中台，60人团队，231GB语料
- [[notes/lectures/ai4s-pinn-deepxde]] — AI4S 第一课：PINN 从入门到 DeepXDE 实战（陆路/耶鲁，90min）
- [[notes/lectures/ai4s-diffusion-models]] — AI4S 第二讲：扩散生成模型从物理原理到蛋白质设计（章敏/浙大，90min）
- [[notes/videos/avbd-siggraph2025]] — AVBD 物理仿真算法 (SIGGRAPH 2025)：B站视频笔记，少迭代收敛 + 大质量比稳定
- [[notes/articles/agentic-engineering-22-tips]] — Matt Van Horn (2026.06) Agentic Engineering 22 条技巧：plan→build loop / 上下文为王 / 语音输入 / 多 agent 并行

## Comparisons
- [[phylstm2-vs-phylstm3-vs-lstm]] — PhyLSTM2/3/LSTM 性能对比 + 选型指南
- [[physics-constrained-training-failure-modes]] — 物理约束训练失败模式：PhyLSTM vs PINN 对比分析

## Queries