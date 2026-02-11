from __future__ import annotations

import json
import subprocess



def test_smoke_run_creates_required_files(tmp_path):
    run_dir = tmp_path / "runs" / "smoke_run"
    cmd = [
        "llm-ss",
        "run",
        "--model_id",
        "sshleifer/tiny-gpt2",
        "--subset",
        "both",
        "--out",
        str(run_dir),
        "--max_examples",
        "2",
    ]

    completed = subprocess.run(cmd, check=False, capture_output=True, text=True)
    assert completed.returncode == 0, completed.stderr

    assert (run_dir / "manifest.json").exists()
    assert (run_dir / "predictions.jsonl").exists()
    assert (run_dir / "metrics.json").exists()
    assert (run_dir / "summary.csv").exists()
    assert (run_dir / "plots").is_dir()

    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    for field in [
        "run_id",
        "created_at",
        "git_commit",
        "model_id",
        "dataset_name",
        "subset",
        "seed",
        "max_examples",
        "score_mode",
    ]:
        assert field in manifest

    assert manifest["model_id"] == "sshleifer/tiny-gpt2"
    assert manifest["dataset_name"] == "McGill-NLP/stereoset"
