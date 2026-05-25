# 베이지안: 기상요인 × 가상화폐 수익률 분석 (한글)

> **3-2 (2022년 2학기)** · 고려대 세종 · 베이지안자료분석PBL

뉴욕(주요 거래소·트레이더가 몰려 있는 지역)의 **기상 조건이 BTC 종가 변동률
분포에 영향을 주는가**를 베이지안 통계로 검증한 학기 단위 PBL 프로젝트.

> _최종 보고서 제목:_ **"기상요인이 가상화폐 종가 변동률 분포에 미치는 영향"**

## 한눈에 보기

- **가설:** 날씨(비/온도 등)가 BTC 종가 변동률 분포를 이동시키는가?
- **데이터:**
  - Bitcoin / Binance 가격 데이터
  - 뉴욕 날씨 데이터 (NewYork_weather_*.csv)
- **방법:**
  1. 데이터 전처리 — 타임스탬프 정렬, `is_rain` 파생, 일별 집계
  2. **정규성 검정** — Shapiro-Wilk, Q-Q plot
  3. **Likelihood / 베이지안 추론** — 기상 조건별 분포 비교

## 폴더 구조

```
bayesian-crypto-weather/
├── README.md / README_KR.md
├── .gitignore
├── notebooks/
│   ├── 01_data_preprocessing.ipynb     날씨+BTC 정렬, 파생변수
│   ├── 02_binance_data.ipynb           Binance/BTC 데이터 정리
│   ├── 03_normality_tests.ipynb        Shapiro-Wilk, Q-Q plot, 히스토그램 피팅
│   └── 04_likelihood_bayesian.ipynb    메인: likelihood + 베이지안 추론 (144셀)
└── docs/
    ├── week1_midterm_presentation.pdf  (1주차 중간발표 - 제안)
    ├── midterm2_presentation_script.docx (2차 중간발표 대본)
    └── final_report_weather_crypto.pdf (최종 보고서)
```

## 파이프라인

| # | 노트북 | 내용 |
|---|---|---|
| 01 | `01_data_preprocessing.ipynb` | 뉴욕 날씨 CSV 로드, `is_rain` 파생 (강수량 NaN/값 기준), 일별 집계 |
| 02 | `02_binance_data.ipynb` | Binance/BTC 가격 데이터 준비 |
| 03 | `03_normality_tests.ipynb` | Shapiro-Wilk, Q-Q plot, `close_pct` 히스토그램에 정규 분포 피팅 |
| 04 | `04_likelihood_bayesian.ipynb` | 날씨+코인 병합, likelihood 평가, 기상 조건별 조건부 수익률 분포에 대한 베이지안 추론 |

## 사용 방법론

- **Shapiro-Wilk 검정** (수익률 정규성)
- **Q-Q plot** vs 정규분포
- **히스토그램 피팅** (mu, sigma 가설별)
- **Likelihood** (기상 조건부)
- **베이지안 추론** (기상 조건별 분포 비교)

## 사용 기술

`Python` · `pandas` · `numpy` · `scipy.stats` · `matplotlib` · `Google Colab`

## 실행 방법

```bash
pip install pandas numpy scipy matplotlib
# 원본 노트북은 Colab + Google Drive 환경
# 노트북 순서대로 실행; 데이터 파일은 repo에서 제외
```

원본은 `MyDrive/베이지안자료분석PBL/data/...` 참조.
원시 날씨·코인 CSV는 repo 미포함 (`.gitignore` 참고).

## 비고

- **PBL** (Problem-Based Learning) 과목.
- 단계적: 1주차 중간발표 → 2차 중간발표 → 최종 보고서.
- 정제된 결과는 `docs/final_report_weather_crypto.pdf` 참고.

---

*작성: 이선재 (Sunjae Lee) · 고려대 세종 빅데이터전공*
*[University-Projects/3-2](../) (2022년 2학기) 하위 프로젝트*
