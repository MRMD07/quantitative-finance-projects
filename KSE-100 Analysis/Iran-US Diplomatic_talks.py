from ast import And
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("Karachi 100 Historical Data.csv")
data['Price'] = data['Price'].str.replace(',','',regex = False).astype(float)
data['Date'] = pd.to_datetime(data['Date'])
data.sort_values(by = 'Date', ascending= True, inplace = True)
data.reset_index(drop = True, inplace = True)

data['Rolling_mean'] = data['Price'].rolling(window = 5).mean()

date = np.array(data['Date'])
price = np.array(data['Price'])

change =(( price[1:]-price[:-1])/price[:-1])*100

start_window = pd.to_datetime('2026-04-06')
end_window = pd.to_datetime('2026-04-17')
window =( data['Date']>= start_window)&( data['Date']<= end_window)

change = np.insert(change, 0, 0)
data['Changes']= change

window_returns = data.loc[window, 'Changes']
stdv = np.std(data['Changes'])

print(stdv)
print(data.loc[window,['Date','Changes']])

# 1. Create a 2-story plotting layout (Top chart for Price, Bottom chart for Changes)
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(11, 7))

# ---------------------------------------------------------
# TOP PANEL: KSE-100 Price and Moving Average