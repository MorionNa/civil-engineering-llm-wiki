---
id: comparison--mtp-mechconv-v2-v20-rk4z-design-evidence
title: MTP-MechConv v2：V20-RK4Z 设计证据与限制
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# MTP-MechConv v2：V20-RK4Z 设计证据与限制

## 为什么从 V19 转向 V20

V19 的频域 Thomas-ZCQ 与同一梯形离散的顺序解在约 `1e-12` 量级一致，但它不能回放当前显式 RK4 真值的加速度；这证明失败源是离散不一致，而不是 FFT 或三对角求解误差。V20 不再更改真值，而是把教师的四阶段 RK4 精确提升为线性时不变状态递推，再在时间频域求解。

## 文献采用矩阵

- Leveque 等的 all-at-once RK 工作支持“从 RK 离散本身构造并行时间系统”，但其迭代预条件与主要的抛物/Stokes 试验不能直接证明本项目振动问题的一步速度。
- Gander 与 Palitta 的 ParaDiag 支持循环结构加低秩校正的时间并行思想，但 Krylov/SMW 迭代不是本项目端到端单次推理的直接答案。
- Caliari 等的 REXII 证明振荡问题中的复移位线性系统可以在 GPU 并行，但对象是线性纯虚谱系统，不能替代非线性本构学习。
- Melenk 与 Rieder 的 RK-CQ 超收敛结论依赖 Radau IIA、拉普拉斯域和数据正则性假设，不能直接迁移到经典显式 RK4。

因此，V20 采用“RK 离散同构 + 频点并行复移位稀疏解”的交集，不采用任何论文未证明的跨问题速度或精度结论。

## Grill 修正后的核心

网络不预测节点等效力，而预测每条边、每个 RK 阶段相对参考刚度的残差：

```
r_e,s = f_e,s - K0_e q_e,s
g_s = F_s - B^T r_s
```

`B^T` 由 MechConv 完成，因此外力符号、作用反作用和矩阵边权重不会被网络隐式学习。线性参考本构对应严格的零残差固定点。

最终网格力由可替换插件计算，最终加速度硬构造：

```
a = M^-1(F-Cv-B^T f_grid)
```

这严格满足用户要求的最终动力平衡。阶段残差与插件阶段力的一致性是训练约束，因为在无迭代的一步推理中把它做成硬闭环会产生循环依赖。

## 不得过度声称

- 精确阶段残差驱动的结果只能叫 `oracle carrier ceiling`，不能叫模型精度。
- 本构可替换意味着 carrier、MechConv 和 tensor 协议不变，允许替换插件/adapter 并重新训练；不是零样本跨本构。
- 首轮只支持对角或固定小块局部质量；一般 consistent mass 会引入额外全局质量求解。
- 标量剪切链 Thomas 只能证明乐观成本。任意规模必须由通用 owner/separator、矩阵边和 513 节点实测证明。
- 全局 contour 只有数值因果性，必须通过冻结的后缀扰动、JVP 和双长度审计。

## 当前状态

V20 只解锁解析 M0，未解锁训练。预注册与完整门槛见 `docs/plans/rk4z_lifted_stage_mechconv_v20_preregister_2026-08-01.md`。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
