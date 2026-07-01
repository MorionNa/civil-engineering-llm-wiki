---
title: "Wu et al. (2025) — CM-PINNs：本构模型约束 PINN 预测非线性结构地震响应"
created: 2026-07-01
updated: 2026-07-01
type: paper-analysis
tags: [physics-informed, pinn, lstm, metamodeling, structural-dynamics, nonlinear-systems, hysteresis, seismic-response, data-scarcity, equation-of-motion, restoring-force, soft-constraint, finite-difference, adaptive-weighting, sdof]
sources: [raw/papers/wu2025-cm-pinn-extracted.md]
methods: [physics-constrained-loss, finite-difference, multi-lstm, adaptive-weighting, collocation-strategy]
results: [cross-domain-generalization, extrapolation-ability, synthetic-data]
failure_modes: [finite-difference-error, physics-constraint-weight-tuning]
datasets: [blwn, synthetic-data]
reproducibility: medium
code_url:
  - 待公开（论文声明发表后将在 GitHub 公开）
dataset_url:
  - BLWN 合成地震动；Chi-Chi 记录用于独立验证；代码/数据待 GitHub 公开
confidence: high
---

# Constitutive model-constrained physics-informed neural networks framework for nonlinear structural seismic response prediction

> **论文：** Yongxin Wu, Zhanpeng Yin, Yufeng Gao, Shangchuan Yang, Yue Hou (2025), *Computer Methods in Applied Mechanics and Engineering*, 443, 118079. DOI: 10.1016/j.cma.2025.118079
> **核心定位：** 在 `[[zhang2020-phylstm-analysis]]` 的 PhyLSTM 路线上进一步把**非线性本构模型**显式放进 physics-informed loss，用 CM-PINNs 预测 SDOF 与 MDOF 剪切结构的非线性地震响应。
> **原文：** `[[raw/papers/wu2025-cm-pinn-extracted]]`；PDF: `[[raw/papers/wu2025-cm-pinn.pdf]]`

## 1. 工程背景 (Engineering Background)
> **⚠️ 非线性类型：材料本构非线性 + 结构滞回响应。** 本文的“非线性”不是 Raissi 2019 那类 PDE 算子非线性，而是结构恢复力 $F_s(u)$ 由**双线性弹塑性本构/滞回模型**决定：屈服后刚度降低，恢复力依赖加载历史和未观测滞回变量 $r$。PINN 的作用不是只把运动方程写进残差，而是把**本构模型计算出的恢复力**作为额外约束嵌入 loss。^[raw/papers/wu2025-cm-pinn-extracted.md]

地震作用下结构响应高度依赖材料与构件的非线性滞回行为；传统 FEM/OpenSees 类时程分析精度高但大规模非线性分析成本高，纯数据驱动 LSTM/CNN 又依赖大量高质量标注且缺乏物理可解释性。工程上真正需要的是能在少样本下保持物理一致、又能快速输出全时程响应的代理模型。

## 2. Research Gap
已有 `[[zhang2020-phylstm-analysis]]` / PhyCNN / PI-LSTM 等 physics-informed 结构响应模型主要嵌入运动方程、状态依赖或导数一致性，但往往没有把**非线性本构模型本身**作为约束显式纳入损失函数。已有本构增强研究更多关注峰值、静态/准静态反演或弹塑性单点问题，尚不足以刻画复杂地震输入下结构响应的时间演化。

## 3. 科学问题 (Scientific Question)
如何在少量地震响应样本下，让序列模型同时满足：(1) 运动方程；(2) 位移-速度导数一致性；(3) 滞回隐变量演化；(4) 非线性本构恢复力一致性，从而可靠预测结构非线性地震响应全时程与峰值？

## 4. 研究目标 (Research Objective)
本文提出 `[[cm-pinns]]`：用 FC-SLSTM 序列网络预测 $u,\dot u,r$ 与恢复力项，用中心差分模块计算导数，用 nonlinear constitutive model (NLCM/BLCM) 生成物理恢复力 $f_{s2}$，并通过自适应 loss 权重把数据项和多类物理项平衡起来。验证目标包括 SDOF 双线性弹塑性系统、对 PhyLSTM 的改进、以及 5-DOF/7-DOF 剪切楼层模型的可扩展性。

## 5. 方法机制 (Method & Mechanism)
CM-PINNs 由三组 FC-SLSTM、中心差分 CDM 与 NLCM 模块组成：FC-SLSTM1 将地震动 $a_g$ 映射到 $Z=\{u,\dot u,r\}$；CDM 得到 $\dot Z=\{\dot u,\ddot u,\dot r\}$；FC-SLSTM2 预测数据驱动恢复力加速度 $f_{s1}$；FC-SLSTM3 用 $\{\Delta\dot u,r\}$ 预测滞回演化 $\dot r$；NLCM/BLCM 根据位移和双线性本构计算物理恢复力 $f_{s2}$。损失由 $L^D_u,L^D_v,L^P_v,L^P_e,L^P_{fs},L^P_r$ 构成，并用 $\omega_j=|L^D_u/(L_j+\epsilon)|$ 初始化权重。→ [[wu2025-cm-pinn-method]]

