---
id: comparison--reproduction-failure-prevention-contract-2026-08-03
title: 复现失败预防合同：从源码到可引用结论的准入门
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
legacy_tags:
- comparison
- limitation
- physics-constraint-weight-tuning
- finite-difference-error
- cross-domain-generalization
- architecture-selection
- equation-of-motion
legacy_sources:
- ../../../../docs/plans/experiment_plan.md
- ../../../../docs/plans/current_remote_experiments.md
- ../../../../reproductions/step-integrator/README.md
- ../../../../reproductions/dynamic-pignn/整理运行报告.md
- ../../../../reproductions/phylstm/README.md
- ../../../../reproductions/graph-phygru/README.md
---

# 复现失败预防合同：从源码到可引用结论的准入门

本页把当前项目已经暴露的错误模式写成可执行合同。它的目的不是增加形式，而是让未来的实验在花费远程 GPU 时间以前就能发现 shape、设备、损失、数据泄漏、独立核验和产物缺失问题。未满足合同的结果可以保留为诊断记录，但不得写成“复现成功”或作为架构晋级依据。

## 1. 总原则：证据先于结论

每个结果必须回答四个问题：

1. **复现了什么**：论文/源码、commit、方程、数据集和训练协议是什么？
2. **模型预测了什么**：位移、速度、加速度、边力、内部状态还是仅仅一个构造的 residual？
3. **谁独立复算**：导数、恢复力、边界、能量和 rollout 是否由训练图之外的实现复算？
4. **在哪些条件下失效**：最差样本、最高频带、换结构、换时间步、换 halo 和自由运行分别如何？

## 2. 源码与数据准入合同

- 保存论文原文/版本、DOI 或 URL、下载日期、文件 hash；原始材料放在 `raw/`，分析页只引用，不覆盖原文。
- 保存官方仓库 URL、commit/tag、运行环境和本地适配差异。官方代码不能运行时，必须把缺失依赖、路径、数据和层数差异写进 negative knowledge。
- 固定并记录质量矩阵、阻尼、刚度/本构参数、激励、时间步、采样率、窗口长度、观测点、train/validation/test split 和随机种子。
- 明确 `full-resolution` 与 `downsampled` 是两个不同实验身份；禁止把降采样 smoke 的好结果写成论文协议结果。
- 明确哪些量是标签、哪些量来自模型回代、哪些量由独立参考求解器产生。由预测量构造的 force-balance 必须标为 constructed check。

## 3. 运行顺序：先小测试，再远程正式实验

### 3.1 本地最小 smoke

正式训练前必须在本地完成最小而非实质性训练的检查：

- 一个 batch 的输入/输出 shape、dtype、device 和梯度；
- 一次前向与一次 loss，确认所有子图能 stitch、固定 DOF 和 active DOF 没有混合；
- 一次独立 residual/constitutive 调用，确认单位、时间步和边索引；
- 一个极小 rollout，检查 NaN、零响应分支、边界漂移和显存峰值。

### 3.2 正式训练

非平凡训练只在项目配置的远程服务器 `senna@172.22.53.130` 上执行，代码同步和运行目录固定为 `/home/senna/nonlinear-pinn-next`；单卡任务串行排队，服务器不可用时不得静默退回本地长时间训练。每次 run 必须保存 resolved config、主机/运行目录、PID（如可得）、stdout/stderr、最终 metrics、checkpoint 和 prediction artifacts。

## 4. 独立物理门：五件事缺一不可

1. **独立导数门**：用独立有限差分或参考积分器从预测 (u) 重建 (v,a)，并报告时间步、边界阶数和误差。
2. **独立 EOM 门**：用独立矩阵组装和独立 constitutive evaluation 检查 (Ma+Cv+f_mathrm{int}-F_mathrm{eff})，不能把网络输出的 (a) 再代回去制造闭环。
3. **边界/初值门**：固定 DOF、active/free DOF、初位移、初速度和反力分别统计；反力不能混入自由节点 accuracy。
4. **状态/本构门**：对于 Bouc-Wen、隐变量或边力，单独检查 state trajectory、滞回环、恢复力和跨激励一致性。
5. **稳定性/能量门**：分别检查 teacher、短 rollout、长 rollout、能量漂移、被动性和 NaN；一个 teacher 指标不能替代其余门。

## 5. 常见失败模式 → 预防动作

