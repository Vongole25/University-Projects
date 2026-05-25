# Reinforcement Learning — CarRacing-v2 (gymnasium)

> **4-1 (2023 Spring)** · Korea University Sejong · *Statistics & AI* course (통계학과 인공지능)

Reinforcement Learning project using **OpenAI Gymnasium** (Box2D physics).
Main environment: **CarRacing-v2** — a top-down car-racing simulator
with continuous control and pixel observations.

## TL;DR

- **Environment:** `CarRacing-v2` (Gymnasium / Box2D)
- **Prerequisites explored:** FrozenLake-v1 for tabular RL fundamentals
- **Stack:** `gymnasium`, `box2d-py`, `pygame`, `PyTorch`

## Repository Structure

```
reinforcement-learning/
├── README.md / README_KR.md
├── .gitignore
├── notebooks/
│   └── 01_carracing_rl.ipynb     Main: CarRacing-v2 RL training
├── _drafts/                       Early environment / tabular RL exploration
│   ├── README.md
│   ├── gymnasium_setup.ipynb     gymnasium + box2d + swig install
│   └── frozenlake_intro.ipynb    FrozenLake-v1 (tabular RL intro)
└── docs/
    └── rl_summary.pdf            Short RL summary doc
```

## Stack

`Python` · `PyTorch` · `gymnasium` · `box2d-py` · `pygame` · `tqdm`

## How to Run

```bash
# Conda recommended for box2d
conda install -y -c conda-forge box2d-py
pip install gymnasium tqdm torch torchvision pygame

jupyter notebook notebooks/01_carracing_rl.ipynb
```

## Notes

- Part of the *Statistics & AI* course — same course also covered NLP
  (see [`../chatbot/`](../chatbot/)).
- Environment setup was non-trivial (Box2D + swig); `_drafts/` keeps the
  setup attempts.
- Lecture materials (instructor's PDFs) intentionally excluded for copyright safety.

---

*Author: Sunjae Lee · B.S. Big Data Science @ Korea University Sejong*
*Part of [University-Projects/4-1](../) (2023 Spring)*
