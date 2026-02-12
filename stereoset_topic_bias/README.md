# StereoSet topic-bias v0.1 (Llama-3 ready)

This package runs **StereoSet topic-bias scoring** with causal LMs and exports:

- `manifest.json`
- `predictions.jsonl`
- `metrics.json`
- `summary.csv`

## Install

From repository root:

```bash
pip install -e stereoset_topic_bias
```

## Hugging Face access (Llama-3)

`meta-llama/Meta-Llama-3-8B-Instruct` may require gated access and accepted license terms.
Set your token before running:

```bash
export HF_TOKEN="YOUR_TOKEN_HERE"
```

## CLI

```bash
llm-ss --help
```

### v0.1 reproduction command (plain-text likelihood, no chat template)

```bash
llm-ss run \
  --model_id meta-llama/Meta-Llama-3-8B-Instruct \
  --subset both \
  --domains "gender,race,religion,profession" \
  --score_mode mean_logprob \
  --dtype bf16 \
  --device_map auto \
  --batch_size 1 \
  --cache_dir ~/.cache/huggingface \
  --out stereoset_topic_bias/runs/<run_id>
```

## Tiny-model smoke example

```bash
llm-ss run \
  --model_id sshleifer/tiny-gpt2 \
  --subset both \
  --max_examples 5 \
  --dtype fp32 \
  --cache_dir ~/.cache/huggingface \
  --out stereoset_topic_bias/runs/smoke_tiny
```

## Notes

- v0.1 scoring is **plain text continuation likelihood** (`mean_logprob`) and intentionally does **not** use chat templates.
- Tie-break policy is fixed: equal scores count as `0.5` for both LMS and SS pairwise indicators.
- `intrasentence` uses `BLANK` (or `____`) splitting where suffix text is included in the continuation score.
- `summary.csv` schema is fixed as:
  `model_id, subset, domain, n, lms, ss, icat`.
