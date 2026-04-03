"""
Euro-Shield 6Y Horizon — Step 6: Sensitivity Analysis
===================================================================
Calculates the impact on Bank Margin for different market shifts.
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
OUTPUT_MD = os.path.join(BASE_DIR, "data", "processed", "sensitivity_results.md")

# Baseline Parameters
S0 = 3600.0
NOMINAL = 100.0

def bs_call_price(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

def calculate_margin(T, r, vol_atm, vol_cap, cap_pct):
    QTY = NOMINAL / S0
    K_ATM = S0
    K_CAP = S0 * cap_pct
    
    # PV of ZC
    cv_zc = NOMINAL * np.exp(-r * T)
    
    # Calls
    call_atm = bs_call_price(S0, K_ATM, T, r, vol_atm)
    call_cap = bs_call_price(S0, K_CAP, T, r, vol_cap)
    
    # Cost & Margin
    call_spread = call_atm - call_cap
    total_cost = cv_zc + QTY * call_spread
    margin = NOMINAL - total_cost
    
    return margin, cv_zc, call_spread

def get_volatility(df_vol: pd.DataFrame, target_strike: float, target_maturity_col: int) -> float:
    # Use closest available strike if exact doesn't exist
    strikes = pd.to_numeric(df_vol.iloc[7:, 2], errors='coerce').dropna()
    idx = (np.abs(strikes - target_strike)).idxmin()
    return float(df_vol.loc[idx, target_maturity_col])

def main():
    print(f"{'='*50}\n  SECTION 5: SENSITIVITY ANALYSIS\n{'='*50}")
    
    rates_df = pd.read_csv(RATES_CSV)
    df_vol = pd.read_excel(EXCEL_PATH, sheet_name="Surface de Volatilité", header=None)
    
    # BASELINE extraction (T=6) -> column 11 for T=6
    r_6 = rates_df[rates_df['T_years'] == 6.0].iloc[0]['ZC_Cont']
    vol_atm_6 = get_volatility(df_vol, S0, 11)
    vol_cap_6 = get_volatility(df_vol, S0 * 1.60, 11)
    
    base_margin, base_zc, base_spread = calculate_margin(6.0, r_6, vol_atm_6, vol_cap_6, 1.60)
    print(f"BASELINE MARGIN: €{base_margin:.3f}")
    
    results = []
    
    # ──────────────────────────────────────────────
    # SCENARIO 1: Rate Shift (-50 bp)
    # ──────────────────────────────────────────────
    r_shift = r_6 - 0.0050
    m_rate, _, _ = calculate_margin(6.0, r_shift, vol_atm_6, vol_cap_6, 1.60)
    diff_rate = m_rate - base_margin
    print(f"Scenario 1 (-50bp Rates): Margin = €{m_rate:.3f} | Diff: €{diff_rate:+.3f}")
    results.append(("-50bp Rates", m_rate, diff_rate))
    
    # ──────────────────────────────────────────────
    # SCENARIO 2: Volatility Shift (+1%)
    # ──────────────────────────────────────────────
    m_vol, _, _ = calculate_margin(6.0, r_6, vol_atm_6 + 0.01, vol_cap_6 + 0.01, 1.60)
    diff_vol = m_vol - base_margin
    print(f"Scenario 2 (+1% Volatility): Margin = €{m_vol:.3f} | Diff: €{diff_vol:+.3f}")
    results.append(("+1% Volatility", m_vol, diff_vol))
    
    # ──────────────────────────────────────────────
    # SCENARIO 3: Maturity (+1 Year, T=7)
    # ──────────────────────────────────────────────
    r_7 = rates_df[rates_df['T_years'] == 7.0].iloc[0]['ZC_Cont']
    # column 12 for T=7
    vol_atm_7 = get_volatility(df_vol, S0, 12)
    vol_cap_7 = get_volatility(df_vol, S0 * 1.60, 12)
    
    m_mat, _, _ = calculate_margin(7.0, r_7, vol_atm_7, vol_cap_7, 1.60)
    diff_mat = m_mat - base_margin
    print(f"Scenario 3 (T=7 Years): Margin = €{m_mat:.3f} | Diff: €{diff_mat:+.3f}")
    results.append(("Maturity 7 Years", m_mat, diff_mat))
    
    # ──────────────────────────────────────────────
    # SCENARIO 4: Cap Variation (59% and 61%)
    # ──────────────────────────────────────────────
    vol_cap_59 = get_volatility(df_vol, S0 * 1.59, 11)
    m_cap_59, _, _ = calculate_margin(6.0, r_6, vol_atm_6, vol_cap_59, 1.59)
    diff_cap_59 = m_cap_59 - base_margin
    print(f"Scenario 4 (Cap 159%): Margin = €{m_cap_59:.3f} | Diff: €{diff_cap_59:+.3f}")
    results.append(("Cap down to 59%", m_cap_59, diff_cap_59))
    
    vol_cap_61 = get_volatility(df_vol, S0 * 1.61, 11)
    m_cap_61, _, _ = calculate_margin(6.0, r_6, vol_atm_6, vol_cap_61, 1.61)
    diff_cap_61 = m_cap_61 - base_margin
    print(f"Scenario 4 (Cap 161%): Margin = €{m_cap_61:.3f} | Diff: €{diff_cap_61:+.3f}")
    results.append(("Cap up to 61%", m_cap_61, diff_cap_61))
    
    # ──────────────────────────────────────────────
    # Markdown Output
    # ──────────────────────────────────────────────
    md = f"""# Section 5: Sensitivity Analysis (Bank Margin)

**Baseline Margin:** €{base_margin:.3f}

| Scenario | Adjusted Parameter | New Margin (€) | Impact vs Baseline | Interpretation |
|----------|--------------------|----------------|--------------------|----------------|
| **1. Rates Fall (-50bp)** | $r = {r_shift*100:.3f}\\% $ | **{m_rate:.3f}** | *{diff_rate:+.3f}* | Lower yields severely harm the bank because the zero-coupon bond becomes much more expensive to purchase. |
| **2. Volatility Rises (+1%)** | $\sigma_{{atm}} = {(vol_atm_6+0.01)*100:.2f}\\%, \sigma_{{cap}} = {(vol_cap_6+0.01)*100:.2f}\\%\ $ | **{m_vol:.3f}** | *{diff_vol:+.3f}* | Higher vol hurts the margin slightly (the product is structurally Short Vega). |
| **3. Extend Maturity (7Y)** | $T = 7, r_7 = {r_7*100:.3f}\\% $ | **{m_mat:.3f}** | *{diff_mat:+.3f}* | Extending maturity is highly beneficial. ZC Bond is heavily discounted, buying the bank much more margin budget to spend on options. |
| **4. Cap Tightened (59%)** | $K_{{cap}} = 159\\%$ | **{m_cap_59:.3f}** | *{diff_cap_59:+.3f}* | Lowering the cap helps the margin. The bank sells a tighter call, capturing more premium. |
| **4. Cap Loosened (61%)** | $K_{{cap}} = 161\\%$ | **{m_cap_61:.3f}** | *{diff_cap_61:+.3f}* | Raising the cap hurts the margin. The short option is further OTM and worthless, returning less premium. |
"""
    with open(OUTPUT_MD, "w") as f:
        f.write(md)
    print(f"\nSaved Sensitivity Results to: {OUTPUT_MD}")

if __name__ == "__main__":
    main()
