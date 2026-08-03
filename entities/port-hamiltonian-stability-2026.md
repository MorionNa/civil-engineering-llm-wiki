---
id: entity--port-hamiltonian-stability-2026
title: Structure- and Stability-Preserving Learning of Port-Hamiltonian Systems (2026)
type: entity
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-02'
updated: '2026-08-02'
confidence: low
legacy_source_files:
- papers/literature_20260802/Port_Hamiltonian_Stability_Learning/manifest.json
- papers/literature_20260802/Port_Hamiltonian_Stability_Learning/PDFs/Structure-_and_Stability-Preserving_Learning_of_Port-Hamiltonian_Systems.pdf
legacy_source_urls:
- https://arxiv.org/abs/2604.13297
legacy_arxiv: 2604.13297v1
legacy_pdf_pages: 8
legacy_sha256: 825476c8e6cdd7b313e227400fc7d62438a1901ff59b8007b6f5ddd6dc010ed4
legacy_evidence_scope: 仅依据本地 8 页 PDF 正文和对应 manifest；manifest 标记 Supporting Information
  未找到。论文直接证据覆盖 port-Hamiltonian 方程、非凸神经 Hamiltonian、多稳定平衡点、J/R/G 结构化参数化、局部稳定性定理及 Toda
  链/双摆示例；不外推到本项目的 MechConv、子图或速度门。
legacy_tags:
- port-hamiltonian
- passivity
- stability
- energy-based-learning
- multiple-equilibria
- symplectic-integrator
evidence_scope: 仅依据本地 8 页 PDF 正文和对应 manifest；manifest 标记 Supporting Information 未找到。论文直接证据覆盖
  port-Hamiltonian 方程、非凸神经 Hamiltonian、多稳定平衡点、J/R/G 结构化参数化、局部稳定性定理及 Toda 链/双摆示例；不外推到本项目的
  MechConv、子图或速度门。
---

# Structure- and Stability-Preserving Learning of Port-Hamiltonian Systems

> **论文**：Binh Nguyen, Nam T. Nguyen and Truong X. Nghiem, “Structure- and Stability-Preserving Learning of Port-Hamiltonian Systems”，arXiv:2604.13297v1（2026）。
> **核心对象**：学习具有能量储存、互联、耗散和端口输入的 port-Hamiltonian 系统，同时在指定平衡点保持局部稳定性。

## PDF 直接支持的内容

### 1. Port-Hamiltonian 结构

论文使用

\[
\dot x=(J(x)-R(x))\nabla H(x)+G(x)u,
\qquad
y=G(x)^\top\nabla H(x),
\]

其中 \(J=-J^\top\) 是互联矩阵，\(R=R^\top\succeq0\) 是耗散矩阵，\(H\) 是 Hamiltonian，\(G\) 是端口矩阵。由 skew-symmetry 可得能量变化中的互联项为零，耗散项不增能量，外部端口通过 \(u^\top y\) 输入/输出能量。

### 2. 非凸 Hamiltonian 与多平衡点

论文没有强制 Hamiltonian 全局凸，而是用正值神经网络乘以在已知平衡点附近激活的平滑 step function，使指定平衡点成为严格局部极小点，从而给出稳定性保证；多个不相交局部区域可对应多个孤立稳定平衡点。\(J\)、\(R\)、\(G\) 也通过反对称/半正定的结构化参数化学习。正文采用 symplectic Euler 或 Verlet 推进，并在 Toda 链和双摆上比较了模型轨迹与 PH-ICNN 基线。

论文的稳定性结论是条件化的：指定平衡点、Hamiltonian 的局部严格极小性以及相应耗散条件满足时，可得到局部稳定/渐近稳定结论；这不是无条件的全局预测精度证明。

## 对 nonlinear-PINN / MechConv 的可迁移启发

1. **能量/耗散插件**：可把能量储存与耗散作为本构插件的可选接口，让边本构输出来自局部能量梯度或耗散项，再由 MechConv 按矩阵边权汇总节点力。
2. **物理可诊断性**：除了 R² 和 EOM 残差，可记录离散能量变化、外力功、耗散非负性和指定平衡点回归，作为低/高频训练的额外诊断。
3. **多个工作点**：对具有多个稳定工作状态的结构，可借鉴局部平衡点包络，而不是把一个全局凸势函数强加给所有材料/工况。
4. **硬结构参数化**：反对称、半正定和正值构造可以作为可替换本构的安全外壳；但与项目的质量/刚度/阻尼矩阵和二阶状态必须通过显式映射连接。

## 明确限制与不可直接宣称的结论

- Port-Hamiltonian 方程一般可表示机械系统，但论文没有直接证明项目采用的离散 \(kx+cv+ma=F\) 组装恒等式；Hamiltonian 梯度、广义动量和项目节点/边力变量之间仍需建立严格映射。
- 论文假设已知稳定平衡点，并在两个小型系统上验证；它没有证明更换任意本构后共享 backbone 的跨本构稳健性，也没有提供本项目的 linear/bilinear/Bouc–Wen 统一协议。
- 正文没有证明大图子图切分与全图端口/能量交换等价；端口边界、跨子图能量通量和接口力仍是未解决的项目问题。
- symplectic Euler/Verlet 的使用不等于端到端预测一定快于 Newmark-beta；论文没有本项目同条件硬件、完整本构/EOM 范围的速度对照，也没有高频结构 R² 门。

## 项目使用建议

把 PH 方法作为**能量/稳定性诊断和可选本构先验**，不要直接替换 temporal-parallel MechConv 的状态与 EOM。只有在显式推导节点力、质量矩阵、阻尼和端口功之间的对应关系后，才允许进入小规模物理 screen。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[entities/index]]
- [[index]]
