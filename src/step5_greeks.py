"""
Euro-Shield 6Y Horizon — Step 5: Greeks Computation
===================================================================
Calculates Delta, Vega, Rho, and Theta for the product.
"""

import os
import pandas as pd
import numpy as np
from scipy.stats import norm

# ──────────────────────────────────────────────
# Setup & File Paths
# ──────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
EXCEL_PATH = os.path.join(BASE_DIR, "data", "raw", "Pricer Energetic - 3 (1).xls")
RATES_CSV = os.path.join(BASE_DIR, "data", "processed", "yield_curve_bootstrapped.csv")
OUTPUT_MD = os.path.join(BASE_DIR, "data", "processed", "greeks_results.md")

# Product Parameters
S0 = 3600.0
NOMINAL = 100.0
T = 6.0
CAP_PCT = 1.60
K_ATM = S0
K_CAP = S0 * CAP_PCT
QTY = NOMINAL / S0

def get_volatility(df_vol: pd.DataFrame, target_strike: float, target_maturity_col: int = 11) -> float:
    for i in range(7, len(df_vol)):
        strike = df_vol.iloc[i, 2]
        if pd.notna(strike) and np.isclose(strike, target_strike):
            return float(df_vol.iloc[i, target_maturity_col])
    raise ValueError(f"Strike not found.")

def n_prime(x):
    """Density of standard normal distribution."""
    return np.exp(-x**2 / 2.0) / np.sqrt(2.0 * np.pi)

def bs_greeks(S, K, T, r, sigma):
    """Compute Delta, Vega, Rho, Theta for a European Call."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    Nd1 = norm.cdf(d1)
    Nd2 = norm.cdf(d2)
    
    delta = Nd1
    # Standard Vega is usually per 1% change, but raw is dS/dSigma
    vega = S * np.sqrt(T) * n_prime(d1) 
    # Standard Rho is usually per 1bp or 1%, raw is dS/dr
    rho = K * T * np.exp(-r * T) * Nd2
    # Standard Theta is usually per 1 day or 1 year, raw is dS/dt (time decay!)
    # Careful: theta is defined as derivative with respect to calendar time passing, so T decreases.
    term1 = -(S * n_prime(d1) * sigma) / (2 * np.sqrt(T))
    term2 = -r * K * np.exp(-r * T) * Nd2
    theta = term1 + term2
    
    return delta, vega, rho, theta

def zc_greeks(Face, T, r):
    """Compute Greeks for a Zero Coupon Bond."""
    pv = Face * np.exp(-r * T)
    delta = 0.0
    vega = 0.0
    rho = -T * pv
    # As time passes (T decreases), PV increases, so standard Theta is d/dt (Face * e^{-r(T-t)}) = r * pv
    theta = r * pv
    
    return delta, vega, rho, theta

def main():
    print(f"{'='*50}\n  STEP 5: PRODUCT GREEKS\n{'='*50}")
    
    # 1. Market Data
    rates_df = pd.read_csv(RATES_CSV)
    row_6y = rates_df[rates_df['T_years'] == T].iloc[0]
    r_continuous = row_6y['ZC_Cont']
    
    df_vol = pd.read_excel(EXCEL_PATH, sheet_name="Surface de Volatilité", header=None)
    vol_atm = get_volatility(df_vol, K_ATM, target_maturity_col=11)
    vol_cap = get_volatility(df_vol, K_CAP, target_maturity_col=11)
    
    # 2. Compute Individual Option Greeks (Raw)
    delta_atm, vega_atm, rho_atm, theta_atm = bs_greeks(S0, K_ATM, T, r_continuous, vol_atm)
    delta_cap, vega_cap, rho_cap, theta_cap = bs_greeks(S0, K_CAP, T, r_continuous, vol_cap)
    
    # 3. Compute ZC Bond Greeks (Raw)
    delta_zc, vega_zc, rho_zc, theta_zc = zc_greeks(NOMINAL, T, r_continuous)
    
    # 4. Compute Product Greeks (Per €100 product)
    # Note: Quantity is QTY.
    # We want standard reporting metrics:
    # Vega usually reported for 1% absolute shift in Volatility (/ 100)
    # Rho usually reported for 1bp shift in rates (/ 10000)
    # Theta usually reported for 1 day passage of time (/ 365)
    
    prod_delta = delta_zc + QTY * (delta_atm - delta_cap)
    
    # Raw sensitivity sum
    raw_vega = vega_zc + QTY * (vega_atm - vega_cap)
    prod_vega_1pct = raw_vega / 100.0
    
    raw_rho = rho_zc + QTY * (rho_atm - rho_cap)
    prod_rho_1bp = raw_rho / 10000.0
    
    raw_theta = theta_zc + QTY * (theta_atm - theta_cap)
    prod_theta_1d = raw_theta / 365.0
    
    print("Individual Component Details (Raw):")
    print(f"ATM Call -> Delta: {delta_atm:.4f}, Vega: {vega_atm:.0f}, Rho: {rho_atm:.0f}, Theta: {theta_atm:.0f}")
    print(f"Cap Call -> Delta: {delta_cap:.4f}, Vega: {vega_cap:.0f}, Rho: {rho_cap:.0f}, Theta: {theta_cap:.0f}")
    print(f"ZC Bond  -> Delta: {delta_zc:.4f}, Vega: {vega_zc:.0f}, Rho: {rho_zc:.0f}, Theta: {theta_zc:.0f}")
    
    print(f"\n{'='*50}\n  PRODUCT GREEK EXPOSURE (Per €100 nominal)\n{'='*50}")
    print(f"Delta               : {prod_delta:.4f} (Underlying equiv % per €100)")
    print(f"Vega (1% vol rise)  : €{prod_vega_1pct:+.4f}")
    print(f"Rho  (1bp rate rise): €{prod_rho_1bp:+.4f}")
    print(f"Theta (1 day passes): €{prod_theta_1d:+.4f}")
    
    # ──────────────────────────────────────────────
    # Output to markdown
    # ──────────────────────────────────────────────
    md = f"""# STEP 5: Greeks

| Greek | Value per €100 nominal | Interpretation for Trader |
|-------|------------------------|---------------------------|
| **Delta** | {prod_delta:.4f} | If spot jumps 1 point, product gains €{prod_delta/100:.4f}. It is highly long delta since we bought more ATM delta than we sold OTM delta. |
| **Vega** (+1%) | **€{prod_vega_1pct:+.4f}** | A 1% uniform rise in volatility increases product value by €{prod_vega_1pct:+.4f}. The product is strictly **Long Vega**. |
| **Rho** (+1bp) | **€{prod_rho_1bp:+.4f}** | A 1bp rise in the yield curve drops product value by €{abs(prod_rho_1bp):.4f}. The ZC bond duration makes the overall product strictly **Short Rho** (exposed to rising rates). |
| **Theta** (1 day)| **€{prod_theta_1d:+.4f}** | Every passing day holding spot constant brings the ZC bond closer to par (`+`), but decays option time value (`-`). Net impact is €{prod_theta_1d:+.4f} per day. |
"""
    with open(OUTPUT_MD, "w") as f:
        f.write(md)
    print(f"\nSaved Greeks to: {OUTPUT_MD}")

if __name__ == "__main__":
    main()
