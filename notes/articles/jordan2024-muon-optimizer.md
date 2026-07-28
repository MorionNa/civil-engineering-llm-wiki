---
title: "Keller Jordan (2024) — Muon：面向神经网络隐藏层的矩阵正交化优化器"
created: 2026-07-28
updated: 2026-07-28
type: article
tags: [optimizer, muon, matrix-orthogonalization, newton-schulz, stochastic-gradient-descent, sgd-momentum, nesterov-momentum, adamw, shampoo, preconditioning, spectral-norm, training-efficiency, sample-efficiency, wallclock-efficiency, large-language-model]
sources: [raw/articles/jordan2024-muon-blog.pdf]
confidence: high
---

# Muon: An optimizer for hidden layers in neural networks

> **作者：** Keller Jordan（文末 citation 同时列出 Yuchen Jin、Vlado Boza、Jiacheng You、Franz Cesista、Laker Newhouse、Jeremy Bernstein）  
> **来源类型：** 技术博客，不是同行评审论文  
> **发布日期：** 2024-12-08；当前 PDF 还包含 2025-07-12 后补的历史关联小节  
> **原文：** https://kellerjordan.github.io/posts/muon/  
> **一句话定位：** Muon 把隐藏层二维权重的 SGD-momentum 更新矩阵用低精度 Newton–Schulz 迭代近似正交化，使各奇异方向获得更均衡的更新尺度；embedding、输出层以及标量/向量参数仍使用 AdamW。

## 1. Muon 是什么

Muon 全称 **MomentUm Orthogonalized by Newton–Schulz**。它只针对神经网络隐藏层中的二维矩阵参数，基本更新为：

$$
G_t=\nabla_\theta \mathcal L_t(\theta_{t-1}),
$$

$$
B_t=\mu B_{t-1}+G_t,
$$

$$
O_t=\operatorname{NewtonSchulz5}(B_t),
$$

$$
\theta_t=\theta_{t-1}-\eta O_t.
$$

因此 Muon 不是从头构造全新梯度，而是：

```text
SGD momentum update
    → matrix normalization
    → 5-step Newton–Schulz post-processing
    → approximately semi-orthogonal update
    → parameter update
```

后续公共实现默认使用 Nesterov-style momentum；博客指出，它在作者测试的所有情形中都略优于普通 SGD momentum。

## 2. 参数适用范围

Muon 的使用范围是其设计的一部分，而不是实现细节：

| 参数类型 | 推荐优化器 |
|---|---|
| 隐藏层二维权重矩阵 | Muon |
| Transformer 的 Q、K、V | 分开应用 Muon |
| embedding | AdamW |
| 最终 classifier / LM head | AdamW |
| bias、LayerNorm scale 等向量或标量 | AdamW 等标准优化器 |
| 4D 卷积核 | 展平后三个维度，将其视为二维矩阵后使用 Muon |

博客特别强调：即使 embedding 和输出头通常也是二维矩阵，经验上仍应使用 AdamW；将 QKV 合并为一个矩阵进行正交化也不如分别处理 Q、K、V。

## 3. 核心操作：把更新变成最近的半正交矩阵

设 momentum 更新矩阵的奇异值分解为：

$$
G=USV^T.
$$

理想正交化操作为：

$$
\operatorname{Ortho}(G)=UV^T,
$$

它等价于寻找 Frobenius 距离下最接近 $G$ 的半正交矩阵：

$$
\operatorname{Ortho}(G)=
\arg\min_O\|O-G\|_F,
$$

并要求 $O^TO=I$ 或 $OO^T=I$，取决于矩阵是高矩阵还是宽矩阵。

这一操作保留更新矩阵的左右奇异向量，却把不同奇异值重新拉到相近尺度。换言之，Muon 主要改变“沿每个奇异方向走多远”，而不是改变这些方向本身。

## 4. 为什么可能有效

博客给出的经验观察是：Transformer 二维参数的 SGD-momentum 和 Adam 更新矩阵通常条件数很高，近似低秩，少数方向支配绝大部分更新，而大量幅值较小的“稀有方向”可能仍对学习有用。

作者的工作假设是：

- 普通更新过度集中在几个大奇异值方向；
- 正交化压平奇异值谱；
- 小奇异值方向因而被相对放大；
- 神经元或通道获得更均衡的学习信号。

这仍是**解释性假说**，不是博客中已经证明的深度网络收敛机理。博客也直接承认，一个经验答案可以只是“它确实有效”，更理论化的动机主要来自 spectral-norm steepest descent 与 Shampoo 分析。

