---
type: paper-analysis
title: 'LeanMarathon: Toward Reliable AI Co-Mathematicians through Long-Horizon Lean
  Autoformalization'
authors:
- Yuanhe Zhang
- Yuekai Sun
- Taiji Suzuki
- Jason D. Lee
- Fanghui Liu
year: 2026
venue: arXiv preprint
tags:
- domain/ai4s
- domain/llm
- evidence/paper
methods:
- blueprint-system-of-record
- dynamic-proof-DAG
- contract-scoped-agents
- two-stage-orchestration
- deterministic-CI-gate
- source-aware-refinement
results:
- seven-target-theorems
- 258-proof-nodes
- no-sorry
- incremental-development
- parallel-PRs
failure_modes:
- goal-drift
- lost-in-the-middle
- coherence-loss
- self-evaluation-bias
- irreversibility
- source-gap
- library-gap
datasets:
- paper-sources
- canonical-target-statements
reproducibility: medium
code_url:
- https://github.com/YuanheZ/LeanMarathon
dataset_url: []
id: paper--zhang2026-leanmarathon-results
status: active
project: civil-engineering-llm-wiki
keywords:
- large-language-models
- language-agents
- scientific-reasoning
- formalization
- autoformalization
- theorem-proving
- proof-assistant
- lean
- lean-4
- mathlib
- long-horizon
- co-mathematician
- benchmark
- evaluation
- mathematics-at-scale
- human-in-the-loop
- reproducibility
- blueprint-system-of-record
- dynamic-proof-DAG
- contract-scoped-agents
- two-stage-orchestration
- deterministic-CI-gate
- source-aware-refinement
- seven-target-theorems
- 258-proof-nodes
- no-sorry
- incremental-development
- parallel-PRs
- goal-drift
- lost-in-the-middle
- coherence-loss
- self-evaluation-bias
- irreversibility
- source-gap
- library-gap
- paper-sources
- canonical-target-statements
- arXiv preprint
sources:
- sources/papers/zhang2026-leanmarathon.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# LeanMarathon 结果证据：完成率、运行成本与失败案例

^[sources/papers/zhang2026-leanmarathon.md]

> 本页只记录预提取文本中有明确位置的实验、数值、表格和案例证据。方法机制见 [[zhang2026-leanmarathon-method]]；总览见 [[zhang2026-leanmarathon-analysis]]；边界解释见 [[zhang2026-leanmarathon-critical]]。

## 1. 实验输入与运行设置

论文 §4 说明，评估使用两篇 2026 年研究论文，主题为 Erdős 问题，输入是每篇论文的 LaTeX source 与独立的 canonical target statements，输出是每个 proof node 均有完整证明的 Lean blueprint。

三次运行分别为：

- **Erdős–Graham**：一次运行覆盖第一篇论文的四个目标定理。
- **Erdos1196**：从 primitive-sets 论文开始，先形式化 #1196。
- **Prim**：以最终的 #1196 blueprint 作为 seed，加入 #164 和 #1217 两个目标，测试增量开发。

实验代理运行于 Codex（GPT-5.5-xhigh，258K，read-only，无 web access）。成功条件是所有 blueprint proof node 有完整证明、不存在 `sorry` 或 `sorry_using`，并通过 Section 3.3 的七项 CI 结构检查。

## 2. 形式化产出（Table 2）

| 运行/目标 | Target theorems | Lean lines | Nodes（def/lem/thm） | Proof nodes | Remaining `sorry` | Status |
|---|---:|---:|---:|---:|---:|---|
| Erdős–Graham | 4 | 8,513 | 39 / 106 / 5 | 111 | 0 | complete |
| #1196 | 1 | 3,988 | 15 / 43 / 1 | 44 | 0 | complete |
| #164 & #1217（Prim） | 2 | 14,592 | 57 / 144 / 3 | 147 | 0 | complete |

