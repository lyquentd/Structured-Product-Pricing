# STEP 5: Greeks

| Greek | Value per €100 nominal | Interpretation for Trader |
|-------|------------------------|---------------------------|
| **Delta** | 0.0081 | If spot jumps 1 point, product gains €0.0001. It is highly long delta since we bought more ATM delta than we sold OTM delta. |
| **Vega** (+1%) | **€-0.2337** | A 1% uniform rise in volatility increases product value by €-0.2337. The product is strictly **Long Vega**. |
| **Rho** (+1bp) | **€-0.0409** | A 1bp rise in the yield curve drops product value by €0.0409. The ZC bond duration makes the overall product strictly **Short Rho** (exposed to rising rates). |
| **Theta** (1 day)| **€+0.0091** | Every passing day holding spot constant brings the ZC bond closer to par (`+`), but decays option time value (`-`). Net impact is €+0.0091 per day. |
