"""
ENERGETIC du CA — Step 3 & 4: Black-Scholes Pricing & Bank Margin
===================================================================
Prices the components of the product using the bootstrapped ZC continuous
rate and implied volatilities from the surface. Computes the bank margin.
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
OUTPUT_MD = os.path.join(BASE_DIR, "data", "processed", "pricing_results.md")

# Product Parameters
S0 = 3600.0
NOMINAL = 100.0
T = 6.0
CAP_PCT = 1.60
K_ATM = S0
K_CAP = S0 * CAP_PCT
QTY = NOMINAL / S0

def get_volatility(df_vol: pd.DataFrame, target_strike: float, target_maturity_col: int = 11) -> float:
    """Finds the volatility for a specific strike from the vol surface."""
    # Excel format: row 6 = headers. Strike is in column 2 (index 2).
    # 6y maturity is in column "6y" (index 11).
    for i in range(7, len(df_vol)):
        strike = df_vol.iloc[i, 2]
        if pd.notna(strike) and np.isclose(strike, target_strike):
            return float(df_vol.iloc[i, target_maturity_col])
    raise ValueError(f"Strike {target_strike} not found in vol surface.")

def bs_call_details(S, K, T, r, sigma):
    """Returns d1, d2, Nd1, Nd2, and Call price."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    Nd1 = norm.cdf(d1)
    Nd2 = norm.cdf(d2)
    
    call_price = S * Nd1 - K * np.exp(-r * T) * Nd2
    return d1, d2, Nd1, Nd2, call_price

def main():
    print(f"{'='*50}\n  STEP 3: EXTRACTING MARKET DATA\n{'='*50}")
    
    # 1. Read Rate Data
    rates_df = pd.read_csv(RATES_CSV)
    # Get 6Y rate
    row_6y = rates_df[rates_df['T_years'] == T].iloc[0]
    r_continuous = row_6y['ZC_Cont']
    df_6y = row_6y['DF']
    
    print(f"Risk-free rate (r) for T={T}y : {r_continuous:.6f} ({r_continuous*100:.3f}%)")
    print(f"Discount Factor for T={T}y   : {df_6y:.6f}")
    
    # 2. Read Volatility Data (from Excel)
    print("\nReading volatility surface from Excel...")
    df_vol = pd.read_excel(EXCEL_PATH, sheet_name="Surface de Volatilité", header=None)
    
    vol_atm = get_volatility(df_vol, K_ATM, target_maturity_col=11)
    vol_cap = get_volatility(df_vol, K_CAP, target_maturity_col=11)
    
    print(f"Volatility ATM (K={K_ATM})    : {vol_atm:.6f} ({vol_atm*100:.2f}%)")
    print(f"Volatility Cap (K={K_CAP}) : {vol_cap:.6f} ({vol_cap*100:.2f}%)")
    
    print(f"\n{'='*50}\n  STEP 4: BLACK-SCHOLES PRICING & MARGIN\n{'='*50}")
    
    # 3. Price Lego 1: Zero Coupon Bond
    pv_zc = NOMINAL * df_6y
    print(f"Lego 1: ZC Bond PV: €{pv_zc:.4f}")
    
    # 4. Price Lego 2: Long ATM Call
    d1_a, d2_a, Nd1_a, Nd2_a, call_atm = bs_call_details(S0, K_ATM, T, r_continuous, vol_atm)
    print(f"\nLego 2: Long ATM Call (K={K_ATM}, vol={vol_atm*100:.2f}%)")
    print(f"  d1 = {d1_a:.4f}, Nd1 = {Nd1_a:.4f}")
    print(f"  d2 = {d2_a:.4f}, Nd2 = {Nd2_a:.4f}")
    print(f"  Call Price = €{call_atm:.4f}")
    
    # 5. Price Lego 3: Short OTM Call (Cap)
    d1_c, d2_c, Nd1_c, Nd2_c, call_cap = bs_call_details(S0, K_CAP, T, r_continuous, vol_cap)
    print(f"\nLego 3: Short 160% Call (K={K_CAP}, vol={vol_cap*100:.2f}%)")
    print(f"  d1 = {d1_c:.4f}, Nd1 = {Nd1_c:.4f}")
    print(f"  d2 = {d2_c:.4f}, Nd2 = {Nd2_c:.4f}")
    print(f"  Call Price = €{call_cap:.4f}")
    
    # 6. Total Valuation per €100 nominal
    call_spread = call_atm - call_cap
    options_cost = QTY * call_spread
    
    total_cost = pv_zc + options_cost
    bank_margin = NOMINAL - total_cost
    
    print(f"\n{'='*50}\n  PRODUCT VALUATION SUMMARY\n{'='*50}")
    print(f"ZC Bond PV (1 unit)                : €{pv_zc:>7.3f}")
    print(f"Call Spread Price (1 unit)         : €{call_spread:>7.3f}")
    print(f"Total Options Cost (Qty × Spread)  : €{options_cost:>7.3f}")
    print(f"---------------------------------------------")
    print(f"Total Product Manufacturing Cost   : €{total_cost:>7.3f}")
    print(f"Selling Price                      : €{NOMINAL:>7.3f}")
    print(f"---------------------------------------------")
    print(f"Upfront Bank Margin                : €{bank_margin:>7.3f} ({bank_margin/NOMINAL*100:.2f}%)")
    
    # ──────────────────────────────────────────────
    # Output markdown doc
    # ──────────────────────────────────────────────
    md = f"""# ENERGETIC du CA \u2014 Pricing Results

### 1. Market Data Parameters (T = 6)
- **Risk-free continuous rate ($r_c$)**: {r_continuous:.6f} ({r_continuous*100:.3f}%)
- **Discount Factor**: {df_6y:.6f}
- **Volatility ATM (K={K_ATM})**: {vol_atm:.6f} ({vol_atm*100:.2f}%)
- **Volatility Cap (K={K_CAP})**: {vol_cap:.6f} ({vol_cap*100:.2f}%)

### 2. Pricing Components
| Component | Formula | Value (€) | Notes |
|-----------|---------|-----------|-------|
| **Lego 1** (ZC Bond) | $100 \times DF_6$ | **{pv_zc:.3f}** | Cost of capital guarantee |
| **Lego 2** (ATM Call)| $BS(S, K={K_ATM})$ | **{call_atm:.3f}** | $d_1$: {d1_a:.3f}, $N(d_1)$: {Nd1_a:.3f} |
| **Lego 3** (160% Call)| $BS(S, K={K_CAP})$ | **{call_cap:.3f}** | $d_1$: {d1_c:.3f}, $N(d_1)$: {Nd1_c:.3f} |

### 3. Valuation & Margin (Per €100 Nominal)
- **Option Quantity:** $100 / S_0 = {QTY:.6f}$
- **Call Spread Cost:** $Qty \times (Call_{{ATM}} - Call_{{160\\%}}) = {options_cost:.3f}$
- **Total Manufacturing Cost:** $PV(ZC) + Option Cost = {total_cost:.3f}$
- **Bank Upfront Margin:** $100 - Cost = {bank_margin:.3f}$ ({bank_margin/NOMINAL*100:.2f}%)
"""
    with open(OUTPUT_MD, "w") as f:
        f.write(md)
    print(f"\nSaved detailed markdown to: {OUTPUT_MD}")

if __name__ == "__main__":
    main()