Table 2 的 proof nodes 统计 lemma 和 theorem declaration，definition 作为全局上下文；Prim 行包含复用的 #1196 blueprint。正文 §4.3 进一步说明，七个目标定理均为 complete、机器检查、无 `sorry`，且没有使用 axiom 或 `native_decide`。

跨三次运行，论文报告共证明 258 个 distinct lemmas and theorems：Erdős–Graham 为 111，#1196 为 44，#164/#1217 在增量运行中新增 103。

## 3. 编排统计（Table 3）

| 指标 | Erdős–Graham | #1196 | #164 & #1217（Prim） |
|---|---:|---:|---:|
| Rounds | 19 | 17 | 40 |
| Workers launched | 58 | 33 | 111 |
| Refiners | 7 | 6 | 25 |
| Merged PRs | 53 | 32 | 93 |
| Critical path（excl. CI wait） | 11:38:23 | 11:32:40 | 40:43:21 |
| Aggregate agent active time | 21:29:41 | 16:26:32 | 71:16:52 |
| Stop-hook / CI wait time | 07:15:10 | 02:15:33 | 07:05:26 |
| Tool-call parsed wall time | 10:16:25 | 06:16:40 | 49:08:03 |
| Total tool calls | 5,273 | 4,067 | 12,204 |
| Total tokens | 308M | 245M | 796M |
| GPT-5.5 API-equivalent cost | $257.17 | $189.43 | $623.54 |

这些数字来自 Table 3，成本采用论文注明的 GPT-5.5 API-equivalent 计价。论文还报告跨三次运行有 135 个 Worker pull requests 落地，单轮最多 16 个并行 PR，且没有产生 merge conflict。Erdős–Graham 的 58 个 Worker 中有 44 个 PR 通过全部检查并合并。

## 4. 增量开发证据

Prim 以完成的 #1196 blueprint 为 seed，复用 59 个节点不变，并新增 145 个节点，其中 103 个是新的 proof obligations；最终 blueprint 为 14,592 行、204 个节点。论文将该结果作为“扩展已有形式化而非从头重启”的增量开发证据。

## 5. Erdős–Graham 案例

该运行共 19 轮，四个目标定理的阻塞 issue 集中在两类结果：Proposition 9 的三段 tail bound 有 8 个 issue，nested-interval construction theorem 有 8 个 issue；论文称没有其他节点被阻塞。

Case C 中，Worker 发现论文选取的 Borel peak 可能本身就是 failure，导致原始选择步骤不成立；Refiner 通过放宽 selection lemma 使 peak 允许 failure，恢复结论。论文把该问题标记为 published proof 中被形式化暴露的 genuine gap。

## 6. #1196 案例

该运行表现为一条深层 cascade。表面估计最终追溯到 Dirichlet eta function 的单调性，再追溯到 Gamma distribution shape parameter 的 stochastic domination 和 Mellin representation。论文指出这些关键事实不在 Mathlib 中，harness 因而构造了论文一句话压缩掉的完整概率论论证。

五个 Refiner 轮次中的五个、八个 issue 中的六个集中在这条 analytic spine；插入的下游叶节点在依赖顺序上完成后，原始缺陷在七轮后闭合。

## 7. #164 与 #1217（Prim）案例

Prim 是最大运行：40 轮、93 个合并 PR、46 个 issue；代理 active compute 为 71 小时，其中并行 critical path 为 41 小时，成本为 $624 GPT-5.5-equivalent。#164 较早证明，#1217 占据大部分运行；Refiner 在 40 轮中的 24 轮运行，最后 9 轮没有 Refiner。

Refiner 记录的 32 个 illness areas 中，26 个被归类为 drift，6 个为 source gap。论文明确举例：#164 的 sub-invariance 声明可由恒等 kernel 满足而失去约束；发散 `tsum` 被 Lean totalize 为 0；不适当的 real `limsup` 语义促成了向 `ENNReal` 的重写。

