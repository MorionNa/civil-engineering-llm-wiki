---
id: paper--zhou2025-learnable-physics-engine-results
title: Zhou & Feng (2025) — Learnable physics engine：结果与实验数字
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/zhou2025-learnable-physics-engine
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
legacy_methods:
- message-passing
- time-marching
- learning-rate-schedule
legacy_results:
- long-horizon-rollout
- extrapolation-ability
- parallel-computing
legacy_failure_modes:
- limitation
- extrapolation-ability
legacy_datasets:
- synthetic-data
legacy_reproducibility: low
legacy_tags:
- physics-simulation
- message-passing
- time-marching
- long-horizon-rollout
- parallel-computing
- extrapolation-ability
- scientific-machine-learning
legacy_sources:
- raw/papers/zhou2025-learnable-physics-engine.xml
evidence_scope: local workspace source record pending canonical verification
---

# Learnable physics engine：结果与实验数字

> 本页只记录 XML 中明确出现的实验设置和结果。论文比较的是 OSB-PD Drucker–Prager 参考模型与其图网络 surrogate；结果中的“长期”是连续 forward prediction（部分例子为 2000 步），不是对任意材料或无限时间的稳定性定理。

## 1. 训练与测试设置

所有 prediction experiments 使用一致的 MPNN2 结构：$\phi^2_e$ 有 5 个隐藏层，每层 30 个单元，隐藏层后使用 Tanh，输出规模为 $N_e\times2$；$\phi^2_v$ 结构基本相同，输出规模为 $N_e\times1$。优化器为 Adam，初始学习率 0.0005，每 100 个 epoch 将学习率乘以 0.1。

能量函数和屈服函数先在预处理数据上单独训练，再装配到完整 surrogate。能量训练的三个 Sobolev 权重均设为 $\gamma_1=\gamma_2=\gamma_3=1$。屈服函数使用不同 level-set 数据集分别训练：

| 训练目标 | XML 中给出的硬化关系 | 测试证据 |
|---|---|---|
| ideal elastic–plastic | $k_{DP}(\varepsilon^p)=k_{DP}$ | 训练损失与单轴拉伸卸载屈服函数预测均表现良好 |
| linear hardening | $k_{DP}(\varepsilon^p)=2k_{DP}(1+2\varepsilon^p)$ | 训练损失与单轴拉伸卸载屈服函数预测均表现良好 |

图 8 展示了能量函数训练 loss 和独立测试集结果；图 9 展示两种硬化数据的屈服函数训练 loss；图 10 是材料点单轴拉伸卸载时的屈服函数预测。XML 没有给出这些图对应的完整数值表、训练样本量、归一化和随机种子，所以这里不把曲线读成未报告的精确百分比。

## 2. Benchmark：板的单轴拉伸与卸载

完整 surrogate 被用于带卸载路径的板单轴拉伸。图 11 按顺序给出初始模型构型、弹性–理想塑性结果以及含硬化的弹塑性结果。

论文的文字结论是：

- 连续 forward prediction 中，累计等效塑性应变会出现轻微误差积累；
- 等效应力的预测仍保持较高精度，误差可忽略或很小；
- 这说明当前状态机能较好保持应力响应，但历史内变量是更敏感的长期误差载体。

这里没有公开单步误差曲线、最大应力误差或漂移率，因此不能补写精确数字。这个 benchmark 主要验证材料点/小域的路径依赖推进，尚不是跨材料或跨本构 OOD 测试。

## 3. Case 1：平面应变方板压头压入

### 3.1 几何、载荷与材料参数

| 项目 | XML 中的设置 |
|---|---|
| 几何 | 方板边长 1 m，厚度 0.1 m |
| 压头 | 刚性压头宽度 $a=0.2$ m |
| 最大竖向位移 | $\Delta=0.05$ m |
| 控制方式 | 位移控制，$\Delta=v\times n_t$，$n_t=2000$ |
| 硬化 | $k_{DP}(\varepsilon^p)=2k_{DP}(1+2\varepsilon^p)$ |
| 杨氏模量 | $E=1$ GPa |
| 泊松比 | $\nu=0.27$ |
| 黏聚力 | $c=40$ MPa |
| 摩擦角 | $\phi=35^\circ$ |
| PD 离散 | $dx=0.01$ m，$\delta=3.015\times dx$ |

### 3.2 对照量与结果

图 13 比较 PD code 与 surrogate 的：

- $u_x,u_y$ 位移场；
- $\sigma_e$ 等效/有效应力场；
- $\varepsilon^p$ 累计塑性应变场；
- 三类场的逐点绝对误差。

XML 明确报告：训练完成后继续 forward 预测 2000 步，最大绝对误差比参考值小 1–2 个数量级。这里的表述是相对数量级，不是一个可由文字恢复的单一百分比；因此应记录为“1–2 orders smaller”，而不是自行转换成某个 MAPE。

该结果同时说明：在同一 teacher 模型、同一材料和离散尺度下，学习的 energy/yield/graph 更新可在较长连续推进中保持空间场形态。但它没有隔离误差来自 MPNN、能量网络、屈服网络还是 PD 参考离散。

## 4. Case 2：圆形洞室开挖

### 4.1 工况与离散

| 项目 | XML 中的设置 |
|---|---|
| 初始应力 | $\sigma_x=\sigma_y=45$ MPa |
| 域几何关系 | $w=h=10d$，$d=13$ m |
| 硬化 | $k_{DP}(\varepsilon^p)=2k_{DP}(1+10\varepsilon^p)$ |
| 杨氏模量 | $E=2.6$ GPa |
| 泊松比 | $\nu=0.3$ |
| 黏聚力 | $c=10$ MPa |
| 摩擦角 | $\phi=30^\circ$ |
| 离散 | $dx=1.3$ m，$\delta=3.015\times dx$ |
| 材料点数 | 10,000 |

