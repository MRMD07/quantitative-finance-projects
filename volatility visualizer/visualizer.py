import yfinance as yf
import pandas as pd
import numpy as np

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


