---
id: papers--guo2026-phy-rlk-analysis
title: Guo & Xu (2026) Phy-RLK：双向地震作用下非线性结构响应的物理残差 LSTM-KAN
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
- method/pinn
- method/transformer
keywords:
- equation-of-motion
- finite-element
- ground-motion
- lstm
- neural-network
- nonlinear-systems
- physics-informed
- restoring-force
- seismic-response
- sequence-modeling
- structural-dynamics
- synthetic-data
sources:
- sources/papers/guo2026-phy-rlk.md
created: '2026-07-16'
updated: '2026-07-31'
confidence: high
methods:
- physical-residual-lstm
- newmark-beta-residual
- embedded-physics
- kan-decoder
- bidirectional-mimo
- supervised-learning
results:
- bidirectional-response-prediction
- peak-displacement-error
- cross-structure-validation
- inference-speedup
failure_modes:
- synthetic-label-dependence
- structure-specific-retraining
- no-public-code
- no-public-data
- no-real-world-validation
- no-uncertainty-quantification
datasets:
- srm-bidirectional-ground-motions
- opensees-six-story-rc-frame
- opensees-five-story-rc-frame
reproducibility: low
contested: false
---

# Physics-guided hybrid network for predicting nonlinear dynamic response of structures under bi-directional ground motions

> **作者：** Zheyi Guo, Jun Xu
> **期刊：** Computer Methods in Applied Mechanics and Engineering, 2026
> **DOI：** 10.1016/j.cma.2025.118422
> **中心模型：** [[phy-rlk]]（Physical Residual LSTM-KAN）

## 1. 工程背景 (Engineering Background)

> **⚡ 非线性类型：材料本构/结构动力非线性。** 非线性来自 OpenSees NLTHA 中纤维梁柱及 Concrete01、Steel01、Steel02、Pinching4 的循环本构与恢复力 $F_s(u,\dot u)$，不是用 PINN 求解含非线性算子的 PDE。Newmark-β 只提供离散动力平衡与运动学残差；LSTM/KAN 的网络非线性也不能与材料非线性混为一类。与显式学习滞回状态的 [[phylstm3]]、把本构写入损失的 [[cm-pinns]] 不同，本研究的材料模型仅用于 OpenSees 标签生成，并未直接嵌入网络。

性能化抗震评估需要位移、峰值楼层加速度和残余变形等 EDP。非线性时程分析精度高，但在大量地震动、PGA 水平和结构方案上反复执行成本很高；纯 LSTM/Transformer 代理虽快，却可能依赖大量标签、忽略动力平衡，并对加速度突变和残余位移不敏感。

## 2. Research Gap

已有 [[phylstm2]] / [[phylstm3]] 等结构动力物理信息序列模型多把运动方程、本构或导数一致性写成额外 loss，容易产生多目标权重与梯度冲突。已有工作也以单向地震输入为主，缺少同时预测两个主轴、各楼层加速度—速度—位移的 MIMO 模型。作者希望把物理残差移入网络结构，而不是继续增加损失项。

## 3. 科学问题 (Scientific Question)

能否把 Newmark-β 动力学残差直接注入 LSTM 的 cell state 与 output gate，在仍只优化监督数据误差的情况下修正逐时刻响应；再用 KAN 解码非线性特征，从而提高双向地震输入下多楼层非线性响应、尤其峰值位移的精度与稳定性？

## 4. 研究目标 (Research Objective)

提出 [[phy-rlk]]：以双向地震加速度为输入，输出各楼层两个方向的加速度、速度、位移；比较 LSTM、Transformer、物理残差 LSTM（Phy-RL）和加入 KAN 解码器的 Phy-RLK，并在六层与五层 RC 框架、多个 PGA 水平上验证精度、局部峰值误差和推理速度。

## 5. 方法机制 (Method & Mechanism)

详见 [[guo2026-phy-rlk-method]]。

- 运动方程：$M\ddot u+C\dot u+F_s(u,\dot u)=-M\Gamma\ddot u_g$；
- Newmark-β（$\gamma=0.5,\beta=0.25$）构造加速度、速度、位移残差；
- 经 tanh 与可训练权重变换的 $R_a,R_v,R_u$ 加入 LSTM cell state 和 output gate；
- 三层物理残差 LSTM 提取长时依赖，KAN 用可学习 B-spline 映射解码每层、每方向的三类响应；
- 训练损失只有两个方向加速度、速度、位移的 MSE 之和，物理残差属于架构偏置而非额外 loss。

## 6. 结果证据 (Result & Evidence)

详见 [[guo2026-phy-rlk-results]]。

