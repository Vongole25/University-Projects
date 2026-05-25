# EC-GBM 기반 주가 예측 (한글)

> **3-2 (2022년 2학기)** · 고려대 세종 · **확률모형캡스톤디자인** · 3조
> 김석범 · 김수호 · **이선재**

**Entropy-Corrected Geometric Brownian Motion (EC-GBM)** 모델을 직접 구현·평가한
캡스톤 프로젝트. 기반 논문:
[Gupta et al., *Sci Rep* 14, 28384 (2024)](https://doi.org/10.1038/s41598-024-79714-3).

## 한눈에 보기

- **동기:** 일반 GBM은 로그-정규 수익률과 일정한 변동성을 가정 → 실제 주가의
  비대칭성·첨도·변동성 변화를 잘 못 잡음.
- **무엇을:** **샤논 엔트로피** 기반으로 보정한 GBM(EC-GBM)을 적용해
  실제 가격 시계열의 결정론적 구조를 더 잘 반영.
- **어떻게:** Python으로 Monte Carlo 시뮬레이션; 엔트로피 감소 threshold 기반
  trajectory 채택.
- **데이터:** AMD 일별 종가, 2020-01-01 ~ 2024-11-30 (1,314 거래일), `yfinance`.

## 폴더 구조

```
stock-prediction-ec-gbm/
├── README.md / README_KR.md
├── .gitignore
├── notebooks/
│   └── 01_ec_gbm_simulation.ipynb   GBM + EC-GBM Python 구현
├── R/
│   ├── README.md
│   └── fda_exploration.R            함수형 데이터 분석 (보조)
└── docs/
    ├── final_report_team3.docx      3조 최종보고서
    ├── presentation_final.pdf       최종 발표 슬라이드
    └── paper_summary_entropy_gbm.docx  기반 논문 정리
```

## 방법론

### GBM (기하 브라운 운동)
$$dS_t = \mu S_t \, dt + \sigma S_t \, dW_t$$

자산 가격 모델링의 고전. 로그-정규 + 일정 `(μ, σ)` 가정.

### EC-GBM (엔트로피 보정 GBM)
- Monte Carlo로 GBM 후보 궤적 다수 생성.
- 각 후보에 대해 **샤논 엔트로피**(이산 히스토그램 기반) 계산.
- 기준 궤적과 결합 시 엔트로피가 `threshold` 이상 감소하면 **채택**
  (결정론적 구조 더 강함 = 더 좋은 적합).
- `M`회 반복.

### 구현 함수
- `generate_gbm_trajectory(S0, μ, σ, T)`: 누적 브라운 → GBM 궤적
- `compute_entropy(data, bins=20)`: 히스토그램 기반 이산 엔트로피
- `ec_gbm(S0, μ, σ, T, M, threshold)`: 메인 루프

## 사용 기술

`Python` (`numpy`, `matplotlib`, `yfinance`) · `R` (`fda` 패키지 — 보조)

## 실행 방법

```bash
pip install numpy matplotlib yfinance
jupyter notebook notebooks/01_ec_gbm_simulation.ipynb
```

## 참고문헌

- Gupta, R., Drzazga-Szczęśniak, E. A., Kais, S. et al.
  **"Entropy corrected geometric Brownian motion."**
  *Scientific Reports* **14**, 28384 (2024).
- 우리 팀의 논문 정리: `docs/paper_summary_entropy_gbm.docx`

## 비고

- 3조 팀 프로젝트: 김석범, 김수호, **이선재**
- 캡스톤 수업 — 최종보고서 + 발표 필수.
- R 보조 코드(`R/fda_exploration.R`)는 초반 함수형 데이터 분석 탐색.

---

*작성: 이선재 (Sunjae Lee) · 고려대 세종 빅데이터전공*
*[University-Projects/3-2](../) (2022년 2학기) 하위 프로젝트*
