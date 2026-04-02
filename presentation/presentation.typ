#set page(
  paper: "presentation-16-9",
  margin: (x: 2cm, y: 1cm),
  fill: rgb("#FFFFFF"),
)

#set text(
  font: "Arial",
  size: 20pt,
  fill: rgb("#1A2B45"), // Navy for institutional feel
)

#let navy = rgb("#1A2B45")
#let lightnavy = rgb("#2C3E50")
#let gray = rgb("#F2F4F7")
#let accent = rgb("#E74C3C") // Red accent for highlights

#let slide(title: "", content) = {
  pagebreak(weak: true)
  rect(width: 100%, height: 4pt, fill: navy)
  v(0.5cm)
  text(28pt, weight: "bold", navy)[#title]
  v(0.5cm)
  content
}

// --- Title Slide ---
#page(
  fill: navy,
  background: {
    place(image("../images/euro_background.png", width: 100%, height: 100%, fit: "cover"))
    place(rect(width: 100%, height: 100%, fill: rgb("#1A2B45B2")))
  }
)[
  #set text(fill: white)
  #align(center + horizon)[
    #text(36pt, weight: "bold")[Euro-Shield 6Y Horizon] \
    #text(24pt)[Structured Product Pricing] \
    #v(1cm)
    #line(length: 50%, stroke: 2pt + white)
    #v(0.5cm)
    #text(18pt)[Case Study — ENERGETIC du CA] \
    #text(16pt)[Quentin Ly]
  ]
  #place(bottom + left, dx: 0.5cm, dy: -0.5cm)[
    #set text(size: 8pt, fill: white)
    APRIL 2026 | Document for internal use only
  ]
]

// --- Slide 2: Overview ---
#slide(title: "Product Overview")[
  #set text(size: 17pt)
  #v(0.5cm)
  #block(
    fill: gray,
    inset: (x: 0.8cm, y: 0.8cm),
    radius: 8pt,
    width: 100%,
    [
      #grid(
        columns: (1.2fr, 1fr),
        gutter: 0.5cm,
        [
          - *Product Name:* Euro-Shield 6Y Horizon \
          - *Underlying:* DJ Euro Stoxx 50 \
          - *Maturity (T):* 6 years \
          - *Spot (S₀):* 3,600 €
        ],
        [
          - *Guaranteed Capital:* 100% \
          - *Maximum Return:* 60% \
          - *Initial Nominal:* 100 € \
          - *Participation:* 100% (capped)
        ]
      )
    ]
  )
]

// --- Slide 3: Payoff Formula ---
#slide(title: "Step 1: Payoff Formalization")[
  #align(center)[
    #box(
      inset: 1cm,
      fill: gray,
      radius: 8pt,
      [
        $ "Payoff"(S_T) = 100 times [1 + max(0, min(0.60, S_T / S_0 - 1))] $
      ]
    )
  ]
  #v(0.5cm)
  #table(
    columns: (1fr, 1.5fr, 1fr),
    inset: 10pt,
    align: horizon,
    [*Scenario*], [*Condition*], [*Return*],
    [Bearish], [$S_T <= 3,600$], [0%],
    [Moderate Bull], [$3,600 < S_T < 5,760$], [0% - 60%],
    [Strong Bull], [$S_T >= 5,760$], [60% (cap)],
  )
]

// --- Slide 4: Lego Decomposition ---
#slide(title: "Step 1: Lego Block Decomposition")[
  The product is engineered using three specific building blocks:
  #v(0.5cm)
  #table(
    columns: (0.8fr, 1.6fr, 2.6fr),
    inset: 8pt,
    fill: (x, y) => if y == 0 { navy } else { if calc.even(y) { gray } else { white } },
    stroke: none,
    [#text(white)[*Block*]], [#text(white)[*Instrument*]], [#text(white)[*Quantity / Details*]],
    [Lego 1], [Zero-Coupon Bond], [Face = 100€, T=6],
    [Lego 2], [Long ATM Call], [$K=3,600$, Qty $approx 0.0278$],
    [Lego 3], [Short OTM Call], [$K=5,760$ (160%), Qty $approx 0.0278$],
  )
]

// --- Slide 5: Lego Decomposition Plot ---
#slide(title: "Lego Block Visualization")[
  #align(center)[
    #image("../images/payoff_decomposition.png", height: 70%)
  ]
]

// --- Slide 6: Payoff Product Plot ---
#slide(title: "Payoff Diagram at Maturity")[
  #align(center)[
    #image("../images/payoff_product.png", height: 70%)
  ]
]

// --- Slide 7: MTM over Time Plot ---
#slide(title: "Mark-to-Market Evolution")[
  #align(center)[
    #image("../images/payoff_time_horizons.png", height: 70%)
  ]
]

// --- Slide 8: Yield Curve Logic ---
#slide(title: "Step 2: Yield Curve Bootstrapping")[
  #v(0.2cm)
  *Logic:* Extract Zero-Coupon rates from market Swap rates.
  #v(0.4cm)
  #grid(
    columns: (1fr, 1.8fr),
    gutter: 1cm,
    [
      #v(0.3cm)
      - *Formula (Integer T):* \
        $"DF"_T = (1 - "Rate"_T sum_{i=1}^{T-1} "DF"_i) / (1 + "Rate"_T)$
      #v(0.6cm)
      - *Formula (Continuous r):* \
        $"ZC"_"cont" = - ln("DF"_T) / T$
    ],
    [
      #v(-0.2cm)
      #image("../images/yield_curve_bootstrapping.png", width: 100%)
    ]
  )
]

