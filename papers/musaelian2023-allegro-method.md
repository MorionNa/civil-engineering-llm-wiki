---
title: "Allegro method"
type: paper-method
---

# Method

## Strict locality

Allegro avoids iterative atom-centered message passing and constructs local pair representations. It decomposes energy into local pair energies:

\[
E_i=\sum_j E_{ij}
\]

forces are obtained by differentiating total energy.fileciteturn95file0L230-L264

## Equivariant tensor product

模型使用 scalar latent space 与 equivariant tensor latent space，并通过 tensor product 融合几何信息。fileciteturn95file0L285-L317

核心：

```
neighbor geometry
      ↓
spherical harmonics
      ↓
equivariant tensor product
      ↓
local environment representation
```

## Scalability

严格局部表示使模型具有：

- 原子数 O(N) scaling；
- 易于空间分解并行；
- 避免 message passing 感受野指数扩张。fileciteturn95file0L647-L672
