"""
ENERGETIC du CA — Section 6: Secondary Market Pricing
===================================================================
Calculates the theoretical price of the product exactly 1 year after issuance
(5 years remaining), assuming the spot price hasn't moved (S=3600).
It also calculates the bank's buyback bid price by applying a bid-ask penalty.
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
OUTPUT_MD = os.path.join(BASE_DIR, "data", "processed", "secondary_market_results.md")

# Product Parameters
S0 = 3600.0
NOMINAL = 100.0
CAP_PCT = 1.60
K_ATM = S0
K_CAP = S0 * CAP_PCT
QTY = NOMINAL / S0

def bs_call_price(S, K, T, r, sigma):
    if T <= 0: return np.maximum(S - K, 0)
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

def calculate_product_value(S, T, r, vol_atm, vol_cap, cap_pct=1.60):
    K_ATM = S0
    K_CAP = S0 * cap_pct
    
    cv_zc = NOMINAL * np.exp(-r * T)
    call_atm = bs_call_price(S, K_ATM, T, r, vol_atm)
    call_cap = bs_call_price(S, K_CAP, T, r, vol_cap)
    
    call_spread = call_atm - call_cap
    total_value = cv_zc + QTY * call_spread
    
    return total_value, cv_zc, call_atm, call_cap

def get_volatility(df_vol: pd.DataFrame, target_strike: float, target_maturity_col: int) -> float:
    strikes = pd.to_numeric(df_vol.iloc[7:, 2], errors='coerce').dropna()
    idx = (np.abs(strikes - target_strike)).idxmin()
    return float(df_vol.loc[idx, target_maturity_col])

def main():
    print(f"{'='*50}\n  SECTION 6: SECONDARY MARKET (1 Year Later)\n{'='*50}")
    
    rates_df = pd.read_csv(RATES_CSV)
    df_vol = pd.read_excel(EXCEL_PATH, sheet_name="Surface de Volatilité", header=None)
    
    # Extract 5Y parameters
    r_5 = rates_df[rates_df['T_years'] == 5.0].iloc[0]['ZC_Cont']
    # 5Y Volatility -> column 10
    vol_atm_5 = get_volatility(df_vol, S0, 10)
    vol_cap_5 = get_volatility(df_vol, S0 * 1.60, 10)
    
    print(f"Residual Maturity: 5 Years")
    print(f"Spot assumed constant at €{S0}")
    print(f"5-Year Interest Rate: {r_5*100:.3f}%")
    print(f"5-Year ATM Vol: {vol_atm_5*100:.2f}% | 160% Cap Vol: {vol_cap_5*100:.2f}%")
    
    # Calculate Mid Value at T+1
    mid_value, zc_val, opt_atm, opt_cap = calculate_product_value(S0, 5.0, r_5, vol_atm_5, vol_cap_5)
    
    print(f"\n{'='*50}\n  MTM PRODUCT VALUATION (MID PRICE)\n{'='*50}")
    print(f"ZC Bond PV (T=5)   : €{zc_val:.3f}")
    print(f"Options Package PV : €{QTY * (opt_atm - opt_cap):.3f}")
    print(f"---------------------------------------------")
    print(f"Theoretical Mid Price : €{mid_value:.3f} (for €100 nominal)")
    
    # Calculate Bid Value (Bank buyback)
    # Bank wants to pay less. They will:
    # 1. Discount ZC bond harder -> raise rates (e.g. +10 bp spread)
    # 2. Underprice the options package -> drop volatility (e.g. -2% vol spread)
    r_bid = r_5 + 0.0010
    vol_atm_bid = vol_atm_5 - 0.02
    vol_cap_bid = vol_cap_5 - 0.02 # Assuming parallel shift in surface
    
    bid_value, bid_zc, bid_atm, bid_cap = calculate_product_value(S0, 5.0, r_bid, vol_atm_bid, vol_cap_bid)
    
    print(f"\n{'='*50}\n  BANK BUYBACK (BID PRICE)\n{'='*50}")
    print("Assuming Bank spread of +10bp on rates and -2% on volatility.")
    print(f"Bid Price quoted to client: €{bid_value:.3f}")
    print(f"Hidden penalty/fees: €{mid_value - bid_value:.3f}")
    
    # Markdown
    md = f"""# Section 6: Secondary Market Pricing

**Assumption:** We advance exactly 1 year into the future. The residual maturity is **5 Years**. We assume the market parameters (rates shape, vol surface shape, and spot $S_0 = 3600$) roll down the curve naturally with no market shock.

### 6.1 T+1 Mid-Price Valuation
| Component | 5-Year Parameter | Value |
|-----------|------------------|-------|
| **Risk-Free Rate ($r_5$)** | `{r_5*100:.3f}%` | ZC Bond PV: **€{zc_val:.3f}** |
| **ATM Vol ($\sigma_5$)** | `{vol_atm_5*100:.2f}%` | ATM Call: **€{opt_atm:.3f}** |
| **Cap Vol ($\sigma_5$)** | `{vol_cap_5*100:.2f}%` | Cap Call: **€{opt_cap:.3f}** |

**Total Options Cost (Qty × Spread):** €{QTY * (opt_atm - opt_cap):.3f}
**Theoretical Mid Price:** **€{mid_value:.3f}**

> **Note:** Even though the spot price hasn't moved, the product value drops from its inception €100 nominal down to ~€{mid_value:.1f}. This is because the embedded upfront margin (€2.58) is immediately wiped out, and the options package sheds 1 year of time value (Theta decay). 

### 6.2 Bank Buyback Price (Bid)
When a client asks to sell their product back to the bank before maturity, the bank applies a bid-ask spread to protect themselves and extract early cancellation fees.

By applying an illustrative **+10 basis points** penalty to the discounting interest rate (lowering the bond PV) and a **-2%** penalty to the option volatilities (cheapening the options package), we arrive at the Bid Price:

- **Client Sell Price (Bid):** **€{bid_value:.3f}** 
- **Implicit Penalty:** €{mid_value - bid_value:.3f}
"""
    with open(OUTPUT_MD, "w") as f:
        f.write(md)

if __name__ == "__main__":
    main()
