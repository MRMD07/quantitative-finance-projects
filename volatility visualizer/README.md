# Real-Time 3D Implied Volatility Surface Visualizer

An end-to-end quantitative pipeline that fetches live option chain data, numerically solves for Black-Scholes Implied Volatility (IV), and fits an interactive 3D volatility surface.



## Overview
The standard Black-Scholes-Merton model assumes constant volatility across all strikes and maturities. In real financial markets, this assumption fails due to crash protection demand, tail risk, and supply-demand imbalances. 

This project constructs the empirical $(K, T, \sigma)$ volatility surface for any equity ticker using live exchange feeds, highlighting the real-world **volatility smile/skew** and **term structure**.

## Key Features
* **Live Ingestion:** Pulls complete option chains (calls/puts) and real-time spot prices dynamically via `yfinance`.
* **Numerical Root Finding:** Inverts the non-linear Black-Scholes formula for $\sigma$ via Brent's Method (`scipy.optimize.brentq`), achieving machine-level precision ($10^{-12}$).
* **Microstructure Data Cleaning:**
  * Computes mid-market prices $(\text{bid} + \text{ask})/2$ with fallback logic to strip out bid-ask spread bias.
  * Filters out contracts violating theoretical intrinsic value floors ($C \le \max(0, S - K e^{-rT})$).
  * Prunes short-dated noise ($T < 25\text{ days}$) to eliminate $1/\sqrt{T}$ division instability.
  * Filters for strike liquidity and non-zero volume.
* **Surface Interpolation & Rendering:** Interpolates sparse, irregular strike/maturity points onto a uniform 2D meshgrid via `scipy.interpolate.griddata` (`linear`), overlaid with discrete quote markers via `plotly.graph_objects`.

## Mathematical Core

Black-Scholes pricing for a European call:

$$C(S, K, T, r, \sigma) = S \cdot N(d_1) - K e^{-rT} N(d_2)$$

where:

$$d_1 = \frac{\ln(S/K) + (r + \frac{1}{2}\sigma^2)T}{\sigma\sqrt{T}}, \quad d_2 = d_1 - \sigma\sqrt{T}$$

Because $\sigma$ cannot be isolated algebraically, the engine sets up an objective function:

$$f(\sigma) = C_{\text{model}}(\sigma) - C_{\text{market}} = 0$$

and solves for $\sigma \in [0.01, 3.0]$ dynamically.

## Tech Stack
* **Language:** Python 3.10+
* **Data Processing:** `pandas`, `numpy`, `yfinance`
* **Numerical Methods:** `scipy` (`optimize.brentq`, `interpolate.griddata`, `stats.norm`)
* **Interactive 3D Graphics:** `plotly`

## Installation & Setup

1. **Clone the repository:**
```bash
git clone [https://github.com/your-username/volatility-surface-visualizer.git](https://github.com/your-username/volatility-surface-visualizer.git)
cd volatility-surface-visualizer
