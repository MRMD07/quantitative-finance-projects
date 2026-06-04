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
