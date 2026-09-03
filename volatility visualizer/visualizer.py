from datetime import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.interpolate import griddata
from scipy.optimize import brentq
from scipy.stats import norm
import yfinance as yf

tk = yf.Ticker("AAPL")

calls = []
puts = []

for date in tk.options:
    chain = tk.option_chain(date)
    chain.calls["Expiration_date"] = date
    chain.puts["Expiration_date"] = date

    calls.append(chain.calls)
    puts.append(chain.puts)

puts_df = pd.concat(puts, ignore_index=True)
calls_df = pd.concat(calls, ignore_index=True)

#Fetch actual current underlying price
Spot = float(tk.fast_info["last_price"])
r = 0.045  # Benchmark risk-free rate proxy (~4.5%)


def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)



def find_volatility(market_price, S, K, T, r):
    # Call option price cannot mathematically trade below intrinsic value
    intrinsic_value = max(0.0, S - K * np.exp(-r * T))
    if market_price <= intrinsic_value or T <= 0:
        return np.nan

    def objective(sigma):
        return black_scholes_call(S, K, T, r, sigma) - market_price

    try:
        # Search volatility between 1% (0.01) and 300% (3.0)
        return brentq(objective, a=0.01, b=3.0, maxiter=100)
    except (ValueError, RuntimeError):
        return np.nan


calls_df["mid_price"] = (calls_df["bid"] + calls_df["ask"]) / 2
calls_df["mid_price"] = calls_df["mid_price"].where(
    calls_df["mid_price"] > 0, calls_df["lastPrice"]
)

now = pd.Timestamp.now().normalize()
calls_df["T"] = (
    pd.to_datetime(calls_df["Expiration_date"]) - now
).dt.days / 365.0

clean_calls = calls_df[
    (calls_df["T"] > 25 / 365.0)
    & (calls_df["mid_price"] > 0.5)
    & (calls_df["volume"]>5)
    & (calls_df["strike"].between(Spot * 0.75, Spot * 1.25))
].copy()

# Fixed: Wrapped inside square brackets [ ... ]
clean_calls["implied_vol"] = [
    find_volatility(row["mid_price"], Spot, row["strike"], row["T"], r)
    for _, row in clean_calls.iterrows()
]
clean_calls.dropna(subset=["implied_vol"], inplace=True)
strikes = clean_calls["strike"].values
maturities = clean_calls["T"].values
ivs = clean_calls["implied_vol"].values

grid_k, grid_t = np.meshgrid(
    np.linspace(strikes.min(), strikes.max(), 40),
    np.linspace(maturities.min(), maturities.max(), 40),
)

grid_iv = griddata(
    points=(strikes, maturities),
    values=ivs,
    xi=(grid_k, grid_t),
    method="linear",  # Smooth surface interpolation
)

fig = go.Figure(
    data=[
        go.Surface(
            x=grid_k,
            y=grid_t,
            z=grid_iv * 100,  # Express IV as %
            colorscale="Viridis",
            colorbar=dict(title="IV (%)"),
        )
    ]
)
fig.add_trace(
    go.Scatter3d(
        x=clean_calls["strike"],
        y=clean_calls["T"],
        z=clean_calls["implied_vol"] * 100,
        mode="markers",
        marker=dict(size=2, color="white", opacity=0.7),
        name="Market Quotes",
    )
)
fig.update_layout(
    title=f"Implied Volatility Surface - AAPL (Spot: ${Spot:.2f})",
    scene=dict(
        xaxis_title="Strike Price ($)",
        yaxis_title="Maturity (Years)",
        zaxis_title="Implied Volatility (%)",
    ),
    width=900,
    height=650,
)

fig.show()