---
id: comparison--mtp-mechconv-v2-mdof50-galerkin-pivot
title: MTP-MechConv v2：50DOF 运动学瓶颈与 Galerkin 粗层转向
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-07-31'
updated: '2026-07-31'
confidence: low
legacy_tags:
- neural-operator
- message-passing
- structural-dynamics
- equation-of-motion
- multilevel-method
- constitutive-model
- scalability
legacy_sources:
- ../../../../docs/literature/nature_retrieval_20260731_report.md
- ../../../../docs/literature/hard_matrix_scalability_literature_delta_2026-07-30.md
- ../../../../docs/plans/mtp_mechconv_v2_implementation_log_2026-07-31.md
---

# MTP-MechConv v2：50DOF 运动学瓶颈与 Galerkin 粗层转向

## 结论

50DOF 试验已经否定“继续调损失、学习率或 epoch 就能把当前局部架构推到
R² 0.9”的假设。当前最优全参数微调结果为：

| 指标 | 25–50DOF 局部适配前沿 `da` | 全参数 100 epoch `dc` |
|---|---:|---:|
| pooled R²(u) | 0.6198 | 0.7351 |
| pooled R²(v) | 0.5594 | 0.6774 |
| pooled R²(a) | 0.3543 | 0.3733 |
| pooled R²(edge force) | 0.4745 | 0.5841 |
| 独立外力重构 R² | 0.9524 | 0.9633 |
| 独立力平衡 relative RMS | 0.2182 | 0.1915 |
| 90 序列前向时间 | 2.388 s | 2.390 s |

`dc` 的训练损失从 16.30 单调下降到 12.82，但加速度和独立物理指标只小幅
改善，说明这不是单纯优化未收敛。

## 独立本构回放排除了 Bouc–Wen 离散器

评价时完全丢弃 learned edge-state history，只用预测 \(u,v\) 从零状态执行
同一个因果 Bouc–Wen Heun/RK4 回放：

- 真实 \(u,v\) 上 edge-force R² = 0.999997；
- `da` 预测 \(u,v\) 上 edge-force R² = -2.0936，relative RMS = 1.7589；
- `dc` 预测 \(u,v\) 上 edge-force R² = -1.1179，relative RMS = 1.4553。

因此本构公式和时间离散本身正确。learned edge-state head 的正 R² 是在补偿
运动学误差；它不能作为跨本构成功证据。后续模型选择必须同时报告 learned
edge force 和 independent causal replay edge force。

## 为什么固定 halo 的局部网络存在结构性上限

线性化频域响应为

\[
x(\omega)=
\left(K+\mathrm{i}\omega C-\omega^2M\right)^{-1}F(\omega).
\]

\(K,C,M\) 可以是稀疏矩阵，但动态柔度矩阵的逆通常稠密，低阶模态具有全局
支撑。当前四个 fine MechConv block 加一层局部 projection 只有约六跳依赖；
它可以改变局部矩阵多项式的系数，却不能感知六跳以外的刚度、边界和动态
状态。

canonical node context 解决了“局部同构节点不知道自己在哪里”，但没有传递
远端动态信息。它带来的改善是真实的，却不足以解决任意结构和任意规模的
全局动力耦合。

## 新优先架构：Galerkin 层级 MechConv

采用归一化分片常数延拓 \(P\)，满足 \(P^\top P=I\)，并令 \(R=P^\top\)。
每一层严格从真实结构矩阵构造：

\[
M_c=P^\top M P,\qquad
C_c=P^\top C P,\qquad
K_c=P^\top K P.
\]

粗层仍使用矩阵边 MechConv；共享参数递归作用到顶层节点数不超过约 6–8。
延拓后的粗修正只进入运动学 hidden：

\[
h_f^\star=h_f+
g\,P\Phi_c(Rh_f;M_c,C_c,K_c),
\]

其中 \(g\) 零初始化。构件力仍只由可替换本构插件产生，加速度仍由

\[
Ma+Cv+f_{\mathrm{int}}=F_{\mathrm{eff}}
\]

硬构造。因此粗层不是 FE 后处理，也不直接制造“更容易平衡”的力。

这对应局部平滑加粗网格修正：

\[
A^{-1}\approx S_{\mathrm{local}}+P A_c^{-1}R.
\]

fine 路径负责局部/高频，粗路径负责固定六跳无法表达的全局低模态。该设计与
[[dolean2024-multilevel-fbpinn-analysis]] 的“粗层恢复全局通信、细层保留局部
高频”机制一致，但额外保留真实矩阵边与硬结构动力平衡；也遵守
[[mtp-mechconv-v2-grill-audit]] 对 coarse path 的限制。

## 已实现和仍未证明的部分

已完成：

- 稀疏消息形式与显式 \(P^\top K P\) 数值逐位一致；
- 对称 fine operator 的 coarse operator 保持对称；
- 限制和延拓互为转置；
- 500 节点层级存储为 \(O(N+E)\)；
- 粗层跨层共享权重，参数量不随层数增长；
- 零初始化时逐位复现父模型；
- coarse hidden 修正不破坏硬 EOM；
- 真实 `dc` 检查点的单步反向传播有限。

当前 `dd` 只做 50DOF 全图、25 epoch 机制筛选。它不能证明子图扩展性。
若机制门槛通过，必须实现两阶段通信：

1. fine 子图独立生成 core hidden/summary；
2. 只在小型 coarse graph 上汇总、交换并广播。

全局低阶动力响应与“所有子图永久零通信”在数学上不兼容。允许一次稀疏粗层
summary 通信，是保留子图训练同时表达稠密动态逆的最低代价；这仍是一个
端到端网络前向，不是 Newmark/FEM 校正。

## `dd` 的否证门槛

epoch 25 必须同时达到：

- pooled R²(u/v/a) 至少 0.75/0.75/0.65；
- independent causal replay edge-force R² 至少 0.60；
- independent force relative RMS 不高于 0.15；
- u/v/a 平均 R² 相对 `dc` 至少提高 0.10；
- high-modal 任一项相对父模型下降不超过 0.02；
- 因果本构直接审计全部有限。

未通过即否定“当前 Galerkin 粗层实现解决了主导瓶颈”，不得靠扩大粗层或延长
epoch 救回。

## 关联

- [[mtp-mechconv-v2-experiment-ledger]]
- [[mtp-mechconv-v2-grill-audit]]
- [[multilevel-fbpinn]]
- [[message-passing-reach-contract]]

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.
