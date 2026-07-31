---
id: papers--luo2025-pinn-pde-review-method
title: Luo et al. (2025) PINN-PDE 综述方法：多轴分类框架
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/paper
- method/neural-architecture-search
- method/pinn
- method/transformer
keywords:
- adaptive-weighting
- collocation-strategy
- deepxde
- neural-network
- neural-tangent-kernel
- physics-informed
- pinn
- review
- soft-constraint
sources:
- sources/papers/luo2025-pinn-pde-review.md
created: '2026-07-16'
updated: '2026-07-31'
confidence: high
methods:
- narrative-review
- taxonomy
- architecture-comparison
- adaptive-sampling
- loss-design
- feature-embedding
results:
- pinn-taxonomy
- application-map
- software-comparison
failure_modes:
- no-systematic-search-protocol
- overlapping-taxonomy
- no-quality-appraisal
reproducibility: low
contested: false
---

# 方法展开：综述分类框架，而非单一算法

> 返回概述 → [[luo2025-pinn-pde-review-analysis]]

## 5.1 证据组织方式

本文采用**叙事综述**：从 PINN 基础公式出发，按技术部件和应用领域组织代表工作。论文没有披露系统检索、文献筛选或质量评分流程，因此这里的“方法”指作者用于理解领域的分类框架，不能解释为新的 PINN 训练算法。

| 证据标签 | 含义 | 可支持的结论 |
|----------|------|--------------|
| 【综述归纳】 | Luo 等对多篇文献的分类与总结 | 可描述研究版图，不可当作统一基准排名 |
| 【被引研究报告】 | 数值/优势来自被引用论文 | 需回到原论文核验设置与统计 |
| 【作者既有工作示例】 | HA、DaPINN 来自作者团队先前工作 | 可作为案例，不能代表综述重新验证全部方法 |

## 5.2 共同 PINN 基线

对状态变量 $u(x,t)$，网络给出近似 $\tilde{u}(x,t;\theta)$，并最小化：

$$
\mathcal L=\mathcal L_{physics}+\mathcal L_{data},\qquad
\mathcal L_{physics}=w_f\mathcal L_f+w_b\mathcal L_b+w_i\mathcal L_i.
$$

$\mathcal L_f$、$\mathcal L_b$、$\mathcal L_i$ 分别约束域内 PDE 残差、边界条件和初始条件；$\mathcal L_{data}$ 拟合观测。这个基线与 [[pinn]] 和 [[raissi2019-pinn-method]] 一致，也暴露出后续分类的三个基本问题：网络能否表达解、点是否覆盖困难区域、不同损失能否同步收敛。

## 5.3 分类轴 A：网络表示

| 架构族 | 综述列举的代表 | 主要动机 |
|--------|----------------|----------|
| MLP | vanilla PINN | 通用基线；规模多靠经验选择 |
| CNN | PhyGeoNet、Spline-PINN、PICNN、f-PICNN | 网格/局部特征、几何映射、时空卷积 |
| RNN | PhyCRNet、CNN-LSTM/PDDO | 时间演化和隐状态 |
| GAN | PI-GAN、Wasserstein PI-GAN | 随机 PDE 与不确定性 |
| KAN | KINN、Chebyshev KAN、PIKAN | 可学习一元函数、样条/多项式表示；参见 [[kin]] |
| Transformer | PIT、PINNsFormer、Transolver | 长程依赖、查询点交互、复杂几何 token |
| 其他 | Auto-PINN、NAS-PINN、SPINN、PirateNets | 自动选架构、可分离计算、残差自适应深度 |

这些类别并不互斥：例如 CNN 可与 RNN、域分解或自适应采样组合。综述的表 2 更像设计组件目录，不是严格的树状 taxonomy。

## 5.4 分类轴 B：空间组织与激活

- **域分解：** XPINN、cPINN 和改进的子域网络把大域拆为多个网络，并用解连续或通量连续约束界面；适合并行和局部复杂度分配。
- **激活函数：** 自适应斜率、物理核函数、Physical Activation Functions 等试图改善收敛或注入先验。
- **边界提醒：** 激活函数非线性是网络表示属性，不等于 PDE 算子或材料本构非线性。

## 5.5 分类轴 C：训练点

综述按“固定 → 周期重采样 → 残差自适应 → 生成式/最优传输采样”梳理：

| 级别 | 方法 | 核心机制 |
|------|------|----------|
| 固定/准随机 | uniform、random、LHS、Halton、Hammersley、Sobol | 训练前确定配点 |
| 残差加密 | RAR、RAD、RAR-D、R3 | 向大残差或传播失败区增加/保留点 |
| 分布学习 | DAS-PINN、DMIS、GAS | 用生成模型、动态网格或混合分布近似残差密度 |
| 联合选择 | PINNACLE、AAS | 联合配置配点/实验点，或用最优传输平滑分布 |
| 作者示例 | HA | 混合随机性与大残差关注，两种重采样策略 |

采样能缓解局部覆盖不足，却不能单独修复低损失伪解；需与 [[wang2023-pinn-spurious-analysis]] 的目标函数诊断区分。

## 5.6 分类轴 D：损失与优化

1. **损失重加权：** 梯度统计退火、[[wang2021-pinn-ntk-failure-analysis|NTK]] 特征值平衡、lbPINN 概率权重、SelectNet、SA-PINN、LA-PINN；
2. **新损失：** gPINN 加入残差梯度，分组正则处理多量级项，$L^p/L^\infty$ 讨论稳定性，“loss jump”讨论不同损失的频率偏好；
3. **关键区分：** 权重平衡改善优化速度，但不能保证目标函数唯一指向真解，也不能替代 [[wang2024-causal-pinn-analysis]] 的时序因果约束。

## 5.7 分类轴 E：特征嵌入与增强

- 随机 Fourier 特征针对 MLP 的谱偏差；
- Prior Dictionary 把任务先验作为输入表示；
- sf-PINN 使用正弦映射；
- DaPINN 用复制、幂级数或 Fourier 级数扩展输入维度。

这些方法修改“网络看见什么”，与采样修改“网络在哪里看”、损失修改“训练时重视什么”是三种不同干预。

## 5.8 应用—软件—展望层

综述用流体、固体、电磁/光学说明应用跨度，并列出 DeepXDE、IDRLnet、NeuroDiffEq、SciANN、TensorDiffEq。最后把高频、多尺度、多物理、噪声/缺失数据、实验数据短缺与可扩展性列为挑战，并引出算子学习的跨实例映射能力。

## 5.9 如何使用这套框架

```text
先诊断瓶颈
  ├─ 表达不足/高频     → 架构或特征嵌入
  ├─ 局部误差集中       → 自适应采样
  ├─ 多损失收敛失衡     → 梯度/NTK 加权
  ├─ 伪解或因果传播失败 → 目标函数与训练时序重构
  └─ 多实例重复求解     → 考虑算子学习
```

这比直接复制某篇“最优 PINN”更可靠：先定位机制，再选择组件，并以 [[raissi2019-pinn-analysis]] 为共同基线做单变量消融。

## 页内导航

- [[luo2025-pinn-pde-review-analysis|← 概述]]
- [[luo2025-pinn-pde-review-results|结果证据 →]]
- [[luo2025-pinn-pde-review-critical|批判分析 →]]

## Evidence By Source

### `sources/papers/luo2025-pinn-pde-review.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/10_1007_s10462-025-11322-7.pdf`

^[sources/papers/luo2025-pinn-pde-review.md]
