---
type: paper-analysis
title: Solving olympiad geometry without human demonstrations
authors:
- Trieu H. Trinh
- Yuhuai Wu
- Quoc V. Le
- He He
- Thang Luong
year: 2024
venue: Nature
tags:
- domain/ai4s
- evidence/paper
methods:
- large-language-models
- machine-learning
- formalization
- theorem-proving
- geometry
results:
- benchmark
- evaluation
- geometry
- olympiad
failure_modes:
- geometry
- formalization
- benchmark
datasets:
- geometry
- olympiad
- benchmark
reproducibility: medium
code_url:
- https://github.com/google-deepmind/alphageometry
dataset_url: []
id: paper--trinh2024-alphageometry-method
status: active
project: civil-engineering-llm-wiki
keywords:
- large-language-models
- scientific-reasoning
- benchmark
- evaluation
- geometry
- olympiad
- machine-learning
- formalization
- theorem-proving
- reproducibility
- Nature
sources:
- sources/papers/trinh2024-alphageometry.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# AlphaGeometry 方法机制

^[sources/papers/trinh2024-alphageometry.md]

本文方法的核心是：用确定性的符号系统生成并验证可执行证明，用神经语言模型提出符号系统本身不会主动生成的辅助构造。完整概览见 [[trinh2024-alphageometry-analysis]]，模型实体见 [[entities/alphageometry]]。

## 1. 几何表示与范围

论文没有直接把 IMO 几何题形式化到 Lean，而采用 GEX、JGEX、MMP/Geometer 和 GeoLogic 一脉的专用几何语言。该语言带有面向合成几何的逻辑、图形、人类式非退化和拓扑假设；每个证明步骤可做逻辑和数值验证，并可由人类按接近 IMO 选手的语法阅读（Methods p. 8）。

专用语言扩展了整数、分数和几何常数，用于覆盖角度、比值、距离及简单代数/算术推理。论文报告约 75% 的 IMO 几何题可适配这一表示；几何不等式和组合几何不在本文环境中。

## 2. 一致前提采样

论文实现 constructive diagram builder language，一次构造一个对象，而不是同时自由采样多个互相约束的前提。这样做的直接目的，是减少生成自相矛盾的前提集合。

动作集合包括：

- 按关系构造新点，例如共线、内心、旁心等；
- 使用数字参数构造满足某种距离条件的点；
- 由已有对象逐步扩展图形状态。

论文指出，可以通过增加更复杂动作来提升合成数据多样性和测试集覆盖；实际系统采用的是足以描述 IMO-AG-30、且能与 DD 配合工作的较简单语言。

## 3. DD：几何规则的演绎闭包

给定前提，structured deductive database（DD）用几何规则反复推出真命题。规则可写成 definite Horn clause：

Q(x) ← P1(x), …, Pk(x)

其中 x 是点对象，Pi 与 Q 是“等长”“共线”等几何谓词。DD 将推理状态组织为可回溯的图结构，节点是可达结论，边连接父节点。

与原始 DD 实现不同，论文使用 graph data structure 表示几何对称性，不只处理函数参数的对称排列，也编码等式、共线和共圆的传递性。部分规则隐式写入图结构，最终把需要展示的规则按需序列化进文本证明（Methods p. 9）。

结构化 DD 在标准非加速硬件上通常可以在几秒内得到演绎闭包，构成搜索循环中的确定性验证器。

## 4. AR：代数推理闭包

论文在 DD 之外加入 algebraic reasoning（AR），以处理几何证明中常见的角度、比值、距离追踪和几何常数运算。DD 与 AR 的结合是本文符号推理部分的主要方法贡献之一。

### 4.1 线性方程表示

输入等式被转换为系数矩阵 A ∈ R^(M×N)，M 是输入等式数量，N 是变量数量。角度等式使用线段方向变量；比值等式使用线段长度的对数变量；距离推理中的变量表示一个“点—直线”对。几何常数如 pi 和 √2 作为默认变量加入矩阵。

在论文给出的表示中，几何等式被整理为变量的线性组合。Gaussian elimination 返回主元列和其余变量的线性组合，从而可穷举检查新的等式是否成立。论文以三条输入等式推出另一条等式作为示例（Methods p. 8；Extended Data Table 2）。

### 4.2 与 DD 交替

DD 输出的新陈述会更新 AR 的系数矩阵；例如 DD 发现 AB 与 CD 平行时，AR 将两条线的 slope 变量写入相等关系。AR 的 Gaussian elimination 产生的新等式再作为 DD 的输入。

这个过程在联合闭包不再扩展时停止。论文强调，DD 与 AR 都是确定性的，只依赖定理前提，不需要额外的设计选择。

## 5. Traceback 与最小前提

每个演绎节点都配有 traceback 算法，返回产生该结论所需的最小直接祖先集合。其用途不是只恢复一条证明路径，而是从闭包图中抽取最小依赖子图 G(N) 及对应前提集合 P。

对等式传递，论文维护 equality transitivity graph，用 breadth-first search 找任意两个变量之间的最短传递路径。对共线和共圆，使用含 3-edge 或 4-edge 的 hypergraph，并把 traceback 视为覆盖目标节点集合的最小生成树问题。