// --- Slide 9: Bootstrapping Results ---
#slide(title: "Bootstrapping Results")[
  Critical data extracted for pricing models:
  #v(0.5cm)
  #table(
    columns: (1fr, 1fr, 1fr, 1fr),
    inset: 10pt,
    [*Maturity*], [*Swap Rate*], [*Discount Factor*], [*ZC Cont ($r_c$)*],
    [1 Year], [3.320%], [0.9678], [3.266%],
    [5 Years], [4.480%], [0.8017], [4.383%],
    [6 Years (T)], [4.605%], [0.7612], [*4.502%*],
    [7 Years], [4.708%], [0.7218], [4.656%],
  )
]

// --- Slide 10: Pricing Parameters ---
#slide(title: "Step 3: Black-Scholes Pricing")[
  #v(0.2cm)
  - *Spot ($S_0$):* 3,600 €
  - *Risk-free Rate (6Y):* 4.502%
  - *Volatility ATM (K=3600):* 27.53%
  - *Volatility Capped (K=5400):* 24.00%
  #v(0.5cm)
  #table(
    columns: (1.8fr, 1fr, 1.8fr),
    inset: 8pt,
    [*Component*], [*Value (€)*], [*Notes*],
    [ZC Bond (Lego 1)], [76.33 €], [Capital guarantee],
    [ATM Call (Lego 2)], [1,331.51 €], [Per unit of index],
    [Cap (Lego 3)], [564.68 €], [Short option premium],
  )
]

// --- Slide 11: Bank Margin ---
#slide(title: "Step 4: Bank Margin Calculation")[
  #v(0.5cm)
  - *Lego 1 (ZC Bond):* $100 times 0.7612 = 76.33$ €
  - *Option Spread Cost:* $(1,331.51 - 564.68) times 0.0278 = 20.98$ €
  #v(0.5cm)
  #block(
    fill: gray,
    inset: 0.8cm,
    radius: 5pt,
    width: 100%,
    [
      - *Manufacturing Cost:* $76.33 + 20.98 =$ *97.31 €*
      - *Selling Price:* *100.00 €*
      - *Upfront Bank Margin:* *2.69%*
    ]
  )
]

// --- Slide 12: Greeks ---
#slide(title: "Step 5: Greeks Analysis (Day 1)")[
  #set text(size: 16pt)
  #v(-0.3cm)
  Exposure per 100€ nominal sold:
  #v(0.2cm)
  #table(
    columns: (0.7fr, 1fr, 3fr),
    inset: 5pt,
    [*Greek*], [*Exposure*], [*Risk Interpretation*],
    [Delta ($Delta$)], [+ 0.0081], [Long Delta — Trader must hedge by selling index.],
    [Vega ($nu$)], [€ - 0.2337], [Short Vega — Capped option dominates sensitivity.],
    [Rho ($rho$)], [€ - 0.0409], [Short Rho — Rates rise decrease bond value.],
    [Theta ($Theta$)], [+ 0.0091], [Positive Theta — Accrued interest > time decay.],
  )
]

// --- Slide 13: Sensitivity ---
#slide(title: "Step 6: Sensitivity Analysis")[
  #set text(size: 16pt)
  #v(-0.3cm)
  Impact of market movements on the 2.69% baseline margin.
  #v(0.2cm)
  #table(
    columns: (1.5fr, 0.8fr, 2fr),
    inset: 5pt,
    [*Scenario*], [*New Margin*], [*Interpretation*],
    [Rates Fall (-50bp)], [0.62%], [High risk — ZC Bond cost surges.],
    [Vol Rises (+1%)], [2.93%], [Benefit — Product is Short Vega.],
    [Extend to 7Y], [6.81%], [Benefit — High discount on ZC.],
    [Cap Tightened (59%)], [2.78%], [Benefit — More premium sold.],
  )
]

// --- Slide 14: Secondary Market ---
#slide(title: "Step 7: Secondary Market Valuation")[
  Assume 1 year has passed ($T=5$ remaining), Spot is unchanged.
  #v(0.5cm)
  #table(
    columns: (1.5fr, 1fr, 1.5fr),
    inset: 10pt,
    [*Instrument*], [*Value (T=1)*], [*Change vs T=0*],
    [ZC Bond (Lego 1)], [80.32 €], [+ 4.06 € (Accrual)],
    [Options (Lego 2 & 3)], [20.96 €], [- 0.07 € (Decay)],
    [*Total Mid-Price*], [*101.28 €*], [*+ 3.99 €*],
  )
  #v(0.5cm)
  *Key takeaway:* The product gains value even if the market is flat, confirming positive Theta accrual.
]

// --- Slide 15: Final ---
#page(
  fill: navy,
  background: {
    place(image("../images/euro_background.png", width: 100%, height: 100%, fit: "cover"))
    place(rect(width: 100%, height: 100%, fill: rgb("#1A2B45B2")))
  }
)[
  #set text(fill: white)
  #align(center + horizon)[
    #text(24pt, weight: "bold")[Euro-Shield 6Y Horizon | Structured Product] \
    #v(1cm)
    #text(16pt)[SKEMA Business School - MSc Financial Markets & Investments]
  ]
  #place(bottom + left, dx: 0.5cm, dy: -0.5cm)[
    #set text(size: 8pt, fill: white)
    APRIL 2026 | Document for internal use only
  ]
]