## 5. Newton–Schulz5 实现

Muon 不直接做 SVD，因为完整 SVD 太慢；也不采用需要 float32 才稳定的 coupled Newton inverse-root 方案。博客选择能在 bfloat16 中运行的 Newton–Schulz 迭代。

核心实现先归一化：

$$
X_0=G/(\|G\|_F+\varepsilon),
$$

再重复 5 次：

$$
A_k=X_kX_k^T,
$$

$$
X_{k+1}=aX_k+(bA_k+cA_k^2)X_k,
$$

最终系数为：

$$
(a,b,c)=(3.4445,-4.7750,2.0315).
$$

对应奇异值上的五次多项式为：

$$
\rho(x)=3.4445x-4.7750x^3+2.0315x^5.
$$

若矩阵行数大于列数，代码先转置，使矩阵乘法沿较小维度进行，迭代结束后再转回。

### 为什么只需要 5 步

传统基线系数 $(2,-1.5,0.5)$ 会稳定收敛到 1，但小奇异值附近上升较慢。作者通过经验化约束优化提高 $\rho'(0)$，允许最终奇异值不精确等于 1，而是在大致 $[0.7,1.3]$ 内振荡。博客报告，这种“不完全正交但收敛更快”的设计没有损害训练 loss，因此 Transformer 和小型卷积网络中 5 步就足够。

## 6. 经验结果

博客汇总的结果包括：

| 任务 | 报告结果 |
|---|---|
| CIFAR-10 达到 94% accuracy | 训练纪录从 3.3 降至 2.6 A100-seconds |
| NanoGPT / FineWeb 达到 3.28 validation loss | 训练速度提高约 1.35× |
| 模型扩展 | 持续观察到 774M 和 1.5B 参数下的训练速度改善 |
| 1.5B Transformer 达到 GPT-2 XL 级 HellaSwag | Muon 为 10 个 8×H100-hours，AdamW 为 13.3 小时 |

博客中的 NanoGPT 图同时比较 Adam、Distributed Shampoo、SOAP 与 Muon：Muon 每步时间略高于 Adam，但样本效率更好，最终 wall-clock 曲线也更快。1.5B 短训练图显示，在相同 token 预算下，调优后的 Muon 曲线低于调优后的 AdamW；另一个 Muon 配置使用少 25% 的 token，仍能达到相近目标区间。

这些数字是博客所报告的 speedrun / reproducible-log 证据，不应自动解释为所有架构、数据和训练阶段上的统一增益。

## 7. 计算和内存开销

在 Newton–Schulz 之前，Muon 就是 SGD-momentum，因此状态内存与 SGD-momentum 同阶。

对于 $n\times m$ 矩阵且 $m\le n$，每一步 NS 迭代额外矩阵乘法开销至多约为：

$$
6nm^2.
$$

使用 $T$ 步 NS 时，额外开销约为 $6Tnm^2$。与线性层前向和反向计算相比，博客估计相对 FLOP overhead 约为：

$$
\frac{Tm}{B},
$$

其中 $m$ 是模型维度，$B$ 是每批 token 数，通常 $T=5$。

博客给出的两个估计：

- NanoGPT speedrun：约 0.7%；
- Llama 405B 训练配置：约 0.5%。

因此作者判断典型语言模型训练中的算术 FLOP overhead 低于 1%。但这不是分布式通信开销的完整评估；超大集群上如何高效分布 Newton–Schulz 仍被列为开放问题。

## 8. 与已有优化器的关系

### 8.1 Shampoo

矩阵 Shampoo 的更新为：

$$
(GG^T)^{-1/4}G(G^TG)^{-1/4}.
$$

对 $G=USV^T$ 展开后，瞬时、无累积的形式恰好成为：

$$
UV^T.
$$

因此关闭 momentum 时，Muon 可以被理解为一种“instantaneous / accumulation-free Shampoo”；在正交化之前加入 momentum，就得到 Muon 的主要形式。差别在于 Muon 用低成本 Newton–Schulz，而不是 inverse-fourth-root 预条件器。

### 8.2 Orthogonal-SGDM

Orthogonal-SGDM 先用 SVD 正交化梯度，再对正交化结果累积 momentum。Muon 的顺序相反：

```text
Muon: gradient → momentum → orthogonalization
Orthogonal-SGDM: gradient → orthogonalization → momentum
```

博客称前者经验表现更好，同时 Newton–Schulz 比 SVD 更适合 GPU。

