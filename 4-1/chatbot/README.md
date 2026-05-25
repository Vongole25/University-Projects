# Korean Chatbot — KoGPT2 Fine-tuning

> **4-1 (2023 Spring)** · Korea University Sejong · *Statistics & AI* course (통계학과 인공지능)

Building a Korean conversational chatbot using **KoGPT2** (SKT's Korean
GPT-2). Compares three approaches: SBERT-based retrieval, KoGPT2 without
fine-tuning (baseline), and KoGPT2 fine-tuned on Q-A pairs + supplementary
SNS data.

## TL;DR

- **Models compared:**
  - **SBERT** (`sentence-transformers`) — retrieval-based chatbot
  - **KoGPT2** (`skt/kogpt2-base-v2`) — generative, original (baseline)
  - **KoGPT2 fine-tuned** — main; trained on ChatbotData + SNS data
- **Data:**
  - [`songys/Chatbot_data`](https://github.com/songys/Chatbot_data) — Korean Q-A pairs
  - Additional SNS-style data (preprocessed)
- **Stack:** `transformers`, `sentence-transformers`, `datasets`, `sentencepiece`, `PyTorch`

## Repository Structure

```
chatbot/
├── README.md / README_KR.md
├── .gitignore
├── notebooks/
│   ├── 01_week2_sbert_kogpt.ipynb           Week-2 class: SBERT + KoGPT comparison
│   ├── 02_kogpt_no_fine_tuning_baseline.ipynb  KoGPT2 original (no fine-tuning) baseline
│   └── 03_chatbot_sunjae_main.ipynb         Main: KoGPT2 fine-tuned on Q-A + SNS data
└── data/
    ├── README.md
    └── ChatbotData.csv                       Korean Q-A pairs (songys/Chatbot_data)
```

## Approach

| # | Notebook | What it does |
|---|---|---|
| 01 | `01_week2_sbert_kogpt.ipynb` | Class-provided baseline — SBERT semantic search vs KoGPT2 generation, side-by-side |
| 02 | `02_kogpt_no_fine_tuning_baseline.ipynb` | Load `skt/kogpt2-base-v2`, generate without any fine-tuning (control) |
| 03 | `03_chatbot_sunjae_main.ipynb` ⭐ | Fine-tune KoGPT2 on `ChatbotData.csv` + additional SNS-style data; main project notebook |

## Stack

`Python` · `PyTorch` · `transformers` (HuggingFace) · `sentence-transformers` ·
`datasets` · `sentencepiece` · `Google Colab`

## How to Run

```bash
pip install transformers sentence-transformers datasets sentencepiece torch
jupyter notebook notebooks/03_chatbot_sunjae_main.ipynb
# Run in order: 01 → 02 → 03 for the full comparison
```

## Notes

- Course project — *Statistics & AI* (통계학과 인공지능), 2023 Spring.
- Same course also covered Reinforcement Learning — see
  [`../reinforcement-learning/`](../reinforcement-learning/) for that project.
- Lecture materials (instructor's PDFs) intentionally excluded for copyright safety.

---

*Author: Sunjae Lee · B.S. Big Data Science @ Korea University Sejong*
*Part of [University-Projects/4-1](../) (2023 Spring)*
