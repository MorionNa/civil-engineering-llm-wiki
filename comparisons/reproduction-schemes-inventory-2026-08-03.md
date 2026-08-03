---
id: comparison--reproduction-schemes-inventory-2026-08-03
title: 2026 当前复现方案总览：证据、优势与边界
type: comparison
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/ai4s
- method/pinn
- method/evaluation
- evidence/report
sources:
- ../../../reproductions/cm-pinn/README.md
- ../../../reproductions/dynamic-pignn/README.md
- ../../../reproductions/graph-phygru/README.md
- ../../../reproductions/hcff-pinn/README.md
- ../../../reproductions/phylstm/README.md
- ../../../reproductions/phylstm-pignn/README.md
- ../../../reproductions/step-integrator/README.md
- ../../../reproductions/upstream/README.md
- ../../../docs/plans/experiment_plan.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
legacy_tags:
- comparison
- structural-dynamics
- physics-informed
- equation-of-motion
- limitation
- architecture-selection
- transfer-learning
legacy_sources:
- ../../../../reproductions/cm-pinn/README.md
- ../../../../reproductions/dynamic-pignn/README.md
- ../../../../reproductions/graph-phygru/README.md
- ../../../../reproductions/hcff-pinn/README.md
- ../../../../reproductions/phylstm/README.md
- ../../../../reproductions/phylstm-pignn/README.md
- ../../../../reproductions/step-integrator/README.md
- ../../../../reproductions/upstream/README.md
- ../../../../docs/plans/experiment_plan.md
---

# 2026 当前复现方案总览：证据、优势与边界

本页把项目当前已经运行过、正在运行或明确作为迁移参考的复现方案放在同一张证据地图中。这里的“复现成功”不是只看一个低损失或一个 pooled (R^2)，而是同时看：来源是否可追溯、数据划分是否公平、动力学残差是否独立、最差样本是否过关、长程 rollout 是否稳定，以及 checkpoint 和预测产物是否可复核。

本总览遵循 [[one-structure-one-model-contract-2026-08-03]]：不把跨结构零样本泛化当作硬门；每个结构可以重新训练一个模型。跨激励、高低频、独立物理、训练时间和公平推理计时仍是硬证据要求。当前精确排名、统一 R² 与速度结论分别见 [[current-structural-pinn-ranking-2026-08-03]]、[[baseline-unified-r2-reassessment-2026-08-03]] 和 [[inference-speed-evidence-2026-08-03]]。

## 1. 证据分级

- **L0 文献范围**：只证明论文提出了某个方法，不能证明本仓库实现正确。
- **L1 源码可运行**：官方或重建代码能完成最小 smoke test；仍不能证明指标或物理正确。
- **L2 复现实验**：固定数据、随机种子、分辨率和训练协议后产生了可保存的指标与预测。
- **L3 独立物理核验**：用独立差分、独立 constitutive evaluation、边界/初值和能量检查复算，不复用训练时的构造量。
- **L4 同结构锁定验证**：对一个结构单独训练后，换未见激励、频带和时间窗，最差样本与 rollout 仍通过预设门槛；跨结构迁移只作为额外结果。

当前大多数方案位于 L1–L2；L3/L4 只能由独立审计和锁定测试授予。[[reproduction-failure-prevention-contract-2026-08-03]] 规定了晋级条件，[[mtp-mechconv-v2-experiment-ledger]] 展示了为什么构造出来的 force-balance 指标不能直接当作预测指标。

## 2. 方案清单：优势、短板与下一道门

| 方案 | 当前优势 | 已知不足或失败模式 | 不能跳过的下一道门 |
|---|---|---|---|
| **CM-PINN** | 三个 FC-SLSTM 子网、中心差分和双线性本构，适合与 PhyLSTM3 做同数据公平对照。 | 没有可直接复用的官方仓库；当前配置是重建的比较基线，不是论文最优设置。 | 在 full-resolution 数据上固定 1000 个 Adam epoch 的协议，补齐独立 EOM、最差样本和预测文件。 |
| **HCFF-PINN** | 有公开官方代码；Fourier 特征和硬初值约束对高频 SDOF 是清楚的强基线。 | 本质是给定一次激励后训练一个响应的 per-instance solver，不是 PhyLSTM 的 meta-model；Bouc-Wen 扩展不能与 90-case 泛化直接横比。 | 明确把它标为单实例基线，并分开报告线性 SDOF 与非线性扩展。 |
| **PhyLSTM / PhyLSTM3** | 论文、官方 GitHub 和 `data_boucwen.mat` 齐全；有明确的已知观测、物理样本和官方 90-case 测试协议。 | 原 TF1.x 代码依赖 CuDNNLSTM、`tf.contrib`、硬编码路径和缺失数据；层数也存在 2/3 层不一致。当前 PyTorch 版本的 smoke test 不能代替 full-resolution accuracy。 | 完成 1501 点、官方 90-case、独立指标与可复核 checkpoint；downsample 结果不能冒充论文复现。 |
| **PhyLSTM-PIGNN** | 把节点位移、边隐状态和恢复力放进图结构，能显式暴露局部状态与边力。 | 隐含的 (f=kdelta+etadelta^3) 具有非可辨识分支；边力恢复弱，即使节点响应看起来不错也不代表本构正确。 | 增加 edge force/constitutive/energy 监督或传感器，并做参数可辨识性与跨激励测试。 |
| **Dynamic PIGNN** | 直接用 (Ma+Cv+Ku=f) 残差约束两节点梁，结构简单，适合验证图输入和力平衡实现。 | fixed reaction 被混进全局 `force_accuracy`，会导致虚高甚至负值；当前 two-node 设置不能证明复杂结构泛化。 | 只使用 active/free DOF 的独立 force residual，拆分反力与自由节点指标，再做结构扩展。 |
| **Graph-PhyGRU** | 目前结构动力学路径中最有竞争力的图聚合 + PhyLSTM/GRU 组合；历史 SDOF full official90 指标较好。 | 5DOF 严格迁移的瓶颈是加速度和顶层边力；历史 champion 没有 checkpoint，GraphMechConvGRU 仍是候选而非 halo 等价证明。 | 保存可复用 checkpoint；完成 full-resolution CM baseline、3DOF→5DOF 最差样本、halo/full graph 一致性。 |
| **Step-integrator：Houbolt / Newmark** | 把时间积分、恢复力、输入历史和 rollout 明确写进模型，能暴露一步预测与长程稳定性的差异。 | Houbolt rollout 明显发散；Newmark 虽改善 teacher 指标仍不稳定；label-free 训练会掉入近零响应/null branch。校准真值历史只证明校准，不证明预测。 | 使用 scheduled sampling/rollout loss、能量/被动性和可观测性约束；训练集校准与锁定测试必须严格分离。 |
| **FBPINNs / MP-Neural-PDE / SGNO / APEBench** | 分别提供局部归一化与窗口、图消息传递、频域神经算子和可重复 benchmark 组织方式。 | 这些上游项目不是本项目的二阶结构 EOM、Bouc-Wen 状态或 halo/full 等价证明；直接移植会混淆“PDE/场预测”与“结构响应/本构识别”。 | 只迁移明确的工程机制，并用本项目独立 EOM、constitutive 和 rollout 合同重新验证。 |
| **PRNN / soft-tissue PI-GNN 等 GitHub 方案** | PRNN 的 intact constitutive plugin、步长/路径依赖意识，以及 PI-GNN 的图/能量代码都可作为实现参考。 | 它们的任务和方程边界不同，不能直接成为 LCO-RK8、二阶 EOM 或结构 halo 的数值权威。 | 固定 upstream commit、逐项建立 transfer boundary；任何迁移代码必须重新通过本项目 tableau、矩阵组装和物理门。 |

