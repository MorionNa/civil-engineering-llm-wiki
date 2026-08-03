---
id: comparison--mtp-mechconv-v2-experiment-ledger
title: MTP-MechConv v2 独立物理实验账本
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
- hard-constraints
- scalability
- constitutive-model
legacy_sources:
- ../../../../docs/plans/mtp_mechconv_v2_implementation_log_2026-07-31.md
---

# MTP-MechConv v2 独立物理实验账本

## 为什么旧 force-balance 分数不能作为预测指标

旧时间并行模型用
\[
a=M^{-1}(F-Cv-f_\mathrm{int})-\Gamma a_g
\]
构造加速度，因此再计算 \(Ma+Cv+f_\mathrm{int}\) 必然回到外力。这能证明程序中的动力平衡闭合，却不能独立证明 \(v\)、\(a\) 或本构力是正确的。v2 将这个量标记为 constructed check，并用
\[
\hat F_\mathrm{ind}=M\,\mathrm{BDF2}(v)+Cv+f_\mathrm{int}
\]
作为独立预测量。

## 20260731bq：扩大高频教师覆盖

总体 R² 已达到位移 0.9552、速度 0.9702、加速度 0.9347、边力 0.9705，但最差位移 R² 只有 0.7439。高模态频带的四项得分为 0.8085–0.8772，仍低于 0.9。构造平衡残差为 \(5.92\times10^{-8}\)，但加速度运动学相对 RMS 为 0.1149。

结论：增加训练频谱覆盖有效，但只带来小幅高频增益；不能把 constructed force-balance R²=1 当成严格物理已经通过。

## 20260731br：同一检查点的 v2 独立复评

独立外力重构的总体 R² 为 0.9692，最差样本 R² 为 0.9491，高频得分为 0.9593；然而独立力平衡相对 RMS 为 0.1755，\(\mathrm{BDF2}(v)\) 与 EOM 加速度的相对 RMS 为 0.1208，均未达到 0.05。

这组结果说明 R² 和相对 RMS 必须同时保留：R² 能确认曲线相关性，但会弱化幅值尺度误差；相对 RMS 能阻止“形状相似但动力幅值不闭合”的模型过关。

## 已实现的架构修正

- 固定物理时间坐标，消除改变预测时长导致历史前缀变化的问题。
- 2DOF 桁架、3DOF 平面框架、6DOF 空间框架的矩阵边线性通路。
- 标量 linear/bilinear/Bouc-Wen 和平面框架双状态 Bouc-Wen 因果插件。
- 本构切换时复用超过 90% 参数的形状兼容迁移。
- O(N+E) 稀疏粗层交换与完整依赖簇 halo，无全图稠密 gather。
- 逐样本独立力残差损失：训练目标 4%、认证门槛 5%，并对每个 batch
  最差 20% 样本施加 hinge，避免 pooled RMS 掩盖失败记录。
- grouped halo 打包时保持各子图粗簇编号完全隔离。
- 同时保存总损失最佳与物理约束词典序最佳 checkpoint。

## 与文献证据的对应

[[message-passing-reach-contract]] 支持显式审计传播 reach，但不能替代 halo 等价测试。[[multilevel-fbpinn]] 支持用多层局部子域改善长程通信，但粗层仍必须保持稀疏、不能直接生成物理构件力。[[unrolled-training]] 支持在训练中暴露闭环误差；本项目将其落实为因果本构扫描和独立运动学残差，而不是在推理端追加求解器。

## 20260731bs：raw50 诊断结果

pooled 位移/速度/加速度/构件力/独立外力 R² 为
0.9552/0.9687/0.9241/0.9658/0.9882，最差样本五项也均大于 0.8。
但独立力相对 RMS 仅从 0.1755 降到 0.1088，独立加速度相对 RMS
从 0.1208 降到 0.0748；最后 50 轮只再改善约 2.2%。高模态构件力
得分下降到 0.7734。raw50 能移动 Pareto 前沿，但已在严格物理门槛
上方停滞，不能继续靠提高固定权重解决。

## 第二轮 grill 后的修正

- 真值因果 BDF2 离散误差为 pooled 0.01313、p95 0.01419，因此
  4% 训练目标与 5% 认证门槛具有可达余量。
