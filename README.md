# University-Projects
Projects carried out in Korea University Sejong Campus(2020 ~ 2026)

# 1. Seoul Land Price Prediction Model

## 📌 Overview
- **Course**: Multivariate Data Analysis PBL (Junior, Spring Semester, Korea University Sejong Campus)  
- **Period**: Apr 2023 – Jun 2023  
- **Objective**: To build a predictive model for Seoul’s official land prices and identify key influencing factors  

---

## 🏙️ Background & Motivation
Official land price is a critical indicator for taxation, finance, and policy-making in South Korea. Also, official land price of Seoul has high volatility, and clear standard of calculating official land price is not enough. 
This project aimed to analyze public land price data of Seoul and develop a **machine learning model** capable of predicting land prices while exploring the main variables affecting them.  

---

## 📂 Data Sources
- Statistical Geographic Information Service (SGIS)  
- Resident Registration Population Statistics  
- National Land Information Platform  
- National Spatial Information Portal  
- Open Architecture Data System for Private Sector  
- Address-based Industry Support Service  
- Public Data Portal 

---

## 🔎 Methodology

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

## 📊 Results & Conclusion

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

## ✨ Outcomes & Learnings
- Applied multivariate analysis concepts to real-world urban land price data  
- Built a complete analysis pipeline from **preprocessing → feature engineering → dimensionality reduction → modeling**  
- Gained hands-on experience with data-driven policy analysis and machine learning workflows  

---
