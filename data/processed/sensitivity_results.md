# Section 5: Sensitivity Analysis (Bank Margin)

**Baseline Margin:** €2.582

| Scenario | Adjusted Parameter | New Margin (€) | Impact vs Baseline | Interpretation |
|----------|--------------------|----------------|--------------------|----------------|
| **1. Rates Fall (-50bp)** | $r = 4.048\% $ | **0.515** | *-2.066* | Lower yields severely harm the bank because the zero-coupon bond becomes much more expensive to purchase. |
| **2. Volatility Rises (+1%)** | $\sigma_{atm} = 28.53\%, \sigma_{cap} = 24.55\%\ $ | **2.815** | *+0.234* | Higher vol hurts the margin slightly (the product is structurally Short Vega). |
| **3. Extend Maturity (7Y)** | $T = 7, r_7 = 4.656\% $ | **6.744** | *+4.162* | Extending maturity is highly beneficial. ZC Bond is heavily discounted, buying the bank much more margin budget to spend on options. |
| **4. Cap Tightened (59%)** | $K_{cap} = 159\%$ | **2.784** | *+0.203* | Lowering the cap helps the margin. The bank sells a tighter call, capturing more premium. |
| **4. Cap Loosened (61%)** | $K_{cap} = 161\%$ | **2.382** | *-0.200* | Raising the cap hurts the margin. The short option is further OTM and worthless, returning less premium. |
