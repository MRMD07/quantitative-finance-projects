# 📈 Global Minimum Variance Portfolio Optimizer (BTC, KSE-100, Gold)

An analytical portfolio optimization engine that computes the **Absolute Minimum Risk Portfolio** across three distinct asset classes: **Cryptocurrency (Bitcoin)**, **Equities (Pakistan's KSE-100 Index)**, and **Commodities (Gold Futures)** using Modern Portfolio Theory (MPT) and symbolic mathematics with SymPy.

---

## 📌 Project Overview

This project determines the optimal asset allocation weights that minimize overall portfolio variance under the constraint that total capital allocation equals 100% ($\sum w_i = 1$). 

Instead of numerical approximations, the model solves the constrained optimization problem **analytically** using the **Method of Lagrange Multipliers** solved symbolically via `sympy`.

---

## 🧮 Mathematical Formulation

### 1. Portfolio Variance ($\sigma_p^2$)
For a three-asset portfolio with weights $w_1$ (BTC), $w_2$ (KSE-100), and $w_3$ (Gold):

$$\sigma_p^2 = w_1^2 \sigma_1^2 + w_2^2 \sigma_2^2 + w_3^2 \sigma_3^2 + 2w_1 w_2 \sigma_{12} + 2w_1 w_3 \sigma_{13} + 2w_2 w_3 \sigma_{23}$$

### 2. Lagrangian Function ($\mathcal{L}$)
Subject to the budget constraint $w_1 + w_2 + w_3 = 1$:

$$\mathcal{L}(w_1, w_2, w_3, \lambda) = \sigma_p^2 - \lambda(w_1 + w_2 + w_3 - 1)$$

### 3. First-Order Necessary Conditions (FONC)
Setting partial derivatives with respect to $w_1, w_2, w_3,$ and $\lambda$ to zero yields a linear system of 4 equations:

$$\frac{\partial \mathcal{L}}{\partial w_1} = 2w_1\sigma_1^2 + 2w_2\sigma_{12} + 2w_3\sigma_{13} - \lambda = 0$$

$$\frac{\partial \mathcal{L}}{\partial w_2} = 2w_1\sigma_{12} + 2w_2\sigma_2^2 + 2w_3\sigma_{23} - \lambda = 0$$

$$\frac{\partial \mathcal{L}}{\partial w_3} = 2w_1\sigma_{13} + 2w_2\sigma_{23} + 2w_3\sigma_3^2 - \lambda = 0$$

$$\frac{\partial \mathcal{L}}{\partial \lambda} = w_1 + w_2 + w_3 - 1 = 0$$

---

## 📁 Folder Structure

```text
├── Bitcoin Historical Data.csv       # Daily historical BTC price data
├── Gold Futures Historical Data.csv  # Daily historical Gold futures data
├── Karachi 100 Historical Data.csv   # Daily historical KSE-100 index data
├── portfolio_optimizer.py            # Main calculation and visualization script
├── requirements.txt                  # Python dependencies
├── README.md                         # Project documentation 
└── portfolio_analysis.png