共线/共圆的最小生成树优化是 NP-hard，论文在此处使用 greedy best-effort 算法。因而这部分不能被解释为在所有几何状态上都求得全局最小 traceback。

AR 的 traceback 被转化为 mixed-integer linear programming：对输入方程设置非负整数决策向量，选择决策值非零的输入行作为目标等式的直接父节点。预提取文本中的公式排版损坏，因此本页保留算法含义，不补写未能确认的完整目标函数。

## 6. Dependency difference 与辅助构造

对从前提到结论的证明图，论文区分：

- 目标结论所依赖的对象和推理步骤；
- 出现在证明中、但不属于结论对象依赖的对象。

后者构成 dependency difference。它们对应符号引擎不会凭空生成的新对象，例如在简单等腰三角形例子中构造 BC 的中点 D。论文把这些步骤抽取为语言模型需要学习的辅助构造，而把其余可达推论留给 DD+AR。

该分解把几何证明中的 auxiliary construction 具体化为 exogenous term generation：每生成一个新对象，搜索树就打开新的分支，分支数理论上可以无限增长。

## 7. Proof pruning

只让每个节点的直接祖先最小，不能保证完整 G(N) 或 P 最小，因为冗余辅助点可能通过无必要的传递路径参与证明。论文对辅助点的子集执行穷举试错：删除候选点后重新运行 DD+AR，只有目标仍可达才保留删除。

这一步在合成数据生成阶段执行，也在测试时每次成功搜索后执行。结果是返回当前试验可获得的最小证明，并减少与实际结论关联很弱的 vacuous auxiliary construction。

## 8. 合成定理—证明生成

生成流程是：

1. 随机采样前提；
2. 用 DD+AR 得到所有可达结论组成的有向无环图；
3. 从任意结论节点 N 做 traceback；
4. 形成训练样本 (P, N, G(N))，即前提、结论和证明；
5. 根据 dependency difference 标出辅助构造；
6. 对证明做 canonicalization 和 deduplication。

论文正文称随机探索采样了近 1 billion 个前提，并获得 100 million 合成定理及证明；Methods 进一步报告 100,000 个 CPU workers 运行 72 h 生成约 500 million proof examples，规范化和去重后得到 100 million unique theorem–proof examples，其中 9 million 至少包含一个辅助构造。

论文还报告辅助构造证明约占合成证明的 9%，并在生成数据中没有发现 IMO-AG-30 的题目；在 JGEX 数据中发现近 20 个主要为中等难度和已知定理的问题。

## 9. Transformer 训练

论文把 (P, N, G(N)) 序列化为：

premises <conclusion> <proof>

语言模型据此学习在给定前提和结论条件下生成证明符号序列。

模型是 Transformer，使用 Meliad 的基础设置：12 层、1,024 embedding dimension、8 个 attention heads、4,096 维 inter-attention dense layer、ReLU 激活；参数量为 151 million，不含输入和输出 embedding layers。Tokenizer 使用 SentencePiece word mode，词表大小 757；最大 context length 为 1,024 tokens；使用 T5-style relative position embedding 和 sequence packing。

训练使用 5% dropout，硬件为 4 个 TPUv3 slice。预训练在全部 100 million 合成证明上进行，batch size 为每 core 16，学习率从 0.01 按 cosine schedule 衰减至 0.001，持续 10,000,000 steps。微调只使用约 9 million 个含辅助构造的证明，保持 0.001 学习率再训练 1,000,000 steps。

无预训练的设置将学习率从 0.01 衰减至 0.001，训练 1,000,000 steps；论文没有进行超参数调优，数值主要为大整数或 Meliad 默认值。

## 10. 神经—符号交替搜索

推理以问题陈述字符串为种子。每一轮语言模型在问题和历史构造条件下生成一条额外句子，描述一个新辅助构造。例子包括“构造点 X，使 ABCX 为平行四边形”。

符号引擎接收新点和新前提后，重新扩展 DD+AR 闭包。若目标结论进入闭包则终止；否则再次调用语言模型。达到最大迭代次数仍未证明时终止并报告失败。

论文使用 beam search 维护语言模型给出的 top-k 构造候选。正文报告测试使用 beam size 512；Methods 的并行化描述中给出每个问题使用 k=512、最大 16 次迭代、每个节点 decoding batch size 32。

每个问题使用 4 个 GPU workers，各自加载一份 Transformer；10,000 个 CPU workers 共享承载不同 beam 的符号求解器。这样的分配允许较早结束的问题释放计算资源给仍在运行的问题。

## 11. 输出与验证

DD+AR 产生的步骤和语言模型输出交错写入证明序列。由于符号引擎每一步都执行逻辑/数值验证，输出可再通过模板自动翻译成自然语言。论文把这种可验证、可读的交错序列作为 AlphaGeometry 的最终证明格式。

但自然语言模板不能自动补上 Gaussian elimination 隐含的所有中间推导，也不能把低层规则自动压缩为人类使用的高层定理。这是方法输出层的已知边界，详见 [[trinh2024-alphageometry-critical]] 与 [[trinh2024-alphageometry-results]]。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[trinh2024-alphageometry-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | https://github.com/google-deepmind/alphageometry |
| **数据集** | 无外部数据集 URL（或使用论文内/合成数据） |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
