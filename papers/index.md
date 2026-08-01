---
id: papers-index
title: Papers Index
type: index
status: active
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-07-16'
updated: '2026-08-01'
confidence: high
---

# Papers Index

> 全文论文采用 `analysis + method + results + critical` 的 1+3 结构。此页是论文分区目录；具体页面也可通过站内搜索和交叉 wikilink 到达。

## 等变图神经网络与大规模物理图学习

### NequIP

- [[batzner2022-nequip-analysis]] — Batzner et al. (2022)：E(3) 等变张量消息传递提高原子势精度与数据效率，Nature Communications。
- [[batzner2022-nequip-method]] — O(3) 不可约表示、球谐、径向网络和 Clebsch–Gordan 张量积。
- [[batzner2022-nequip-results]] — MD-17、水/冰、反应界面、玻璃态和离子输运结果。
- [[batzner2022-nequip-critical]] — 长程作用、解释性、并行感受野和结构动力迁移。

### Allegro

- [[musaelian2023-allegro-analysis]] — Musaelian et al. (2023)：严格局部 pair-centered 等变原子势，Nature Communications。
- [[musaelian2023-allegro-method]] — 双潜空间、学习环境嵌入、density trick 与迭代张量积。
- [[musaelian2023-allegro-results]] — revised MD-17、3BPA、QM9、Li$_3$PO$_4$ 和亿原子扩展。
- [[musaelian2023-allegro-critical]] — 局部性、长程项、pair 显存和结构图迁移。

### SevenNet

- [[park2024-sevennet-parallel-gnn-ip-analysis]] — Park et al. (2024)：NequIP 类 GNN 原子势空间分解并行。
- [[park2024-sevennet-parallel-gnn-ip-method]] — ghost atoms、逐层正向特征和反向梯度通信。
- [[park2024-sevennet-parallel-gnn-ip-results]] — 32 GPU 弱扩展、SevenNet-0 和十万级非晶体系。
- [[park2024-sevennet-parallel-gnn-ip-critical]] — 通信开销、GPU 利用率、负载均衡和子结构迁移。

## 组合式神经算子与训练动力学

- [[zhang2026-legonet-analysis]] — LegONet：边界适配谱基、结构保持块与算子组合。
- [[li2025-functional-scaling-laws-analysis]] — Functional Scaling Laws：学习率计划下完整 loss trajectory。
- [[zeraatkar2026-pgt-analysis]] — PGT：Green 函数物理偏置进入 attention。
- [[li2025-node-onet-analysis]] — NODE-ONet：物理编码 Neural ODE 算子网络。
- [[li2026-sgno-analysis]] — SGNO：谱生成神经算子和长时稳定性。
- [[mandl2025-separable-pi-deeponet-analysis]] — Sep-PI-DeepONet：可分离 trunk 与高维物理残差计算。

## PINN 与自动优化

- [[wang2024-nas-pinn-analysis]] — NAS-PINN：自动设计 PINN 网络结构。
- [[kolzhetsov2026-rl-adaptive-loss-control-analysis]] — 强化学习动态调节 PINN 损失权重。
- [[rathore2024-pinn-loss-landscape-analysis]] — PINN loss landscape、Hessian 谱与二阶优化。
- [[penwarden2024-kolmogorov-n-width-piml-analysis]] — 多任务 PIML 的最坏情形泛化度量。
- [[gao2025-adaptive-loss-pinn-analysis]] — APINNs：有界自适应损失权重。

## 结构动力响应

- [[meng2026-seisgpt-analysis]] — SeisGPT。
- [[wu2025-cm-pinn-analysis]] — CM-PINNs。
- [[zhang2020-phylstm-analysis]] — PhyLSTM2/3。
- [[du2026-hcff-pinn-analysis]] — HCFF-PINN。
- [[liu2025-site-response-pinn-analysis]] — 地震场地反应 PINN。

## 计算力学与倒塌

- [[giles2025-avbd-analysis]] — AVBD。
- [[lu2013-collapse-rc-highrise-analysis]] — RC 高层倒塌模拟。
- [[goswami2022-variational-deeponet-analysis]] — V-DeepONet 相位场裂纹算子学习。

## 计算机视觉与建筑图纸

- [[ronneberger2015-unet-analysis]] — U-Net。
- [[zhao2017-pspnet-analysis]] — PSPNet。
- [[chen2018-deeplabv3plus-analysis]] — DeepLabv3+。
- [[sun2019-hrnetv2-analysis]] — HRNetV2。
- [[xie2021-segformer-analysis]] — SegFormer。

## 生成式三维与遥感

- [[lee2026-skyfall-gs-analysis]] — Skyfall-GS。
- [[amapcvlab2026-abotearth-analysis]] — ABot-Earth。

## 大语言模型与架构搜索

- [[fedus2021-switch-transformer-analysis]] — Switch Transformer。
- [[lepikhin2021-gshard-analysis]] — GShard。
- [[jiang2024-mixtral-of-experts-analysis]] — Mixtral。
- [[dai2024-deepseek-moe-analysis]] — DeepSeekMoE。
- [[chen2021-tenas-analysis]] — TE-NAS。
- [[chen2021-autoformer-analysis]] — AutoFormer。

