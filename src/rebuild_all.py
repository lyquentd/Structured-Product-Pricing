import pandas as pd
import numpy as np
from scipy.stats import norm
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
EXCEL_PATH = os.path.join(BASE_DIR, "data", "raw", "Pricer Energetic - 3 (1).xls")
RATES_CSV = os.path.join(BASE_DIR, "data", "processed", "yield_curve_bootstrapped.csv")

S0 = 3600.0
NOMINAL = 100.0
T = 6.0

# 1. READ MARKET DATA
rates_df = pd.read_csv(RATES_CSV)
r_6 = rates_df[rates_df['T_years'] == 6.0].iloc[0]['ZC_Cont']
df_vol = pd.read_excel(EXCEL_PATH, sheet_name="Surface de Volatilité", header=None)

def get_vol(target_strike, maturity_col):
    strikes = pd.to_numeric(df_vol.iloc[7:, 2], errors='coerce').dropna()
    idx = (np.abs(strikes - target_strike)).idxmin()
    return float(df_vol.loc[idx, maturity_col])

vol_atm = get_vol(3600, 11)   # Col 11 is T=6
vol_150 = get_vol(5400, 11)

# 2. PRICING FUNCTIONS
def bs_vanilla(S, K, T, r, sigma, is_call=True):
    if T==0: return max(S-K,0) if is_call else max(K-S,0)
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if is_call: return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2), norm.cdf(d1), norm.cdf(d2)
    else: return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1), norm.cdf(-d1), norm.cdf(-d2)

def bs_digital(S, K, T, r, sigma, payout):
    if T==0: return payout if S>=K else 0
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return payout * np.exp(-r * T) * norm.cdf(d2), norm.cdf(d1), norm.cdf(d2)

def price_product(S, T_val, r_val, v_atm, v_150):
    zc_pv = NOMINAL * np.exp(-r_val * T_val)
    qty = NOMINAL / 3600.0
    
    call_atm, d1_atm, d2_atm = bs_vanilla(S, 3600, T_val, r_val, v_atm)
    call_150, d1_150, d2_150 = bs_vanilla(S, 5400, T_val, r_val, v_150)
    # Digital payout is exactly 10 euros per 100 nominal.
    # Wait, the nominal is 100. Payout is 10.
    digi_150, d1_dig, d2_dig = bs_digital(S, 5400, T_val, r_val, v_150, 10.0)
    
    total = zc_pv + qty * (call_atm - call_150) + digi_150
    return total, zc_pv, call_atm, call_150, digi_150

# Base pricing
base_price, zc, c_atm, c_150, digi = price_product(S0, T, r_6, vol_atm, vol_150)
margin = 100.0 - base_price

# Sensitivity
margin_rate_down, _, _, _, _ = price_product(S0, T, r_6 - 0.0050, vol_atm, vol_150)
margin_vol_up, _, _, _, _ = price_product(S0, T, r_6, vol_atm+0.01, vol_150+0.01)

r_7 = rates_df[rates_df['T_years'] == 7.0].iloc[0]['ZC_Cont']
vol_atm_7 = get_vol(3600, 12)
vol_150_7 = get_vol(5400, 12)
margin_t_7, _, _, _, _ = price_product(S0, 7.0, r_7, vol_atm_7, vol_150_7)

# Sec Market
r_5 = rates_df[rates_df['T_years'] == 5.0].iloc[0]['ZC_Cont']
vol_atm_5 = get_vol(3600, 10)
vol_150_5 = get_vol(5400, 10)
sec_val, sec_zc, sec_atm, sec_150, sec_digi = price_product(S0, 5.0, r_5, vol_atm_5, vol_150_5)

# Greeks (finite diff)
dP = 0.01
price_up,_,_,_,_ = price_product(S0 * 1.01, T, r_6, vol_atm, vol_150)
price_dn,_,_,_,_ = price_product(S0 * 0.99, T, r_6, vol_atm, vol_150)
delta = (price_up - price_dn) / (S0 * 0.02) * S0  # Delta per 100 nominal

price_v_up,_,_,_,_ = price_product(S0, T, r_6, vol_atm+0.01, vol_150+0.01)
price_v_dn,_,_,_,_ = price_product(S0, T, r_6, vol_atm-0.01, vol_150-0.01)
vega = (price_v_up - price_v_dn) / 2.0  # per 1% vol

price_r_up,_,_,_,_ = price_product(S0, T, r_6+0.0001, vol_atm, vol_150)
price_r_dn,_,_,_,_ = price_product(S0, T, r_6-0.0001, vol_atm, vol_150)
rho = (price_r_up - price_r_dn) / 2.0  # per 1bp

price_t_up,_,_,_,_ = price_product(S0, T - 1/365.0, r_6, vol_atm, vol_150)
theta = (price_t_up - base_price) # 1 day passing

print("=== VOLS ===")
print(f"Vol ATM: {vol_atm:.4f}, Vol 150%: {vol_150:.4f}")
print("=== NEW BASE PRICING ===")
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
print("=== GREEKS ===")
print(f"Delta: {delta:.4f}")
print(f"Vega: {vega:.4f}")
print(f"Rho: {rho:.4f}")
print(f"Theta: {theta:.4f}")
print("=== SEC MARKET ===")
print(f"Cost: {sec_val:.3f}")
