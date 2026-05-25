# Survival Analysis on Heart Failure Clinical Records

> 🥇 **1st Place**, Department Data Analysis Competition · Korea University Sejong (2023) · Team

Predicting death and providing personalized survival probability for heart-failure patients
by combining **traditional statistics**, **survival models (Cox PH, AFT)**, and
**machine learning classifiers**.

## TL;DR

- **Data:** UCI Heart Failure Clinical Records (299 patients, 13 features)
- **Pipeline:**
  1. Traditional statistical tests (Chi², Mann-Whitney U, Shapiro-Wilk)
  2. Variable selection via **Borda count** → 2 key features
  3. ML classifiers: Logistic Regression (Stratified K-Fold CV), Random Forest
  4. Survival analysis: **Cox PH** + Kaplan-Meier + **AFT** by age group
- **Result:** Selected 2-variable model **outperforms** the full-feature model.
  Cox-significant variables align with ML feature importance.
  Age-stratified AFT survival curves provided for clinical decision support.

## Repository Structure

```
survival-analysis-heart-failure/
├── README.md                       (this file)
├── README_KR.md                    (Korean version)
├── BACKGROUND.md                   (full project background, methods, conclusion)
├── data/
│   └── heart_failure_clinical_records_dataset.csv   (UCI, 299 rows)
├── notebooks/
│   ├── 01_traditional_statistics.ipynb     Chi²·Mann-Whitney·Shapiro-Wilk
│   ├── 02_machine_learning.ipynb           LogReg + RF + K-M curve (main)
│   └── 03_cox_survival_analysis.ipynb      Cox PH + Forest Plot
└── figures/                        (optional output figures)
```

## Methods (one-liner each)

| Notebook | What it does |
|---|---|
| **01** Traditional Statistics | Group comparison and normality tests on each feature |
| **02** Machine Learning | Logistic Regression + Random Forest, stratified 5-fold CV, MCC |
| **03** Cox Survival | CoxPHFitter, concordance index, Hazard Ratio forest plot |

For full methodology and equations, see **[BACKGROUND.md](./BACKGROUND.md)**.

## How to Run

```bash
# 1. Install dependencies
pip install pandas numpy scipy scikit-learn matplotlib lifelines

# 2. Open notebooks in order
jupyter notebook notebooks/01_traditional_statistics.ipynb
# (data path inside notebooks is relative: ../data/...)
```

## Data Source

[UCI Machine Learning Repository — Heart Failure Clinical Records](https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records)
(Chicco & Jurman, 2020. Two hospitals in Pakistan, 2015.)

The CSV is included here for reproducibility (12 KB, public domain).

## Stack

`Python` · `pandas` · `scikit-learn` · `lifelines` · `scipy` · `matplotlib`

---

*Author: Sunjae Lee · B.S. Big Data Science @ Korea University Sejong*
*Part of [University-Projects](https://github.com/Vongole25/University-Projects)*
