import pandas as pd
import numpy as np
from scipy.stats import norm
import os

df_rates = pd.read_excel('data/raw/Pricer Energetic - 3 (1).xls', sheet_name='Courbe des taux', header=None)
df_vol = pd.read_excel('data/raw/Pricer Energetic - 3 (1).xls', sheet_name="Surface de Volatilité", header=None)

def get_zc_cont(t_target):
    idx = df_rates[df_rates.iloc[:, 1] == t_target].index[0]
    taux_raw_base = df_rates.iloc[idx, 4] # Col E
    # But wait, user used shifted rates (-0.50%)
    # Let's use the exact values from user's screen:
    # 6Y: Taux = 4.60%. Exactly = 4.6049999...%
    return np.log(1 + taux_raw_base)

r_6 = get_zc_cont(6.0)
r_5 = get_zc_cont(5.0)
r_7 = get_zc_cont(7.0)

def get_vol(target_strike, maturity_col):
    strikes = pd.to_numeric(df_vol.iloc[7:, 2], errors='coerce').dropna()
    idx = (np.abs(strikes - target_strike)).idxmin()
    return float(df_vol.loc[idx, maturity_col])

vol_atm = get_vol(3600, 11)   # Col 11 is T=6
vol_150 = get_vol(5400, 11)   # Col 11 is T=6

S0 = 3600.0
NOMINAL = 100.0
T = 6.0

def bs_vanilla(S, K, T, r, sigma, is_call=True):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

def bs_digital(S, K, T, r, sigma, payout):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return payout * np.exp(-r * T) * norm.cdf(d2)

def price_product(S, T_val, r_val, v_atm, v_150):
    zc_pv = NOMINAL * np.exp(-r_val * T_val)
    qty = NOMINAL / 3600.0
    c_atm = bs_vanilla(S, 3600, T_val, r_val, v_atm)
    c_cap = bs_vanilla(S, 5400, T_val, r_val, v_150)
    digi_150 = bs_digital(S, 5400, T_val, r_val, v_150, 10.0)
    total = zc_pv + qty * (c_atm - c_cap) + digi_150
    return total, zc_pv, c_atm, c_cap, digi_150

# Base pricing
base_price, zc, c_atm, c_150, digi = price_product(S0, T, r_6, vol_atm, vol_150)
margin = 100.0 - base_price

# Sensitivity
margin_rate_down, _, _, _, _ = price_product(S0, T, r_6 - 0.0050, vol_atm, vol_150)
margin_vol_up, _, _, _, _ = price_product(S0, T, r_6, vol_atm+0.01, vol_150+0.01)

vol_atm_7 = get_vol(3600, 12)
vol_150_7 = get_vol(5400, 12)
margin_t_7, _, _, _, _ = price_product(S0, 7.0, r_7, vol_atm_7, vol_150_7)

# Sec Market
vol_atm_5 = get_vol(3600, 10)
vol_150_5 = get_vol(5400, 10)
sec_val, sec_zc, sec_atm, sec_150, sec_digi = price_product(S0, 5.0, r_5, vol_atm_5, vol_150_5)

print("=== NEW BASE PRICING ===")
print(f"r_6 = {r_6:.6f}")
print(f"ZC: {zc:.3f}")
print(f"Call ATM: {c_atm:.3f}")
print(f"Call 150%: {c_150:.3f}")
print(f"Digital 150%: {digi:.3f}")
print(f"Total Base Cost: {base_price:.3f}")
print(f"Margin: {margin:.3f}")
print("=== SENSITIVITIES ===")
print(f"Rates -50bp Cost: {margin_rate_down:.3f} | Margin: {100-margin_rate_down:.3f}")
print(f"Vol +1% Cost: {margin_vol_up:.3f} | Margin: {100-margin_vol_up:.3f}")
print(f"T=7 Cost: {margin_t_7:.3f} | Margin: {100-margin_t_7:.3f}")
print("=== SEC MARKET ===")
print(f"Cost: {sec_val:.3f}")
