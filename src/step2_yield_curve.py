"""
ENERGETIC du CA — Step 2: Yield Curve Bootstrapping
======================================================
Reads swap rates from Excel, bootstraps ZC discrete and
continuous rates, and computes Discount Factors for all maturities.
"""

import os
import pandas as pd
import numpy as np

# ──────────────────────────────────────────────
# Setup & File Paths
# ──────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
EXCEL_PATH = os.path.join(BASE_DIR, "data", "raw", "Pricer Energetic - 3 (1).xls")
OUTPUT_CSV = os.path.join(BASE_DIR, "data", "processed", "yield_curve_bootstrapped.csv")
OUTPUT_MD = os.path.join(BASE_DIR, "data", "processed", "yield_curve_bootstrapped.md")

def main():
    # Read the yield curve sheet from Excel
    print("Reading 'Courbe des taux' from Excel...")
    df_raw = pd.read_excel(EXCEL_PATH, sheet_name="Courbe des taux", header=None)

    # The data starts at row 3 (using pandas zero-indexing)
    # Column 1: T (années)
    # Column 3: Nb Jours
    # Column 4: Taux (the rate to use)
    
    data = []
    
    for i in range(3, len(df_raw)):
        row = df_raw.iloc[i]
        t_years = row[1]
        rate = row[4]
        
        # Break if we hit empty rows
        if pd.isna(t_years) or pd.isna(rate):
            continue
            
        data.append({
            'T_years': float(t_years),
            'Rate': float(rate)
        })

    df = pd.DataFrame(data)
    
    # Let's ensure integer years are perfectly integers for precision
    df['is_integer_year'] = df['T_years'].apply(lambda x: x.is_integer() and x > 0)
    
    # ──────────────────────────────────────────────
    # Bootstrapping logic
    # ──────────────────────────────────────────────
    # We maintain a sum of DFs for integer years 1, 2, 3...
    sum_df_int = 0.0
    
    # To store calculated metrics
    dfs = []
    zc_conts = []
    zc_discs = []

    # Iterate over all rows
    # Note: We assume the rows are sorted by T_years in the Excel sheet
    df = df.sort_values(by='T_years').reset_index(drop=True)
    
    # Keep track of DFs for each integer year T=1, 2, 3... to compute the sum correctly
    # since not all integer years might be explicitly present, 
    # but in this case 1Y to 10Y are continuous, and then 12Y, etc.
    # Wait, if there are missing integer years (e.g. 11Y), the standard swap bootstrap 
    # interpolates rates. For our needs (valuation at 6 years and 5 years), we have all 
    # the needed integer years (1..10).
    
    dict_integer_dfs = {}

    for idx, row in df.iterrows():
        t = row['T_years']
        rate = row['Rate']
        
        if row['is_integer_year']:
            t_int = int(t)
            # Find the sum of DF for i=1 to t-1
            # We assume we have all necessary previous integer DFs
            current_sum_df = sum([dict_integer_dfs.get(i, 0.0) for i in range(1, t_int)])
            
            # DF_T = (1 - Rate_T * sum_{i=1}^{T-1} DF_i) / (1 + Rate_T)
            df_val = (1.0 - rate * current_sum_df) / (1.0 + rate)
            dict_integer_dfs[t_int] = df_val
        else:
            # For fractional years (< 1Y), it's a simple zero rate
            # Let's use standard compound formula: DF_T = 1 / (1 + Rate_T)^T
            # or simple interest: 1 / (1 + Rate_T * T) 
            # We'll use continuous-equivalent for consistency:
            df_val = 1.0 / ((1.0 + rate) ** t)
            
        # ZC Continuous = -ln(DF_T) / T
        zc_c = -np.log(df_val) / t
        
        # ZC Discrete = (1/DF_T)^(1/T) - 1
        zc_d = (1.0 / df_val)**(1.0 / t) - 1.0
        
        dfs.append(df_val)
        zc_conts.append(zc_c)
        zc_discs.append(zc_d)
        
    df['DF'] = dfs
    df['ZC_Cont'] = zc_conts
    df['ZC_Disc'] = zc_discs

    # ──────────────────────────────────────────────
    # Output and Formats
    # ──────────────────────────────────────────────
    print("\n✅ Bootstrapping complete. Sample results:")
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 200)
    print(df.head(15))

    # Save to CSV
    df.to_csv(OUTPUT_CSV, index=False)
    
    # Save to Markdown table
    md_str = df.to_markdown(index=False, floatfmt=".6f")
    with open(OUTPUT_MD, "w") as f:
        f.write("# ENERGETIC du CA \u2014 Bootstrapped Yield Curve\n\n")
        f.write("This table contains the bootstrapped Zero-Coupon rates and Discount Factors based on the swap rates provided in the case study.\n\n")
        f.write(md_str)

    print(f"\nSaved CSV to: {OUTPUT_CSV}")
    print(f"Saved MD to: {OUTPUT_MD}")

if __name__ == "__main__":
    main()
