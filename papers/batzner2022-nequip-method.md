---
title: "Batzner et al. (2022) — NequIP 方法"
created: 2026-07-31
updated: 2026-07-31
type: paper-analysis
---

# NequIP 方法机制

## E(3)-equivariant representation

NequIP 使用标量、向量和高阶张量特征，并通过 O(3) 不可约表示描述几何状态。fileciteturn113file0L181-L196

## Equivariant convolution

卷积滤波器由径向函数和球谐函数组成：

$$S^{(l)}_m(r_{ij})=R(r_{ij})Y^{(l)}_m(\hat r_{ij})$$

通过 Clebsch-Gordan 张量积保持旋转等变。fileciteturn113file0L202-L215

## Energy-force consistency

网络预测总势能：

$$E=\sum_iE_i$$

力由：

$$F_i=-\nabla_iE$$

获得，保证能量守恒。fileciteturn113file0L161-L169

## 与普通GNN区别

```text
Invariant GNN
 distance/scalar
       ↓
 scalar message passing

NequIP
 relative vectors
       ↓
 tensor features
       ↓
 equivariant convolution
```

## 对结构动力迁移

对应：

```text
structure graph
      ↓
geometry-aware tensor features
      ↓
equivariant MechConv
      ↓
physics-consistent response
```

