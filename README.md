# University-Projects
Projects carried out in Korea University Sejong Campus(2020 ~ 2026)

# 1. Seoul Land Price Prediction Model

##  Overview
- **Course**: Multivariate Data Analysis PBL (Junior, Spring Semester, Korea University Sejong Campus)  
- **Period**: Apr 2023 – Jun 2023  
- **Objective**: To build a predictive model for Seoul’s official land prices and identify key influencing factors  

---

##  Background & Motivation
Official land price is a critical indicator for taxation, finance, and policy-making in South Korea. Also, official land price of Seoul has high volatility, and clear standard of calculating official land price is not enough. 
This project aimed to analyze public land price data of Seoul and develop a **machine learning model** capable of predicting land prices while exploring the main variables affecting them.  

---

##  Data Sources
- Statistical Geographic Information Service (SGIS)  
- Resident Registration Population Statistics  
- National Land Information Platform  
- National Spatial Information Portal  
- Open Architecture Data System for Private Sector  
- Address-based Industry Support Service  
- Public Data Portal 

---

##  Methodology

1. **Feature Engineering**  
   - Generated derived variables (e.g., ratios, categorical encodings, interaction terms)  
   - Improved explanatory power by creating meaningful new features from raw data  

2. **Exploratory Data Analysis (EDA)**  
   - Handled missing values and detected outliers  
   - Visualized distributions and correlations among variables  
   - Identified multicollinearity and redundant features  

3. **Factor Analysis**  
   - Extracted latent factors from correlated variables  
   - Reduced dimensionality while preserving interpretability of constructs  

4. **Feature Selection**  
   - Conducted correlation analysis and multicollinearity diagnostics  
   - Selected the most relevant predictors for land price estimation  

5. **Dimensionality Reduction (PCA)**  
   - Applied Principal Component Analysis to summarize high-dimensional features  
   - Retained principal components explaining the majority of variance  

6. **Clustering**  
   - Grouped districts with similar characteristics using PCA-transformed data  
   - Identified region-specific patterns in land prices  

7. **Predictive Modeling**  
   - Built and compared Multiple Linear Regression, Random Forest, and XGBoost models  
   - Evaluated performance with R² and RMSE metrics  

---

##  Results & Conclusion

- **Cluster-specific modeling improved performance significantly compared to using the entire dataset.**  
  - Without clustering, XGBoost achieved only **R² = 58.78%**.  
  - After clustering, prediction performance improved across all clusters.

- **Model performance by cluster:**  
  | Cluster   | Best Model   | R² Score |
  |-----------|--------------|----------|
  | Cluster_0 | XGBoost      | **86.00%** |
  | Cluster_1 | XGBoost      | 70.95%   |
  | Cluster_2 | XGBoost      | 81.17%   |
  | Cluster_3 | Random Forest| 81.32%   |

- **Key insights:**  
  - All clusters except **Cluster_3** (commercial districts with high working population) selected **XGBoost** as the best model.  
  - **Cluster_0**, characterized by strong healthcare and infrastructure development, showed the **highest predictive accuracy (86%)**.  
  - **Cluster_3** was relatively small in size, and **Random Forest** performed better than XGBoost in this cluster.  

➡️ Overall, **clustering enhanced predictive performance**, showing that regional characteristics play a crucial role in land price estimation.

---

##  Outcomes & Learnings
- Applied multivariate analysis concepts to real-world urban land price data  
- Built a complete analysis pipeline from **preprocessing → feature engineering → dimensionality reduction → modeling**  
- Gained hands-on experience with data-driven policy analysis and machine learning workflows  

---

# 2. Analysis of the Effect of Weather Factors on Cryptocurrency Closing Price Volatility

##  Project Overview
- **Course**: Bayesian Statistical Analysis PBL (3rd Year, 2nd Semester, Korea University Sejong Campus)  
- **Period**: October 2023 – December 2023  
- **Objective**: To analyze whether weather factors influence cryptocurrency closing price volatility through Bayesian inference.  

---

##  Background and Purpose
The cryptocurrency market is far more volatile and unpredictable than traditional financial markets.  
While previous studies have mainly focused on economic indicators (e.g., MFI, Williams %R),  
weather factors such as **temperature, humidity, cloud cover, and solar radiation** may affect **investor psychology** but have been insufficiently studied.  

This project aims to:
1. Compare a model using only economic indicators with one that combines economic and weather data through **Bayesian inference**.  
2. Construct and analyze **prior distributions**, **likelihood functions**, and **posterior distributions**,  
   and quantitatively evaluate explanatory power using the **Bayes Factor**.  

---

##  Data Sources
| Category | Description | Source |
|-----------|-------------|--------|
| Cryptocurrency Closing Prices | Daily price data and rate of change calculations | Binance API |
| Economic Indicators | MFI, Williams %R, and other market momentum indicators | Derived from Binance data |
| Weather Data | Temperature, humidity, cloud cover, and solar radiation | Visual Crossing (New York City) |

---

##  Methodology

1. **Prior Distribution**  
   - Based on the histogram of cryptocurrency return rates,  
     the empirical prior was defined as a normal distribution with mean = 0.06 and standard deviation = 3.3725.  

2. **Likelihood Function**  
   - Applied PCA (Principal Component Analysis) to remove variable correlation.  
   - Used Gaussian Kernel Density Estimation (GKDE) to define joint probability distributions  
     for economic and combined datasets.  

3. **Posterior Update**  
   - Combined prior and likelihood to calculate posterior probabilities across volatility intervals.  
   - Normalized so that total probability equals 1.  

4. **Confidence Interval Comparison**  
   - Classical approach: Bootstrap-based 95% confidence interval.  
   - Bayesian approach: 95% HPDI (Highest Posterior Density Interval).  

5. **Hypothesis Testing and Bayes Factor**  
   - H₀: The return rate lies in the negative interval.  
   - H₁: The return rate lies in the positive interval.  
   - Compared model support using Bayes Factors.  

---

##  Results and Analysis

| Dataset | Posterior Mean | Std. Dev | 95% HPDI | Bayes Factor |
|----------|----------------|-----------|-----------|---------------|
| Economic Data | 0.03978 | 3.4937 | (-3.0, 3.5) | 1.76 |
| Economic + Weather | 0.02173 | 3.3741 | (-2.5, 2.45) | 1.44 |

- **Slight decrease in standard deviation** after adding weather data → reduced uncertainty.  
- **Bayes Factor decreased (1.76 → 1.44)** → explanatory power slightly weakened.  
- **KL Divergence** analysis showed that the combined model more closely resembled real-world data.  

---

##  Conclusion
- The inclusion of weather factors **marginally reduced uncertainty**,  
  but did **not significantly enhance model explanatory power**.  
- Bayesian hypothesis testing showed stronger support for the **economic-only model (H₁)**.  
- However, KL Divergence indicated that the combined model better mirrored real data distributions.  
➡️ Overall, the **effect of weather data was limited**, but it shows potential as a **supplementary factor reflecting investor sentiment**.  

---

##  Learning Outcomes
- Implemented and interpreted core Bayesian concepts such as **Bayes Factor, HPDI, and Posterior Predictive Check (PPC)**.  
- Compared classical vs. Bayesian methods to understand model reliability and uncertainty.  
- Experimented with integrating **non-economic variables (weather data)** into financial modeling.  

---

