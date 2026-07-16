# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Last updated: 2026-07-16 | Total pages: 241 (Papers: 173, Notes: 5, Entities: 57, Comparisons: 4)

## Papers
- [[meng2026-seisgpt-analysis]] — Meng et al. (2026) SeisGPT：物理信息结构响应基础模型，270,694 建筑、205 万 NLTHA、约 40,000× 加速，Nature Communications
- [[meng2026-seisgpt-method]] — SeisGPT 方法：SDR 低保真先验 + 质量刚度图编码 + Spectral Duhamel–Green Mixer
- [[meng2026-seisgpt-results]] — SeisGPT 结果：未见建筑、真实微调、跨体系零样本、稀疏传感器、IDA 与振动台验证
- [[meng2026-seisgpt-critical]] — SeisGPT 贡献+Negative（FE 标签依赖/楼层域/无失稳后倒塌/无不确定度）+研究机会
- [[lee2026-skyfall-gs-analysis]] — Lee et al. (2026) Skyfall-GS：卫星 3DGS 重建 + 扩散 IDU，生成可自由飞行的沉浸式 3D 城市，ECCV 2026
- [[lee2026-skyfall-gs-method]] — Skyfall-GS 方法：多时相外观建模、opacity 正则、MoGe 伪深度、课程式 FlowEdit IDU
- [[lee2026-skyfall-gs-results]] — Skyfall-GS 结果：DFC FIDCLIP 27.03，NYC 10.29；用户偏好 79–94%；1km 多块扩展
- [[lee2026-skyfall-gs-critical]] — Skyfall-GS 贡献+Negative（off-nadir/扩散幻觉/逐场景成本）+可迁移+研究机会
- [[wu2025-cm-pinn-analysis]] — Wu et al. (2025) CM-PINNs：本构模型约束 PINN 预测非线性结构地震响应，CMAME
- [[wu2025-cm-pinn-method]] — CM-PINNs 方法：FC-SLSTM + CDM + NLCM/BLCM + 六项物理/数据损失
- [[wu2025-cm-pinn-results]] — CM-PINNs 结果：SDOF 2% CI 达 99.01%，5/7-DOF 平均 R≈0.998
- [[wu2025-cm-pinn-critical]] — 贡献+Negative（双线性/低维/合成数据限制）+本构 PINN 研究机会
- [[chen2025-at-pinn-hc-analysis]] — Chen et al. (2025) AT-PINN-HC：三硬约束策略 + 五辅助函数，振动 PINN 误差降 1-4 数量级，CMAME
- [[chen2025-at-pinn-hc-method]] — AT-PINN-HC 方法：边界位移/初始位移/初始速度 HC + 三角函数/指数函数最优
- [[chen2025-at-pinn-hc-results]] — AT-PINN-HC 结果：Euler-Bernoulli 梁/超音速面板/玻璃板三基准，迭代减少 78%
- [[chen2025-at-pinn-hc-critical]] — AT-PINN-HC 贡献+Negative（逐案例选择/自动机制缺乏）+可迁移+8 项研究机会
- [[li2025-movingload-pinn-analysis]] — Li et al. (2025) PINN 求解桥梁移动荷载动力响应：FEM-free 替代方案，因果权重+傅里叶嵌入，AEI
- [[li2025-movingload-pinn-method]] — 移动荷载 PINN 方法：无量纲 PDE + 高斯 Dirac 近似 + 两阶段 Adam→L-BFGS
- [[li2025-movingload-pinn-results]] — 移动荷载 PINN 结果：5 案例 vs FEM + 消融研究（傅里叶嵌入/因果权重/数据敏感性）
- [[li2025-movingload-pinn-critical]] — 贡献+Negative（无量纲假设限制/频域未扩展）+可迁移+8 项研究机会
- [[li2025-girder-dynamic-pinn-analysis]] — Li et al. (2025) 斜拉桥主梁动力线形 PINN 反演：双代理网络 + 时空因果权重，AEI
- [[li2025-girder-dynamic-pinn-method]] — 斜拉桥 PINN 方法：连续弹性支撑简化 + Net_u/Net_f 双网络 + 差异化损失
- [[li2025-girder-dynamic-pinn-results]] — 斜拉桥 PINN 结果：传感器/路面/损伤/噪声四维度敏感性验证
- [[li2025-girder-dynamic-pinn-critical]] — 贡献+Negative（二维简化/恒定刚度）+可迁移+与 li2025-movingload-pinn 对照
- [[goswami2022-variational-deeponet-analysis]] — Goswami et al. (2022) V-DeepONet：变分能量约束 DeepONet 预测准脆性材料裂纹路径，CMAME
- [[goswami2022-variational-deeponet-method]] — V-DeepONet 方法：branch-trunk 架构 + 相位场能量泛函 + 混合训练策略
- [[goswami2022-variational-deeponet-results]] — V-DeepONet 结果：单边缺口拉伸/L 形面板，内插外推均优，毫秒级推理
- [[goswami2022-variational-deeponet-critical]] — 贡献+Negative（准静态假设/2D 限制/ℓc 敏感）+可迁移+9 项研究机会
- [[xiong2025-confseq-analysis]] — Xiong et al. (2025) ConfSeq：内坐标 token 化 + 标准 Transformer = 3D 分子 SOTA；500× 加速于扩散模型
- [[xiong2025-confseq-method]] — ConfSeq 方法：二面角/键角/伪手性 token + 四大任务统一 Transformer 架构
- [[xiong2025-confseq-results]] — ConfSeq 结果：构象预测 COV-P +10.5pp，生成 500× 加速，DUDE AUC 0.76
- [[xiong2025-confseq-critical]] — ConfSeq 贡献+Negative+可迁移（内坐标范式→蛋白质/材料）+ 8 项研究机会
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
- [[raissi2019-pinn-analysis]] — Raissi et al. (2019) 🏛️ PINN 开山之作：AD 统一处理非线性 PDE，JCP 16,874c
- [[raissi2019-pinn-method]] — PINN 方法：连续/离散时间模型 + AD 免线性化处理非线性项（$uu_x$, $u^3$, $\|h\|^2h$）
- [[raissi2019-pinn-results]] — 五类非线性 PDE (Burgers/Schrödinger/Allen-Cahn/N-S/KdV) 统一验证
- [[raissi2019-pinn-critical]] — 贡献+Negative（软约束违背/激波误差/非线性刚度）+可迁移+7 研究机会
- [[wang2024-causal-pinn-analysis]] — Wang et al. (2024) 因果性 PINN：重构损失函数尊重时间因果，解 Sifan Wang 三部曲终章，CMAME
- [[wang2024-causal-pinn-method]] — 因果权重公式 $w_i=\exp(-\epsilon\sum_{k<i}\mathcal{L}_k)$ + 时间前沿推进算法
- [[wang2024-causal-pinn-results]] — Lorenz/KS/N-S 三基准验证，因果权重提供诊断能力
- [[wang2024-causal-pinn-critical]] — 贡献+Negative+可迁移：NTK退火+伪时间步进+因果训练=三重保护
- [[zhao2026-causal-attention-analysis]] — Zhao et al. (2026) Causal Attention：自适应初始条件误差驱动的因果权重，采样解耦+免退火，JCP
- [[zhao2026-causal-attention-method]] — CA 方法：λ(t,x)=exp(-ϵξt) 权重 + mMLP + Fourier 特征 + 重采样集成
- [[zhao2026-causal-attention-results]] — CA 结果：Allen-Cahn/KdV/KS/Burgers 六 benchmark SOTA，3D 不陷入维度灾难
- [[zhao2026-causal-attention-critical]] — CA 贡献+Negative（Burgers 次优/IC-BC不兼容/tanh 梯度消失）+ 8 项研究机会
- [[wang2024-kinn-analysis]] — Wang et al. (2024) KINN：KAN 替代 MLP 做 PINN 骨干，B 样条激活，CMAME
- [[wang2024-kinn-method]] — KINN 方法：B 样条 KAN + 三种 PDE 形式（强/能量/逆问题）
- [[wang2024-kinn-results]] — 六类固体力学问题 5/6 优于 MLP-PINN（复杂几何除外）
- [[wang2024-kinn-critical]] — 贡献+Negative（张量积网格限制/训练慢/NTK缺失）+7 研究机会
- [[sojitra2026-fedonet-analysis]] — Sojitra et al. (2026) FEDONet：Fourier 嵌入 DeepONet 实现谱精度算子学习，JCP
- [[sojitra2026-fedonet-method]] — FEDONet 方法：随机 Fourier 特征嵌入 trunk + branch → 自适应 Fourier 级数
- [[sojitra2026-fedonet-results]] — 5 PDE (Burgers/Poisson/Eikonal/Allen-Cahn/KS) 混沌刚性系统获益最大
- [[sojitra2026-fedonet-critical]] — 贡献+Negative+可迁移：Fourier-V-DeepONet 潜在方向
- [[jagtap2019-adaptive-activation-analysis]] — Jagtap et al. (2019) 自适应激活函数加速 PINN：全局/局部可训练斜率 + 恢复项，JCP
- [[jagtap2019-adaptive-activation-method]] — 自适应激活方法：全局 σ(nax) vs 局部 σ(na_ix) + 斜率恢复项防退化
- [[jagtap2019-adaptive-activation-results]] — MNIST/CIFAR/Burgers/Allen-Cahn/Helmholtz 五基准，局部模式加速 5×
- [[jagtap2019-adaptive-activation-critical]] — 贡献+Negative（仅 tanh/无理论保证）+可迁移+5 研究机会
- [[wang2021-pinn-ntk-failure-analysis]] — Wang et al. (2021) PINN 训练失败 NTK 分析：谱偏差 + 特征值自适应退火，JCP
- [[wang2021-pinn-ntk-failure-method]] — PINN NTK 推导：多损失分块 NTK + 收敛速率证明 + 自适应学习率算法
- [[wang2021-pinn-ntk-failure-results]] — 4 PDE 验证（Poisson/波动/Burgers/Allen-Cahn），NTK 退火 L² 误差降 4 数量级
- [[wang2021-pinn-ntk-failure-critical]] — 贡献+Negative（无限宽度假设/有限网络偏离）+可迁移+8 项研究机会
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

