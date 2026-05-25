# 심부전 환자 사망 예측 — 생존분석 프로젝트 (한글 참고본)

> 🥇 **1등 수상** — 고려대학교 세종캠퍼스 학과 데이터분석 대회 (2022, 팀)

전통적 통계 + 생존분석(Cox PH, AFT) + 머신러닝을 결합해
심부전 환자의 사망 여부를 예측하고 개인별 생존확률을 제공한다.

## 한눈에 보기

- **데이터:** UCI Heart Failure (환자 299명, 13개 변수)
- **분석 흐름:**
  1. 전통적 통계 검정 (카이제곱, Mann-Whitney U, Shapiro-Wilk)
  2. 보르다 리스트로 핵심 변수 2개 선정
  3. 머신러닝 분류기 (로지스틱 회귀 + 5-fold CV, 랜덤 포레스트)
  4. 생존분석 (Cox PH + Kaplan-Meier + 연령 그룹별 AFT)
- **결과:** 2개 변수만 사용한 모델이 전체 변수 모델보다 **더 나은 성능**.
  Cox 모형의 유의 변수가 ML 변수 중요도와 일치.
  연령 그룹별 AFT 생존곡선으로 임상 의사결정 지원.

## 폴더 구조

```
survival-analysis-heart-failure/
├── README.md                       (영문)
├── README_KR.md                    (이 파일)
├── BACKGROUND.md                   (배경·방법·결론 상세)
├── data/                           UCI 데이터 (CSV)
├── notebooks/
│   ├── 01_traditional_statistics.ipynb     전통적 통계 검정
│   ├── 02_machine_learning.ipynb           메인 ML 모델
│   └── 03_cox_survival_analysis.ipynb      Cox PH + 위험비
└── figures/                        결과 이미지 (선택)
```

## 노트북별 역할

| 노트북 | 내용 |
|---|---|
| **01** 전통적 통계 | 그룹 비교·정규성 검정 (Chi², Mann-Whitney, Shapiro-Wilk) |
| **02** 머신러닝 | 로지스틱 회귀 + 랜덤포레스트, Stratified 5-fold CV, MCC 평가, K-M 곡선 |
| **03** Cox 생존분석 | CoxPHFitter, Concordance Index, Hazard Ratio Forest Plot |

자세한 방법론과 수식은 **[BACKGROUND.md](./BACKGROUND.md)** 참고.

## 실행 방법

```bash
pip install pandas numpy scipy scikit-learn matplotlib lifelines
jupyter notebook notebooks/01_traditional_statistics.ipynb
# (노트북 내 데이터 경로는 상대경로 ../data/... 로 수정됨)
```

## 데이터 출처

[UCI ML Repository — Heart Failure Clinical Records](https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records)
(Chicco & Jurman, 2020 / 파키스탄 2개 병원, 2015)

데이터셋 자체는 공개 자료이므로 repo에 포함.

## 사용 기술

`Python` · `pandas` · `scikit-learn` · `lifelines` · `scipy` · `matplotlib`

---

*작성: 이선재 (Sunjae Lee) · 고려대 세종 빅데이터전공*
*[University-Projects](https://github.com/Vongole25/University-Projects) 의 하위 프로젝트*
