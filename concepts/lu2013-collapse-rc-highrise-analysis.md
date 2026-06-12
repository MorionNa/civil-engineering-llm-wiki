---
title: "Lu et al. (2013) — RC 高层建筑极端地震倒塌模拟: 论文分析"
created: 2026-06-11
updated: 2026-06-11
type: concept
tags: [structural-dynamics, nonlinear-systems, seismic-response, collapse-simulation,
       rc-structures, fiber-beam-element, multilayer-shell, elemental-deactivation,
       finite-element, high-rise-building, progressive-collapse, material-failure-criteria]
sources: [raw/papers/lu2013-collapse-rc-highrise.md, raw/papers/10_1002_eqe_2240.pdf]
methods: [fiber-beam-element, multilayer-shell, elemental-deactivation, finite-element, contact-algorithm, strain-based-failure]
results: [collapse-process-simulation, soft-story-identification, failure-criteria-sensitivity]
failure_modes: [no-full-scale-validation, model-assumption-limitations, failure-criteria-arbitrariness]
datasets: [el-centro-ground-motion, duzce-ground-motion, fema-p695-far-field]
reproducibility: medium
code_url: []
dataset_url:
  - https://ngawest2.berkeley.edu/
confidence: high
---

# RC 高层建筑在极端地震下的倒塌模拟

> Xiao Lu, **Xinzheng Lu (陆新征)**, Hong Guan, Lieping Ye (叶列平).  
> Earthquake Engineering & Structural Dynamics, 2013, 42(5): 705–723. DOI: 10.1002/eqe.2240  
> 清华土木系 + Griffith University

## 1. 工程背景 (Engineering Background)
> 为什么这个问题在工程上重要？

汶川(2008)、海地(2010)、玉树(2010)等强震反复证明：**结构倒塌是地震伤亡的首要原因**。然而，即使世界上最大的振动台也无法进行足尺高层建筑倒塌试验。数值模拟成为唯一可行的替代手段——但此前的研究大多局限于简单结构（框架、桥梁），极少涉及含有数千根梁柱和剪力墙的**真实高层建筑**。本文直接将倒塌模拟推向工程实践。

## 2. Research Gap
> 已有研究缺了什么？

- 离散元(DEM)、应用元(AEM)等方法虽有进展，但**距模拟复杂真实高层建筑仍有很长的路**。
- 现有 FE 倒塌研究缺少对**高层建筑全系统倒塌过程**的刻画——尤其是 frame-core tube（框架-核心筒）这种中国最常见的高层结构体系。
- **材料级失效准则对倒塌模拟结果的影响**（混凝土压碎应变、钢筋屈曲/断裂应变）缺乏系统讨论。

## 3. 科学问题 (Scientific Question)
> 核心难题是什么？

**在统一 FE 框架内，如何将材料本构（微米级应变）与结构系统级倒塌过程（宏观失效模式识别、弱层定位、碎片碰撞）关联起来，形成可工程实用的高层建筑倒塌模拟方法？**

## 4. 研究目标 (Research Objective)
> 本文想实现什么？

提出并验证一个基于通用 FE 软件（MSC.MARC）的 RC 高层建筑倒塌模拟数值模型，包含：(1) 纤维梁单元 + 多层壳单元的材料-构件-结构跨尺度建模，(2) 基于应变的单元失效准则和去激活机制，(3) 碎片接触碰撞算法。用三个算例（10 层框架 + 两栋真实高层）展示方法可行性。

## 5. 方法机制 (Method & Mechanism)
> 本文方法如何工作？ → [[lu2013-collapse-rc-highrise-method]]

**三个核心组件**：

① **纤维梁单元**（beams/columns）：截面离散为混凝土纤维+钢筋纤维，每根纤维有独立单轴本构。考虑箍筋约束效应、Bauschinger 效应、拉伸刚化。嵌入 MSC.MARC via UBEAM 子程序。

② **多层壳单元**（shear walls）：壳沿厚度分多层——混凝土层 + 弥散钢筋层（正交各向异性）。直接关联材料本构→墙体非线性行为，天然处理面内/面外耦合和弯剪耦合。

③ **单元去激活**（elemental deactivation）：当任何积分点应变超过材料失效准则时，该纤维/层退出工作。**所有纤维/层失效 → 单元去激活 → 孤立节点移除**。四种失效准则：非约束混凝土压碎(ε>0.33%)、约束混凝土软化至零、钢筋拉断(ε>10% or 15%)、钢筋屈曲(ε<-0.5% or -1.0%)。

+ **接触碰撞**：MSC.MARC 内置接触算法处理失效碎片与剩余结构的碰撞。

## 6. 结果证据 (Result & Evidence)
> 什么结果支撑结论？ → [[lu2013-collapse-rc-highrise-results]]

- **构件验证**：纤维梁模型 vs 4 组柱试验（S-1, YW0, Yi frame, Tang deterioration）——滞回曲线、强度退化吻合良好。多层壳模型 vs 4 组墙试验（单墙、TC1/TC2 筒体、钢骨混凝土墙）——承载力与退化行为吻合。

- **10 层框架**（El-Centro PGA=2000gal）：第 8 层（截面变化处）和第 1 层形成软弱层，4.4s 完全倒塌。清晰展示 P-Δ 效应驱动的侧向倒塌机制。

- **18 层框筒**（El-Centro PGA=1500gal）：首层核心筒外翼缘混凝土压碎（轴力+弯矩主导，非剪力）→ 力重分布 → 柱屈曲 → 上部结构与地下室碰撞 → 整体倒塌。

