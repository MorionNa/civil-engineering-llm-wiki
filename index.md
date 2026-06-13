# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Last updated: 2026-06-13 | Total pages: 66

## Concepts
- [[concepts/ai4s/ai4s-pinn-deepxde-tutorial]] — AI4S第一课：PINN 从入门到 DeepXDE 实战（陆路/耶鲁，90min）
- [[avbd-siggraph2025-video]] — AVBD 物理仿真算法 (SIGGRAPH 2025)：B站视频笔记，少迭代收敛 + 大质量比稳定
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
- [[concepts/ai4s/diffusion-models-ai4s-lecture2]] — AI4S第二讲：扩散生成模型从物理原理到蛋白质设计（章敏/浙大，90min）
- [[agentic-engineering-22-tips]] — Matt Van Horn (2026.06) Agentic Engineering 22 条技巧：plan→build loop / 上下文为王 / 语音输入 / 多 agent 并行 / skill 自动化
- [[jiang2024-mixtral-of-experts-analysis]] — Jiang et al. (2024) Mixtral 8x7B 概述：SMoE 以 13B 激活参数超越 Llama 2 70B，首个开源实用级 MoE LLM
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

## Entities
- [[bouc-wen-model]] — Bouc-Wen 率相关滞回模型
- [[peer-strong-motion-database]] — PEER 强震数据库
- [[phylstm2]] — PhyLSTM2 双 LSTM 架构
- [[phylstm3]] — PhyLSTM3 三 LSTM 架构
- [[pseudo-time-stepping]] — 伪时间步进方法：自适应步长原理 + 与 PhyLSTM 权重调参的关联

## Comparisons
- [[phylstm2-vs-phylstm3-vs-lstm]] — PhyLSTM2/3/LSTM 性能对比 + 选型指南
- [[physics-constrained-training-failure-modes]] — 物理约束训练失败模式：PhyLSTM vs PINN 对比分析

## Queries