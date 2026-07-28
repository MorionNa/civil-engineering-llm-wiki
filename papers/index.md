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
