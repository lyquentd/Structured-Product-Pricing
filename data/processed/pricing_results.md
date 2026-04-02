# ENERGETIC du CA — Pricing Results

### 1. Market Data Parameters (T = 6)
- **Risk-free continuous rate ($r_c$)**: 0.045482 (4.548%)
- **Discount Factor**: 0.761175
- **Volatility ATM (K=3600.0)**: 0.275332 (27.53%)
- **Volatility Cap (K=5760.0)**: 0.235492 (23.55%)

### 2. Pricing Components
| Component | Formula | Value (€) | Notes |
|-----------|---------|-----------|-------|
| **Lego 1** (ZC Bond) | $100 	imes DF_6$ | **76.118** | Cost of capital guarantee |
| **Lego 2** (ATM Call)| $BS(S, K=3600.0)$ | **1331.509** | $d_1$: 0.742, $N(d_1)$: 0.771 |
| **Lego 3** (160% Call)| $BS(S, K=5760.0)$ | **564.684** | $d_1$: -0.053, $N(d_1)$: 0.479 |

### 3. Valuation & Margin (Per €100 Nominal)
- **Option Quantity:** $100 / S_0 = 0.027778$
- **Call Spread Cost:** $Qty 	imes (Call_{ATM} - Call_{160\%}) = 21.301$
- **Total Manufacturing Cost:** $PV(ZC) + Option Cost = 97.418$
- **Bank Upfront Margin:** $100 - Cost = 2.582$ (2.58%)