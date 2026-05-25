# Bayesian Analysis: Weather × Cryptocurrency Returns

> **3-2 (2022 Fall)** · Korea University Sejong · Bayesian Data Analysis PBL

Investigating whether **weather conditions in New York** (where major exchanges
and traders are concentrated) systematically affect the **distribution of
Bitcoin closing-price returns**, using Bayesian statistics.

> _Final report title:_ **"기상요인이 가상화폐 종가 변동률 분포에 미치는 영향"**
> (The Impact of Meteorological Factors on the Distribution of Cryptocurrency Closing-Price Returns)

## TL;DR

- **Hypothesis:** Weather (rain / temperature / etc.) shifts the distribution
  of BTC closing-price returns.
- **Data:**
  - **Bitcoin / Binance** price data
  - **New York weather data** (NewYork_weather_*.csv)
- **Methods:**
  1. Data preprocessing — align timestamps, derive `is_rain`, daily aggregation
  2. **Normality testing** — Shapiro-Wilk, Q-Q plot for return distribution
  3. **Likelihood-based / Bayesian inference** — modeling the distribution under
     different weather conditions
- **Why it's interesting:** Cross-domain Bayesian study mixing financial
  time-series with environmental signals.

## Repository Structure

```
bayesian-crypto-weather/
├── README.md / README_KR.md
├── .gitignore
├── notebooks/
│   ├── 01_data_preprocessing.ipynb     Align weather + BTC time series, derive features
│   ├── 02_binance_data.ipynb           Binance/BTC data acquisition & cleanup
│   ├── 03_normality_tests.ipynb        Shapiro-Wilk, Q-Q plots, histogram fitting
│   └── 04_likelihood_bayesian.ipynb    Main: likelihood + Bayesian inference (144 cells)
└── docs/
    ├── week1_midterm_presentation.pdf  (project proposal & hypothesis)
    ├── midterm2_presentation_script.docx
    └── final_report_weather_crypto.pdf (final report)
```

## Pipeline

| # | Notebook | What it does |
|---|---|---|
| 01 | `01_data_preprocessing.ipynb` | Reads NewYork weather CSVs, derives `is_rain` (binary from precipitation NaN/non-NaN), aggregates daily |
| 02 | `02_binance_data.ipynb` | Binance/BTC price data preparation |
| 03 | `03_normality_tests.ipynb` | `scipy.stats.shapiro`, `probplot` (Q-Q), normal-fit overlays on histogram of `close_pct` |
| 04 | `04_likelihood_bayesian.ipynb` | Merges weather + coin data; likelihood evaluation; Bayesian posterior on the conditional return distribution |

## Methods

- **Shapiro-Wilk test** for normality of close-price returns (`close_pct`)
- **Q-Q plot** vs normal distribution
- **Histogram fitting** under (mu, sigma) hypotheses
- **Likelihood** under weather-conditional hypotheses
- **Bayesian inference** comparing return distributions under different weather regimes

## Stack

`Python` · `pandas` · `numpy` · `scipy.stats` · `matplotlib` · `Google Colab`

## How to Run

```bash
pip install pandas numpy scipy matplotlib
# Notebooks were authored in Google Colab; data was kept in Google Drive.
# Run notebooks in order; data files are not included (see .gitignore).
```

The original notebooks read from `MyDrive/베이지안자료분석PBL/data/...`.
Raw weather & crypto CSVs are excluded from this repo.

## Notes

- **PBL** (Problem-Based Learning) course at Korea University Sejong.
- Multi-stage: 1st midterm presentation → 2nd midterm → final report.
- See `docs/final_report_weather_crypto.pdf` for the polished writeup.

---

*Author: Sunjae Lee · B.S. Big Data Science @ Korea University Sejong*
*Part of [University-Projects/3-2](../) (2022 Fall)*