表 4 报告最常被重新打开的 Prim 节点：`kernel-path-data-exists` 在 10 个不同 Refiner 轮次中重开，`constructed-path-data-exists` 和 `random-model-exists` 各 8 轮，`chain-density-selection` 与 `reverse-fatou-path-extraction` 各 7 轮，`eps-modified-chain-subinvariant` 为 4 轮。

该运行出现 12 次 complete-proof downgrade，分布在 7 轮；父节点声明变化后，依赖证明按规则整体替换为 placeholder，而不是部分编辑。

## 8. 消融实验（Table 5）

同一 Erdős–Graham 论文的早期 harness 与当前 harness 只改变两项设计：早期 Refiner 看不到 source proof，且 Worker 受物理 Lean 行数预算约束。早期运行约 12 天后停止；论文报告的对比为：

| 指标 | Earlier harness | Current harness |
|---|---:|---:|
| Outcome | stalled | complete |
| Wall-clock | 约 12 天 | 论文未披露/无法从提供文本确认 |
| Blueprint restarts | ~8 | 1 |
| Issues filed | 137 | 16 |
| Citing a line budget | 14 | 0 |
| Source proof given to Refiner | no | yes |
| Final Main.lean | 12,910 lines, 26 `sorry` | 8,513 lines, 0 `sorry` |

提取文本未能可靠还原 Table 5 当前 harness 的 wall-clock 字符串，因此不补写具体天数。正文只明确给出早期约十二天，并说明当前运行完整收敛。

## 9. Aristotle baseline（Table 6）

论文让可访问的商业 Lean agent Aristotle 接收相同类型的 paper source 与 target statements，并运行到其自身停止点。Table 6 报告：

| 论文/指标 | Aristotle | LeanMarathon |
|---|---:|---:|
| Erdős–Graham：targets proven | 0/3 | 3/3 |
| Erdős–Graham：Lean lines delivered | 751 | 8,513 |
| Erdős–Graham：remaining `sorry` | 2 | 0 |
| Erdős–Graham：outcome | failed | complete |
| #1196：targets proven | 0/1 | 1/1 |
| #1196：Lean lines delivered | 24 | 3,988 |
| #1196：remaining `sorry` | 1 | 0 |
| #1196：outcome | failed | complete |

正文称 Aristotle 在 Erdős–Graham 上运行超过 40 小时，在 #1196 上超过 24 小时。Table 6 的 Erdős–Graham 目标分母为 3，而 Table 2/§4.2 对该运行描述为 4 个 target theorems；论文提供的文本没有解释这一口径差异，本页保留表内原值，不自行校正。

## 10. 失败案例：unit-distance disproof

论文还尝试形式化 OpenAI 对 Erdős unit-distance conjecture 的 disproof。由于关键代数数论几乎不在 Mathlib 中，Blueprinter 没有诚实的形式化支点；运行用 dummy record 模拟 number field，并以 placeholder values 通过类型检查，但后续几何步骤无法使用真实对象，最终在同一节点反复停滞，未达到目标。

这不是一个成功率数字，而是论文明确报告的 scope-boundary case：harness 可以编排工作，却不能补上远离现有库覆盖范围的先决定理。

## 11. 复现所需的已知信息

已披露：代码仓库 `https://github.com/YuanheZ/LeanMarathon`；Codex/GPT-5.5-xhigh、258K、read-only、无 web access；两类输入（论文 source 与 canonical target statements）；三次运行名称；Table 2/3/5/6 的统计；CI 七项检查。

论文未披露或从提供文本无法确认：独立 dataset URL、每次运行的完整输入文件包、Lean/Mathlib 精确 commit、完整 PR/issue artifact、端到端环境锁定文件。因而 frontmatter 的 `reproducibility` 标为 `medium`，不是 `high`。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[zhang2026-leanmarathon-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | https://github.com/YuanheZ/LeanMarathon |
| **数据集** | 无外部数据集 URL（或使用论文内/合成数据） |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
