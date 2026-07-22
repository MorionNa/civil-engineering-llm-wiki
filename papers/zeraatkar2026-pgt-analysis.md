---
title: "Zeraatkar et al. (2026) — Physics-Guided Transformer (PGT): Physics-Aware Attention Mechanism for PINNs"
created: 2026-07-22
updated: 2026-07-22
type: paper-analysis
tags: [physics-informed, pinn, transformer, attention, ai4s, neural-operator, sparse-reconstruction]
sources: [raw/papers/2603.27929v1.pdf]
confidence: high
---

# Physics-Guided Transformer (PGT)

## 1. Core Idea

PGT addresses the limitation that conventional PINNs introduce physics only through loss functions. The paper argues that governing equations should influence representation learning itself. The proposed model embeds physical structure into Transformer self-attention through a physics-guided bias term.

The paper introduces PGT for reconstructing continuous physical fields from sparse observations in PDE-governed nonlinear systems. The authors test one-dimensional heat diffusion and two-dimensional incompressible Navier–Stokes systems. fileciteturn103file0L6-L18

## 2. Physics-aware Attention

Standard attention:

$$Attention(Q,K,V)=softmax(QK^T/\sqrt d)V$$

PGT introduces:

$$Attention(Q,K,V)=softmax(QK^T/\sqrt d+\Gamma)V$$

where Gamma is obtained from the Green's function of the governing PDE. The paper defines:

$$\Gamma_{ij}=log G(x_i-x_j,t_i-t_j;\theta_p)$$

The logarithm converts the multiplicative Green function into an additive attention bias. Tokens outside the causal domain receive $-\infty$ bias and therefore zero attention weight. fileciteturn103file0L204-L213

## 3. Heat Kernel Bias

For diffusion systems, the heat kernel provides:

$$\Gamma_{ij}=-\frac{||x_i-x_j||^2}{4\alpha\Delta t}-\frac d2 log(4\pi\alpha\Delta t)$$

This embeds:

- spatial locality;
- diffusion length scale;
- temporal causality.

The influence radius follows the physical diffusion scale:

$$\sigma=\sqrt{2\alpha\Delta t}$$

The paper notes that hyperbolic systems can use wave-front causal kernels, while elliptic problems use spatial Green functions. fileciteturn103file0L214-L235

## 4. Architecture

PGT contains:

1. Physics-guided Transformer encoder;
2. Cross-attention query conditioning;
3. FiLM-modulated SIREN implicit decoder.

Sparse observations are converted into context tokens, processed by physics-guided attention, and queried at arbitrary coordinates $(x,t)$. fileciteturn103file0L160-L165

The decoder uses FiLM modulation to adjust amplitude, bias and frequency according to inferred physical context. fileciteturn103file0L260-L273

## 5. Loss Function

Unlike pure architecture-only physics models, PGT still uses physics losses.

Total objective:

$$L=\frac{1}{2\sigma^2_{data}}L_{data}+\frac{1}{2\sigma^2_{PDE}}L_{PDE}+\frac{1}{2\sigma^2_{BC}}L_{BC}+\frac{1}{2\sigma^2_{IC}}L_{IC}$$

Components:

### Data loss

$$L_{data}=||u_\Theta-u^{obs}||^2$$

### PDE residual

$$L_{PDE}=||F(u_\Theta)-f||^2$$

### Boundary and initial conditions

$$L_{BC},L_{IC}$$

The weights are uncertainty-based and learned automatically through trainable variance parameters, avoiding manual balancing of loss terms. fileciteturn103file0L279-L281 fileciteturn103file0L336-L368

## 6. Experimental Results

Heat equation:

- 100 observations;
- relative L2 error $5.9\times10^{-3}$;
- about 38 times lower than PINN. fileciteturn103file0L21-L23

Navier-Stokes cylinder wake:

- 1500 scattered spatiotemporal samples;
- PDE residual $8.3\times10^{-4}$;
- relative L2 error 0.034. fileciteturn103file0L24-L29

## 7. Ablation Findings

The paper shows:

- removing physics-guided attention mainly harms reconstruction accuracy;
- removing PDE loss mainly harms PDE compliance;
- both mechanisms are complementary.

The full model achieves reconstruction error $6.50\times10^{-5}$ and PDE residual $8.30\times10^{-4}$ in the Navier-Stokes ablation. fileciteturn103file0L570-L584

## 8. Relation to Structural Dynamics

PGT differs from CM-PINNs and SeisGPT:

| Method | Physics injection |
|-|-|
| CM-PINNs | constitutive constraints in loss |
| PGT | physics-aware attention propagation |
| SeisGPT | structural operators and spectral propagation |

Potential structural adaptation:

$$\Gamma=f(M,K,C,\Phi,t)$$

where attention bias can encode:

- modal coupling;
- floor connectivity;
- causal wave propagation;
- damping effects.

## 9. Limitations

- Tested mainly on PDE field reconstruction;
- heat-kernel bias is naturally suited to diffusion-like systems;
- nonlinear constitutive behavior is not explicitly modeled;
- extension to strong nonlinear structural dynamics remains open.

## Related

- [[pgt]]
- [[pinn]]
- [[cm-pinns]]
- [[seisgpt]]
