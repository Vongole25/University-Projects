from __future__ import annotations

import csv
import json

from llm_ss.cli import cmd_analyze


def _row(example_id: str, subset: str, domain: str, stereo: float, anti: float, unrel: float) -> dict:
    return {
        "example_id": example_id,
        "subset": subset,
        "domain": domain,
        "context": "ctx",
        "candidates": {
            "stereotype": "a",
            "anti-stereotype": "b",
            "unrelated": "c",
        },
        "scores": {
            "stereotype": stereo,
            "anti-stereotype": anti,
            "unrelated": unrel,
        },
    }


def test_analyze_writes_ci_delta_and_plots(tmp_path):
    run_dir = tmp_path / "runs" / "tiny"
    run_dir.mkdir(parents=True)

    manifest = {"model_id": "tiny-model"}
    (run_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    predictions = [
        _row("1", "intersentence", "gender", 0.9, 0.1, 0.0),
        _row("2", "intersentence", "gender", 0.2, 0.6, 0.1),
        _row("3", "intersentence", "race", 0.7, 0.2, 0.1),
        _row("4", "intersentence", "race", 0.1, 0.4, 0.0),
        _row("5", "intrasentence", "religion", 0.8, 0.3, 0.2),
        _row("6", "intrasentence", "profession", 0.1, 0.1, 0.1),
    ]
    with (run_dir / "predictions.jsonl").open("w", encoding="utf-8") as f:
        for row in predictions:
            f.write(json.dumps(row) + "\n")

    args = type("Args", (), {"run_dir": str(run_dir), "bootstrap": 50, "seed": 123})
    rc = cmd_analyze(args)
    assert rc == 0

    summary_path = run_dir / "summary_with_ci.csv"
    delta_path = run_dir / "delta_ss.csv"
    plots_dir = run_dir / "plots"

    assert summary_path.exists()
    assert delta_path.exists()
    assert plots_dir.exists()

    with summary_path.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows
    assert list(rows[0].keys()) == [
        "model_id",
        "subset",
        "domain",
        "n",
        "lms",
        "lms_ci_low",
        "lms_ci_high",
        "ss",
        "ss_ci_low",
        "ss_ci_high",
        "icat",
        "icat_ci_low",
        "icat_ci_high",
    ]

    with delta_path.open("r", encoding="utf-8") as f:
        delta_rows = list(csv.DictReader(f))
    assert list(delta_rows[0].keys()) == ["subset", "domain_a", "domain_b", "delta_ss", "ci_low", "ci_high", "significant"]

    plot_files = list(plots_dir.glob("*.png"))
    assert plot_files
