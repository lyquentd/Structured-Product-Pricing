"""
ENERGETIC du CA — Yield Curve Bootstrapping Plot
======================================================
Visualizes the bootstrapped Zero-Coupon rates and Discount Factors from the
processed CSV file and saves the result as a high-resolution, professional plot.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ──────────────────────────────────────────────
# Setup & File Paths
# ──────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "yield_curve_bootstrapped.csv")
OUTPUT_IMAGE = os.path.join(BASE_DIR, "images", "yield_curve_bootstrapping.png")

# ──────────────────────────────────────────────
# Modern Styling Parameters (Institutional Look)
# ──────────────────────────────────────────────
COLOR_PRIMARY = "#00205B"      # Navy Blue
COLOR_SECONDARY = "#C60C30"    # Rich Red
COLOR_ACCENT = "#78BE21"       # Fresh Green
COLOR_NEUTRAL = "#F4F4F4"      # Light Gray background
COLOR_TEXT = "#333333"         # Dark Gray text
FONT_FAMILY = "sans-serif"     # Standard clean font

def main():
    if not os.path.exists(DATA_PATH):
        print(f"❌ Error: Data file not found at {DATA_PATH}. Please run 'src/step2_yield_curve.py' first.")
        return

    # Load data
    df = pd.read_csv(DATA_PATH)
    
    # --- Start Plotting ---
    plt.close('all')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)
    fig.patch.set_facecolor('white')

    # 1. Zero-Coupon Rates Plot
    ax1.plot(df['T_years'], df['ZC_Cont'] * 100, label='Continuous ZC Rate', color=COLOR_PRIMARY, linewidth=2.5, marker='o', markersize=6, alpha=0.9)
    ax1.plot(df['T_years'], df['ZC_Disc'] * 100, label='Discrete ZC Rate', color=COLOR_SECONDARY, linewidth=2, linestyle='--', marker='s', markersize=5, alpha=0.8)
    
    # Styling for Rates Plot
    ax1.set_title("Zero-Coupon Yield Curve", fontsize=16, fontweight='bold', pad=15, color=COLOR_PRIMARY)
    ax1.set_xlabel("Maturity (Years)", fontsize=12, labelpad=10)
    ax1.set_ylabel("Rate (%)", fontsize=12, labelpad=10)
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='lower right', frameon=True, shadow=False, borderpad=1)
    ax1.set_ylim(bottom=df['ZC_Cont'].min() * 80 if df['ZC_Cont'].min() > 0 else 0)
    
    # 2. Discount Factors Plot
    ax2.plot(df['T_years'], df['DF'], label='Discount Factor', color=COLOR_ACCENT, linewidth=3, marker='D', markersize=5, alpha=0.9)
    # Fill under the curve for a premium look
    ax2.fill_between(df['T_years'], df['DF'], color=COLOR_ACCENT, alpha=0.1)

    # Styling for DF Plot
    ax2.set_title("Discount Factors (DF)", fontsize=16, fontweight='bold', pad=15, color=COLOR_PRIMARY)
    ax2.set_xlabel("Maturity (Years)", fontsize=12, labelpad=10)
    ax2.set_ylabel("Price / Value (EUR)", fontsize=12, labelpad=10)
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='upper right', frameon=True, shadow=False, borderpad=1)
    ax2.set_ylim(0, 1.05)

    # Adding informative text box about Bootstrapping
    textstr = (
        "Methodology: Bootstrapping\n"
        f"Base Data: Swap Rates (Pricer Energetic)\n"
        f"Maturity Range: {df['T_years'].min()}Y to {df['T_years'].max()}Y\n"
        f"Final 10Y DF: {df.iloc[-1]['DF']:.4f}\n"
        "Calibration: Linear Interpolated Zero Rates"
    )
    props = dict(boxstyle='round,pad=0.5', facecolor='#F9F9F9', alpha=0.8, edgecolor='#CCCCCC')
    ax2.text(0.05, 0.05, textstr, transform=ax2.transAxes, fontsize=10, verticalalignment='bottom', bbox=props)

    # Overall Layout & Improvements
    plt.suptitle("ENERGETIC du CA - Yield Curve Calibration & Discounting", fontsize=20, fontweight='bold', y=1.02, color=COLOR_PRIMARY)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Save the plot
    os.makedirs(os.path.dirname(OUTPUT_IMAGE), exist_ok=True)
    plt.savefig(OUTPUT_IMAGE, bbox_inches='tight')
    
    print(f"✅ Success! Plot saved to: {OUTPUT_IMAGE}")
    plt.show()

if __name__ == "__main__":
    main()
