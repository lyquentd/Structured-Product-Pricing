#set page(
  paper: "a4",
  margin: (x: 2cm, y: 2.5cm),
  header: align(right, text(8pt, fill: gray)[Euro-Shield 6Y Horizon - Project Methodology]),
  footer: [
    #set align(center)
    #text(8pt, fill: gray)[
      #context counter(page).display("1 / 1", both: true)
    ]
  ]
)

#set text(
  font: "New Computer Modern",
  size: 11pt,
  fill: rgb("#333333")
)

#let navy = rgb("#002060")
#let silver = rgb("#C0C0C0")

// --- Title Page ---
#align(center + horizon)[
  #text(24pt, weight: "bold", fill: navy)[Project Methodology Documentation]
  #v(1cm)
  #text(16pt, weight: "medium")[Euro-Shield 6Y Horizon — Structured Product Pricing]
  #v(5mm)
  #text(12pt, fill: gray)[SKEMA Business School — Financial Markets & Investments]
  #v(2cm)
  #line(length: 100%, stroke: 0.5pt + silver)
  #v(1cm)
  #grid(
    columns: (1fr, 1fr),
    align: (left, right),
    [**Author:** Quentin LY],
    [**Date:** April 2026]
  )
]

#pagebreak()

// --- TOC ---
#outline(indent: 1.5em)

#pagebreak()

// --- Content ---

= Overview
The objective of this project is to build an institutional-grade pricing and analysis engine for the *Euro-Shield 6Y Horizon* structured product. This document outlines the technical environment, the project architecture, and the modular methodology used to decompose this complex financial instrument into verifiable "Lego" blocks.

= Technical Environment
The project is built using a modern Python ecosystem focused on performance, reproducibility, and clarity.

== Core Tools
- *Package & Env Manager:* `uv` (v0.11+). Used for ultra-fast dependency resolution and virtual environment isolation.
- *Language:* Python 3.9+.
- *Documentation/Reporting:* Typst. Used for generating high-quality PDF reports and presentations with minimal overhead.

== Primary Dependencies
- `pandas`: Data manipulation and results tabulating.
- `matplotlib`: Institutional-grade technical plots and payoff diagrams.
- `scipy`: Financial optimization and normal distribution calculations.
- `pymupdf`: PDF parsing for raw document analysis.
- `tabulate`: Formatting console outputs for README generation.

= Project Structure
The repository is organized following a strict data-science pipeline structure to ensure separation of concerns between raw inputs, processed data, and visual assets.

== Directory Hierarchy
- `data/raw/`: Contains original case study documents (PDFs) and market data (Excel files).
- `data/processed/`: Contains intermediate calculation results (CSV, MD) used to populate the main README.
- `images/`: Stores all generated plots, diagrams, and "Lego" decompositions.
- `src/`: The core logic directory containing modular scripts for each step of the pricing workflow.
- `methodology/`: Contains Typst/LaTeX sources and final PDF reports/methodology docs.

== Key Configuration Files
- `pyproject.toml`: Defines the project workspace, dependencies, and environment requirements.
- `README.md`: The central hub of the project, summarizing all findings and serving as the primary interface for users.
- `.python-version`: Locks the local environment to a specific Python version.

#pagebreak()
= Methodology: Step-by-Step Build
The project follows a 9-step methodology, moving from theoretical payoff formalization to secondary market dynamics.

== Step 1: Payoff Formalization & Visualization
Decomposition of the product into "Lego" blocks: a Long Zero-Coupon Bond, a Long ATM Call, and a Short OTM Call (Cap). Mathematical verification that the sum of these blocks equals the promised product payoff.

== Step 2: Yield Curve Bootstrapping
Conversion of raw market swap rates into a continuous zero-coupon yield curve. This enables precise discounting for the capital guarantee component.

== Step 3 & 4: Black-Scholes Pricing & Margin
Implementation of the Black-Scholes model to price the embedded options. The difference between the selling price (€100) and the manufacturing cost (Lego sum) determines the bank's upfront margin.

== Step 5: Greeks & Risk Exposure
Calculation of Delta, Gamma, Vega, Rho, and Theta. This step identifies the product as a "Short Vega" and "Long Theta" instrument, explaining its behavior as it approaches maturity.

== Step 6: Sensitivity Analysis
Stress-testing the bank margin against market shifts (Rates +/- 50bp, Volatility +/- 1%, Maturity shifts). This quantifies the robustness of the pricing model.

== Step 7: Secondary Market Pricing
Valuation of the product after inception (e.g., $T=1$). Analysis of the "Pull-to-par" effect and the impact of funding penalties on bid prices during client buybacks.

= Conclusion
By maintaining a modular codebase in `src/` and a central documentation hub in `README.md`, the project ensures that every financial assumption is transparent, verifiable, and reproducible. The use of `uv` and `typst` ensures that the technical environment is easy to reconstruct on any machine.