- 新 loss 直接使用
  \(M\mathrm{BDF2}(v)+Cv+f_\mathrm{int}-F_\mathrm{eff}\)，并按每个样本
  的有效外力 RMS 归一化。
- hinge 对最差 20% 样本计算，训练目标留出 1 个百分点泛化余量。
- grouped sparse-coarse 的跨子图粗簇污染已修复，并通过独立执行与
  三子图打包的一致测试。
- 高频 weight=5 暂停；独立物理通过后才从 weight=2 做单因素短筛。

## 当前决策

- `official90` 继续仅作开发集。
- `20260731bu` 正在验证逐样本独立力尾部 hinge；主 checkpoint 按
  “物理约束优先、总损失次优”选择。
- 架构与损失冻结后再生成一次性 locked test，并执行跨本构、
  50/500/5k/50k 自由度和 batch=1 公平速度认证。

## 20260731bu：逐样本力平衡尾部约束结果

`bu` 的 pooled 位移/速度/加速度/构件力 R² 为
0.9540/0.9676/0.9208/0.9641，最差样本位移 R² 为 0.8011，因此响应精度
满足预先约定的 worst-case 路线。独立力平衡 relative RMS 仍为 0.0993，
p95/max 为 0.1146/0.1293；独立加速度 relative RMS 为 0.0683。高模态构件力
R² 只有 0.7642。固定二次罚项在 150 epoch 末仍缓慢下降，但未过 0.05 门槛，
故不能作为最终候选。

## 20260731bw：容量与约束算法的定向后继

后继方案从 `bu/model_best_constraint.pt` 出发，解冻第 3、4 个时域块，将学习率
降为 `2.5e-5`，并对 \(g=\max(r_\mathrm{force}-0.04,0)\) 使用
\(\lambda g+\rho g^2/2\) 与 \(\lambda\leftarrow\lambda+\rho g\)。
远程正式启动前 151 项测试全部通过；测试覆盖矩阵边权、本构插件、halo 隔离、
节点预算、逐样本物理损失和高频窗函数。训练 PID 与控制器 PID 均单独保存。

## 关联页面


- [[mtp-mechconv-v2]]
- [[mtp-mechconv-v2-grill-audit]]
- [[mtp-mechconv-v2-evidence]]
- [[multilevel-fbpinn]]

## 20260731bx: staged AL is a rejected Pareto path

The complete nine-checkpoint sweep found no acceptable intermediate state.
Independent force RMS decreased monotonically from 0.09717 at epoch 25 to
0.07532 at epoch 150, but response and high-modal scores decreased with it.
The staged dual schedule therefore does not solve the shared-representation
conflict.

## 20260731ca: architecture-isolated consistency adapter

The next controlled experiment freezes the `bu` MechConv backbone and every
existing head.  A separate zero-initialized 873-parameter causal adapter maps
the defect `BDF2(v_base)-a_base` to a bounded low-pass velocity correction.
The corrected velocity is integrated to displacement, the constitutive plugin
is evaluated again, and hard EOM acceleration is assembled again.  This keeps
matrix-edge MechConv, halo decomposition, and constitutive replaceability
unchanged while giving the independent physics defect its own parameter
subspace.

## 20260731ca: local adapter is stable but under-reaching

At epoch 50, independent force RMS was 0.09880 versus 0.09929 for `bu`.
Correction RMS was only 0.181% of predicted velocity, and high-Nyquist
correction energy was negligible.  The experiment therefore preserved
accuracy but failed the preregistered 15% improvement rule.  The causal
five-step filter lacks the long memory needed to invert an acceleration
defect into a trajectory-level velocity correction.

The next controlled successor emits an acceleration correction and integrates
it causally inside the end-to-end graph.  It adds only one scalar direct-defect
gain, for 874 total trainable parameters.

## 20260731cb–cd：积分适配器分支终止

`cb` 将局部速度修正改为网络内加速度积分，但 epoch 25/50/75 的独立力
relative RMS 仅为 0.09894/0.09874/0.09877，相对 `bu` 的 0.09929 改善不足
1%。`cc` 的固定增益扫描也只得到不足 1% 的改善，并损害最差样本位移精度。
这说明受限速度适配器不是动力平衡残差的有效逆算子。

## 20260731ce–cf：失败投影定位本构切线问题

