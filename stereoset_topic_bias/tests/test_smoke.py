from __future__ import annotations

import csv
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


REQUIRES = ["torch", "transformers", "datasets"]
missing = [name for name in REQUIRES if importlib.util.find_spec(name) is None]


@pytest.mark.skipif(bool(missing), reason=f"missing runtime dependencies: {missing}")
def test_smoke_run_creates_required_files_with_content(tmp_path):
    run_dir = tmp_path / "runs" / "smoke_run"
    env = os.environ.copy()
    env["PYTHONPATH"] = str((Path.cwd() / "stereoset_topic_bias" / "src")) + os.pathsep + env.get("PYTHONPATH", "")

    cmd = [
        sys.executable,
        "-m",
        "llm_ss.cli",
        "run",
        "--model_id",
        "sshleifer/tiny-gpt2",
        "--subset",
        "both",
        "--out",
        str(run_dir),
        "--max_examples",
        "5",
        "--dtype",
        "fp32",
    ]

    completed = subprocess.run(cmd, check=False, capture_output=True, text=True, env=env)
    if completed.returncode != 0:
        network_markers = ["ProxyError", "403 Forbidden", "Can't load the configuration", "ConnectionError"]
        if any(marker in completed.stderr for marker in network_markers):
            pytest.skip("network/model hub access is unavailable in this environment")
    assert completed.returncode == 0, completed.stderr

    manifest_path = run_dir / "manifest.json"
    preds_path = run_dir / "predictions.jsonl"
    metrics_path = run_dir / "metrics.json"
    summary_path = run_dir / "summary.csv"

    assert manifest_path.exists()
    assert preds_path.exists()
    assert metrics_path.exists()
    assert summary_path.exists()
    assert (run_dir / "plots").is_dir()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["model_id"] == "sshleifer/tiny-gpt2"
    assert manifest["dataset_name"] == "McGill-NLP/stereoset"

    pred_lines = [line for line in preds_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(pred_lines) > 0

    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    assert "overall" in metrics
    assert metrics["overall"]["n"] > 0

    with summary_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert rows
    domains = {row["domain"] for row in rows}
    assert domains