- [[amapcvlab2026-abotearth-analysis]] — AMAP CV Lab (2026) ABot-Earth 0.5：生成式 3D 地球模型，卫星图像→3DGS 城市场景 <10min/km²，覆盖 190+ 国家
- [[amapcvlab2026-abotearth-method]] — ABot-Earth 方法：compression-generation + 卫星条件 + 原生多 LOD 解码 + EarthScape 生产管线
- [[amapcvlab2026-abotearth-results]] — ABot-Earth 结果：FID 16.1 vs baselines，vs Google Earth 全球覆盖率+视觉质量对比
- [[amapcvlab2026-abotearth-critical]] — ABot-Earth 贡献+Negative（仅航拍/全闭源/非公平 FID）+可迁移（"重建→生成"范式/Bhattacharyya 裁剪）+7 项研究机会

- [[linka2022-bayesian-pinn-analysis]] — Linka et al. (2022) BPINN 概述：贝叶斯推理+PINN，6模型对比COVID-19动力系统
- [[linka2022-bayesian-pinn-method]] — BPINN 方法：阻尼谐振子物理 + HMC采样，6模型架构对比
- [[linka2022-bayesian-pinn-results]] — BPINN 结果：NN/PINN/SAPINN vs BI/BNN/BPINN 完整对比矩阵+决策树
- [[linka2022-bayesian-pinn-critical]] — BPINN 贡献+Negative（HMC极贵/小数据差）+可迁移（物理→似然范式）+12项研究机会