直接使用 BDF2 积分会累积低频漂移；采用离散
`D_BDF2 + C/M + K/M I_trap` 的块对角动态逆仍然失败，因为 Bouc-Wen
在固定预测滞回状态时的位移切线是 `alpha*K`，不是完整弹性刚度 `K`。
本构插件接口因此新增 `projection_stiffness_scale`：线性为 1，双线性为
屈服后刚度比，Bouc-Wen 为 alpha。网络主体不感知具体本构类型。

## 20260731cg–ch：切线感知投影首次通过核心物理门槛

单层、relaxation=0.60 是预注册窄筛中最小的物理通过点。pooled
位移/速度/加速度/构件力 R² 为 0.91028/0.95704/0.92003/0.96392，
独立动力平衡 R² 为 0.99759。独立力 relative RMS 的 mean/p95/max 为
0.04908/0.05972/0.06436；独立加速度为 0.03377/0.04369/0.04576。
由网络输出重新组装的动力方程残差为 5.84e-8，且整个投影位于一次前向
推理内部。其 halo 传播半径为 6，official90 前向时间为 0.578 s。

当前主要短板是高模态构件力 R² 仍为 0.76432。`ci` 冻结 MechConv、
投影层和本构插件，只训练输出头及高频残差头，使网络学习对固定物理投影
进行前馈预补偿；这是一项与架构主体隔离的高频恢复实验。

## 20260731ci–cm：输出头恢复仅形成微小 Pareto 改善

仅训练既有输出头后，epoch25/50 的 pooled 位移 R² 提高到
0.92144/0.92547，但独立力 RMS 变为 0.05017/0.05149，越过 0.05 门槛；
高模态构件力也只提高到 0.76727/0.76961。基线与 epoch25 的权重插值
alpha=0.75 是较稳健的暂定点：pooled 位移/速度/加速度/构件力 R² 为
0.91964/0.95955/0.92078/0.96407，独立力 R² 为 0.99756，独立力/加速度
RMS 为 0.04942/0.03400。90 条序列一次前向耗时 0.5767 秒。

## 50DOF 烟雾测试：能分图运行不等于能跨规模预测

5DOF checkpoint 在 50DOF、17步图上可完成 grouped-halo 推理，但
加速度 R² 仅 0.729，构件力 R² 为 -439，独立物理 RMS 约 0.202。
主要原因是非因果整轨本构插件由 edge head 预测 Bouc-Wen 内变量，
该尺度没有在跨规模图上训练。后续认证必须区分“任意规模可执行”和
“任意规模精度”，并比较硬因果本构扫描或跨规模子图训练。

## 20260731cn：最后一次 official90 高频结构证伪

新增参数小于1%的零初始化 edge-local 适配器，直接读取归一化相对位移
与速度的因果带通特征，只修正本构状态 logits，不直接预测构件力。
全部 MechConv、极点、既有 heads、本构和投影冻结。epoch25 若高模态
构件力 R² 小于 0.7843，或独立力 RMS 大于 0.0505，则永久终止该分支。

## 20260731cp–cq：规模与速度正式认证未通过

alpha=0.75 模型在 50/500/5k/50k DOF 上均能按 6-hop halo 执行，但
50k 前向为 1.511 秒，优化向量化 Bouc-Wen RK4 仅 0.132 秒，模型慢约
11.4 倍。构件力 R² 分别为 -67/-742/-7483/-74891，独立物理 RMS 也均
大于 0.05。因此目前只能声称“任意规模可执行”，不能声称任意规模精度
或速度优势。

把预测滞回内变量替换为硬因果本构扫描，在 17 步短烟雾中将 50DOF
构件力 R² 提高到 0.892，但 65 步正式结果仍为负，且 50k 耗时增加到
2.158 秒。节点位移 R² 高并不保证层间位移差和滞回力准确。

## 20260731cr–cs：跨规模子图训练

`cr` 使用训练区十条地震动的确定性增强，由独立 RK4 生成 40 条精确
50DOF Bouc-Wen 轨迹，不包含测试地震动。`cs` 在 5 个 10-core halo
子图上训练最后两层 MechConv 和响应 heads；warmstart 保留目标 50DOF
图自己的响应及构件属性尺度。batch=5 时首 epoch 约 8.2 秒。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.
