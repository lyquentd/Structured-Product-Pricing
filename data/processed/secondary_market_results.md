# Section 6: Secondary Market Pricing

**Assumption:** We advance exactly 1 year into the future. The residual maturity is **5 Years**. We assume the market parameters (rates shape, vol surface shape, and spot $S_0 = 3600$) roll down the curve naturally with no market shock.

### 6.1 T+1 Mid-Price Valuation
| Component | 5-Year Parameter | Value |
|-----------|------------------|-------|
| **Risk-Free Rate ($r_5$)** | `4.419%` | ZC Bond PV: **€80.176** |
| **ATM Vol ($\sigma_5$)** | `27.18%` | ATM Call: **€1180.069** |
| **Cap Vol ($\sigma_5$)** | `22.93%` | Cap Call: **€415.841** |

**Total Options Cost (Qty × Spread):** €21.229
**Theoretical Mid Price:** **€101.404**

> **Note:** Even though the spot price hasn't moved, the product value drops from its inception €100 nominal down to ~€101.4. This is because the embedded upfront margin (€2.58) is immediately wiped out, and the options package sheds 1 year of time value (Theta decay). 

### 6.2 Bank Buyback Price (Bid)
When a client asks to sell their product back to the bank before maturity, the bank applies a bid-ask spread to protect themselves and extract early cancellation fees.

By applying an illustrative **+10 basis points** penalty to the discounting interest rate (lowering the bond PV) and a **-2%** penalty to the option volatilities (cheapening the options package), we arrive at the Bid Price:

- **Client Sell Price (Bid):** **€101.378** 
- **Implicit Penalty:** €0.027
