# Euro-Shield 6Y Horizon — 5-Minute Oral Presentation Pitch

> **Instructions for the speaker:** 
> - This script is precisely ~600 words, designed to take exactly **5 minutes** when spoken at a comfortable, professional pace (120-130 words per minute).
> - Each part takes roughly **1 minute**.
> - It explicitly covers all 7 assignment steps: Marketing, Payoff, Margin, Greeks, Sensitivity, Secondary Market, and Imagination.

---

## 🎙️ Part 1: Product Marketing & Payoff (1 minute)

"Good morning everyone. Today we present our pricing and risk analysis for the ENERGETIC structured product—which we have rebranded for retail clients as the **'Euro-Shield 6Y Horizon'**.

Under MiFID profiling, our target client is a conservative retail investor who desires equity market exposure but refuses to risk their principal. 
The value proposition is simple: 100% downward capital protection, and 100% direct participation in the Euro Stoxx 50's upside, heavily capped at a 60% maximum return over 6 years.

The obvious pro for the client is absolute safety. The cons? Their upside is severely limited, they forfeit all index dividends, and their capital is deeply illiquid for 6 years. 

To build this computationally, we successfully decomposed the payoff into four exact Lego blocks: A Zero-Coupon Bond for protection, a Long ATM Call to capture upside, and a Short 150% Cap Call and a Long 10% Digital Call to finance the structure."

---

## 🎙️ Part 2: Pricing Methodology & Bank Margin (1 minute)

"To determine how much true margin the bank makes, we built a fully programmatic Black-Scholes pricer rather than relying on Excel approximations.

First, we mathematically bootstrapped the yield curve from the raw swap rates. This precisely returned a 6-year continuous risk-free rate of **4.55%** and a Discount Factor of 0.76. 
Thus, purchasing the Zero-Coupon bond capital guarantee costs the bank **€76.33** today.

Next, we pulled our implied volatilities directly from the surface: **27.5%** for the ATM call and **23.5%** for the Cap.
Pricing these options dynamically, buying the required quantity of ATM calls and selling the Caps costs us **€20.98**.

Combining the bond and the exact option spread, the total manufacturing cost of the Euro-Shield is **€97.31**. Since we sell it to the retail client at €100 nominal, the bank comfortably locks in a Day-1 upfront margin of **2.69%**. This perfectly aligns with standard institutional retail margins."

---

## 🎙️ Part 3: Greeks & Risk Exposure (1 minute)

"Once the product is sold, what are the exact risks held by the trading desk? We calculated the Greeks to find out.

We are mathematically heavily **Short Rho**: because the Zero-Coupon bond has such a long 6-year duration, even a tiny rise in interest rates sharply depreciates our portfolio.

However, the most fascinating, critical insight we discovered is regarding Vega. The product is structurally **Short Vega**. You might assume that because we bought ATM options and sold OTM options, we should be Long Vega. 
But because the 6-year interest rate is extremely high at 4.5%, the mathematical *forward* price of the index is heavily inflated to roughly 4,700. This forward shift severely increases the volatility sensitivity of our 5,400 Short Cap. Therefore, if implied volatility spikes, the product becomes exponentially more expensive to hedge, and the trader bleeds money."

---

## 🎙️ Part 4: Sensitivity Analysis & Secondary Market (1 minute)

"We aggressively stress-tested our 2.69% margin against these market shocks.

The biggest threat to profitability is falling yield curves. If rates drop by just 50 basis points, the Zero-Coupon bond becomes far too expensive to manufacture, and our €2.58 margin completely collapses to just **€0.81**. Conversely, if we simply extended the product maturity to 7 years, the bond is discounted further, and our bank margin skyrockets to **€7.07**.

Moving to the Secondary Market, we advanced the simulation exactly 1 year. Assuming the spot price remained totally flat, the product theoretically surged in value on the secondary market to **€101.28**. 
This mathematically proves our Theta calculation: the massive positive "pull-to-par" accrual of the Zero-Coupon bond easily dominates the slight negative time-decay of the 6-year options."

---

## 🎙️ Part 5: Imagination & Conclusion (1 minute)

"Finally, we considered the future of structural innovation.

For an alternative priceable product today, we propose a **'Reverse Convertible Note'**. This appeals to clients in flat, low-volatility markets, allowing them to trade down their capital protection for a massive fixed yield, synthetically replicated using standard Black-Scholes Put writing.

Looking 10 years ahead, we foresee true exotic innovation: an **'AI-Dynamic Allocation Note'**. Instead of tracking the static Stoxx 50, the underlying performs daily algorithmic rotations between equities, crypto, and clean energy using real-time global sentiment analysis—priced dynamically via advanced Monte Carlo neural networks.

To conclude, this case study perfectly replicates real-world structuring: balancing 100% client security with a robust, mathematically sound 2.69% structured profit margin.

Thank you for your time, we are now open to your questions."