## 3. 已形成的共识

### 3.1 最有价值的优势

1. **物理对象逐步显式化**：从 PINN 的残差，推进到节点状态、边状态、恢复力、质量/阻尼/刚度和时间积分器，错误更容易定位。
2. **图结构适合结构迁移**：节点/边语义比纯序列模型更接近结构拓扑；但它只有在边界条件、局部邻域和消息传递范围被独立审计后才有迁移意义。
3. **多层证据开始分离**：官方代码、重建代码、smoke test、正式训练、独立物理审计和锁定测试不再被混成一个“已复现”标签。
4. **失败结果也能复用**：Houbolt 发散、label-free null branch、5DOF 加速度退化和边力不可辨识都已经是后续架构选择的约束，而不是需要被掩盖的负面结果。

### 3.2 反复出现的不足

- **构造量泄漏**：如果用模型自己生成的加速度再回代 EOM，得到的 force-balance (R^2) 只能说明闭环代数自洽，不能说明位移、速度、加速度或本构力预测正确。
- **分辨率与协议漂移**：downsample、不同时间步、不同观测比例或不同测试集会改变难度；必须把它们写进结果身份，不能只比较一个数字。
- **pooling 掩盖尾部**：平均或 pooled 指标会掩盖最差激励、最高频带、顶层和边界节点的失败；最差样本、p95/max 和每个物理量必须同时保留。
- **可辨识性不足**：只监督位移时，多个边力/内部状态可能产生相同节点响应；需要 edge force、constitutive、energy、传感器或跨激励约束。
- **teacher/rollout 混淆**：一步 teacher 指标好不等于长程 rollout 稳定；校准真值历史也不等于自由运行预测。
- **产物不完整**：没有 resolved config、commit、日志、checkpoint、预测和独立审计文件，就不能把结果升级为可引用证据。

## 4. 当前决策矩阵

| 用途 | 可以采用的方案 | 只能作为参考的方案 | 主要判据 |
|---|---|---|---|
| 单实例高频响应基线 | HCFF-PINN | FBPINNs、SGNO | 同一激励、同一时间网格、硬初值和独立残差 |
| PhyLSTM 论文复现 | PhyLSTM3、CM-PINN | PhyLSTM-PIGNN | full-resolution、官方 90-case、独立指标与 checkpoint |
| 结构图响应预测 | Graph-PhyGRU、Dynamic PIGNN | MP-Neural-PDE、soft-tissue PI-GNN | active DOF、边力、本构和跨拓扑验证 |
| 时间推进器 | Newmark 作为诊断 baseline | Houbolt、label-free Newmark | teacher 与 rollout 分开，禁止近零分支，能量/稳定性过门 |
| 大规模/halo 设计 | 图消息传递、FBPINN 局部化的机制 | 任何未完成 full/halo 等价测试的候选 | reach、边界隔离、缩放、full-resolution 对照 |

## 5. 结论

当前最稳妥的路线不是把所有方案合成一个总榜，而是保留任务边界：HCFF-PINN 作为单实例高频基线，PhyLSTM3/CM-PINN 作为论文协议基线，Graph-PhyGRU/Dynamic PIGNN 作为结构图候选，Step-integrator 作为时间推进与失败诊断，FBPINNs/MP-Neural-PDE/SGNO/APEBench/PRNN/PI-GNN 作为受限迁移参考。任何方案要成为正式结论，都必须满足 [[reproduction-failure-prevention-contract-2026-08-03]] 的证据合同。

## Provenance

^[../../../reproductions/phylstm/README.md] ^[../../../reproductions/cm-pinn/README.md]
