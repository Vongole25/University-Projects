from __future__ import annotations

import argparse
import json
from pathlib import Path

from .dataset import DATASET_NAME, load_stereoset_subset
from .io import ensure_run_layout, write_json, write_jsonl, write_summary_csv
from .metrics import aggregate_metrics, build_summary_rows
from .scorer import CausalLMScorer, build_prefix_and_continuation
from .utils import generate_run_id, get_git_commit, set_seed, utc_now_iso


def _parse_domains(domains_text: str) -> set[str] | None:
    raw = [chunk.strip() for chunk in domains_text.split(",") if chunk.strip()]
    return set(raw) if raw else None


def cmd_run(args: argparse.Namespace) -> int:
    set_seed(args.seed)

    out_path = Path(args.out)
    if out_path.name == "runs":
        out_path = out_path / generate_run_id()

    layout = ensure_run_layout(out_path)
    run_id = out_path.name

    subsets = [args.subset] if args.subset in {"intersentence", "intrasentence"} else ["intersentence", "intrasentence"]
    domains = _parse_domains(args.domains)
    max_examples = args.max_examples if args.max_examples is not None and args.max_examples > 0 else None

    scorer = CausalLMScorer(
        model_id=args.model_id,
        dtype=args.dtype,
        device_map=args.device_map,
        score_mode=args.score_mode,
        cache_dir=args.cache_dir,
    )

    predictions: list[dict] = []
    skipped_counts: dict[str, int] = {
        "invalid_labels": 0,
        "intrasentence_blank_missing": 0,
        "scoring_errors": 0,
    }
    selected_split: dict[str, str] = {}

    for subset in subsets:
        loaded = load_stereoset_subset(
            subset=subset,
            domains=domains,
            max_examples=max_examples,
            cache_dir=args.cache_dir,
        )
        selected_split[subset] = loaded.split_name
        skipped_counts["invalid_labels"] += loaded.skipped_invalid_labels

        for ex in loaded.examples:
            try:
                scores = {}
                for label in ["stereotype", "anti-stereotype", "unrelated"]:
                    prefix, continuation = build_prefix_and_continuation(ex.subset, ex.context, ex.candidates[label])
                    scores[label] = scorer.score(prefix=prefix, continuation=continuation)
            except ValueError as err:
                if "BLANK" in str(err) or "____" in str(err):
                    skipped_counts["intrasentence_blank_missing"] += 1
                else:
                    skipped_counts["scoring_errors"] += 1
                continue
            except Exception:
                skipped_counts["scoring_errors"] += 1
                continue

            predictions.append(
                {
                    "example_id": ex.example_id,
                    "subset": ex.subset,
                    "domain": ex.domain,
                    "context": ex.context,
                    "candidates": ex.candidates,
                    "scores": scores,
                }
            )

    metrics = aggregate_metrics(predictions, skip_counts=skipped_counts)
    summary_rows = build_summary_rows(args.model_id, predictions)

    manifest = {
        "run_id": run_id,
        "created_at": utc_now_iso(),
        "git_commit": get_git_commit(Path.cwd()),
        "model_id": args.model_id,
        "dataset_name": DATASET_NAME,
        "subset": args.subset,
        "domains": sorted(domains) if domains else "all",
        "seed": args.seed,
        "max_examples": args.max_examples,
        "score_mode": args.score_mode,
        "dtype": args.dtype,
        "device_map": args.device_map,
        "batch_size": args.batch_size,
        "cache_dir": args.cache_dir,
        "selected_splits": selected_split,
        "skip_counts": skipped_counts,
        "num_predictions": len(predictions),
    }

    write_json(layout["manifest"], manifest)
    write_jsonl(layout["predictions"], predictions)
    write_json(layout["metrics"], metrics)
    write_summary_csv(
        layout["summary"],
        summary_rows,
        fieldnames=["model_id", "subset", "domain", "n", "lms", "ss", "icat"],
    )

    print(f"[llm-ss] run complete: {out_path} (n={len(predictions)})")
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
    print("[llm-ss] report")
    print(json.dumps(metrics, indent=2, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="llm-ss", description="StereoSet topic-bias CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run StereoSet scoring")
    run_parser.add_argument("--model_id", default="meta-llama/Meta-Llama-3-8B-Instruct")
    run_parser.add_argument("--subset", choices=["intersentence", "intrasentence", "both"], default="both")
    run_parser.add_argument(
        "--domains",
        default="gender,race,religion,profession",
        help="Comma-separated StereoSet domains.",
    )
    run_parser.add_argument("--max_examples", type=int, default=None)
    run_parser.add_argument("--seed", type=int, default=42)
    run_parser.add_argument("--score_mode", default="mean_logprob")
    run_parser.add_argument("--dtype", choices=["bf16", "fp16", "fp32"], default="bf16")
    run_parser.add_argument("--device_map", default="auto")
    run_parser.add_argument("--batch_size", type=int, default=1)
    run_parser.add_argument("--cache_dir", default=None)
    run_parser.add_argument("--out", required=True, help="Run output directory, e.g. runs/<run_id>")
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
