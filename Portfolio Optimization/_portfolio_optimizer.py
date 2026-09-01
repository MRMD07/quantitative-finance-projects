
import pandas as pd
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

btc_data = pd.read_csv("Bitcoin Historical Data.csv")
gold_data = pd.read_csv("Gold Futures Historical Data.csv")
kse100_data = pd.read_csv("Karachi 100 Historical Data.csv")

btc_data['Change %'] = btc_data['Change %'].str.replace('%','',regex = False).astype(float)
gold_data['Change %'] = gold_data['Change %'].str.replace('%','',regex = False).astype(float)
kse100_data['Change %'] = kse100_data['Change %'].str.replace('%','',regex = False).astype(float)

btc_data.sort_values(by = 'Date', ascending= True, inplace = True)
gold_data.sort_values(by = 'Date', ascending= True, inplace = True)
kse100_data.sort_values(by = 'Date', ascending= True, inplace = True)

btc_data['Change %'] = btc_data['Change %'].astype(float)
gold_data['Change %'] = gold_data['Change %'].astype(float)
kse100_data['Change %'] = kse100_data['Change %'].astype(float)


btc_variance = btc_data['Change %'].var()
gold_variance = gold_data['Change %'].var()
kse100_variance = kse100_data['Change %'].var()

btc_gold_cov = btc_data['Change %'].cov(gold_data['Change %'])
btc_kse100_cov = btc_data['Change %'].cov(kse100_data['Change %'])
gold_kse100_cov = gold_data['Change %'].cov(kse100_data['Change %'])

l, w1, w2, w3, kv, gv, bv, kbv, kgv, gbv = sp.symbols('l w1 w2 w3 kv gv bv kbv kgv gbv')
kgv = gold_kse100_cov
kbv = btc_kse100_cov
gbv = btc_gold_cov
kv = kse100_variance
bv = btc_variance
gv = gold_variance

eq1 = sp.Eq(w1 + w2 + w3, 1)
eq2 = sp.Eq((2*w1*bv)+(2*w2*kbv)+(2*w3*gbv) - l,0)
eq3 = sp.Eq((2*w1*kbv)+(2*w2*kv)+(2*w3*kgv) - l,0)
eq4 = sp.Eq((2*w1*gbv)+(2*w2*kgv)+(2*w3*gv) - l,0)

solution = sp.solve([eq1, eq2, eq3, eq4],(w1,w2,w3,l))
print(solution)


# 1. Convert SymPy solutions to standard Python floats and map to asset names
portfolio_weights = {
    'Bitcoin (w1)': float(solution[w1]),
    'KSE-100 (w2)': float(solution[w2]),
    'Gold (w3)': float(solution[w3])
}

# 2. Create the plot
plt.figure(figsize=(9, 5))
colors = ['#F7931A', '#00A651', '#D4AF37'] # Asset matching colors (Orange, Green, Gold)

# 3. Plot bars
bars = plt.bar(portfolio_weights.keys(), portfolio_weights.values(), color=colors, edgecolor='black')

# 4. Add a baseline at 0 to clearly show the negative/short position
plt.axhline(0, color='black', linewidth=1.2, linestyle='-')

# 5. Add value labels on top/bottom of each bar
for bar in bars:
    height = bar.get_height()
    label_y = height + 0.02 if height >= 0 else height - 0.05
    plt.text(bar.get_x() + bar.get_width()/2.0, label_y, f'{height*100:.2f}%', 
             ha='center', va='center', fontweight='bold')

# 6. Titles and Layout clean up
plt.title('Absolute Minimum Risk Portfolio Allocations (KSE-100 / BTC / GOLD)', fontsize=12, fontweight='bold', pad=15)
plt.ylabel('Portfolio Weight (Percentage Allocation)', fontsize=10)
plt.ylim(min(portfolio_weights.values()) - 0.1, max(portfolio_weights.values()) + 0.1)
plt.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()