<!-- AUTO-REGISTRY:START -->

## Complete Registry

- [[papers/akhauri2022-eznas-analysis]] — Akhauri et al. (2022) — EZNAS: Evolving Zero Cost Proxies For NAS Scoring 论文分析
- [[papers/akhauri2022-eznas-critical]] — EZNAS 批判性分析 — 贡献、局限、可迁移与未来方向
- [[papers/akhauri2022-eznas-method]] — EZNAS 方法机制 — 遗传编程驱动零成本 NAS 代理自动发现
- [[papers/akhauri2022-eznas-results]] — EZNAS 结果证据 — 跨搜索空间评分-精度相关性
- [[papers/amapcvlab2026-abotearth-analysis]] — AMAP CV Lab (2026) — ABot-Earth 0.5: Generative 3D Earth Model 论文分析
- [[papers/amapcvlab2026-abotearth-critical]] — ABot-Earth 0.5 — 贡献+Negative+可迁移+研究机会
- [[papers/amapcvlab2026-abotearth-method]] — ABot-Earth 0.5 — 方法机制展开
- [[papers/amapcvlab2026-abotearth-results]] — ABot-Earth 0.5 — 实验结果与证据
- [[papers/batzner2022-nequip-analysis]] — Batzner et al. (2022) — NequIP：E(3) 等变图神经网络原子势
- [[papers/batzner2022-nequip-critical]] — Batzner et al. (2022) — NequIP 批判、迁移与研究机会
- [[papers/batzner2022-nequip-method]] — Batzner et al. (2022) — NequIP 方法机制
- [[papers/batzner2022-nequip-results]] — Batzner et al. (2022) — NequIP 结果证据
- [[papers/chen2018-deeplabv3plus-analysis]] — Chen et al. (2018) — DeepLabv3+: Encoder-Decoder with Atrous Separable Convolution: 论文分析
- [[papers/chen2018-deeplabv3plus-critical]] — DeepLabv3+ 贡献·Negative·可迁移·研究机会
- [[papers/chen2018-deeplabv3plus-method]] — DeepLabv3+ 方法机制展开
- [[papers/chen2018-deeplabv3plus-results]] — DeepLabv3+ 实验结果展开
- [[papers/chen2021-autoformer-analysis]] — Chen et al. (2021) — AutoFormer: 视觉 Transformer 架构搜索: 论文分析
- [[papers/chen2021-autoformer-critical]] — AutoFormer 贡献·局限·可迁移·研究机会
- [[papers/chen2021-autoformer-method]] — AutoFormer 方法机制：Weight Entanglement + 弹性搜索空间
- [[papers/chen2021-autoformer-results]] — AutoFormer 实验结果：ImageNet / 迁移学习 / 蒸馏
- [[papers/chen2021-tenas-analysis]] — Chen et al. (2021) — TE-NAS: Training-Free NAS via NTK: 论文分析
- [[papers/chen2021-tenas-critical]] — TE-NAS 贡献·局限·可迁移·研究机会
- [[papers/chen2021-tenas-method]] — TE-NAS 方法机制：NTK 条件数 + 线性区域 + Pruning 搜索
- [[papers/chen2021-tenas-results]] — TE-NAS 实验结果：NAS-Bench-201 / DARTS / ImageNet
- [[papers/chen2025-at-pinn-hc-analysis]] — Chen et al. (2025) — AT-PINN-HC：硬约束策略增强的时间推进 PINN 结构振动分析
- [[papers/chen2025-at-pinn-hc-critical]] — Chen et al. (2025) — 贡献 / 知识点 / Negative / 可迁移 / 研究机会
- [[papers/chen2025-at-pinn-hc-method]] — Chen et al. (2025) — AT-PINN-HC 方法机制展开
- [[papers/chen2025-at-pinn-hc-results]] — Chen et al. (2025) — AT-PINN-HC 实验结果展开
- [[papers/chittyvenkata2022-nas-transformers-survey]] — Chitty-Venkata et al. (2022) — NAS for Transformers Survey: 论文分析
- [[papers/dai2024-deepseek-moe-analysis]] — Dai et al. (2024) — DeepSeekMoE: 论文分析
- [[papers/dai2024-deepseek-moe-critical]] — Dai et al. (2024) — DeepSeekMoE 贡献+Negative+可迁移+机会
- [[papers/dai2024-deepseek-moe-method]] — Dai et al. (2024) — DeepSeekMoE 方法展开
- [[papers/dai2024-deepseek-moe-results]] — Dai et al. (2024) — DeepSeekMoE 实验结果
- [[papers/du2026-hcff-pinn-analysis]] — Du et al. (2026) — HCFF-PINN：频率先验 Fourier 特征与初值硬约束的无标签结构动力求解
- [[papers/du2026-hcff-pinn-critical]] — Du et al. (2026) — HCFF-PINN 贡献、局限与研究机会
- [[papers/du2026-hcff-pinn-method]] — Du et al. (2026) — HCFF-PINN 方法机制展开
- [[papers/du2026-hcff-pinn-results]] — Du et al. (2026) — HCFF-PINN 数值结果与证据核查
- [[papers/fedus2021-switch-transformer-analysis]] — Fedus et al. (2021) — Switch Transformers: 论文分析
- [[papers/fedus2021-switch-transformer-critical]] — Fedus et al. (2021) — 贡献 / 知识点 / Negative / 可迁移 / 研究机会
- [[papers/fedus2021-switch-transformer-method]] — Fedus et al. (2021) — 方法机制展开
- [[papers/fedus2021-switch-transformer-results]] — Fedus et al. (2021) — 结果证据展开
- [[papers/gao2025-adaptive-loss-pinn-analysis]] — Gao et al. (2025) — APINNs：多任务自适应损失加权求解非线性 PDE
- [[papers/gao2025-adaptive-loss-pinn-critical]] — Gao et al. (2025) — APINNs 贡献、局限与研究机会
- [[papers/gao2025-adaptive-loss-pinn-method]] — Gao et al. (2025) — APINNs 方法机制展开
- [[papers/gao2025-adaptive-loss-pinn-results]] — Gao et al. (2025) — APINNs 数值结果与证据核查
- [[papers/giles2025-avbd-analysis]] — Giles et al. (2025) — Augmented Vertex Block Descent (AVBD): 论文分析
- [[papers/giles2025-avbd-critical]] — AVBD 贡献·局限·可迁移·机会
- [[papers/giles2025-avbd-method]] — AVBD 方法机制展开
- [[papers/giles2025-avbd-results]] — AVBD 实验结果展开
- [[papers/goswami2022-variational-deeponet-analysis]] — Goswami et al. (2022) — A Physics-Informed Variational DeepONet for Crack Path Prediction: 论文分析
- [[papers/goswami2022-variational-deeponet-critical]] — Goswami et al. (2022) — 贡献 / 知识点 / Negative / 可迁移 / 研究机会
- [[papers/goswami2022-variational-deeponet-method]] — Goswami et al. (2022) — 方法机制展开
- [[papers/goswami2022-variational-deeponet-results]] — Goswami et al. (2022) — 结果证据展开
- [[papers/guo2026-phy-rlk-analysis]] — Guo & Xu (2026) Phy-RLK：双向地震作用下非线性结构响应的物理残差 LSTM-KAN
- [[papers/guo2026-phy-rlk-critical]] — Guo & Xu (2026) Phy-RLK 批判：物理偏置、合成标签与泛化边界
- [[papers/guo2026-phy-rlk-method]] — Guo & Xu (2026) Phy-RLK 方法：Newmark-β 残差门控与 KAN 解码
- [[papers/guo2026-phy-rlk-results]] — Guo & Xu (2026) Phy-RLK 结果：双向 RC 框架响应与峰值误差
- [[papers/jagtap2019-adaptive-activation-analysis]] — Jagtap et al. (2019) 自适应激活函数加速 PINN 收敛
- [[papers/jagtap2019-adaptive-activation-critical]] — Jagtap et al. (2019) 自适应激活函数 — 贡献·Negative·可迁移
- [[papers/jagtap2019-adaptive-activation-method]] — Jagtap et al. (2019) 自适应激活函数 — 方法展开
- [[papers/jagtap2019-adaptive-activation-results]] — Jagtap et al. (2019) 自适应激活函数 — 结果展开
- [[papers/jiang2024-mixtral-of-experts-analysis]] — Jiang et al. (2024) — Mixtral of Experts: 论文分析
- [[papers/jiang2024-mixtral-of-experts-critical]] — Mixtral 8x7B 贡献·局限·可迁移·机会
- [[papers/jiang2024-mixtral-of-experts-method]] — Mixtral 8x7B 方法机制展开
- [[papers/jiang2024-mixtral-of-experts-results]] — Mixtral 8x7B 实验结果展开
- [[papers/kolzhetsov2026-rl-adaptive-loss-control-analysis]] — Kolzhetsov et al. (2026) — RL-Based Adaptive Loss Control：强化学习动态调节 PINN 损失权重
- [[papers/kolzhetsov2026-rl-adaptive-loss-control-critical]] — Kolzhetsov et al. (2026) — RL Adaptive Loss Control 批判与迁移
- [[papers/kolzhetsov2026-rl-adaptive-loss-control-method]] — Kolzhetsov et al. (2026) — RL Adaptive Loss Control 方法
- [[papers/kolzhetsov2026-rl-adaptive-loss-control-results]] — Kolzhetsov et al. (2026) — RL Adaptive Loss Control 结果
- [[papers/lahoti2026-mamba3-analysis]] — Lahoti et al. (2026) — Mamba-3：基于状态空间原理的高效序列建模
- [[papers/lahoti2026-mamba3-critical]] — Mamba-3 批判与研究机会
- [[papers/lahoti2026-mamba3-method]] — Mamba-3 方法：状态空间原理驱动的三项改进
- [[papers/lahoti2026-mamba3-results]] — Mamba-3 结果
- [[papers/lee2024-aznas-analysis]] — Lee & Ham (2024) — AZ-NAS: Assembling Zero-Cost Proxies for NAS 论文分析
- [[papers/lee2024-aznas-critical]] — Lee & Ham (2024) — AZ-NAS: 贡献 / 失败知识 / 可迁移知识 / 研究机会
- [[papers/lee2024-aznas-method]] — Lee & Ham (2024) — AZ-NAS: 方法机制详解
- [[papers/lee2024-aznas-results]] — Lee & Ham (2024) — AZ-NAS: 结果证据详解
- [[papers/lee2026-skyfall-gs-analysis]] — Lee et al. (2026) — Skyfall-GS：从卫星影像合成可自由飞行的沉浸式 3D 城市
- [[papers/lee2026-skyfall-gs-critical]] — Skyfall-GS 批判性分析：贡献、幻觉边界、可迁移机制与研究机会
- [[papers/lee2026-skyfall-gs-method]] — Skyfall-GS 方法：卫星 3DGS 重建 + 课程式扩散 IDU
- [[papers/lee2026-skyfall-gs-results]] — Skyfall-GS 结果：感知质量、几何消融、用户研究与多块扩展
- [[papers/lepikhin2021-gshard-analysis]] — Lepikhin et al. (2020) — GShard: 论文分析
- [[papers/lepikhin2021-gshard-critical]] — Lepikhin et al. (2020) — 贡献 / 知识点 / Negative / 可迁移 / 研究机会
- [[papers/lepikhin2021-gshard-method]] — Lepikhin et al. (2020) — 方法机制展开
- [[papers/lepikhin2021-gshard-results]] — Lepikhin et al. (2020) — 结果证据展开
- [[papers/li2021-bossnas-analysis]] — Li et al. (2021) — BossNAS: Block-wisely Self-supervised NAS for Hybrid CNN-Transformers 论文分析
- [[papers/li2021-bossnas-critical]] — BossNAS 批判性分析：贡献、局限与可迁移洞见
- [[papers/li2021-bossnas-method]] — BossNAS 方法细节：Ensemble Bootstrapping 与 HyTra 搜索空间
- [[papers/li2021-bossnas-results]] — BossNAS 实验结果：ImageNet / CIFAR / 迁移学习
- [[papers/li2025-functional-scaling-laws-analysis]] — Li et al. (2025) — Functional Scaling Laws：学习率计划下完整损失轨迹的函数型缩放律
- [[papers/li2025-functional-scaling-laws-critical]] — Functional Scaling Laws 批判分析：贡献、限制与迁移机会
- [[papers/li2025-functional-scaling-laws-method]] — Functional Scaling Laws 方法：内禀时间、SDE 与遗忘核卷积
- [[papers/li2025-functional-scaling-laws-results]] — Functional Scaling Laws 结果：WSD 优势与 LLM loss 轨迹预测
- [[papers/li2025-girder-dynamic-pinn-analysis]] — Li et al. (2025) — 基于PINN的斜拉桥主梁动态线形重建：论文分析
- [[papers/li2025-girder-dynamic-pinn-critical]] — Li et al. (2025) — 贡献 / Negative / 可迁移 / 研究机会
- [[papers/li2025-girder-dynamic-pinn-method]] — Li et al. (2025) — 方法机制：双代理模型PINN斜拉桥动态线形重建
- [[papers/li2025-girder-dynamic-pinn-results]] — Li et al. (2025) — 实验结果：传感器稀疏条件下的MGDA重建验证
- [[papers/li2025-localized-waves-pinn-analysis]] — Li & Wang (2025) — Bäcklund 变换约束 PINN 生成非线性 PDE 局域波：论文分析
- [[papers/li2025-localized-waves-pinn-critical]] — Li & Wang (2025) — Bäcklund-PINN 的贡献、局限与研究机会
- [[papers/li2025-localized-waves-pinn-method]] — Li & Wang (2025) — Bäcklund 变换约束双输出 PINN：方法机制
- [[papers/li2025-localized-waves-pinn-results]] — Li & Wang (2025) — 局域波实验：数值结果与证据
- [[papers/li2025-movingload-pinn-analysis]] — Li et al. (2025) — 基于物理信息神经网络的桥梁移动荷载动力响应分析：论文分析
- [[papers/li2025-movingload-pinn-critical]] — Li et al. (2025) — 贡献 / Negative / 可迁移 / 研究机会
- [[papers/li2025-movingload-pinn-method]] — Li et al. (2025) — 方法机制：PINN 桥梁移动荷载动力响应分析
- [[papers/li2025-movingload-pinn-results]] — Li et al. (2025) — 实验结果：五组数值实验验证
- [[papers/li2025-node-onet-analysis]] — Deep Neural ODE Operator Networks for PDEs (NODE-ONet)：物理编码神经常微分方程算子网络
- [[papers/li2025-node-onet-critical]] — NODE-ONet 批判分析
- [[papers/li2025-node-onet-method]] — NODE-ONet 方法机制
- [[papers/li2025-node-onet-results]] — NODE-ONet 结果与证据
- [[papers/li2026-exsgd-analysis]] — Li et al. (2026) — ExSGD：利用历史梯度的分布式大批量建筑提取训练优化
- [[papers/li2026-exsgd-critical]] — ExSGD 贡献与批判
- [[papers/li2026-exsgd-method]] — ExSGD 方法机制
- [[papers/li2026-exsgd-results]] — ExSGD 实验结果
- [[papers/li2026-sgno-analysis]] — Li et al. (2026) — SGNO：稳定长时域 PDE 滚动预测的谱生成神经算子
- [[papers/li2026-sgno-critical]] — SGNO 批判分析
- [[papers/li2026-sgno-method]] — SGNO 方法机制
- [[papers/li2026-sgno-results]] — SGNO 结果与证据
- [[papers/linka2022-bayesian-pinn-analysis]] — Linka et al. (2022) — Bayesian PINNs for Nonlinear Dynamical Systems: 论文分析
- [[papers/linka2022-bayesian-pinn-critical]] — Linka et al. (2022) — Bayesian PINNs: 贡献/知识/Negative/可迁移/机会
- [[papers/linka2022-bayesian-pinn-method]] — Linka et al. (2022) — Bayesian PINNs: 方法机制展开
- [[papers/linka2022-bayesian-pinn-results]] — Linka et al. (2022) — Bayesian PINNs: 结果证据展开
- [[papers/liu2025-site-response-pinn-analysis]] — Liu et al. (2025) — PINN 用于一维地震场地反应分析：论文分析
- [[papers/liu2025-site-response-pinn-critical]] — Liu et al. (2025) — 场地反应 PINN：贡献、局限与研究机会
- [[papers/liu2025-site-response-pinn-method]] — Liu et al. (2025) — 地震场地反应 PINN：方法机制
- [[papers/liu2025-site-response-pinn-results]] — Liu et al. (2025) — 场地反应 PINN：结果与定量证据
- [[papers/lu2013-collapse-rc-highrise-analysis]] — Lu et al. (2013) — RC 高层建筑极端地震倒塌模拟: 论文分析
- [[papers/lu2013-collapse-rc-highrise-critical]] — Lu et al. (2013) 贡献·局限·可迁移·机会
- [[papers/lu2013-collapse-rc-highrise-method]] — Lu et al. (2013) 倒塌模拟方法展开
- [[papers/lu2013-collapse-rc-highrise-results]] — Lu et al. (2013) 倒塌模拟结果展开
- [[papers/luo2025-pinn-pde-review-analysis]] — Luo et al. (2025) PINN 求解 PDE 综合综述：分类框架与证据边界
- [[papers/luo2025-pinn-pde-review-critical]] — Luo et al. (2025) PINN-PDE 综述批判：覆盖边界、时效性与复现价值
- [[papers/luo2025-pinn-pde-review-method]] — Luo et al. (2025) PINN-PDE 综述方法：多轴分类框架
- [[papers/luo2025-pinn-pde-review-results]] — Luo et al. (2025) PINN-PDE 综述结果：分类、比较与证据层级
- [[papers/maimon2026-sparse-dense-analysis]] — Maimon et al. (2026) — Sparse-to-Dense Coding Transformation Between Hippocampal CA3 and CA1 论文分析
- [[papers/maimon2026-sparse-dense-critical]] — Maimon et al. (2026) — 贡献 / 失败知识 / 可迁移知识 / 研究机会
- [[papers/maimon2026-sparse-dense-method]] — Maimon et al. (2026) — 方法机制详解
- [[papers/maimon2026-sparse-dense-results]] — Maimon et al. (2026) — 实验结果证据详解
- [[papers/mandl2025-separable-pi-deeponet-analysis]] — Mandl et al. (2025) — Separable Physics-Informed DeepONet
- [[papers/mandl2025-separable-pi-deeponet-critical]] — Mandl et al. (2025) — Sep-PI-DeepONet critical analysis
- [[papers/mandl2025-separable-pi-deeponet-method]] — Sep-PI-DeepONet Method
- [[papers/mandl2025-separable-pi-deeponet-results]] — Sep-PI-DeepONet Results
- [[papers/meng2026-seisgpt-analysis]] — Meng et al. (2026) — SeisGPT：面向高保真结构响应预测的物理信息基础模型
- [[papers/meng2026-seisgpt-critical]] — SeisGPT 批判性分析：基础模型边界、FE 标签依赖与工程部署
- [[papers/meng2026-seisgpt-method]] — SeisGPT 方法：SDR 低保真先验、质量刚度图编码与 SDG-Mixer
- [[papers/meng2026-seisgpt-results]] — SeisGPT 结果：跨建筑预测、跨体系零样本、稀疏重建与 IDA
- [[papers/musaelian2023-allegro-analysis]] — Musaelian et al. (2023) — Allegro：严格局部等变原子势
- [[papers/musaelian2023-allegro-critical]] — Musaelian et al. (2023) — Allegro 批判、迁移与研究机会
- [[papers/musaelian2023-allegro-method]] — Musaelian et al. (2023) — Allegro 方法机制
- [[papers/musaelian2023-allegro-results]] — Musaelian et al. (2023) — Allegro 结果证据
- [[papers/park2024-sevennet-parallel-gnn-ip-analysis]] — Park et al. (2024) — SevenNet：可扩展并行图神经网络原子势
- [[papers/park2024-sevennet-parallel-gnn-ip-critical]] — Park et al. (2024) — SevenNet 批判、迁移与研究机会
- [[papers/park2024-sevennet-parallel-gnn-ip-method]] — Park et al. (2024) — SevenNet 并行方法
- [[papers/park2024-sevennet-parallel-gnn-ip-results]] — Park et al. (2024) — SevenNet 结果证据
- [[papers/penwarden2024-kolmogorov-n-width-piml-analysis]] — Penwarden et al. (2024) — Kolmogorov n-width：多任务 PIML 的最坏情形泛化度量
- [[papers/penwarden2024-kolmogorov-n-width-piml-critical]] — Penwarden et al. (2024) — Kolmogorov n-width PIML 批判分析
- [[papers/penwarden2024-kolmogorov-n-width-piml-method]] — Penwarden et al. (2024) — Kolmogorov n-width PIML 方法
- [[papers/penwarden2024-kolmogorov-n-width-piml-results]] — Penwarden et al. (2024) — Kolmogorov n-width PIML 实验结果
- [[papers/raissi2019-pinn-analysis]] — Raissi et al. (2019) PINN 开山之作：非线性 PDE 的深度学习求解框架
- [[papers/raissi2019-pinn-critical]] — Raissi et al. (2019) PINN — 贡献·Negative·可迁移·研究机会
- [[papers/raissi2019-pinn-method]] — Raissi et al. (2019) PINN 方法展开：连续/离散时间模型 + 非线性 PDE 的 AD 处理
- [[papers/raissi2019-pinn-results]] — Raissi et al. (2019) PINN 结果展开：五类非线性 PDE 的求解验证
- [[papers/rathore2024-pinn-loss-landscape-analysis]] — Rathore et al. (2024) — PINN 训练挑战：损失景观、病态性与二阶优化
- [[papers/rathore2024-pinn-loss-landscape-critical]] — PINN 损失景观论文批判分析
- [[papers/rathore2024-pinn-loss-landscape-method]] — PINN 损失景观与 NysNewton-CG 方法
- [[papers/rathore2024-pinn-loss-landscape-results]] — PINN 损失景观结果与证据
- [[papers/real2020-automl-zero-analysis]] — Real et al. (2020) — AutoML-Zero: 从零进化机器学习算法 论文分析
- [[papers/real2020-automl-zero-critical]] — Real et al. (2020) — 深度分析：贡献 / 知识点 / Negative Knowledge / 可迁移 / 研究机会
- [[papers/real2020-automl-zero-method]] — Real et al. (2020) — 方法详解：AutoML-Zero 的三组件搜索空间与进化引擎
- [[papers/real2020-automl-zero-results]] — Real et al. (2020) — 实验结果详解：进化发现的算法与技术涌现
- [[papers/ronneberger2015-unet-analysis]] — Ronneberger et al. (2015) — U-Net: 论文分析
- [[papers/ronneberger2015-unet-critical]] — U-Net 贡献·局限·可迁移·机会
- [[papers/ronneberger2015-unet-method]] — U-Net 方法机制展开
- [[papers/ronneberger2015-unet-results]] — U-Net 实验结果展开
- [[papers/ru2020-nago-analysis]] — Ru et al. (2020) — Neural Architecture Generator Optimization 论文分析
- [[papers/ru2020-nago-critical]] — Ru et al. (2020) — NAGO 贡献 · 局限 · 延伸
- [[papers/ru2020-nago-method]] — Ru et al. (2020) — NAGO 方法机制详解
- [[papers/ru2020-nago-results]] — Ru et al. (2020) — NAGO 实验结果详解
- [[papers/serianni2023-training-free-nas-rnn-transformers-analysis]] — Serianni & Kalita (2023) — Training-free NAS for RNNs and Transformers 论文分析
- [[papers/serianni2023-training-free-nas-rnn-transformers-critical]] — Serianni & Kalita (2023) — Critical Analysis: Training-free NAS for RNNs and Transformers
- [[papers/serianni2023-training-free-nas-rnn-transformers-method]] — Serianni & Kalita (2023) — Method: Training-free NAS Proxies for RNNs and Transformers
- [[papers/serianni2023-training-free-nas-rnn-transformers-results]] — Serianni & Kalita (2023) — Results: Training-free NAS for RNNs and Transformers
- [[papers/so2021-primer-analysis]] — So et al. (2021) — Primer: Searching for Efficient Transformers for Language Modeling 论文分析
- [[papers/so2021-primer-critical]] — So et al. (2021) — Primer 贡献·局限·可迁移·研究机会
- [[papers/so2021-primer-method]] — So et al. (2021) — Primer: 搜索空间、SQ-TC 搜索算法与训练策略
- [[papers/so2021-primer-results]] — So et al. (2021) — Primer: 关键实验与结果
- [[papers/sojitra2026-fedonet-analysis]] — Sojitra et al. (2026) — FEDONet: Fourier-Embedded DeepONet for Spectrally Accurate Operator Learning: 论文分析
- [[papers/sojitra2026-fedonet-critical]] — Sojitra et al. (2026) — 贡献 / 知识点 / Negative / 可迁移 / 研究机会
- [[papers/sojitra2026-fedonet-method]] — Sojitra et al. (2026) — 方法机制展开
- [[papers/sojitra2026-fedonet-results]] — Sojitra et al. (2026) — 结果证据展开
- [[papers/song2025-rl-pinns-analysis]] — Song (2025) — RL-PINNs：强化学习驱动的单轮自适应配点
- [[papers/song2025-rl-pinns-critical]] — RL-PINNs 批判分析
- [[papers/song2025-rl-pinns-method]] — RL-PINNs 方法机制
- [[papers/song2025-rl-pinns-results]] — RL-PINNs 结果与证据
- [[papers/sun2019-hrnetv2-analysis]] — Sun et al. (2019) — High-Resolution Representations for Labeling Pixels and Regions (HRNetV2): 论文分析
- [[papers/sun2019-hrnetv2-critical]] — HRNetV2 贡献·Negative·可迁移·研究机会
- [[papers/sun2019-hrnetv2-method]] — HRNet 方法机制展开
- [[papers/sun2019-hrnetv2-results]] — HRNetV2 实验结果展开
- [[papers/tao2026-fpikan]] — Tao et al. (2026) FPIKAN：Fourier 特征增强的物理信息 KAN（摘要级概览）
- [[papers/wang2020-hat-analysis]] — Wang et al. (2020) — HAT: Hardware-Aware Transformers: 论文分析
- [[papers/wang2020-hat-critical]] — HAT 贡献·局限·可迁移·研究机会
- [[papers/wang2020-hat-method]] — HAT 方法机制：SuperTransformer + 延迟预测器 + 进化搜索
- [[papers/wang2020-hat-results]] — HAT 实验结果：四任务×三硬件 BLEU-Latency 全面对比
- [[papers/wang2021-pinn-ntk-failure-analysis]] — Wang et al. (2021) PINN 训练失败机制：神经正切核 (NTK) 视角
- [[papers/wang2021-pinn-ntk-failure-critical]] — Wang et al. (2021) PINN 失败机制 — 贡献·Negative·可迁移·研究机会
- [[papers/wang2021-pinn-ntk-failure-method]] — Wang et al. (2021) PINN 失败机制 — 方法展开：NTK 推导与自适应算法
- [[papers/wang2021-pinn-ntk-failure-results]] — Wang et al. (2021) PINN 失败机制 — 结果展开：四个 PDE 谱偏差验证
- [[papers/wang2023-pinn-spurious-analysis]] — Wang et al. (2023) — When PINNs Go Wrong: Pseudo-Time Stepping Against Spurious Solutions
- [[papers/wang2023-pinn-spurious-critical]] — Wang et al. (2023) — 贡献 / 知识点 / Negative / 可迁移 / 研究机会
- [[papers/wang2023-pinn-spurious-method]] — Wang et al. (2023) — 方法机制展开
- [[papers/wang2023-pinn-spurious-results]] — Wang et al. (2023) — 结果证据展开
- [[papers/wang2024-causal-pinn-analysis]] — Wang et al. (2024) — Respecting Causality for Training PINNs: 因果训练范式
- [[papers/wang2024-causal-pinn-critical]] — Wang et al. (2024) 因果训练 PINN — 贡献 / 知识点 / Negative / 可迁移 / 研究机会
- [[papers/wang2024-causal-pinn-method]] — Wang et al. (2024) 因果训练 PINN — 方法展开：因果损失函数与时序权重
- [[papers/wang2024-causal-pinn-results]] — Wang et al. (2024) 因果训练 PINN — 结果展开：混沌系统首次成功
- [[papers/wang2024-kinn-analysis]] — Wang et al. (2024) KINN：以 Kolmogorov–Arnold 网络替代 MLP 的物理信息神经网络骨干
- [[papers/wang2024-kinn-critical]] — Wang et al. (2024) KINN — 贡献·Negative·可迁移·研究机会
- [[papers/wang2024-kinn-method]] — Wang et al. (2024) KINN 方法机制展开：KAN 替换 MLP + 三种 PDE 形式
- [[papers/wang2024-kinn-results]] — Wang et al. (2024) KINN 结果展开：六类固体力学问题的 KAN vs MLP 系统对比
- [[papers/wang2024-nas-pinn-analysis]] — Wang & Zhong (2024) — NAS-PINN: Neural architecture search-guided physics-informed neural network
- [[papers/wang2024-nas-pinn-critical]] — Wang & Zhong (2024) — NAS-PINN critical analysis
- [[papers/wang2024-nas-pinn-method]] — Wang & Zhong (2024) — NAS-PINN method
- [[papers/wang2024-nas-pinn-results]] — Wang & Zhong (2024) — NAS-PINN results
- [[papers/wu2025-cm-pinn-analysis]] — Wu et al. (2025) — CM-PINNs：本构模型约束 PINN 预测非线性结构地震响应
- [[papers/wu2025-cm-pinn-critical]] — Wu et al. (2025) — CM-PINNs 贡献、Negative Knowledge 与研究机会
- [[papers/wu2025-cm-pinn-method]] — Wu et al. (2025) — CM-PINNs 方法机制展开
- [[papers/wu2025-cm-pinn-results]] — Wu et al. (2025) — CM-PINNs 实验结果展开
- [[papers/xie2021-segformer-analysis]] — Xie et al. (2021) — SegFormer: Simple and Efficient Design for Semantic Segmentation with Transformers: 论文分析
- [[papers/xie2021-segformer-critical]] — SegFormer 贡献·Negative·可迁移·研究机会
- [[papers/xie2021-segformer-method]] — SegFormer 方法机制展开
- [[papers/xie2021-segformer-results]] — SegFormer 实验结果展开
- [[papers/xiong2025-confseq-analysis]] — Xiong et al. (2025) — ConfSeq 构象描述语言：3D 分子结构与 AI 的桥梁
- [[papers/xiong2025-confseq-critical]] — ConfSeq 贡献 + Negative + 可迁移 + 研究机会
- [[papers/xiong2025-confseq-method]] — ConfSeq 方法机制：内坐标序列化与 Transformer 统一架构
- [[papers/xiong2025-confseq-results]] — ConfSeq 实验结果：四大任务全面 SOTA
- [[papers/xu2021-nas-bert-analysis]] — Xu et al. (2021) — NAS-BERT: Task-Agnostic BERT Compression with NAS: 论文分析
- [[papers/xu2021-nas-bert-critical]] — NAS-BERT 批判分析：贡献 · 知识点 · Negative · 可迁移 · 研究机会
- [[papers/xu2021-nas-bert-method]] — NAS-BERT 方法机制：Block-Wise Supernet 训练 + Progressive Shrinking + Model Selection
- [[papers/xu2021-nas-bert-results]] — NAS-BERT 实验结果：GLUE · SQuAD · Ablation · Multi-Size 验证
- [[papers/zeraatkar2026-pgt-analysis]] — Physics-Guided Transformer (PGT)：面向 PINN 的物理感知注意力机制
- [[papers/zeraatkar2026-pgt-critical]] — Physics-Guided Transformer 批判分析
- [[papers/zeraatkar2026-pgt-method]] — Physics-Guided Transformer 方法机制
- [[papers/zeraatkar2026-pgt-results]] — Physics-Guided Transformer 结果与证据
- [[papers/zhang2020-phylstm-analysis]] — Zhang et al. (2020) — PhyLSTM 论文分析
- [[papers/zhang2020-phylstm-critical]] — Zhang et al. (2020) — 贡献 / 知识点 / Negative / 可迁移 / 研究机会
- [[papers/zhang2020-phylstm-method]] — Zhang et al. (2020) — 方法机制展开
- [[papers/zhang2020-phylstm-results]] — Zhang et al. (2020) — 结果证据展开
- [[papers/zhang2025-mrf-pinn]] — Zhang et al. (2025) — MRF-PINN：多感受野卷积物理信息网络（摘要级概览）
- [[papers/zhang2026-legonet-analysis]] — Zhang et al. (2026) — LegONet：可插拔、结构保持的组合式 PDE 神经算子积木
- [[papers/zhang2026-legonet-critical]] — LegONet 贡献与局限
- [[papers/zhang2026-legonet-method]] — LegONet 方法机制：结构保持 operator blocks 与组合式 PDE 求解
- [[papers/zhang2026-legonet-results]] — LegONet 结果：跨 PDE 组合、长时稳定与结构保持
- [[papers/zhao2017-pspnet-analysis]] — Zhao et al. (2017) — Pyramid Scene Parsing Network (PSPNet): 论文分析
- [[papers/zhao2017-pspnet-critical]] — PSPNet 贡献·Negative·可迁移·研究机会
- [[papers/zhao2017-pspnet-method]] — PSPNet 方法机制展开
- [[papers/zhao2017-pspnet-results]] — PSPNet 实验结果展开
- [[papers/zhao2021-memory-efficient-dnas-analysis]] — Zhao et al. (2021) — Memory-Efficient Differentiable Transformer Architecture Search 论文分析
- [[papers/zhao2021-memory-efficient-dnas-critical]] — DARTSformer 批判分析：贡献 · 知识点 · Negative · 可迁移 · 研究机会
- [[papers/zhao2021-memory-efficient-dnas-method]] — DARTSformer 方法机制：Multi-Split Reversible Network + BP-with-Reconstruction + DARTS
- [[papers/zhao2021-memory-efficient-dnas-results]] — DARTSformer 实验结果：WMT'14 En-De / En-Fr · WMT'18 En-Cs · Ablation
- [[papers/zhao2026-causal-attention-analysis]] — Casual Attention: 自适应因果性时空加权 PINN 训练 — 论文分析
- [[papers/zhao2026-causal-attention-critical]] — Casual Attention 批判性分析：贡献 / Negative / 可迁移 / 研究机会
- [[papers/zhao2026-causal-attention-method]] — Casual Attention 方法展开：CA 权重 + mMLP + Fourier 特征 + 重采样
- [[papers/zhao2026-causal-attention-results]] — Casual Attention 实验结果：Allen-Cahn / KdV / KS / Burgers 全基准

- [[papers/chen2026-empm-analysis]] — Chen et al. (2026) — EMPM 论文分析
- [[papers/chen2026-empm-method]] — EMPM 方法机制：可微 MPM、离线与在线参数识别
- [[papers/chen2026-empm-results]] — EMPM 结果证据：弹性/弹塑性对象、在线校正与运行时间
- [[papers/chen2026-empm-critical]] — EMPM 批判、迁移与研究机会

<!-- AUTO-REGISTRY:END -->
