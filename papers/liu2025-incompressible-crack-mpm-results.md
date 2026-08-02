---
id: paper--liu2025-incompressible-crack-mpm-results
title: "Liu et al. (2025) — 体积保持 MPM 不可压缩裂纹模型结果证据"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- brazilian-disc
- fracture-parameters
- granular-debris
- performance
- visual-validation
sources:
- sources/papers/liu2025-incompressible-crack-mpm.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
evidence_scope: full-text
---

# 结果与证据

## 巴西圆盘压缩

论文将本文方法与传统 MPM 和仅含线性应力软化的 MPM 对比。本文方法在压缩下产生贯穿、分支和边缘粉碎式裂纹；线性软化响应更软且断裂推迟，传统 MPM 基本不能形成可控裂纹。该证据主要是视觉和定性行为对照。^[sources/papers/liu2025-incompressible-crack-mpm.md]

## 高模量压缩

在更高 Young 模量场景中，本文方法更早出现脆性裂纹，而线性软化模型难以稳定地产生相似行为。作者还与 Wolper 等 CD-MPM 进行视觉对照，并指出后者在约 $E>10^6$ 的高模量设置中难以运行；但两种实现的 CPU/GPU、参数和代码路径并不完全一致，因此不能视为严格同平台性能基准。

## 复杂几何与多种载荷

兔子、龙、犰狳、多犰狳和拉伸加载场景显示模型可用于复杂表面、薄弱附肢和多碎片相互作用。碎裂首先发生在腿、耳等弱部位，较大外力产生更小碎片。

## 参数影响

完全损伤阈值 $\xi$ 主要控制断裂难易与起裂时机：阈值较小更易断裂。体积保留参数 $\eta$ 主要控制完全损伤后的残余体积、延性/脆性和能量释放，对裂纹形态影响大于对起裂时刻的影响。

## 碎屑体积保持

二维碎屑堆在两侧墙体反复往复压缩时，本文方法大多数粒子保持接近初始体积；对比方法在多次循环后出现大量体积增长。作者将差异归因于额外体积变形梯度对真实体积状态的跟踪。

## 运行性能

测试硬件为 i7-10700K、RTX 3070 8GB 和 16GB RAM。330 万粒子、$E=6\times10^8$ Pa 的场景每帧约 1.08 s。玻璃板压球的 40 步平均耗时中，本文方法相对传统 MPM 总耗时增加 7.9%，相对线性软化模型增加 3.2%；新增成本主要位于粒子状态更新与 P2G。

## 证据局限

- 结果以图形学视觉合理性为主，没有报告裂纹路径误差、峰值荷载、耗散能或碎片粒径分布误差；
- 巴西圆盘没有与实验力–位移曲线或裂纹统计定量对照；
- 不同方法的硬件与参数并非全部统一；
- 没有网格分辨率收敛表，作者明确承认低分辨率下裂纹增厚与流体化；
- 没有真实混凝土、岩石或冰材料的系统标定。

## 关联页面

- [[liu2025-incompressible-crack-mpm-analysis]]
- [[liu2025-incompressible-crack-mpm-method]]
- [[liu2025-incompressible-crack-mpm-critical]]
- [[concepts/volume-preserving-debris-plasticity]]