- 六层框架：Phy-RLK 的加速度/速度/位移 $R^2$ 为 0.921/0.919/0.896，较纯数据模型的误差指标降低 65.6%–93.1%；
- 相对 Phy-RL，作者报告 KAN 带来平均 9.2% 的精度提升，位移 MSE 降低 58.7%；
- 峰值位移误差为 $0.074\pm0.077$，低于 Transformer 的 $0.222\pm0.204$ 和 LSTM 的 $0.199\pm0.188$；95% 区间从 LSTM 的 0.717 收窄到 0.295；
- 五层框架的三类响应 $R^2$ 为 0.932/0.944/0.959，且各 PGA 水平 $R^2>0.89$；
- 六层算例推理 `<50 ms`、OpenSees 约 1200 s；论文自报约 2400 倍，但原始时间与该倍数算术不一致，不能无条件复述。

## 7. 贡献 (Contribution)

1. 将 Newmark-β 物理残差从 loss 移入 LSTM 的状态与门控通路，形成 architecture-level physics guidance；
2. 构建双向输入、多楼层、多物理量同时输出的结构响应代理；
3. 用 Phy-RL → Phy-RLK 对照分离物理残差与 KAN 解码器的增益；
4. 在两个具有不同构件本构和几何的 RC 框架上测试相同网络配置；
5. 同时报告全时程指标和峰值位移误差分布，贴近抗震 EDP 需求。

## 8. 核心知识点 (Core Knowledge)

- “物理信息”不一定只能作为 loss：数值积分器也可成为递归单元内部的误差修正通路。
- 但只用 data loss 意味着模型仍需要 OpenSees 全时程标签；它是**物理引导监督代理**，不是无标签 PDE/ODE 求解器。
- KAN 的贡献是对 LSTM 隐特征做自适应非线性解码；它没有直接表示 Concrete01/Steel/Pinching4 本构。
- 双向预测价值在于保留两个主轴耦合输入，而不仅是分别训练两个单向模型。

## 9. Negative Knowledge

详见 [[guo2026-phy-rlk-critical]]。核心边界包括：标签和测试均来自 OpenSees+SRM；每个结构仍需专属训练；未验证真实双向记录、振动台或传感器噪声；没有不确定度；代码与数据只声明可索取。物理残差没有作为独立指标报告，因而“更物理一致”主要由性能消融间接支持。

## 10. 可迁移知识 (Transferable Knowledge)

| 知识 | 迁移方式 |
|------|----------|
| 数值积分残差注入 recurrent state | 将 Newmark-β 换为广义 α、RK 或状态空间积分器 |
| 架构内物理 + 单数据损失 | 避开 [[cm-pinns]] 的多物理 loss 权重冲突，但保留残差监测 |
| KAN 解码时序隐特征 | 在 [[phylstm2]] / [[phylstm3]] 后端替换 MLP，单独消融 KAN 收益 |
| 双向 MIMO | 扩展到扭转耦合、多点输入、长跨结构多支座激励 |

## 11. 研究机会 (Research Opportunity)

1. 让质量、阻尼、本构和几何成为条件输入，形成跨结构模型而非逐结构重训；
2. 把可微 Concrete/Steel/Pinching 或 [[bouc-wen-model]] 恢复力模块直接接入残差；
3. 在真实双向地震记录、振动台与实测结构上做 domain-shift 验证；
4. 同时优化 data loss 并监控/约束 physics residual，验证残差是否真正下降；
5. 引入概率输出或 ensemble，给 EDP 与易损性分析提供置信区间；
6. 统一端到端计时口径，复核训练、数据生成、推理和 FEM 加速比。

## 12. 可复现性 (Reproducibility)

**🔴 低。** 架构公式、主要超参数、SRM 与两类结构均有较详细描述，但代码、OpenSees 模型文件、训练/测试索引和数据未公开；声明仅为“向作者索取”。

| 项目 | 说明 |
|------|------|
| **等级** | low |
| **官方代码** | 未见公开仓库 |
| **数据集** | Data available on request，无公开 URL |
| **软件依赖** | PyTorch；OpenSees；SRM 人工双向地震动 |
| **关键配置** | hidden size 64、lr=0.001、batch=16、tanh residual、1500 epochs、Adam、patience=20、RTX 4080 |
| **复现缺口** | KAN 网格/阶次、完整材料参数、随机种子、划分索引、物理残差权重初始化、模型文件与测速脚本 |

## 关联页面

- [[phy-rlk]] — 模型实体
- [[phylstm2]] / [[phylstm3]] — 物理损失型 LSTM 前序路线
- [[cm-pinns]] — 本构模型约束型路线
- [[bouc-wen-model]] — 可用于后续显式滞回残差的对照本构

## Evidence By Source

### `sources/papers/guo2026-phy-rlk.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/10_1016_j_cma_2025_118422.xml`

^[sources/papers/guo2026-phy-rlk.md]
