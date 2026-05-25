# Stock Price Prediction with EC-GBM (Entropy-Corrected GBM)

> **3-2 (2022 Fall)** · Korea University Sejong · Probability Models Capstone Design (확률모형캡스톤디자인) · Team 3
> 김석범 · 김수호 · **이선재**

Implementing and evaluating an **Entropy-Corrected Geometric Brownian Motion
(EC-GBM)** model for stock price prediction, based on
[Gupta et al., *Sci Rep* 14, 28384 (2024)](https://doi.org/10.1038/s41598-024-79714-3).

## TL;DR

- **Why:** Standard GBM assumes log-normal returns and constant volatility,
  which doesn't fit real financial data well (skewness, kurtosis, regime changes).
- **What:** Apply **EC-GBM** — GBM augmented with **Shannon entropy** based
  correction — to capture deterministic structure in real price series.
- **How:** Monte-Carlo simulation in Python; trajectory acceptance based on
  entropy reduction threshold.
- **Data:** AMD daily closing prices, 2020-01-01 → 2024-11-30 (1,314 trading days),
  via `yfinance`.

## Repository Structure

```
stock-prediction-ec-gbm/
├── README.md / README_KR.md
├── .gitignore
├── notebooks/
│   └── 01_ec_gbm_simulation.ipynb   Python implementation: GBM + EC-GBM
│                                    (Monte Carlo + Shannon entropy)
├── R/
│   ├── README.md
│   └── fda_exploration.R            Functional Data Analysis (supplementary)
└── docs/
    ├── final_report_team3.docx      Final report (Team 3)
    ├── presentation_final.pdf       Final presentation slides
    └── paper_summary_entropy_gbm.docx  Reference paper summary
```

## Methods (Notebook `01_ec_gbm_simulation.ipynb`)

### Geometric Brownian Motion (GBM)
$$dS_t = \mu S_t \, dt + \sigma S_t \, dW_t$$

Classical stochastic process for asset prices; assumes log-normality and
constant `(μ, σ)`.

### Entropy-Corrected GBM (EC-GBM)
- Generate many candidate GBM trajectories via Monte Carlo.
- For each candidate, compute **Shannon entropy** over a discretized histogram.
- **Accept** trajectory only if combining it with the reference reduces entropy
  by more than `threshold` (more deterministic structure → better fit).
- Repeat over `M` trials.

### Implementation details
- `generate_gbm_trajectory(S0, μ, σ, T)`: cumulative Brownian path → GBM
- `compute_entropy(data, bins=20)`: histogram-based discrete Shannon entropy
- `ec_gbm(S0, μ, σ, T, M, threshold)`: main loop with entropy-based acceptance

## Stack

`Python` (`numpy`, `matplotlib`, `yfinance`) · `R` (`fda` package — supplementary)

## How to Run

```bash
pip install numpy matplotlib yfinance
jupyter notebook notebooks/01_ec_gbm_simulation.ipynb
```

## Reference

- Gupta, R., Drzazga-Szczęśniak, E. A., Kais, S. et al.
  **"Entropy corrected geometric Brownian motion."**
  *Scientific Reports* **14**, 28384 (2024).
  [Paper link](https://doi.org/10.1038/s41598-024-79714-3)
- See `docs/paper_summary_entropy_gbm.docx` for our team's reading notes.

## Notes

- Team project (3조): 김석범, 김수호, **이선재** (Sunjae Lee)
- Capstone-style course — final report + final presentation required.
- R supplementary code (`R/fda_exploration.R`) is an early exploration of
  Functional Data Analysis; not central to the EC-GBM result.

---

*Author: Sunjae Lee · B.S. Big Data Science @ Korea University Sejong*
*Part of [University-Projects/3-2](../) (2022 Fall)*