## Entities
### 物理信息机器学习
- [[seisgpt]] — SeisGPT: 质量–刚度图 + SDG-Mixer 的多建筑结构响应基础模型
- [[bayesian-pinn]] — Bayesian PINN: PINN + 贝叶斯推理，物理残差 = 似然因子，HMC 采样
- [[hamiltonian-monte-carlo]] — HMC: 哈密顿蒙特卡洛采样，BPINN 核心推理引擎
- [[pinn]] — Physics-Informed Neural Network: 物理约束神经网络，PDE 正逆问题求解范式
- [[cm-pinns]] — CM-PINNs: 本构模型约束 PINN，显式约束非线性恢复力预测地震响应
- [[neural-tangent-kernel]] — NTK: 神经正切核，解释 PINN 训练失败的理论工具
- [[causal-training]] — 因果训练: 尊重物理时间因果的损失加权策略
- [[causal-attention]] — Causal Attention (CA): 初始条件误差驱动的因果权重，采样解耦+免退火
- [[kin]] — KINN/KAN: 可学习 B 样条激活替代 MLP，Kolmogorov-Arnold 定理
- [[fedonet]] — FEDONet: Fourier 嵌入 DeepONet，谱精度算子学习
- [[deeponet]] — DeepONet: 深度算子网络，学习无限维映射的通用神经算子
- [[cable-stayed-bridge]] — 斜拉桥: 索支撑桥型，主梁动力线形 (MGDA) 健康监测

### 远程感知与生成式3D
- [[skyfall-gs]] — Skyfall-GS: 多视角卫星重建 + 课程式扩散 IDU 的可自由飞行 3D 城市
- [[abot-earth]] — ABot-Earth: 阿里高德生成式 3D 地球模型，卫星→3DGS
- [[abot-3dgs]] — ABot-3DGS: 城市级 3DGS 重建引擎
- [[3d-gaussian-splatting]] — 3D Gaussian Splatting: 实时可微渲染的场景表示
- [[from-orbit-to-ground]] — FromOrbit2Ground: 卫星图像→3DGS 转换模块
- [[clod-gs]] — CLOD-GS: 连续 LOD 3DGS 方法

### 大语言模型
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
- [[at-pinn-hc]] — AT-PINN-HC: 硬约束增强时间推进 PINN，结构振动分析
- [[confseq]] — ConfSeq: 分子构象描述语言，内坐标 token 化 + 标准 Transformer
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
- [[seisgpt-vs-phylstm-cm-pinns]] — SeisGPT vs PhyLSTM vs CM-PINNs：大规模基础模型、物理序列模型与本构约束路线对比
- [[skyfall-gs-vs-abot-earth]] — Skyfall-GS vs ABot-Earth：逐场景观测精修路线 vs 行星级前向生成路线
- [[phylstm2-vs-phylstm3-vs-lstm]] — PhyLSTM2/3/LSTM 性能对比 + 选型指南
- [[physics-constrained-training-failure-modes]] — 物理约束训练失败模式：PhyLSTM vs PINN 对比分析

## Queries