---
title: "SeisGPT 方法：SDR 低保真先验、质量刚度图编码与 SDG-Mixer"
created: 2026-07-16
updated: 2026-07-16
type: paper-analysis
tags: [physics-informed, metamodeling, deep-learning, sequence-modeling, transformer, lora, structural-dynamics, nonlinear-systems, seismic-response, finite-element, high-rise-building, real-time-simulation, gpu-computing]
sources: [raw/papers/meng2026-seisgpt.pdf, raw/papers/meng2026-seisgpt-extracted.md]
confidence: high
---

# SeisGPT 方法机制

## 1. 输入输出与滑动窗口

SeisGPT 的输入包括：

- 外部激励历史 $X_e$；
- SDR 模块生成的楼层粗响应 $X_s$；
- 楼层质量矩阵 $M$ 与等效刚度矩阵 $K$；
- SeisGPT-R 中额外加入稀疏传感器观测 $X_r$。

所有响应统一采样为 $\Delta t=0.02$ s。每个训练样本含历史窗口 $T_m=1000$ 步和预测窗口 $T_p=20$ 步，目标为最后 20 步的高保真非线性楼层响应。相邻窗口沿完整时程滑动，但各窗口独立预测，避免完全自回归滚动的累积漂移，并支持长时程并行推理。

## 2. 大规模结构数据生成

作者先用三类定制扩散模型自动生成建筑与结构布置：

1. **ArchiFlux：** 生成功能分区与建筑平面；
2. **StructFlux：** 布置柱和剪力墙等主要抗侧构件；
3. **BeamFlux：** 生成梁系。

三者基于 FLUX + ControlNet，训练数据为用不同颜色标注隔墙、窗、门、梁、柱、墙的真实建筑图。生成后再执行竖向/水平传力路径检查、净距检查、构件尺寸设计、轴压比/抗弯强度校核、层间位移约束和配筋计算。

最终形成：

| 结构类型 | 模型数 | 分析数 | 层数 |
|---|---:|---:|---:|
| 框架 | 150,000 | 1,300,000 | 1–10 |
| 框架–剪力墙 | 60,000 | 520,000 | 11–20 |
| 剪力墙 | 60,000 | 220,000 | 10–30 |
| 真实建筑 FE | 694 | 13,880 | 2–30 |
| **合计** | **270,694** | **2,053,880** | — |

每个模型随机选择地震动并在 x/y 方向进行 OpenSees 非线性时程分析。训练域主要采用 RC 路径相关弹塑性本构，激励库还包含白噪声、地铁振动和冲击荷载。

## 3. SDR：精细 FE 到楼层降阶先验

SDR 不是传统仅含相邻层弹簧的三对角剪切模型。作者对精细 FE 模型每层依次施加单位水平力，收集位移场 $U$，通过

$$KU=F$$

并施加 $K_{ij}=K_{ji}$ 的对称约束，以约束最小二乘得到**全带宽楼层刚度矩阵** $K$。楼层质量 $M$ 由楼板自重、竖向构件分摊质量和活荷载组成。

全带宽 $K$ 可隐式凝聚弯剪耦合、平面不规则和部分扭转柔度对平动方向的影响，比三对角 stick model 更有表达力。但当前 SDR 分方向提取平动算子，不显式保留转动自由度和双向耦合。

SDR 采用常平均加速度 Newmark：

$$\gamma=0.5,\qquad \beta=0.25$$

并求解

$$M\ddot u+C\dot u+Ku=G,$$

其中 $C=\alpha_RM+\beta_RK$，Rayleigh 阻尼由第一、第三阶频率确定。SDR 只提供线性粗响应，非线性弹塑性部分由深层模型从 NLTHA 标签学习。

## 4. 多流特征嵌入与门控融合

激励 $X_e$、SDR 响应 $X_s$、时间位置和楼层属性分别投影到统一 latent space。模型使用：

- 时间嵌入；
- 楼层嵌入；
- 正弦位置编码；
- enhanced gated fusion，动态融合激励、粗响应和结构特征。

## 5. 质量–刚度感知 PIGNN

每层视作图节点。先构造质量归一化结构算子：

$$D=M^{-1/2}KM^{-1/2}.$$

若 $D_{ij}\neq0$，则建立从楼层 $j$ 到 $i$ 的边，边属性为 $d_{ij}=D_{ij}$，并保留 self-loop。PIGNN 使用 GATv2 风格的边条件注意力：

$$e_{ij}^{h,l}=a_h^T\operatorname{LeakyReLU}(W_i^hh_i^l+W_j^hh_j^l+W_e^hd_{ij}),$$

$$\alpha_{ij}^{h,l}=\operatorname{softmax}_{j\in\mathcal N(i)}e_{ij}^{h,l}.$$

