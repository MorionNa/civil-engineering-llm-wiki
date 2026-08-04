---
type: entity
title: AlphaGeometry synthetic theorem–proof data
tags:
- domain/ai4s
- entity/dataset
id: entity--alphageometry-synthetic
status: active
project: civil-engineering-llm-wiki
keywords:
- geometry
- olympiad
- benchmark
- machine-learning
- theorem-proving
- formalization
- reproducibility
sources:
- sources/papers/trinh2024-alphageometry.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# AlphaGeometry synthetic theorem–proof data

^[sources/papers/trinh2024-alphageometry.md]

## 定义

该数据资产是 AlphaGeometry 为几何定理证明生成的合成定理—证明语料，不是从人类证明直接翻译得到的演示数据。它由随机几何前提、DD+AR 可达结论、traceback 依赖子图和辅助构造标注组成。

生成机制详见 [[trinh2024-alphageometry-method]]，对应模型见 [[entities/alphageometry]]。

## 生成流程

1. constructive diagram builder 逐个采样一致的几何对象和前提。
2. DD 与 AR 交替计算从这些前提可达的结论闭包。
3. 对任意结论节点执行 traceback，提取必要前提与证明依赖图。
4. 用 dependency difference 找出参与证明、但不属于目标结论对象依赖的辅助构造。
5. 对定理—证明序列做 canonicalization 和 deduplication。

最终训练样本可表示为 (P, N, G(N))：必要前提 P、结论 N 和依赖子图 G(N)。

## 规模与组成

论文正文报告约 100 million 个唯一合成定理—证明样本，约 9%（约 9 million）含至少一个辅助构造；最长合成证明长度为 247 步。Methods 报告数据生成阶段先由 100,000 个 CPU workers 运行 72 h 得到约 500 million examples，再经规范化和去重保留约 100 million unique examples。

模型先在全部 100 million 合成证明上预训练，再在含辅助构造的约 9 million 子集上微调。论文还报告合成数据中没有发现 IMO-AG-30 原题，在 JGEX 问题集合中发现近 20 个主要为中等难度和已知定理的问题。

## 数据性质

- 数据中的前提不是人工题库直接抽取；论文强调不使用已有人工设计题集的定理前提，并按采样动作均匀随机生成 eligible constructions。
- 随机生成的定理通常不符合人类偏好的对称性，但覆盖的几何场景更宽。
- 辅助构造数据是语言模型学习 exogenous term generation 的主要监督来源；纯 deduction 数据用于学习其所连接的符号引擎行为。
- 语料受专用几何语言、diagram builder 动作集和 DD+AR 规则覆盖限制，因此规模不能等同于完整人类几何知识。

## 可用性与边界

论文 Data availability 说明支撑发现的数据位于 Extended Data 和 Supplementary Information，并提供 source data；Code availability 给出 <https://github.com/google-deepmind/alphageometry>。预提取文本没有给出该 100 million 语料的独立下载 URL，因此本实体不填写 dataset_url，也不声称完整训练语料已公开。

若要复现该数据资产，需要同时固定几何表示、随机前提采样器、DD+AR 规则、traceback 和 proof-pruning 实现；仅下载模型代码不足以证明获得同一语料。

## 关联页面

数据在 [[trinh2024-alphageometry-results]] 中对应规模、消融和测试结果，在 [[trinh2024-alphageometry-critical]] 中对应覆盖边界与复现机会。它是 AlphaGeometry 的合成训练数据实体，不是通用 theorem-proving 占位实体。
