---
id: comparison--structure-preserving-candidates-20260802
title: 'Structure-Preserving Candidates for MechConv: SPON, PNO, SP-NODE and Port-Hamiltonian
  (2026-08-02)'
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-02'
updated: '2026-08-02'
confidence: low
legacy_source_files:
- papers/literature_20260802/Structure-Preserving_Operator_Learning/manifest.json
- papers/literature_20260802/Peridynamic_Neural_Operators/manifest.json
- papers/literature_20260802/Structure-Preserving_NODE_Stiff/manifest.json
- papers/literature_20260802/Port_Hamiltonian_Stability_Learning/manifest.json
- knowledge/civil-engineering-llm-wiki/comparisons/mtp-mechconv-v2-experiment-ledger.md
legacy_evidence_scope: 四篇论文的证据仅限各自本地 PDF 正文及 manifest；项目现状仅引用 experiment-ledger 的已记录结果。本文的迁移建议是明确标注的项目推论，不是论文结论。
legacy_tags:
- mechconv
- structure-preserving
- operator-learning
- constitutive-plugin
- stiff-dynamics
- port-hamiltonian
- scalability
evidence_scope: 四篇论文的证据仅限各自本地 PDF 正文及 manifest；项目现状仅引用 experiment-ledger 的已记录结果。本文的迁移建议是明确标注的项目推论，不是论文结论。
---

# 结构保持候选对 MechConv 的比较

## 结论先行

四篇论文分别提供空间离散、非局部本构、刚性时间推进和能量/稳定性方面的可迁移组件，但**都不能直接证明本项目的四项核心门槛**：

1. 精确的 \(kx+cv+ma=F\)（含项目质量/阻尼/边力组装）的端到端恒等式；
2. 更换本构后仍保持同一 backbone、同一训练协议并通过跨本构门；
3. 任意大图切成子图、处理接口后与全图训练/推理等价；
4. 在同一数据、硬件、完整本构和 EOM 计时范围内快于 Newmark-beta 或 FEM。

因此，本比较只能产生候选设计组件，不能把“structure-preserving”标签当作项目验收证据。

## 证据与可迁移性对照

| 候选 | 论文直接保证/展示 | 对 MechConv 最有价值的迁移点 | 不能替代的项目证据 |
|---|---|---|---|
| **SPON / SPON-MG** | FE 编码/解码、复杂网格、某些边界条件精确满足；SPON-MG 用稀疏 restriction/prolongation 和粗层消息传递；给出 FE 假设下的算子近似界 | 把矩阵边权、DOF 映射和多层图处理器分层；候选用于大图/子图接口 | 没有二阶 EOM 恒等式、跨本构试验、子图等价定理或 Newmark 速度门 |
| **PNO** | 以 ordinary state-based peridynamics 形式学习非局部本构；结构化输出声称保持客观性及线/角动量平衡；展示复杂材料与分辨率/几何泛化 | 作为可替换的局部/非局部 edge constitutive plugin；把几何不变量、horizon 权重、边力对称化交给插件 | 没有项目的 \(ma\)、阻尼和时间闭合；没有跨本构共享 backbone 证据、子图接口等价或 Newmark 对照 |
| **Structure-Preserving NODE** | \(du/dt=A_Lu+g(u)\)；Hurwitz 线性块、Lipschitz 非线性块、指数积分器；在 Robertson/KS 上展示刚性和长时稳定 | 将可解释线性动力学放入受控 proposal/高频残差分支，非线性留给 MechConv/本构插件 | 一阶 ODE 不是项目二阶 EOM；autoencoder 可能改变物理变量；没有边力、子图或跨本构项目门 |
| **Port-Hamiltonian** | 通过 \(J=-J^\top\)、\(R\succeq0\)、Hamiltonian 和端口结构表达能量/耗散；在已知平衡点附近给出局部稳定性结果 | 能量、耗散、平衡点和端口功作为诊断/先验；可包裹可替换本构 | 没有项目离散 \(kx+cv+ma=F\) 映射、任意子图能量通量、跨本构或速度门 |

## 逐项边界审计

### EOM：不能把守恒/稳定性等同于项目硬平衡

PNO 的内部力结构和 PH 的能量不等式都很有价值，但它们回答的是不同问题：前者约束非局部内力的几何/动量结构，后者约束能量储存与耗散。项目要求的是在每次端到端 forward 中用明确的矩阵和边力得到

\[
M a = F_{\mathrm{ext}}-C v-f_{\mathrm{int}}(u,v,\text{history}),
\]

并同时满足位移–速度–加速度的运动学关系。四篇论文均没有替项目完成这一步的离散推导和测量。

### 可替换本构：接口启发不等于跨本构证明

PNO 最接近“本构插件”，SPON 最接近“结构层/处理器分离”，NODE 最适合“线性/非线性分工”，PH 最适合“能量安全外壳”。一个可行的组合推论是：

```text
结构层: M, C, B, 图拓扑, 矩阵边权, 子图接口
    ↓
可替换边本构: linear / bilinear / Bouc–Wen / nonlocal plugin
    ↓
MechConv: Bᵀ·f_edge → f_int
    ↓
temporal-parallel EOM: v, u, a 与力平衡
```

但这只是架构假设。正式证据必须在相同 backbone hash、相同指标和相同速度范围下逐个替换本构，并报告平均与最差样本 R²、独立加速度/力残差。

### 大规模与子图：多层网格不等于子图等价

SPON-MG 的 restriction/prolongation 是最直接的规模扩展启发；PNO 的 horizon 邻域适合局部边计算；但二者都没有证明本项目所需的“切分—接口交换—拼接”与全图结果等价。必须额外验证：跨子图边是否保留、接口位移/速度是否连续、接口力是否反对称、粗层信息是否造成可接受的误差和延迟。

### 高频与速度：论文示例不能替项目背书

Structure-Preserving NODE 对刚性 ODE 的指数积分经验可指导高频分支设计，SPON 的有限元离散可提高空间表示能力；但论文没有使用本项目的结构动力学数据和完整 forward 计时。任何“快于 Newmark-beta/FEM”的结论都必须覆盖本构评估、MechConv、EOM、projection（若有）和数据搬运，且与同硬件基线比较。

## 推荐的下一轮候选优先级（仅设计，不是已验证结果）

1. **保留 temporal-parallel MechConv/EOM 主干**：上一轮硬冲量桥已经说明，替换最终状态闭环会破坏已训练 response proposal；本轮不应重复该类替换。
2. **先做 PNO-inspired constitutive adapter**：只替换/新增 edge plugin，保留节点力组装和 EOM；先用零初始化和冻结主干做小屏。
3. **再做 SPON-MG-inspired spatial hierarchy**：在小图上完成全图/子图接口等价 smoke 后，才进入大图训练。
4. **把 NODE/PH 限定为受控辅助分支**：NODE 只提供稳定的线性–非线性高频 proposal，PH 只提供能量/耗散诊断或安全正则；二者都不能绕过独立 EOM 验收。

## 必须执行的项目级验收清单

- 平均或最差样本的 `u/v/a/edge-force` R² 门；
- 逐样本独立加速度（非构造式）与独立力平衡残差；
- `M`, `C`, `B` 和矩阵边权的 shape、dtype、梯度、设备检查；
- linear/bilinear/Bouc–Wen 至少三类插件的同协议复测；
- 全图与子图接口的位移、速度、加速度、边力和功/能量差异；
- 低频/正常结构高频分桶；
- 完整端到端 forward 与 Newmark/FEM 的同硬件中位数和 P95。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
