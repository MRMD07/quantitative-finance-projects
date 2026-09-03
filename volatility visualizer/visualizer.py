import yfinance as yf
import pandas as pd
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

tk= yf.Ticker('AAPL')

calls = []
puts = []

for date in tk.options:

    chain = tk.option_chain(date)
    chain.calls["Expiration_date"]=date
    chain.puts["Expiration_date"]=date

    calls.append(chain.calls)
    puts.append(chain.puts)

puts_df = pd.concat(puts, ignore_index = True)
calls_df = pd.concat(calls, ignore_index= True)

Spot = puts

def black_scholes_call(S, K, T, r, sigma):
    # Calculates the theoretical call price
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

def find_volatility(market_price, S, K, T, r):
    # Objective function: difference between model price and target market price
    def objective(sigma):
        return black_scholes_call(S, K, T, r, sigma) - market_price