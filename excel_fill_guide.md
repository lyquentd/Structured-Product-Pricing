# 📊 Excel Template Exact Answer Key
Here is your step-by-step, sheet-by-sheet guide to filling exactly what the Excel template (`Pricer Energetic - 3 (1).xls`) asks for. **All instructions and answers are provided in English as requested.**

---

## 📑 1. Sheet: `Résumé`
**Do not touch anything here.** 
This sheet is solely your professor's grading rubric (up to 120 points). It will auto-update or be filled by the grader. The only task required here is to copy and paste your "Structuring Scheme" (the flow diagram) into the dedicated empty box (around Row 32) once you have drawn it in Sheet 3.

---

## 📢 2. Sheet: `2. Marketing`
You must write syntheses in the empty blue boxes provided:
- **Bank / Slogan:** Example: *[Your Bank Name]* - "Innovation serving your security." Strengths: Financial solidity, expertise in structured products.
- **Product / Arguments:** Name: **Euro-Shield 6Y Horizon** (or Energetic 6Y).
  - *Pros (Avantages) :* 100% downward capital guarantee, equity market upside exposure up to +60%.
  - *Cons (Inconvénients) :* No dividend yields, performance is capped, and capital is highly illiquid for 6 years.
- **Client Needs:** Ideal for a conservative MiFID profile (retail client) in an uncertain economic context, seeking to protect their initial capital while aiming to beat inflation if the European equity market outperforms.
- **Max / Min Value:** Minimum return is **100** (capital returned). Maximum return is **160** (60% capped return).
- *(Do not forget to insert the payoff graph image here showing the flat 100 base, 45-degree angle, and flat 160 cap).*

---

## 🧱 3. Sheet: `3. a b c d` (Basic Blocks)
Fill out the rows corresponding to questions a, b, c, and d:
- **3.a. Capital guarantee?**
  - "Yes, a total 100% guarantee."
  - "The financial instrument proposed to fulfill this obligation is a Zero-Coupon Bond."
  - "Characteristics: Maturity = 6 years, Nominal Value = 100."
- **3.b. Call or Put Types (Lego)?**
  - **Lego 1:** Zero-Coupon Bond (Bought / Long)
  - **Lego 2:** Vanilla Call (Bought / Long)
  - **Lego 3:** Vanilla Call (Sold / Short / Cap)
  - **Lego 4:** Digital Call (Bought / Long / Bonus)
- **3.c. Maturity, Strike Price, etc.**
  - **Lego 1:** Maturity 6 years, Face value = 100.
  - **Lego 2:** Maturity 6 years, Strike = 3600 (ATM = 100%), Quantity = 100/3600.
  - **Lego 3:** Maturity 6 years, Strike = 5400 (150% Cap), Quantity = 100/3600.
  - **Lego 4:** Maturity 6 years, Strike = 5400 (150% Trigger), Payout = 10.
- **3.d. Flow Diagram:** Draw arrows showing: The client pays 100 to the trading desk. The desk buys 1 ZCB, buys the ATM Call, sells the Cap Call, and buys the 10% Digital Call.

---

## 💶 4. Sheet: `4. a b c d e ` (Pricing)
*Note: The ZCB rate calculations are done in the 'Courbe des taux' sheet (see Section 8 below).*

- **4.b. Present Value of the Guarantee (ZC Bond PV):** 
  - Maturity: **6**, Rate Type: **Continuous**, Rate Used: **4.502%** (0.04502).
  - **Valeur max:** **100** (This is the Nominal amount being guaranteed).
  - Present Value: `=100 * EXP(-4.502% * 6)` $\rightarrow$ **76.328**.
- **4.c. Option Pricing:**
  - **Lego 2 (Buy ATM) :** Spot: 3600 | Type: Call | Maturity: 6 | Strike: 3600 | Volatility: 27.53% | ZC1: 4.502% | ZC2: 0% | Forward: 4728.4 | Price: **1327.52** 
  - **Lego 3 (Sell Cap) :** Spot: 3600 | Type: Call | Maturity: 6 | Strike: 5400 | Volatility: 24.00% | ZC1: 4.502% | ZC2: 0% | Forward: 4728.4 | Price: **654.55** 
  - **Lego 4 (Buy Digital) :** Spot: 3600 | Type: Digital Call | Mat: 6 | Strike: 5400 | Payout: 10 | Vol: 24.00% | Price: **2.29** *(formula: Payout * EXP(-r*t) * N(d2))*
- **4.d. Margin:**
  - Selling Price: **100** | Option Total Cost: **20.98** `=(1327.52 - 654.55)*(100/3600) + 2.29` | Total Product Cost: **97.31** `=(76.33+20.98)` | Margin: **2.69**
- **4.e. Client Cancellation:**
  - Price ready to pay: **~97.31** (minus bid-ask spread).
  - Why? Because the bank has not yet "amortized" its margin over time and must unwind the raw raw hedges on the market at their un-margined manufacturing cost.

---

## 📊 5. Sheet: `5.` (Sensitivities)
Fill in the tables with new option prices and margins under different scenarios. Use these target margins to verify your internal math:
- **If Rates drop -50 bp :** The new margin collapses to **+0.616 €**.
- **If Vol Spread +1% :** The new margin slightly rises to **+2.925 €**.
- **If Maturity +1 Year (T=7) :** The new margin skyrockets to **+6.807 €**.
- **If Cap tightened to 149% :** The new margin rises to **+2.784 €**.
- **If Cap loosened to 151% :** The new margin drops to **+2.382 €**.

*(You will need to run the exact same Black-Scholes formulas from Sheet 4 for each of these scenarios in this sheet to prove the margin math).*

---

## 🛒 6. Sheet: `6.` (Secondary Market T+1)
Using the market data for **T = 5 years** (Residual Maturity) from the final two sheets:
- **6.a. Forward Underlying & ZC:**
  - 5-Year continuous ZC Rate: **4.383%**
  - Forward: `=3600 * EXP(4.383% * 5)` -> **4482.1**
- **6.b. Value of Lego Blocks:** (Use ATM Vol 5Y = 27.18%, and Cap Vol 5Y = 22.93%).
  - ZC PV (T=5): **80.322**
  - Heavily weighted Options Spread Cost : **20.962**
  - MTM Mid Price (Product Value): `= 80.322 + 20.962` = **101.284**

---

## 🤯 7. Sheet: `7. Imagination`
- **Pricable product today:** "Reverse Convertible with a Barrier". The client sells a put, giving up capital protection in exchange for massive fixed yield. Easily pricable with standard Black-Scholes pure.
- **Product in 10 years:** "AI-Dynamic Allocation Note". An underlying basket that auto-rebalances every hour between Crypto, Equities, and Carbon Credits using real-time Artificial Intelligence sentiment analysis. Requires deep neural network Monte Carlo simulators, impossible to price with simple BS today.

---

## 📈 8. Sheet: `Courbe des taux` (Bootstrapping Calculations)
This is where exercise `4.a` from Sheet 4 is actually executed. Place these formulas in the empty cells:
- **All Rows (Formula to drag down from 1Y to 30Y) :**
  - DF `= 1 / (1 + Taux_Utilisé)^T_années`
  - Continuous ZC (ZC continu) `= -LN(DF) / T_années`
- *You will know your formulas work perfectly because your T=6 year row will yield exactly : DF = **76.33%** (0.7633) and ZC = **4.50%** (0.04502).*