### 8.3 Stochastic spectral descent / RMSspectral

更早的 spectral descent 方法也通过 SVD 或 randomized SVD 正交化更新，但缺少 momentum。博客认为 momentum 对 Muon 的最佳经验表现是必要的。

## 9. 证据标准：competitive task framework

这篇博客不只介绍优化器，还提出优化研究的证据标准。作者批评大量“优于 AdamW”的方法使用了未充分调优的 baseline，导致结果难以复现和延续。

建议的新方法应尽可能在 competitive training task 上证明自己：

1. prior record 本身通常已经被多人充分调优；
2. 若新优化器只是利用了差 baseline，后续参赛者可以换回硬件优化良好的标准方法重新破纪录；
3. 因而长期保留在纪录历史中的方法更不容易只是一次性的调参假象。

博客以 NanoGPT speedrunning 为 Muon 的主要证据：首次替换 AdamW 后报告约 35% 加速；此后连续 12 次新纪录仍采用 Muon，并由 7 位不同研究者完成。该证据比单篇一次性对比更强，但仍集中在特定竞争任务。

## 10. Negative Knowledge

- **Muon 不是 AdamW 的全参数替代品。** 它只用于隐藏层二维矩阵；完整训练必须是 Muon + AdamW 等混合配置。
- **“正交化为什么有效”尚未定论。** 稀有方向放大是作者推测，不是已完成的因果验证。
- **近似正交是刻意的。** 5 步 tuned NS 并不把所有奇异值精确变为 1，而是用可接受误差换 wall-clock 效率。
- **规模证据有限。** 博客验证到 1.5B，是否适用于 20B+ 参数、1T+ token 在文中仍是开放问题。
- **分布式实现未解决。** 单卡/小集群 FLOP overhead 很低，不代表超大集群通信和分片同样简单。
- **训练阶段泛化未知。** 预训练有效不等于 finetuning、RL 或稀疏/低秩适配也有效。
- **证据来自技术博客和竞争日志。** 可复现日志很有价值，但不等同于系统化、多任务、同行评审的优化器研究。
- **baseline 公平性仍需逐任务检查。** 博客强调调优 AdamW，但具体增益仍依赖 batch、学习率、weight decay、momentum 和模型实现。

## 11. 对科学机器学习和结构动力模型的可迁移价值

以下是基于 Muon 机制的研究推断，不是博客已经验证的结论：

| Muon 机制 | 可能的 SciML / 结构动力用途 |
|---|---|
| 压平更新奇异值谱 | 缓解 PINN/Neural Operator 隐藏层更新被少数方向支配的问题 |
| 只处理二维隐藏层 | 可直接用于 MLP、Transformer、KAN 外围线性层和图网络投影矩阵 |
| Muon + AdamW 混合 | 隐藏表示用 Muon，物理参数、归一化参数、输入/输出层保留 AdamW |
| Q/K/V 分开处理 | 可用于 [[pgt]] 等物理引导 Transformer，避免合并 QKV 后的尺度混杂 |
| competitive evidence | 对新的 PINN 优化策略建立固定算力、固定误差阈值和 wall-clock 排行基准 |

值得优先验证的不是“Muon 是否让单次训练 loss 更低”，而是：

- 在相同误差阈值下减少多少 wall-clock；
- 是否改善高自由度模型的训练稳定性；
- PDE/平衡方程 residual、数据 loss 和初边值 loss 的收敛是否更均衡；
- 对长时外推和跨结构泛化是否有稳定收益；
- 与 [[functional-scaling-law]] 中的学习率计划和完整 loss trajectory 是否存在耦合。

## 12. 实践检查表

```text
[ ] 仅选择 hidden 2D matrices
[ ] embedding / output head / scalar / vector 使用 AdamW
[ ] Q、K、V 分开建立 Muon parameter groups
[ ] 使用 Nesterov-style momentum 作为默认候选
[ ] Newton–Schulz 输入先做 Frobenius normalization
[ ] bfloat16，默认 5 steps
[ ] 同时调优 AdamW baseline 与 Muon 超参数
[ ] 报告 tokens-to-target 和 wallclock-to-target
[ ] 报告每步时间、显存、分布式通信成本
[ ] 至少在预训练之外验证 finetuning 或物理任务
```

## 关联页面

- [[muon]]
- [[functional-scaling-law]]
- [[wang2021-pinn-ntk-failure-analysis]]
- [[pgt]]
- [[legonet]]
