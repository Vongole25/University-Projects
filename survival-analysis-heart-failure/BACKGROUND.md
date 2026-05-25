# Project Background & Objectives

## 제목
**머신러닝과 생존분석을 활용한 심부전 환자의 사망 예측 및 생존확률 제공**
*(Predicting Death and Providing Survival Probability of Heart Failure Patients via Machine Learning and Survival Analysis)*

---

## 1. Background

심혈관 질환(CVDs)은 전 세계적으로 사망 원인 1위를 차지하며, 매년 약 1,790만 명의
생명을 앗아간다 (전 세계 사망자의 31%). 심부전(Heart Failure)은 심혈관 질환에
의해 발생하는 흔한 사건이며, 조기 진단과 적절한 치료가 이루어진다면 많은 사망을
예방할 수 있다.

따라서 본 연구는 실제 심부전 환자 데이터를 활용해
- (1) 환자의 사망 여부를 예측하는 머신러닝 모델을 개발하고,
- (2) 개인별 생존 확률을 제공하는 것을

목표로 한다.

## 2. Dataset

- **Source:** UCI Machine Learning Repository — Heart Failure Clinical Records
- **수집처:** 파키스탄 소재 2개 병원
- **표본 수:** 환자 299명
- **변수 (13개):**
  - 인구학/임상: `age`, `sex`, `smoking`, `diabetes`, `high_blood_pressure`, `anaemia`
  - 검사 수치: `creatinine_phosphokinase`, `ejection_fraction`, `platelets`,
    `serum_creatinine`, `serum_sodium`
  - 추적: `time` (추적 기간), `DEATH_EVENT` (사망 여부)

## 3. Methods

### 3.1 Cox Proportional Hazards Model
위험률(hazard rate) 기반으로 독립 변수들이 환자의 사망 위험에 미치는
상대적 영향을 추정한다.

$$h(t \mid X) = h_0(t) \cdot \exp(\beta_1 X_1 + \beta_2 X_2 + \cdots + \beta_p X_p)$$

- $h(t \mid X)$: 특정 시간 $t$에서의 조건부 위험률
- $h_0(t)$: 기저 위험률
- $X_i$: 독립 변수, $\beta_i$: 회귀 계수

### 3.2 AFT (Accelerated Failure Time) Model
생존 시간을 직접 모델링하며, 변수들이 생존 시간을 어떻게 가속/지연시키는지
분석한다.

$$\log(T) = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \cdots + \beta_p X_p + \varepsilon$$

- $T$: 생존 시간
- $\varepsilon$: 특정 분포(Weibull, Log-Normal 등)를 따르는 오차항

### 3.3 Variable Selection — 보르다 리스트(Borda Count)
전통적 통계 검정(Chi-Squared, Mann-Whitney U, Shapiro-Wilk)을 기반으로
변수 중요도를 종합 순위화하여 핵심 변수 2개를 선정.

### 3.4 Machine Learning Classifiers
- Logistic Regression (with Stratified K-Fold CV)
- Random Forest
- 평가: Accuracy, Matthews Correlation Coefficient(MCC) 등

## 4. Conclusion

- 전통적 통계 방법 + 보르다 리스트로 두 개의 중요 변수를 선정한 결과,
  전체 변수를 사용하는 것보다 **더 높은 예측 성능**을 확인.
  → 효율적인 변수 선택이 모델 성능 향상에 중요함.
- **Cox 비례 위험 모형**으로 도출한 유의미한 변수가 ML 결과와 일치.
- 환자를 **세 연령 그룹**으로 나누어 각 그룹에 적합한 생존 확률을 제시.
- 의료진이 환자를 조기에 선별하고 맞춤형 치료 전략을 수립하는 데 활용 가능.

## 5. Award

🥇 **1st Place** — Department Data Analysis Competition,
Korea University Sejong (2022) · Team
