---
id: entity--raj2026-history-dependent-constitutive
title: Raj et al. (2026) — History-Dependent Constitutive Laws and Identifiability
type: entity
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-01'
updated: '2026-08-01'
confidence: low
legacy_evidence_scope: first-3-pages-only
legacy_tags:
- constitutive-modeling
- history-dependent
- internal-variables
- identifiability
- causal-learning
- energetic-modeling
- ai4s
legacy_sources:
- papers/literature_20260801/HistoryDependentConstitutive_2605_14179/PDFs/A_Neural-Network_Framework_to_Learn_History-Dependent_Constitutive_Laws_and_Identifiability_of_Internal_Variables.pdf
- papers/literature_20260801/HistoryDependentConstitutive_2605_14179/manifest.json
evidence_scope: first-3-pages-only
---

# Raj et al. (2026)：历史依赖本构律与内部变量可辨识性

## 论文记录

- **题目：** *A Neural-Network Framework to Learn History-Dependent Constitutive Laws and Identifiability of Internal Variables*
- **作者：** Mayank Raj, Lianghao Cao, Andrew Stuart, Kaushik Bhattacharya
- **版本：** arXiv:2605.14179（v1）
- **验证状态：** `open_access_downloaded`；26 页；SHA-256 `5b579cfa27e13023cfb3e369fe28874a42395f1688067bb89a89af8ee159b5a`
- **本地 PDF：** `papers/literature_20260801/HistoryDependentConstitutive_2605_14179/PDFs/A_Neural-Network_Framework_to_Learn_History-Dependent_Constitutive_Laws_and_Identifiability_of_Internal_Variables.pdf`
- **manifest：** 同目录 `manifest.json`；SI 状态：`not_found`

## 证据范围

本页摘要只依据已抽取的前 3 页（含论文开头、问题设定与框架概览）整理，**未做全文深读**。因此不记录后续实验、定理证明、数据集、超参数或数值性能，也不把论文中可能在后文出现的结论外推为已验证事实。

## 摘要

论文讨论如何用神经网络学习具有路径依赖的本构关系：当前应力/响应不能只由当前应变或当前输入点决定，而要由加载历史及其所携带的内部状态共同决定。框架把材料响应写成带内部变量的演化系统，并将网络学习目标与因果时间推进、状态更新以及能量一致性联系起来，使模型能够表示 history-dependent constitutive law，而不是把每个时刻当成互相独立的回归样本。

前 3 页同时把“内部变量是什么”与“能否从观测中唯一识别”区分开来。不同的潜在状态参数化可能产生完全相同的可观测本构响应，即内部变量存在等价变换或不可辨识方向；因此，网络逐点拟合得到的 latent 不自动具有材料学上的状态含义。只有当状态沿合法历史演化，并满足相应的因果与能量约束时，latent trajectory 才能被解释为候选内部变量表示。

## 可迁移结论（面向结构工程与 PINN）

1. **因果/能量历史依赖律：** 对滞回、塑性、损伤、黏弹性等材料，结构响应模型应学习“输入历史 → 状态演化 → 当前响应”的因果链，并把能量耗散或储能约束作为可检查的物理接口；单点输入输出拟合不足以定义合法本构律。
2. **内部变量等价性与可辨识性：** 即使两个网络的 latent 维度、坐标或轨迹不同，只要它们诱导相同的可观测响应，就可能属于等价表示。内部变量的维度、坐标和语义不能仅凭低训练误差宣称已被恢复，需要额外的可辨识性分析或规范化约束。
3. **逐点 latent ≠ 合法历史：** 每个时间点都有一个看似合理的隐变量，并不意味着这些点能拼成满足演化律、初值、路径依赖和能量条件的历史。对 PINN/神经本构模块，应独立检查时间递推、循环加载、卸载再加载和能量收支，而不能只检查点态残差。

## 与本 Wiki 的关系

- [[cm-pinns]]：CM-PINNs 已将显式本构恢复力嵌入结构动力学约束；本页补充其上游问题——如何学习并审计一般 history-dependent law 与内部状态。
- [[causal-training]]：因果训练关注时间方向上的优化权重；本论文的迁移重点是把因果性推进到材料状态演化和本构合法性层面。
- [[bouc-wen-model]]：Bouc–Wen 是可显式写出的率相关滞回模型，可作为学习型历史依赖本构的对照与回归测试对象。

## 未验证与边界

- 未完成全文深读，未核验论文后续实验、证明和全部假设。
- 未据此断言任何特定结构材料、RC 构件或工程数据集上的性能提升。
- `SI not_found` 仅表示本次下载任务未找到 Supporting Information，不等于论文不存在补充材料版本。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.
