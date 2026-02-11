# StereoSet topic-bias v0.1 (Bootstrap)

This directory contains the **PR1 bootstrap scaffold** for a StereoSet topic-bias package.

## Install

From repository root:

```bash
pip install -e stereoset_topic_bias
```

## CLI

```bash
llm-ss --help
llm-ss run --model_id sshleifer/tiny-gpt2 --subset both --out stereoset_topic_bias/runs/<run_id> --max_examples 2
llm-ss analyze --run_dir stereoset_topic_bias/runs/<run_id> --bootstrap 1000
llm-ss report --run_dir stereoset_topic_bias/runs/<run_id>
```

## Current bootstrap behavior

- `run` creates required artifacts (`manifest.json`, `predictions.jsonl`, `metrics.json`, `summary.csv`, `plots/`) with placeholder content.
- `analyze` and `report` currently write/read placeholder summaries and are intended to be expanded in PR2/PR3.

## Important notes

- Future versions that actually load LLMs and datasets may require:
  - Hugging Face authentication token (`HF_TOKEN`) for gated assets.
  - Explicit acceptance of model/dataset licenses on Hugging Face.
- This PR does **not** execute full evaluation logic yet.

## Run output schema

`runs/<run_id>/`
- `manifest.json`
- `predictions.jsonl`
- `metrics.json`
- `summary.csv`
- `plots/`
