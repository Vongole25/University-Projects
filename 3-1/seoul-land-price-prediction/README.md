# Seoul Land Price & Real Estate — Administrative Dong Clustering

> **3-1 (2022 Spring)** · Korea University Sejong · Big Data Practicum · Team 10 (10조)

Multi-week, end-to-end data analysis on Seoul real-estate / land-price data,
culminating in **PCA + clustering of administrative dongs (행정동)** with
geospatial visualization.

## TL;DR

- **Data:** 부동산 데이터 (수업 제공, ~2023-04) + 행정구역 코드 (KIKmix) +
  서울 행정동 GeoJSON.
- **Goal:** Discover natural groupings of Seoul administrative dongs based on
  real-estate and demographic features, including individual official land prices
  (개별공시지가).
- **Pipeline:** EDA → variable selection / preprocessing → dimensionality
  reduction → PCA + clustering → group-level analysis + map visualization.

## Repository Structure

```
seoul-land-price-prediction/
├── README.md / README_KR.md
├── .gitignore
├── notebooks/
│   ├── 01_eda.ipynb                                   Week 2 — EDA, outliers, basic stats
│   ├── 02_variable_selection_preprocessing.ipynb     Week 2 — variable selection,
│   │                                                  Seoul subset, missing values
│   ├── 03_dimensionality_reduction.ipynb              Week 3 — correlation, hex plots,
│   │                                                  variable reduction
│   ├── 04_pca_clustering.ipynb                        Week 4 — PCA + clustering
│   └── 05_group_analysis_visualization.ipynb          Week 5 — cluster profiling,
│                                                      hangjeongdong matching, viz
├── data/
│   ├── README.md
│   ├── real_estate_data_230403.xlsx     (course-provided real estate data)
│   ├── KIKmix_admin_codes_20210401.xlsx (administrative district codes)
│   ├── seoul_hangjeongdong.geojson      (Seoul admin-dong boundaries)
│   └── grouped.csv                      (intermediate result from notebooks)
└── docs/
    ├── team10_week1_presentation.pdf
    ├── team10_week1_slides.pptx
    └── week4_presentation_script.docx   (only partial scripts retained)
```

## Pipeline (Week by Week)

| Week | Notebook | What it does |
|---|---|---|
| 2 | `01_eda.ipynb` | Module setup, missing-value check, outlier removal, basic statistics, visualizations |
| 2 | `02_variable_selection_preprocessing.ipynb` | Filter to Seoul, select location / land-use / population variables, handle missingness |
| 3 | `03_dimensionality_reduction.ipynb` | Correlation matrix, hexagonal binning plots, prof feedback iteration, reduce variable count |
| 4 | `04_pca_clustering.ipynb` | Variable scaling, **Principal Component Analysis (PCA)**, clustering |
| 5 | `05_group_analysis_visualization.ipynb` | Assign cluster IDs, **legal-dong → admin-dong (행정동) mapping**, group profiling, map viz |

## Methods Used

- **EDA & Preprocessing:** outlier removal, missing value treatment, variable selection
- **Dimensionality Reduction:** correlation analysis, hex binning, manual reduction
- **PCA:** scaling + principal component analysis
- **Clustering:** k-means or hierarchical (see notebook 04)
- **Spatial Visualization:** GeoPandas + Seoul hangjeongdong GeoJSON

## Stack

`Python` · `pandas` · `numpy` · `scikit-learn` (PCA, clustering) ·
`matplotlib` / `seaborn` · `GeoPandas` · `Jupyter`

## How to Run

```bash
pip install pandas numpy scikit-learn matplotlib seaborn geopandas openpyxl
jupyter notebook notebooks/01_eda.ipynb
# Run notebooks in order (01 → 05)
```

Notebooks reference data with relative paths (`../data/`).

## Notes

- Team project (10조) — collaborated with classmates.
- Iterative weekly feedback from instructor reflected in successive notebooks
  (see `notebooks/03_*` "교수님 피드백" section).
- Only week-1 presentation and week-4 script survived; later week documents
  were lost.

---

*Author: Sunjae Lee · B.S. Big Data Science @ Korea University Sejong*
*Part of [University-Projects/3-1](../) (2022 Spring)*