计算分两阶段：

1. $n_t<1000$：施加边界条件，建立初始原位应力；
2. $1000<n_t<2000$：删除图 14 红圈内的粒子，模拟洞室开挖。

### 4.2 结果

图 15 比较 PD code 和 surrogate 的位移、等效应力、累计塑性应变及绝对误差场。论文文字报告：

- 长距离 forward 预测的位移最大绝对误差约比实际值低一个数量级；
- surrogate 预测的等效塑性应变区比 PD code 更平滑；
- 平滑性被归因于替代后的神经网络屈服函数具有高阶连续、光滑的性质。

“更平滑”是正面数值表现，也可能掩盖尖锐屈服边界、局部化或剪切带的过度平滑，不能单独等同于更接近真实材料。此处尤其需要后续用局部塑性带宽度、峰值梯度和网格收敛来验证。

## 5. Case 3：边坡稳定分析

### 5.1 工况、边界与材料

| 项目 | XML 中的设置 |
|---|---|
| 边坡高度 | 20 m |
| 坡角 | $\beta=45^\circ$ |
| 土体重度 | 20 kN/m³ |
| 杨氏模量 | $E=20$ MPa |
| 泊松比 | $\nu=0.35$ |
| 黏聚力 | $c=4$ kPa |
| 内摩擦角 | $\phi=10^\circ$ |
| 本构 | 理想弹–塑性，$k_{DP}(\varepsilon^p)=k_{DP}$ |
| 屈服参数 | $\alpha_{DP}=\sin\phi/3$，$k_{DP}=c\cos\phi$ |
| 约束 | 左/右边界水平位移受限，底边完全约束 |
| 离散 | $dx=0.5$ m，$\delta=3.015\times dx$ |

### 5.2 结果

图 17 比较位移场及其绝对误差；图 18 比较静水压力 $P_e$、累计塑性应变及误差。论文报告：

- 自重作用下 surrogate 可以准确预测边坡位移场；
- 最大位移绝对误差约比实际值低一个数量级；
- 静水压力预测与 PD 计算相符；
- 塑性区分布能识别经典边坡失稳模式。

这个案例把验证从压头局部加载扩展到重力、自重和边界约束下的地质工程场景，但仍使用论文定义的理想 Drucker–Prager 材料，不能替代真实边坡的地下水、层理、裂隙和空间变异性分析。

## 6. Speed performance：GPU 规模对照

### 6.1 总体设置

作者用 100 个数值例子、每个例子 2000 个计算时间步，对比 proposed framework 和 OSB-PD model 的计算时间。硬件写明为 AMD 5950x CPU 与 NVIDIA RTX 3080 GPU。论文的总体结论是 proposed method 的计算速度约为 OSB-PD 的两个数量级优势，原因归于 GPU 的高性能并行计算。

### 6.2 材料点数缩放数字

XML 对图 19(c)给出的具体端点是：

| 材料点数 | PD physical model | surrogate |
|---:|---:|---:|
| 3,600 | 200 s | 10 s |
| 90,000 | 3,000 s | 45 s |

因此点数增加 25 倍时，PD 时间增加 15 倍，surrogate 时间增加 4.5 倍。按端点粗略计算，PD 的时间比为约 15 倍，surrogate 为约 4.5 倍；但论文没有给出每个点数下的完整曲线、显存峰值或经过同等 GPU 优化的 PD 基线。

“约两个数量级”应保留论文原话的近似性：具体端点的 200/10 与 3000/45 并非固定的 100 倍。速度优势还混合了图网络张量化、硬件差异、参考 PD 代码实现和可能不同的并行策略。

## 7. 结果的证据强度

| 结论 | 直接证据 | 可接受的表述 | 不应外推的表述 |
|---|---|---|---|
| 能量函数可学 | 图 8 独立测试集曲线 | 在论文数据域内拟合准确 | 对任意材料能量都准确 |
| 屈服面可演化 | 图 9–10，两类硬化和单轴卸载 | 能表示所训练的理想/线性硬化 | 已解决复杂循环/软化塑性 |
| 长期 forward 有效 | benchmark、Case 1–3，最长文字明确为 2000 步 | 在给定 OSB-PD 任务中保持场预测 | 任意长时间稳定或无漂移 |
| 全域场一致 | 图 13、15、17、18 | 位移/应力/塑性区与 PD 参考相符 | 与实验或现场真值一致 |
| GPU 更快 | 图 19，10–45 s 对 200–3000 s | 给定硬件和实现下具有规模优势 | 普适快于所有优化求解器 |

## 8. 复现提示与缺失数字

原文没有给出：训练/验证/测试样本数、归一化方式、epoch 总数、停止准则、随机种子、每步时间间隔、完整误差表、显存使用、PD 代码版本或公开权重。原文的数据可用性声明只是“Data will be made available on request”。因此结果页可以可靠记录 XML 中的设置和数量级，但不能补出图中曲线的精确像素读数，也不能声称有公开 benchmark 包。

## 关联页面

- [[zhou2025-learnable-physics-engine-analysis]] — 12 维总览与结果解释
- [[zhou2025-learnable-physics-engine-method]] — 训练目标、level-set 和 MPNN 细节
- [[zhou2025-learnable-physics-engine-critical]] — 结果边界、风险与后续实验
- [[learnable-physics-engine]] — 统一实体页
- [[message-passing-reach-contract]] — 检查长期图消息传播范围
- [[mp-pde]] — 长 rollout 图求解器对照
- [[cm-pinns]] — 本构一致性约束的相关路线

^[sources/papers/zhou2025-learnable-physics-engine]
