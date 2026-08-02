---
id: sources--papers--feng2026-mpm-lite
title: "Feng et al. (2026) — MPM Lite：线性核与无粒子积分"
type: source
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- apic
- implicit-mpm
- linear-kernel
- material-point-method
- mpm-lite
- particle-independent-integration
- rotation-free-stretch
sources:
- raw/papers/feng2026-mpm-lite-source.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
evidence_scope: full-text
code_url:
- https://mpmlite.github.io
dataset_url: []
---

# 来源记录：MPM Lite

## 文献信息

- **英文题名：** MPM Lite: Linear Kernels and Integration Without Particles
- **作者：** Xiang Feng、Yunuo Chen、Chang Yu、Hao Su、Demetri Terzopoulos、Yin Yang、Joe Masterjohn、Alejandro Castro、Chenfanfu Jiang
- **期刊：** ACM Transactions on Graphics, 45(4), Article 152, July 2026
- **DOI：** 10.1145/3811294
- **证据范围：** 用户提供的 20 页正式全文。
- **项目页：** https://mpmlite.github.io

## 证据地图

- 第 1–3 页：研究动机、传统 MPM 的粒子积分与宽模板瓶颈、三项核心贡献及相关工作。
- 第 4–7 页：粒子—单元中心—网格节点传递、广延 Kirchhoff 应力重采样、有限元式积分、旋转无关伸长重构与材料混合。
- 第 7–8 页：完整 Unload–Integrate–Load 算法及显式/隐式分支。
- 第 8–13 页：显式和隐式性能、PPC 扩展、VBD 耦合、多材料与断裂/塑性算例、守恒与内存分析。
- 第 14 页：小时玻璃模态、边界条件、各向异性、欠积分和子单元变化等局限。
- 第 15–20 页：传递误差、旋转无关参考解误差和三维 Neo-Hookean 反演附录。

## 证据边界

论文证明的是计算机图形学与连续体仿真场景中 MPM Lite 的数值机制、稳定性、材料适用性和特定硬件实现效率。论文没有验证钢筋混凝土构件、本构断裂标定、建筑结构地震倒塌、工程尺度接触参数或与梁壳/AEM/FEM 的守恒耦合。本知识库中的结构倒塌与局部 MPM 迁移内容均明确标记为迁移推论。

## 生成页面

- [[papers/feng2026-mpm-lite-analysis]]
- [[papers/feng2026-mpm-lite-method]]
- [[papers/feng2026-mpm-lite-results]]
- [[papers/feng2026-mpm-lite-critical]]
- [[entities/mpm-lite]]
- [[concepts/particle-independent-grid-integration]]
- [[concepts/rotation-free-stretch-reconstruction]]