| 失败模式 | 为什么会误导 | 以后强制执行 |
|---|---|---|
| 用预测加速度构造 force-balance | 代数闭环天然容易得到高 (R^2)，不代表运动学或本构力正确。 | 由预测位移独立差分得到 (a)，并保留独立 residual、相对 RMS、p95/max。 |
| 把 fixed reaction 混入 global force accuracy | 反力可能主导分母，使指标虚高或变成负数。 | 只在 active/free DOF 报 force accuracy；reaction 单列。 |
| 用 pooled 指标掩盖最差样本 | 高平均值可能掩盖高频、顶层、边界或单个激励失败。 | 同时报告 mean、median、p95、max、worst-case 和每个物理量。 |
| downsample 结果冒充论文复现 | 时间分辨率改变了导数误差、频带和训练难度。 | 结果名称带 resolution；full-resolution locked test 通过前不能晋级。 |
| 只监督节点位移却宣称边力/本构正确 | 内部状态存在 null space，多组边力可能产生同一节点响应。 | 加 edge force/constitutive/energy/sensor 或跨激励可辨识性测试。 |
| teacher 很好但 rollout 发散 | 一步拟合没有约束误差累积和输入分布漂移。 | scheduled sampling、rollout loss、自由运行曲线和能量门分开记录。 |
| 真值历史校准成功 | 它只说明在给定真实历史上可拟合，不说明模型能从自己的预测继续走。 | 校准历史只作 L2/L3 证据；另做自由 rollout 和 locked test。 |
| 不同层数/数据/路径的官方代码直接横比 | 实现差异变成了方法差异。 | 逐项记录 code diff；先复原论文协议，再单独报告工程适配。 |
| 只保存最后一个数字 | 结果无法定位、复核、回滚，也无法解释失败。 | 按第 7 节保存完整 run bundle；缺项即 fail-closed。 |

## 6. 图、halo 和结构迁移合同

- 先证明 full graph 的矩阵端点组装正确，再讨论稀疏/halo 加速；稀疏消息传递不能用“看起来相似”替代 reach 和边界隔离测试。
- 每个子图保留全局节点/边 ID、局部编号、固定/active 标记和 halo 标记；禁止跨子图编号碰撞。
- 对 full graph 与 halo graph 使用同一 checkpoint、同一输入、同一时间步，逐节点/逐边比较输出、残差和梯度；先过数值等价门，再做速度/显存比较。
- 换拓扑、换自由度和换频带时，至少保留一个 full-resolution baseline；5DOF 的加速度和顶层边力不能被 displacement 的好指标覆盖。
- 任何从 FBPINNs、MP-Neural-PDE、SGNO、APEBench、PRNN 或 PI-GNN 迁移的代码都必须标注 transfer boundary，不能直接继承其“可扩展”结论。

## 7. 可引用 run bundle

每个正式 run 目录至少包含：

```text
resolved_config.yaml
environment.txt
git_commit.txt
host_and_run_dir.txt
pid.txt                  # 若可得
stdout.log
stderr.log
metrics.json
predictions.npz          # 或等价的可读预测文件
checkpoint.pt            # 或等价模型文件
independent_audit.json
failure_notes.md
```

`metrics.json` 必须包含数据划分、resolution、seed、训练步数、各物理量指标、worst-case/p95，以及独立 residual 的定义。任何异常退出、缺 checkpoint、缺预测、审计失败或配置不可解析的 run 都标记为 `failed`，不能只留下“最好的一次”。

## 8. 晋级矩阵

| 等级 | 含义 | 最低条件 |
|---|---|---|
| P0 | 文献/源码线索 | 来源、范围和局限已记录。 |
| P1 | 可运行实现 | 本地 smoke、配置和代码差异已保存。 |
| P2 | 可复现实验 | 正式 run bundle 完整，数据协议固定，指标可复核。 |
| P3 | 物理可信候选 | 五个独立物理门通过，且报告最差样本和失败边界。 |
| P4 | 可迁移/可引用结论 | full-resolution locked test、跨结构/频带/halo 验证、独立复核和 checkpoint 全部通过。 |

当前方案的具体分层见 [[reproduction-schemes-inventory-2026-08-03]]；外部 GitHub 迁移边界见 [[cycle35_github_prnn_pignn_refresh_20260803]]。

## 9. 每次新复现提交前的短清单

- [ ] 论文、代码、数据和 commit 已固定并写入 frontmatter/run bundle。
- [ ] full/downsample、时间步、观测比例、split 和 seed 已写清。
- [ ] 本地 shape/device/loss/subgraph/最小 rollout smoke 通过。
- [ ] 正式训练在指定远程路径串行完成，日志、checkpoint、预测和 config 齐全。
- [ ] 独立导数、独立 EOM、active/reaction、状态/本构、rollout/能量均有结果。
- [ ] mean 与 worst-case/p95 同时通过预设门槛；未通过项写入 negative knowledge。
- [ ] 只有达到相应 P 等级后，才把结果写入论文页、比较页或项目结论。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.
