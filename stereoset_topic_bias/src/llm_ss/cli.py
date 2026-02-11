from __future__ import annotations

import argparse
import json
from pathlib import Path

from .io import ensure_run_layout, write_json, write_jsonl, write_summary_csv
from .utils import generate_run_id, get_git_commit, set_seed, utc_now_iso


DATASET_NAME = "McGill-NLP/stereoset"


def cmd_run(args: argparse.Namespace) -> int:
    set_seed(args.seed)

    out_path = Path(args.out)
    if out_path.name == "runs":
        out_path = out_path / generate_run_id()

    layout = ensure_run_layout(out_path)
    run_id = out_path.name

    manifest = {
        "run_id": run_id,
        "created_at": utc_now_iso(),
        "git_commit": get_git_commit(Path.cwd()),
        "model_id": args.model_id,
        "dataset_name": DATASET_NAME,
        "subset": args.subset,
        "seed": args.seed,
        "max_examples": args.max_examples,
        "score_mode": args.score_mode,
    }

    predictions: list[dict] = []
    metrics = {
        "status": "bootstrap",
        "num_predictions": 0,
        "note": "Placeholder metrics. Full evaluation lands in PR2/PR3.",
    }
    summary_rows = [
        {"metric": "status", "value": "bootstrap"},
        {"metric": "num_predictions", "value": 0},
    ]

    write_json(layout["manifest"], manifest)
    write_jsonl(layout["predictions"], predictions)
    write_json(layout["metrics"], metrics)
    write_summary_csv(layout["summary"], summary_rows, fieldnames=["metric", "value"])

    print(f"[llm-ss] bootstrap run created: {out_path}")
    return 0


def cmd_analyze(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir)
    layout = ensure_run_layout(run_dir)

    metrics = {
        "status": "analyze_bootstrap",
        "bootstrap_samples": args.bootstrap,
        "note": "Placeholder analyze output. Statistical bootstrap will be added in PR3.",
    }
    write_json(layout["metrics"], metrics)
    write_summary_csv(
        layout["summary"],
        [
            {"metric": "status", "value": "analyze_bootstrap"},
            {"metric": "bootstrap_samples", "value": args.bootstrap},
        ],
        fieldnames=["metric", "value"],
    )
    print(f"[llm-ss] analyze bootstrap complete: {run_dir}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir)
    metrics_path = run_dir / "metrics.json"
    if not metrics_path.exists():
        print(f"[llm-ss] missing metrics: {metrics_path}")
        return 1

    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    print("[llm-ss] report (bootstrap)")
    print(json.dumps(metrics, indent=2, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="llm-ss", description="StereoSet topic-bias CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Create a run artifact directory")
    run_parser.add_argument("--model_id", required=True)
    run_parser.add_argument(
        "--subset", choices=["intersentence", "intrasentence", "both"], default="both"
    )
    run_parser.add_argument("--out", required=True, help="Run output directory, e.g. runs/<run_id>")
    run_parser.add_argument("--seed", type=int, default=42)
    run_parser.add_argument("--max_examples", type=int, default=0)
    run_parser.add_argument("--score_mode", default="logprob")
    run_parser.set_defaults(func=cmd_run)

    analyze_parser = subparsers.add_parser("analyze", help="Analyze an existing run")
    analyze_parser.add_argument("--run_dir", required=True)
    analyze_parser.add_argument("--bootstrap", type=int, default=1000)
    analyze_parser.set_defaults(func=cmd_analyze)

    report_parser = subparsers.add_parser("report", help="Print summary report for a run")
    report_parser.add_argument("--run_dir", required=True)
    report_parser.set_defaults(func=cmd_report)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
