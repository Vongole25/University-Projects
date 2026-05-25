<!--
  Vongole25/University-Projects/README.md
  → 학부 프로젝트 모음 repo의 메인 README
-->

# University Projects — Korea University, Sejong (2020–2026)

Selected coursework, competition, and research projects from my B.S. in **Big Data Science**
at Korea University, Sejong Campus. Each subdirectory has its own README with details.

> Author: **Sunjae Lee** · 📝 [Blog](https://it-study-2002.tistory.com/) · ✉ leeseonjae0111@gmail.com

---

## 🥇 Competition Projects

### 1. Survival Analysis on Clinical Data — 🥇 1st Place
**Department Data Analysis Competition**, Korea University Sejong · 2022 · Team
- Applied **Cox proportional hazards** and parametric survival models to clinical data.
- Produced interpretable risk stratification and survival curves for outcome prediction.
- Stack: `R` · `Python` · `lifelines`

### 2. Defective Coffee Bean Classification — 🥈 2nd Place
**T-SUM Data Analysis Competition**, Korea University Sejong · 2023 · Team of 4
- Image classifier using **EfficientNet-B0** with transfer learning.
- Handled class imbalance via weighted sampling and on-the-fly augmentation.
- Stack: `PyTorch` · `EfficientNet` · `Albumentations`
- 📁 See: [`/computer-vision/coffee-bean-classification`](https://github.com/Vongole25/Computer-Vision)

### 3. Deepfake Detection — 🥉 3rd Place
**T-SUM Data Analysis Competition**, Korea University Sejong · 2023 · Team of 4
- Frame-level CNN feature extraction for binary classification (real vs deepfake).
- Investigated temporal aggregation across video frames.
- Stack: `PyTorch` · `OpenCV` · `CNN`

### 4. Biodiversity × Environmental Modeling — Top 9 Finalist
**National Environment Data Competition**, Ministry of Environment · Team
- Statistical modeling of species diversity vs environmental variables.
- Made it to the final 9 out of nation-wide entries.

---

## 📚 Coursework Projects

### 5. Stock Price Prediction with EC-GBM
- Ensemble gradient boosting (XGBoost / LightGBM) on financial time-series.
- Feature engineering on technical indicators and lagged returns.
- Stack: `Python` · `XGBoost` · `LightGBM` · `pandas`

### 6. Bayesian Analysis: Cryptocurrency × Weather
- Bayesian inference exploring cross-domain correlation between weather data and crypto returns.
- Used PyMC for posterior estimation and HDI visualization.
- Stack: `PyMC` · `numpy` · `matplotlib`

### 7. Seoul Officially Assessed Land Price Prediction
- Regression on geospatial and demographic features (zoning, transit access, population).
- Stack: `Python` · `scikit-learn` · `GeoPandas`

---

## 🧪 Research Experience (separate repo)

**Undergraduate Research Assistant** — Big Data Science Lab (Advisor: Prof. Bo-Seung Choi), 2023–2024
- COVID-19 case counts vs population mobility, modeled with **SARIMAX**.
- Code & notes not in this repo (research data restricted).

---

## 🛠 Common Stack

`Python` · `PyTorch` · `scikit-learn` · `pandas` · `NumPy` · `R` · `XGBoost` · `Jupyter`

---

## 📂 Repo Structure (planned)

```
University-Projects/
├── README.md                              (this file)
├── survival-analysis/
│   ├── README.md
│   ├── notebooks/
│   └── data_description.md
├── stock-prediction-ec-gbm/
├── bayesian-crypto-weather/
├── land-price-prediction/
└── biodiversity-modeling/
```

*Defective bean & Deepfake projects live in the [Computer-Vision](https://github.com/Vongole25/Computer-Vision) repo.*

---

📌 Currently preparing for **NLP graduate school admission (2027 Spring intake)** — see [my profile](https://github.com/Vongole25).
