# Papers Index

概念笔记：涵盖核心概念、讲座笔记、方法论笔记。

## 组合式神经算子与训练动力学

- [[zhang2026-legonet-analysis]] — Zhang et al. (2026) LegONet：边界适配谱基 + E/H/R 结构保持块 + Strang splitting，组合式复用 PDE 机制
- [[zhang2026-legonet-method]] — LegONet 方法：baseplate、共享系数接口、trajectory-free operator matching 与可插拔推理
- [[zhang2026-legonet-results]] — LegONet 结果：4 类 baseplate、10 个 PDE；湍流/刚性/3D/OOD 长时稳定性验证
- [[zhang2026-legonet-critical]] — LegONet 贡献+Negative（baseplate 依赖/有限块库/splitting error）+结构动力学迁移
- [[li2025-functional-scaling-laws-analysis]] — Li et al. (2025) FSL：用内禀时间与遗忘核统一描述学习率计划下完整 loss trajectory，NeurIPS 2025
- [[li2025-functional-scaling-laws-method]] — FSL 方法：intrinsic-time SDE + Volterra 卷积 + signal-learning/noise-forgetting 分解
- [[li2025-functional-scaling-laws-results]] — FSL 结果：WSD > 指数衰减 > 恒定学习率；0.1B–1B LLM 跨计划拟合与预测
- [[li2025-functional-scaling-laws-critical]] — FSL 贡献+Negative（核代理/连续时间/渐近隐藏常数/规模限制）+PINN 调度迁移
- [[li2026-sgno-analysis]] — Li et al. (2026) SGNO：非正谱生成元 + ETD-inspired correction，提高 PDE 长时自回归稳定性
- [[li2025-node-onet-analysis]] — Li et al. (2025) NODE-ONet：物理编码 Neural ODE 学习 PDE 算子并增强时间外推
- [[zeraatkar2026-pgt-analysis]] — Zeraatkar et al. (2026) PGT：Green 函数物理偏置进入 Transformer attention

## 域分解 PINN、预条件与可学习物理引擎

- [[moseley2023-fbpinn-analysis]] — Moseley et al. (2023) FBPINN：重叠子域、局部归一化与训练调度缓解大域/高频 PINN
- [[moseley2023-fbpinn-method]] — FBPINN 方法：光滑窗函数、连续拼接、active/fixed/inactive 调度与邻域通信
- [[moseley2023-fbpinn-results]] — FBPINN 结果：高频/多尺度、二阶 ODE、Burgers 与 2+1D 波动证据
- [[moseley2023-fbpinn-critical]] — FBPINN 负知识：单线程成本、划分敏感、高维采样与传统法差距
- [[dolean2024-multilevel-fbpinn-analysis]] — Dolean et al. (2024) Multilevel FBPINN：粗层增强跨子域全局通信
- [[dolean2024-multilevel-fbpinn-method]] — Multilevel FBPINN 方法：指数层级、稀疏点—子域映射与强/弱缩放定义
- [[dolean2024-multilevel-fbpinn-results]] — Multilevel FBPINN 结果：Laplacian/Helmholtz 强弱缩放与基线比较
- [[dolean2024-multilevel-fbpinn-critical]] — Multilevel FBPINN 负知识：术语边界、最高波数失败与多 GPU 未验证
- [[kopanicakova2024-dd-preconditioning-analysis]] — Kopaničáková et al. (2024) Schwarz 参数域预条件 PINN
- [[kopanicakova2024-dd-preconditioning-method]] — ASPQN/MSPQN 方法：层参数子域、局部 L-BFGS 与全局准牛顿校正
- [[kopanicakova2024-dd-preconditioning-results]] — SPQN 结果：共同误差阈值下 MSPQN 约 10×、ASPQN 约 28× 墙钟加速
- [[kopanicakova2024-dd-preconditioning-critical]] — SPQN 负知识：多 GPU 资源混杂、全网复制与固定层分组
- [[hu2022-xpinn-generalization-analysis]] — Hu et al. (2022) XPINN 泛化：复杂度下降与子域样本稀释的权衡
- [[hu2022-xpinn-generalization-method]] — XPINN 方法：prior/posterior bound、PDE 稳定性与分区诊断
- [[hu2022-xpinn-generalization-results]] — XPINN 结果：KdV/heat/advection/Poisson/Euler 五题重建矩阵
- [[hu2022-xpinn-generalization-critical]] — XPINN 负知识：oracle 分区、loss 竞争及原文数值主语/总结冲突
- [[zhou2025-learnable-physics-engine-analysis]] — Zhou & Feng (2025) MPNN 可解释岩土弹塑性 Learnable Physics Engine
- [[zhou2025-learnable-physics-engine-method]] — LPE 方法：OSB-PD 图、H2 Sobolev 能量、level-set 屈服与 Newton 修正
- [[zhou2025-learnable-physics-engine-results]] — LPE 结果：冲头/洞室/边坡与 3,600–90,000 材料点效率
- [[zhou2025-learnable-physics-engine-critical]] — LPE 负知识：同源监督、训练摊销、过度平滑与热力学边界
