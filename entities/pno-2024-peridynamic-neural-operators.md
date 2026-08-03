---
id: entity--pno-2024-peridynamic-neural-operators
title: Peridynamic Neural Operators (PNO, 2024)
type: entity
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-02'
updated: '2026-08-02'
confidence: low
legacy_source_files:
- papers/literature_20260802/Peridynamic_Neural_Operators/manifest.json
- papers/literature_20260802/Peridynamic_Neural_Operators/PDFs/Peridynamic_Neural_Operators_A_Data-Driven_Nonlocal_Constitutive_Model_for_Complex_Material_Responses.pdf
legacy_source_urls:
- https://arxiv.org/abs/2401.06070
legacy_arxiv: 2401.06070v1
legacy_pdf_pages: 37
legacy_sha256: 0ddf85758c1a0fa4028b50b0e7346bdbb199921df72cf9449f4a3577dc0344f7
legacy_evidence_scope: 仅依据本地 37 页 PDF 正文和对应 manifest；manifest 标记 Supporting Information
  未找到。论文直接证据覆盖普通状态型近场动力学本构、非局部神经算子、客观性/线性与角动量平衡、分辨率与几何/载荷泛化，以及二维准静态示例；不把论文对动态任务的可适用性表述当作已验证结果。
legacy_tags:
- peridynamics
- neural-operator
- nonlocal-constitutive-model
- objectivity
- momentum-balance
- message-passing
evidence_scope: 仅依据本地 37 页 PDF 正文和对应 manifest；manifest 标记 Supporting Information 未找到。论文直接证据覆盖普通状态型近场动力学本构、非局部神经算子、客观性/线性与角动量平衡、分辨率与几何/载荷泛化，以及二维准静态示例；不把论文对动态任务的可适用性表述当作已验证结果。
---

# Peridynamic Neural Operators（PNO）

> **论文**：Siavash Jafarzadeh et al., “Peridynamic Neural Operators: A Data-Driven Nonlocal Constitutive Model for Complex Material Responses”，arXiv:2401.06070v1（2024）。
> **核心对象**：学习普通状态型 peridynamics 的非局部本构，而不是直接把载荷映射为一个特定几何上的位移场。

## PDF 直接支持的内容

### 1. 把神经算子放进非局部本构结构

PNO 学习标量 force state \(t\) 和 influence state \(\omega\)，并把它们放进 ordinary state-based peridynamics 的非局部积分形式。论文给出的实现可写成两层消息传递：第一层依据参考键向量、影响函数和变形后的键长变化计算非局部 dilatation；第二层根据局部边特征、dilatation、键长变化等预测边上的力状态，随后进行对称化和方向聚合。

论文明确将 PNO 设计为 ordinary、mobile 的材料模型，因此声称由该结构自动继承：

- 对平移和旋转的框架不变性/客观性；
- 线动量和角动量平衡；
- 对不同几何、外载和离散分辨率的泛化潜力。

这些性质来自其 peridynamic 结构化组装，而不是来自一个泛化的“任意 MLP 都自动守恒”的结论。

### 2. 训练协议与实验范围

论文用节点坐标、位移和外力/体力数据训练本构算子。损失直接度量由算子产生的内部力与外载的相对误差；在无外力情形，论文另行讨论避免零解的损失处理。网络主体是浅层 MLP，边邻域由 horizon \(\delta\) 确定。正文实验包括 graphene、各向异性超弹性材料和生物组织，重点是二维、准静态材料响应；正文说该架构可扩展到更高维和动态情形，但这些话不等同于本项目的高频动力学验证。

## 对 nonlinear-PINN / MechConv 的可迁移启发

1. **可替换本构插件**：PNO 最适合借鉴为 `edge constitutive plugin` 的接口范式：输入参考/当前几何、相对位移或应变不变量、矩阵边权与历史特征，输出边内力或边力状态；MechConv 再负责按有向边组装节点内力。
2. **矩阵边权和局部子图**：horizon 邻域天然给出局部边集合；非均匀体积权、影响函数和几何权可以作为矩阵边权。对大结构可先在局部邻域上计算，再由全局 MechConv 汇总，但跨子图截断误差和接口力必须单独测量。
3. **物理不变量**：将相对位置/相对位移、变形后键长和方向对称化放到插件内部，有助于降低网络学习刚体运动和方向变化的负担。
4. **噪声与非线性**：论文报告其结构化本构在噪声数据和复杂材料响应上的鲁棒性启发，可用于设计本项目的本构插件训练集，而不是直接复用其准静态指标。

## 明确限制与不可直接宣称的结论

- PNO 的非局部内部力平衡不是本项目的显式 \(kx+cv+ma=F\) 闭环；论文没有直接证明带质量、阻尼和时间积分的二阶动力学 EOM 恒等式。
- 论文主要展示单一 PNO 本构在其数据上的学习，不证明任意 linear/bilinear/Bouc–Wen 插件可以共享同一 backbone 并达到本项目的跨本构门槛。
- horizon 邻域的 resolution-independent 表述不能替代“任意大图切成子图后拼接与全图等价”的接口定理或实验。
- 正文实验不是本项目定义的低/高频结构响应协议，未给出与 Newmark-beta/FEM 的同条件端到端推理时间对照，也没有本项目要求的四通道 R² 门。

## 项目使用建议

把 PNO 当作**可替换边本构层**的候选，不把它当作最终动力学求解器。任何实现都应保留 MechConv 的节点力组装和 temporal-parallel EOM 路径，并同时记录：插件输出力、节点组装力、独立加速度、跨本构 R²、子图接口残差和完整 forward 时间。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[entities/index]]
- [[index]]
