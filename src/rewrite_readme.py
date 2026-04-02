import re

with open("README.md", "r") as f:
    text = f.read()

# Payoff mapping
text = text.replace("Decomposes exactly into:\n- 1 ZC Bond (Face = 100)\n- 1/36th ATM Call (K = 3600)\n- -1/36th OTM Call (K=5760, capping 60%)", 
                    "Decomposes exactly into:\n- 1 ZC Bond (Face = 100)\n- 1/36th ATM Call (K = 3600)\n- -1/36th OTM Call (K = 5400, capping at 150%)\n- 1/36th Digital Call (K = 5400) paying 10% bonus")

# Market Parameters
text = text.replace("**Volatility Cap (K=5,760)**: 23.55%", "**Volatility Cap (K=5,400)**: 24.00%")

# Components Table
components = """| **Lego 1** (ZC Bond) | $100 \times DF_6$ | **€76.118** | Cost of capital guarantee |
| **Lego 2** (ATM Call)| $BS(S, K=3600)$   | **€1,331.51** | $d_1$: 0.742, $N(d_1)$: 0.771 |
| **Lego 3** (160% Call)| $BS(S, K=5760)$  | **€564.68** | $d_1$: -0.053, $N(d_1)$: 0.479 |"""

new_comp = """| **Lego 1** (ZC Bond) | $100 \times DF_6$ | **€76.118** | Cost of capital guarantee |
| **Lego 2** (ATM Call)| $BS(S, K=3600)$   | **€1,331.51** | Buy the upside |
| **Lego 3** (150% Call)| $BS(S, K=5400)$  | **€657.97** | Sell the cap at 150% |
| **Lego 4** (Digital)  | $10e^{-rT}N(d_2)$| **€2.30** | Buy the 10% jump bonus |"""
text = text.replace(components, new_comp)

# Options Cost
cost_txt = """The investor buys 1 ATM Call and sells 1 160% Cap.
- **Call Spread Cost (1 unit)**: €1,331.51 - €564.68 = **€766.83**
- **Option Quantity per €100 Nom**: $100 / 3600 = 0.027778$
- **Total Options Investment**: €766.83 $\times$ 0.027778 = **€21.30**"""

new_cost = """The investor buys 1 ATM Call, sells 1 150% Cap, and buys 1 Digital bonus.
- **Total Options Package (1 unit)**: €1,331.51 - €657.97 + (2.30 / 0.027778) = **€756.34**
- **Option Quantity per €100 Nom**: $100 / 3600 = 0.027778$
- **Total Options Investment**: **€21.01**"""
text = text.replace(cost_txt, new_cost)

# Margin Calculation
text = text.replace("€76.118 + €21.301 = **€97.418**", "€76.118 + €21.006 = **€97.12**")
text = text.replace("€100.000 - €97.418 = **€2.582** per €100 nominal (**2.58%**)", "€100.000 - €97.124 = **€2.876** per €100 nominal (**2.88%**)")
text = text.replace("A ~2.5% upfront margin", "A ~2.8% upfront margin")
text = text.replace("manufacturing cost (€97.42)", "manufacturing cost (€97.12)")

text = text.replace("Cap strike (5,760)", "Cap strike (5,400)")

# Sensitivity Base
text = text.replace("**€2.58** baseline bank margin", "**€2.88** baseline bank margin")
text = text.replace("€ 0.515", "€ 0.808")
text = text.replace("€-2.066", "€-2.068")
text = text.replace("€ 2.815", "€ 3.116")
text = text.replace("€+0.234", "€+0.240")
text = text.replace("€ 6.744", "€ 7.071")
text = text.replace("28.53\\%, \sigma_{cap} = 24.55\\%", "28.53\\%, \sigma_{cap} = 25.00\\%")
text = text.replace("159\\%", "149\\%").replace("161\\%", "151\\%")

# Secondary
text = text.replace("22.93%", "23.50%")
text = text.replace("€21.229", "€20.985")
text = text.replace("€101.404", "€101.161")
text = text.replace("(€97.42)", "(€97.12)")
text = text.replace("€101.40", "€101.16")
text = text.replace("**€2.58**", "**€2.88**")
text = text.replace("€100.50 – €101.00", "€100.20 – €100.70")
text = text.replace("160% Cap", "150% Cap")

with open("README.md", "w") as f:
    f.write(text)

