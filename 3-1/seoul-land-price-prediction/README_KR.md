# 서울시 부동산·공시지가 — 행정동 군집 분석 (한글)

> **3-1 (2022년 1학기)** · 고려대 세종 · 빅데이터실습 · 10조 팀 프로젝트

부동산/공시지가 데이터 기반 end-to-end 분석으로, 최종적으로
**서울 행정동을 PCA + 군집화**하여 지리 시각화까지 완성한 학기 단위 프로젝트.

## 한눈에 보기

- **데이터:** 수업 제공 부동산 데이터(~2023-04) + 행정구역 코드(KIKmix) +
  서울 행정동 GeoJSON
- **목표:** 부동산·인구·공시지가 변수 기반으로 서울 행정동의 자연스러운 그룹을 탐색
- **흐름:** EDA → 변수 선택·전처리 → 차원 축소 → PCA + 군집 → 군집별 분석 + 지도 시각화

## 폴더 구조

```
seoul-land-price-prediction/
├── README.md / README_KR.md
├── .gitignore
├── notebooks/
│   ├── 01_eda.ipynb                                  2주차 — EDA, 이상치, 기초통계
│   ├── 02_variable_selection_preprocessing.ipynb    2주차 — 변수 선택, 서울 한정, 결측 처리
│   ├── 03_dimensionality_reduction.ipynb             3주차 — 상관행렬, 헥사곤 플롯, 변수 축소
│   ├── 04_pca_clustering.ipynb                       4주차 — PCA + 군집화
│   └── 05_group_analysis_visualization.ipynb         5주차 — 군집별 특성, 법정동→행정동, 시각화
├── data/  (수업 제공 + 공공데이터)
└── docs/  (1주차 발표 + 4주차 대본)
```

## 주차별 흐름

| 주차 | 노트북 | 내용 |
|---|---|---|
| 2 | `01_eda.ipynb` | 모듈 셋업, 결측값/이상치 확인, 기초통계, 시각화 |
| 2 | `02_variable_selection_preprocessing.ipynb` | 서울 지역 필터, 위치/토지이용/인구 변수 선택 |
| 3 | `03_dimensionality_reduction.ipynb` | 상관행렬, 헥사곤 플롯, 교수님 피드백 반영, 변수 축소 |
| 4 | `04_pca_clustering.ipynb` | 스케일링, **PCA**, 군집화 |
| 5 | `05_group_analysis_visualization.ipynb` | 군집 ID 부여, **법정동→행정동 변환**, 그룹별 특징, 지도 시각화 |

## 사용 방법론

- **EDA·전처리**: 이상치 제거, 결측 처리, 변수 선택
- **차원 축소**: 상관 분석, 헥사곤 비닝, 수작업 축소
- **PCA**: 스케일링 + 주성분 분석
- **군집화**: K-means 또는 계층적 (노트북 04 참고)
- **공간 시각화**: GeoPandas + 서울 행정동 GeoJSON

## 사용 기술

`Python` · `pandas` · `numpy` · `scikit-learn` · `matplotlib`/`seaborn` ·
`GeoPandas` · `Jupyter`

## 실행 방법

```bash
pip install pandas numpy scikit-learn matplotlib seaborn geopandas openpyxl
jupyter notebook notebooks/01_eda.ipynb
# 01 → 05 순서대로 실행
```

데이터는 상대경로 `../data/` 참조.

## 비고

- 10조 팀 프로젝트.
- 주차별 교수님 피드백을 다음 노트북에 반영 (노트북 03 "교수님 피드백" 섹션 참고).
- 1주차 발표 자료와 4주차 대본만 남아있음 (이후 주차 자료는 학기 중 분실).

---

*작성: 이선재 (Sunjae Lee) · 고려대 세종 빅데이터전공*
*[University-Projects/3-1](../) (2022년 1학기) 하위 프로젝트*