- **20 层框筒**（El-Centro PGA=4000gal vs Duzce PGA=4000gal）：两种地震动产生**不同倒塌模式**——El-Centro 在第 10 层弱层起爆，Duzce 脉冲型地震动在首层起爆。归因于频率成分差异激发的不同振型。

- **失效准则敏感性**（FEMA P695 22 条远场地震，Sa(T1)=4.0g）：**钢筋屈曲应变** 0.5%→1.0% 使倒塌概率从 81.8% 降至 63.6%，而受拉断裂应变 10%→15% 几乎无影响——因框筒倒塌由压溃主导。

## 7. 贡献 (Contribution)
> 本文新增了什么？ → [[lu2013-collapse-rc-highrise-critical]]

1. 首次在通用 FE 框架中集成纤维梁+多层壳+单元去激活，实现**真实 RC 高层框筒建筑的全过程倒塌模拟**。
2. 引入**材料级应变失效准则**并通过 22 条地震动参数研究揭示了**钢筋屈曲应变比受拉断裂应变对倒塌概率影响更大**的规律。
3. 为框筒结构体系提供了**弱层定位方法和倒塌机制解释**（刚度突变处应力集中→核心筒外翼缘压碎→力重分布→柱屈曲→碰撞倒塌）。

## 8. 核心知识点 (Core Knowledge)
> 读完这篇论文应该记住什么？

1. RC 高层框筒倒塌的**典型链式机制**：核心筒外翼缘压碎（轴力+倾覆弯矩）→ 力重分布到周边柱 → 柱屈曲 → 碰撞倒塌。
2. 倒塌**不总是从首层开始**——截面/材料变化处的刚度突变是关键弱层标识。
3. **不同地震动可导致同一结构的不同倒塌模式**（脉冲型 vs 持时型），因为激发不同振型。
4. 倒塌模拟中，**材料失效准则的选取影响巨大**——对压溃主导的结构，钢筋屈曲应变的敏感性远超受拉断裂应变。

## 9. Negative Knowledge
> 风险、失败边界 → [[lu2013-collapse-rc-highrise-critical]]

- **无足尺验证**：所有系统级倒塌结果没有实验对照。地震动缩放到 5-10 倍设计水准本质上是"what-if"研究，不代表真实地震行为。
- **纤维梁的脆性剪切假设**：当内部剪力超过抗剪强度时，强度和刚度骤降为零——这对剪切主导的矮柱可能过于保守/激进。
- **失效准则的任意性**：钢筋屈曲应变 0.5% vs 1.0%、拉断 10% vs 15%——这些值来自文献范围，缺乏针对本文结构体系的标定。倒塌概率对这些值敏感（~18 个百分点差异）。
- **接触算法简化**：MSC.MARC 默认接触容差 = min(5% 单元边长, 25% 厚度)——对大规模倒塌可能不合理。
- **未考虑楼板**：多层壳只模拟剪力墙，楼板效应未讨论（框架-核心筒中楼板是重要传力构件）。

## 10. 可迁移知识 (Transferable Knowledge)
> 哪些经验可用于其他研究？ → [[lu2013-collapse-rc-highrise-critical]]

| 知识点 | 迁移到 |
|--------|--------|
| 材料应变→构件→系统跨尺度建模范式 | 任何基于 FE 的结构极端行为模拟（爆炸、火灾、连续倒塌） |
| 刚度突变处 = 弱层的工程判断准则 | 结构抗震设计中的薄弱层快速筛查 |
| FEMA P695 远场地震动集 + IDA 倒塌概率评估框架 | 任何需要评估倒塌概率的结构体系 |
| 材料失效准则的参数敏感性分析 | 提醒所有倒塌模拟研究必须报告准则选取依据 |

## 11. 研究机会 (Research Opportunity)
> 下一步可以研究什么？ → [[lu2013-collapse-rc-highrise-critical]]

1. **足尺/大比例实验验证**——文中明确称此为最大局限
2. **基于物理的失效准则标定**——用细观模型（如 lattice model）标定宏观 FE 的等效失效应变
3. **ML 替代倒塌模拟**——用本文模拟结果训练 surrogate model 进行参数量化（倒塌概率、失效准则、地震动变异性的联合影响）
4. **与 [[zhang2020-phylstm-analysis]] 的交叉**：PhyLSTM 验证案例中包含 Bouc-Wen 滞回模型，是否能与纤维梁/多层壳的滞回退化行为建立联系？

## 12. 可复现性 (Reproducibility)

**🟡 中复现性** — 无开源代码，但方法描述详尽，依赖商业 FE 软件

| 项目 | 说明 |
|------|------|
| **等级** | 🟡 中 |
| **官方代码** | ❌ 无（基于 MSC.MARC 商业软件 + UBEAM 子程序） |
| **数据集** | 地震动记录公开（PEER NGA-West2：`ngawest2.berkeley.edu`）；FEMA P695 远场地震动集公开 |
| **协议** | 无 |

**复现要点**：方法论足够详尽——纤维梁/多层壳的单元类型、材料本构参数、四种失效准则的具体应变阈值全部公开。可在其他 FE 平台（Abaqus/OpenSees/ANSYS）复现，但需自行编写子程序。失效准则的应变阈值来自文献范围，换结构体系需重新标定。

## 关联页面
- [[lu2013-collapse-rc-highrise-method]] — 方法机制展开（纤维梁+多层壳+去激活）
- [[lu2013-collapse-rc-highrise-results]] — 实验结果展开
- [[lu2013-collapse-rc-highrise-critical]] — 贡献 + Negative + 可迁移 + 机会
- [[zhang2020-phylstm-analysis]] — PhyLSTM 滞回建模（可交叉迁移的替代方案）