## 6. 结果证据 (Result & Evidence)
SDOF 验证中，加入本构约束的 CM-PhyLSTM 相比 PhyLSTM 把 2% 误差阈值内的置信区间从 84.97% 提高到 92.28%，位移最大峰值误差从 12.11% 降到 8.11%。FC-SLSTM 进一步把 2% CI 提到 97.23%，最大位移峰值误差降至 5.92%；自适应权重初始化最终把 2% CI 提到 99.01%，最大/平均位移峰值误差降至 4.14%/0.75%。MDOF 中，5-DOF 和 7-DOF 顶层/中层响应平均 $R$ 分别达 0.9978 和 0.9986。→ [[wu2025-cm-pinn-results]]

## 7. 贡献 (Contribution)
1. 把非线性本构模型作为显式 physics-informed loss 约束嵌入结构动力响应预测，而不是只约束运动方程。
2. 提出 FC-SLSTM，解决深层 LSTM 中浅层特征被逐层稀释的问题。
3. 给出适合多 loss PINN 的自适应权重初始化策略。
4. 从 SDOF 扩展到 5-DOF/7-DOF 剪切楼层模型，证明本构约束代理模型具备一定结构尺度扩展能力。→ [[wu2025-cm-pinn-critical]]

## 8. 核心知识点 (Core Knowledge)
这篇文章的关键不是“再做一个 LSTM”，而是把结构动力 PINN 从 $M\ddot u+C\dot u+R=F$ 的**运动方程约束**推进到 $R=\mathcal{C}(u,\text{history})$ 的**本构一致性约束**。对于考虑塑性、损伤、滞回的结构响应预测，恢复力不能只由黑箱网络学，必须用本构模块收缩解空间。

## 9. Negative Knowledge
CM-PINNs 仍依赖已知且可张量化的本构模型；当前只验证双线性本构、BLWN 合成输入和低维剪切模型，尚未证明可处理复杂 RC 构件、退化/捏拢、接触、局部破坏或高维真实结构。导数仍用中心差分而非自动微分，可能继承 `[[zhang2020-phylstm-analysis]]` 的有限差分误差；代码和数据虽声明将公开，但当前未给出具体 GitHub 链接。

## 10. 可迁移知识 (Transferable Knowledge)
| 知识 | 可迁移方向 | 迁移方式 |
|---|---|---|
| 本构模块 $f_{s2}=\mathcal{C}(u)$ | Bouc-Wen、Clough、退化滞回、损伤模型 | 将本构算法写成可微/可反传张量计算，作为恢复力一致性 loss |
| $f_{s1}$ vs $f_{s2}$ 双恢复力约束 | 数据驱动恢复力识别 | 让网络预测恢复力，同时用物理本构收缩其可行域 |
| FC-SLSTM | 结构响应、车桥耦合、风振响应 | 用 skip + FC 预处理保留浅层时序特征 |
| 自适应 loss 初始化 | 多物理 loss PINN | 以主要数据项为 baseline，按初始 loss 量级平衡各项 |

## 11. 研究机会 (Research Opportunity)
最直接的后续方向是：把 BLCM 换成 Bouc-Wen/退化 Bouc-Wen/RC 滞回模型，测试真实地震记录和实验构件；把本构参数作为可识别变量，形成“响应预测 + 本构参数反演”一体化框架；与 `[[chen2025-at-pinn-hc-analysis]]` 的硬约束初始条件、`[[li2025-movingload-pinn-analysis]]` 的因果权重、`[[wang2023-pinn-spurious-analysis]]` 的伪时间步进结合，解决长时程训练稳定性。

## 12. 可复现性 (Reproducibility)
| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中 |
| **官方代码** | 论文声明“data and codes will be publicly available on GitHub after publication”，但 PDF 中未给出具体 URL |
| **数据集** | 100 条 BLWN 记录，30 s、50 Hz、1501 时间步；10 条标注训练、90 条测试，额外 50 条 collocation；Chi-Chi 地震记录用于 OpenSeesPy 验证 |
| **实现信息** | Python 3.9 + PyTorch；Adam 20,000 epochs；初始 lr=1e-3，3000 epochs 后降到 5e-4；Intel i7-11700K + RTX 3070 |
| **复现要点** | BLCM 必须全张量化并保留梯度；中心差分边界用前/后向差分；自适应 loss 权重要按 $L^D_u$ 初始化 |

## 关联页面
- [[cm-pinns]] — 本文提出的本构模型约束 PINN 框架
- [[zhang2020-phylstm-analysis]] — 直接 baseline：PhyLSTM/多 LSTM 物理约束结构动力模型
- [[bouc-wen-model]] — 可替换 BLCM 的典型率相关滞回本构
- [[pinn]] — PINN 基础范式
- [[physics-constrained-training-failure-modes]] — 物理约束训练失败模式对比
