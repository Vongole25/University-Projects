# 강화학습 — CarRacing-v2 (gymnasium) (한글)

> **4-1 (2023년 1학기)** · 고려대 세종 · **통계학과 인공지능** 수업

**OpenAI Gymnasium** (Box2D 물리 엔진) 환경 기반 강화학습 프로젝트.
메인 환경: **CarRacing-v2** — 픽셀 관측 + 연속 제어 자동차 레이싱 시뮬레이터.

## 한눈에 보기

- **환경:** `CarRacing-v2` (Gymnasium / Box2D)
- **사전 학습:** `FrozenLake-v1` (tabular RL 기초)
- **사용 기술:** `gymnasium`, `box2d-py`, `pygame`, `PyTorch`

## 폴더 구조

```
reinforcement-learning/
├── README.md / README_KR.md
├── .gitignore
├── notebooks/
│   └── 01_carracing_rl.ipynb      메인 — CarRacing-v2 학습
├── _drafts/                        초기 환경 설정 / tabular RL 입문
│   ├── gymnasium_setup.ipynb
│   └── frozenlake_intro.ipynb
└── docs/
    └── rl_summary.pdf
```

## 사용 기술

`Python` · `PyTorch` · `gymnasium` · `box2d-py` · `pygame` · `tqdm`

## 실행 방법

```bash
# Box2D는 conda 권장
conda install -y -c conda-forge box2d-py
pip install gymnasium tqdm torch torchvision pygame

jupyter notebook notebooks/01_carracing_rl.ipynb
```

## 비고

- **통계학과 인공지능** 수업의 RL 프로젝트 (2023년 1학기).
- 같은 수업에서 NLP 챗봇도 진행 → [`../chatbot/`](../chatbot/) 참고.
- 환경 설정(Box2D + swig)이 까다로워 `_drafts/`에 시도 흔적 보존.
- 교수님 강의 자료(PDF)는 저작권상 제외.

---

*작성: 이선재 (Sunjae Lee) · 고려대 세종 빅데이터전공*
*[University-Projects/4-1](../) (2023년 1학기) 하위 프로젝트*
