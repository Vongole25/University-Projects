# 한국어 챗봇 — KoGPT2 파인튜닝 (한글)

> **4-1 (2023년 1학기)** · 고려대 세종 · **통계학과 인공지능** 수업

SKT의 한국어 GPT-2 모델인 **KoGPT2**를 사용해 한국어 대화형 챗봇을 구축.
**SBERT 기반 검색**, **KoGPT2 원본(baseline)**, **KoGPT2 파인튜닝(메인)** 세 가지
접근을 비교.

## 한눈에 보기

- **비교 모델:**
  - **SBERT** (`sentence-transformers`) — 검색 기반 챗봇
  - **KoGPT2** (`skt/kogpt2-base-v2`) — 생성형, 원본 (baseline)
  - **KoGPT2 파인튜닝** — 메인, Q-A + SNS 데이터로 추가 학습
- **데이터:** `songys/Chatbot_data` (한국어 Q-A 쌍) + SNS 스타일 데이터
- **사용 기술:** `transformers`, `sentence-transformers`, `datasets`, `PyTorch`

## 폴더 구조

```
chatbot/
├── README.md / README_KR.md
├── .gitignore
├── notebooks/
│   ├── 01_week2_sbert_kogpt.ipynb              2주차 수업 — SBERT + KoGPT 비교
│   ├── 02_kogpt_no_fine_tuning_baseline.ipynb  KoGPT2 원본 (baseline)
│   └── 03_chatbot_sunjae_main.ipynb            메인: Q-A + SNS 파인튜닝
└── data/
    ├── README.md
    └── ChatbotData.csv                          한국어 Q-A 쌍
```

## 접근법

| # | 노트북 | 내용 |
|---|---|---|
| 01 | `01_week2_sbert_kogpt.ipynb` | 수업 기본 — SBERT 의미 검색 vs KoGPT2 생성, 비교 |
| 02 | `02_kogpt_no_fine_tuning_baseline.ipynb` | `skt/kogpt2-base-v2` 로드, 파인튜닝 없이 생성 (control) |
| 03 | `03_chatbot_sunjae_main.ipynb` ⭐ | 메인 — `ChatbotData.csv` + SNS 데이터로 KoGPT2 파인튜닝 |

## 사용 기술

`Python` · `PyTorch` · `transformers` · `sentence-transformers` ·
`datasets` · `sentencepiece` · `Google Colab`

## 실행 방법

```bash
pip install transformers sentence-transformers datasets sentencepiece torch
jupyter notebook notebooks/03_chatbot_sunjae_main.ipynb
# 01 → 02 → 03 순서로
```

## 비고

- **통계학과 인공지능** 수업의 NLP 프로젝트 (2023년 1학기).
- 같은 수업에서 강화학습도 진행 →
  [`../reinforcement-learning/`](../reinforcement-learning/) 참고.
- 교수님 강의 자료(PDF)는 저작권상 의도적으로 제외.

---

*작성: 이선재 (Sunjae Lee) · 고려대 세종 빅데이터전공*
*[University-Projects/4-1](../) (2023년 1학기) 하위 프로젝트*