多头消息聚合后，经 LayerNorm、GELU、Dropout 和残差更新。这里的图连接不是人为邻接，而是由全带宽质量–刚度耦合决定，因此远距离楼层也可直接交换信息。

## 6. 从楼层算子到 token-space 谱算子

不同建筑层数不同，批处理时需 padding。作者只在有效楼层上构造物理算子，再通过 valid-floor embedding $P_b$ 和共享 floor-to-token lifting $W_L$ 映射到固定 token 坐标：

$$L_b=W_LP_b,$$

$$B_{tok,b}=L_b\tilde D_bL_b^T.$$

其中 $\tilde D_b$ 是按 trace-averaged stiffness scale 归一化后的 $D_b$。随后做可微特征分解：

$$B_{tok,b}=U_b\Lambda_bU_b^T,$$

$$\omega_{i,b}=\sqrt{\lambda_{i,b}+\epsilon_\lambda}.$$

$U_b$ 是该建筑在 latent token space 中的模态基，$\lambda_i$ 则作为频率型坐标。

## 7. SDG-Mixer：Green 函数式谱传播

每个谱分量的两个 latent channel 被视为相平面状态：

$$
\begin{bmatrix}\hat z_a'\\\hat z_b'\end{bmatrix}
=A_{i,h}e^{-\alpha_{i,h}}R(\theta_{i,h})
\begin{bmatrix}\hat z_a\\\hat z_b\end{bmatrix},
$$

$$R(\theta)=
\begin{bmatrix}
\cos\theta&-\sin\theta\\
\sin\theta&\cos\theta
\end{bmatrix}.
$$

其物理含义：

- $e^{-\alpha}$：阻尼衰减；
- $\theta$：相位推进；
- $A$：结构条件化振幅调制。

这些参数由频率 proxy 和建筑全局结构描述符共同生成，因此每栋建筑具有不同的谱传播规律。

## 8. 有界有理谱修正

纯线性模态传播不足以表示屈服、刚度退化和模型误差。作者引入：

$$r_{i,h}=\sum_{k=1}^{K_r}\frac{a_k^h}{b_k^h+\lambda_i+\epsilon_\lambda},$$

其中

$$a_k^h=\tanh(\tilde a_k^h),\qquad b_k^h=\operatorname{softplus}(\tilde b_k^h)+\epsilon_b.$$

最终振幅为：

$$A_{i,h}=G_hs_h(1+r_{i,h}).$$

该修正不直接修改特征值，而是按谱位置调整增益；tanh/softplus 约束避免分母为零和无限放大，使非线性校正保持稳定。

## 9. 残差门控与 FFN

SDG-Mixer 使用近零初始化的有界残差门：

$$Z_{out}=Z+\beta\,SDGMixer(RMSNorm(Z);B_{tok},d),$$

$$\beta=\tanh\rho.$$

随后连接 SwiGLU FFN，均采用 pre-norm residual layout。通道宽度 $C=256$，latent resolution $d=4096$。

## 10. SeisGPT-Enhanced 与 LoRA

SeisGPT-Base 在大规模合成数据上预训练后，用 694 个真实建筑 FE 响应微调为 Enhanced。建筑个性化时冻结原网络，仅在线性层插入 LoRA。消融表明 encoder-only LoRA 在单条记录条件下取得最佳综合改善，说明建筑差异主要应在结构表征阶段适配。

## 11. SeisGPT-R 稀疏观测融合

稀疏观测 $X_r$ 以 floor×time tensor 输入：有传感器楼层保留历史，无传感器楼层使用 missing placeholder；未观测响应只作为目标，避免泄漏。

PIGNN 输出 $H_i$ 与传感器嵌入 $S_i$ 在结构编码后融合：

$$\alpha_i=\sigma(W[H_i\|S_i]+b),$$

$$Z_i=\alpha_iS_i+(1-\alpha_i)H_i.$$

这种设计允许可靠传感器增强局部预测，同时在缺测楼层依赖结构物理先验维持空间连续性。

## 12. 方法机制总结

SeisGPT 的关键不是单个模块，而是三级物理注入：

1. **输入层：** SDR 低保真动力响应；
2. **空间层：** 质量–刚度图消息传递；
3. **时间/全局层：** 特征分解 + Green 函数式谱传播。

因此它与只在 loss 中加平衡方程的 PINN 不同，物理先验直接决定表示空间和传播算子。

## 关联页面

- `[[meng2026-seisgpt-analysis]]`
- `[[meng2026-seisgpt-results]]`
- `[[meng2026-seisgpt-critical]]`
- `[[seisgpt]]`
- `[[seisgpt-vs-phylstm-cm-pinns]]`
