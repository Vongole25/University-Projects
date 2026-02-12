from __future__ import annotations

import csv
import json
import random
from pathlib import Path

from .metrics import score_triplet

VALID_SUBSETS = {"intersentence", "intrasentence"}
VALID_DOMAINS = {"gender", "race", "religion", "profession"}


def load_predictions(run_dir: str | Path) -> list[dict]:
    preds_path = Path(run_dir) / "predictions.jsonl"
    predictions: list[dict] = []
    if not preds_path.exists():
        return predictions

    with preds_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            predictions.append(json.loads(line))
    return predictions


def group_examples(preds: list[dict]) -> dict[tuple[str, str], list[dict]]:
    grouped: dict[tuple[str, str], list[dict]] = {}
    for pred in preds:
        subset = pred.get("subset")
        domain = pred.get("domain") or pred.get("bias_type")
        if subset not in VALID_SUBSETS or domain not in VALID_DOMAINS:
            continue
        grouped.setdefault((subset, domain), []).append(pred)
    return grouped


def compute_scores(examples: list[dict]) -> tuple[float, float, float, int]:
    n = len(examples)
    if n == 0:
        return 0.0, 0.0, 0.0, 0

    lms_vals: list[float] = []
    ss_vals: list[float] = []
    icat_vals: list[float] = []
    for ex in examples:
        triplet = score_triplet(ex["scores"])
        lms_vals.append(triplet["lms"])
        ss_vals.append(triplet["ss"])
        icat_vals.append(triplet["icat"])

    lms = sum(lms_vals) / n
    ss = sum(ss_vals) / n
    icat = sum(icat_vals) / n
    return lms, ss, icat, n


def _percentile(sorted_values: list[float], pct: float) -> float:
    if not sorted_values:
        return 0.0
    if len(sorted_values) == 1:
        return float(sorted_values[0])
    idx = (len(sorted_values) - 1) * pct
    lo = int(idx)
    hi = min(lo + 1, len(sorted_values) - 1)
    frac = idx - lo
    return float(sorted_values[lo] * (1.0 - frac) + sorted_values[hi] * frac)


def bootstrap_ci(examples: list[dict], B: int, seed: int) -> dict[str, float]:
    lms, ss, icat, n = compute_scores(examples)
    result = {
        "n": n,
        "lms": lms,
        "lms_ci_low": lms,
        "lms_ci_high": lms,
        "ss": ss,
        "ss_ci_low": ss,
        "ss_ci_high": ss,
        "icat": icat,
        "icat_ci_low": icat,
        "icat_ci_high": icat,
    }
    if n == 0:
        return result

    rng = random.Random(seed)
    lms_draws: list[float] = []
    ss_draws: list[float] = []
    icat_draws: list[float] = []
    for _ in range(B):
        sample = [examples[rng.randrange(n)] for _ in range(n)]
        draw_lms, draw_ss, draw_icat, _ = compute_scores(sample)
        lms_draws.append(draw_lms)
        ss_draws.append(draw_ss)
        icat_draws.append(draw_icat)

    lms_draws.sort()
    ss_draws.sort()
    icat_draws.sort()

    result.update(
        {
            "lms_ci_low": _percentile(lms_draws, 0.025),
            "lms_ci_high": _percentile(lms_draws, 0.975),
            "ss_ci_low": _percentile(ss_draws, 0.025),
            "ss_ci_high": _percentile(ss_draws, 0.975),
            "icat_ci_low": _percentile(icat_draws, 0.025),
            "icat_ci_high": _percentile(icat_draws, 0.975),
        }
    )
    return result


def _bootstrap_ss(examples: list[dict], rng: random.Random) -> float:
    n = len(examples)
    if n == 0:
        return 0.0
    sample = [examples[rng.randrange(n)] for _ in range(n)]
    _, ss, _, _ = compute_scores(sample)
    return ss


def delta_ss_bootstrap(groupA: list[dict], groupB: list[dict], B: int, seed: int) -> dict[str, float | bool]:
    _, mean_a, _, _ = compute_scores(groupA)
    _, mean_b, _, _ = compute_scores(groupB)
    mean_delta = mean_a - mean_b

    if not groupA or not groupB:
        return {
            "delta_ss": mean_delta,
            "ci_low": mean_delta,
            "ci_high": mean_delta,
            "significant": False,
        }

    rng = random.Random(seed)
    deltas: list[float] = []
    for _ in range(B):
        delta = _bootstrap_ss(groupA, rng) - _bootstrap_ss(groupB, rng)
        deltas.append(delta)

    deltas.sort()
    ci_low = _percentile(deltas, 0.025)
    ci_high = _percentile(deltas, 0.975)
    significant = not (ci_low <= 0.0 <= ci_high)
    return {
        "delta_ss": mean_delta,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "significant": significant,
    }


def read_model_id(run_dir: str | Path) -> str:
    run_path = Path(run_dir)
    manifest_path = run_path / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("model_id"):
            return str(manifest["model_id"])

    summary_path = run_path / "summary.csv"
    if summary_path.exists():
        with summary_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            first = next(reader, None)
            if first and first.get("model_id"):
                return str(first["model_id"])

    return "unknown"
