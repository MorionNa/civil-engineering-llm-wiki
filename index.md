# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Last updated: 2026-06-11 | Total pages: 30

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
- [[concepts/ai4s/diffusion-models-ai4s-lecture2]] — AI4S第二讲：扩散生成模型从物理原理到蛋白质设计（章敏/浙大，90min）
- [[agentic-engineering-22-tips]] — Matt Van Horn (2026.06) Agentic Engineering 22 条技巧：plan→build loop / 上下文为王 / 语音输入 / 多 agent 并行 / skill 自动化
- [[wang2023-pinn-spurious-analysis]] — Wang et al. (2023) PINN 伪解问题概述：PDE 残差 loss 的缺陷 + 伪时间步进方案
- [[wang2023-pinn-spurious-method]] — 伪时间步进 + 自适应步长方法展开
- [[wang2023-pinn-spurious-results]] — Helmholtz/Klein-Gordon/Navier-Stokes/Rayleigh-Taylor 实验结果
- [[wang2023-pinn-spurious-critical]] — 贡献 + 知识点 + Negative + 可迁移 + 研究机会
- [[zhang2020-phylstm-analysis]] — Zhang et al. (2020) PhyLSTM 概述：12 维度论文分析总览
- [[zhang2020-phylstm-method]] — PhyLSTM2/3 方法机制展开：架构数据流图、损失函数详解、训练策略
- [[zhang2020-phylstm-results]] — 两个验证案例结果展开：MRF 和 Bouc-Wen
- [[zhang2020-phylstm-critical]] — 贡献 + 知识点 + Negative + 可迁移 + 研究机会。**含 PINN 失败模式关联**

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