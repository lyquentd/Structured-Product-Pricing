import numpy as np
import matplotlib.pyplot as plt
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
IMAGES_DIR = os.path.join(BASE_DIR, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

# Performance of underlying (S_T / S_0)
s_perf = np.linspace(0.5, 2.0, 500)

# Build Legos
zc_bond = np.full_like(s_perf, 100.0)
long_call_atm = np.maximum(0, s_perf - 1.0) * 100
short_call_cap = -np.maximum(0, s_perf - 1.50) * 100
digital_call = np.where(s_perf >= 1.50, 10.0, 0.0)

# Total product
total_payoff = zc_bond + long_call_atm + short_call_cap + digital_call

# Plot 1: Decomposition
plt.figure(figsize=(10, 6))
plt.plot(s_perf, zc_bond, '--', label='Lego 1: ZC Bond', color='gray')
plt.plot(s_perf, long_call_atm, '--', label='Lego 2: Long Call ATM 100%', color='green')
plt.plot(s_perf, short_call_cap, '--', label='Lego 3: Short Call Cap 150%', color='red')
plt.plot(s_perf, digital_call, '--', label='Lego 4: Long Digital Call 150%', color='orange')
plt.plot(s_perf, total_payoff, '-', label='Product Total Payoff', color='blue', linewidth=3)
plt.axvline(1.0, color='black', alpha=0.2, linestyle=':')
plt.axvline(1.5, color='black', alpha=0.2, linestyle=':')
plt.title("Euro-Shield 6Y Horizon - 4-Lego Decomposition")
plt.xlabel("Index Performance (S_T / S_0)")
plt.ylabel("Redemption % of Nominal")
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0f}%'.format(y)))
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0f}%'.format(x*100)))
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, "payoff_decomposition.png"))
plt.close()

# Plot 2: Total Product
plt.figure(figsize=(10, 6))
plt.plot(s_perf, total_payoff, '-', color='#004b79', linewidth=4)
plt.axvline(1.5, color='#4ba3d3', linestyle='--')
plt.axhline(100, color='gray', linestyle='--', alpha=0.5)
plt.fill_between(s_perf, 150, 160, where=s_perf>=1.5, color='#4ba3d3', alpha=0.2)
plt.text(0.75, 102, "Capital protected at maturity", ha='center',
         bbox=dict(facecolor='white', edgecolor='lightblue', boxstyle='round,pad=0.3'))
plt.text(1.25, 130, "Linear participation\nfrom 100% to 150%", ha='center',
         bbox=dict(facecolor='white', edgecolor='lightblue', boxstyle='round,pad=0.3'))
plt.text(1.75, 162, "Maximum redemption: 160%", ha='center', fontweight='bold')
plt.text(1.75, 145, "+10% bonus above 150%", ha='center',
         bbox=dict(facecolor='aliceblue', edgecolor='lightblue', boxstyle='round,pad=0.3'), color='#005a96')
plt.title("Euro-Shield 6Y Horizon - True Final Payoff")
plt.xlabel("Euro Stoxx 50 performance at maturity")
plt.ylabel("Redemption (% of nominal)")
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0f}%'.format(y)))
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0f}%'.format(x*100)))
plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, "payoff_product.png"))
plt.close()

from scipy.stats import norm

def bs_vanilla(S, K, T, r, sigma):
    with np.errstate(divide='ignore', invalid='ignore'):
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return np.where(T == 0, np.maximum(S-K,0), call_price)

def bs_digital(S, K, T, r, sigma, payout):
    with np.errstate(divide='ignore', invalid='ignore'):
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        val = payout * np.exp(-r * T) * norm.cdf(d2)
    return np.where(T == 0, np.where(S>=K, payout, 0), val)

# Plot 3: Time Horizons (MTM Evolution)
S_arr = s_perf * 3600.0
horizons = [6.0, 3.0, 1.0, 0.0]
plt.figure(figsize=(10, 6))

# Approximate static parameters for the visualization
r_mock = 0.045
vol_atm = 0.27
vol_cap = 0.24

for h in horizons:
    if h == 0.0:
        plt.plot(s_perf, total_payoff, label='At Maturity (T=0)', color='black', linewidth=3)
    else:
        zc_pv = 100 * np.exp(-r_mock * h)
        qty = 100.0 / 3600.0
        c_atm = bs_vanilla(S_arr, 3600, h, r_mock, vol_atm)
        c_cap = bs_vanilla(S_arr, 5400, h, r_mock, vol_cap)
        d_cap = bs_digital(S_arr, 5400, h, r_mock, vol_cap, 10.0)
        mtm = zc_pv + qty * (c_atm - c_cap) + d_cap
        plt.plot(s_perf, mtm, label=f'Time to Maturity: {h}y')

plt.title("Euro-Shield 6Y Horizon - Mark-to-Market Evolution")
plt.xlabel("Index Performance (S_T / S_0)")
plt.ylabel("Theoretical Mid Price (% of Nominal)")
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0f}%'.format(y)))
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0f}%'.format(x*100)))
plt.axhline(100, color='gray', linestyle='--', alpha=0.5)
plt.axvline(1.0, color='gray', linestyle='--', alpha=0.5)
plt.axvline(1.5, color='gray', linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, "payoff_time_horizons.png"))
plt.close()
