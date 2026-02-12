from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from .analysis import bootstrap_ci, delta_ss_bootstrap, group_examples, load_predictions, read_model_id
from .dataset import DATASET_NAME, load_stereoset_subset
from .io import ensure_run_layout, write_json, write_jsonl, write_summary_csv
from .metrics import aggregate_metrics, build_summary_rows
from .plots import plot_ss_bars, plot_ss_heatmap
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

    preds = load_predictions(run_dir)
    groups = group_examples(preds)
    model_id = read_model_id(run_dir)

    summary_rows: list[dict] = []
    for (subset, domain), examples in sorted(groups.items()):
        stats = bootstrap_ci(examples, B=args.bootstrap, seed=args.seed)
        summary_rows.append(
            {
                "model_id": model_id,
                "subset": subset,
                "domain": domain,
                "n": stats["n"],
                "lms": round(float(stats["lms"]), 6),
                "lms_ci_low": round(float(stats["lms_ci_low"]), 6),
                "lms_ci_high": round(float(stats["lms_ci_high"]), 6),
                "ss": round(float(stats["ss"]), 6),
                "ss_ci_low": round(float(stats["ss_ci_low"]), 6),
                "ss_ci_high": round(float(stats["ss_ci_high"]), 6),
                "icat": round(float(stats["icat"]), 6),
                "icat_ci_low": round(float(stats["icat_ci_low"]), 6),
                "icat_ci_high": round(float(stats["icat_ci_high"]), 6),
            }
        )

    delta_rows: list[dict] = []
    for subset in ["intersentence", "intrasentence"]:
        domains = sorted({domain for (row_subset, domain) in groups if row_subset == subset})
        for i, domain_a in enumerate(domains):
            for domain_b in domains[i + 1 :]:
                delta = delta_ss_bootstrap(
                    groups[(subset, domain_a)],
                    groups[(subset, domain_b)],
                    B=args.bootstrap,
                    seed=args.seed,
                )
                delta_rows.append(
                    {
                        "subset": subset,
                        "domain_a": domain_a,
                        "domain_b": domain_b,
                        "delta_ss": round(float(delta["delta_ss"]), 6),
                        "ci_low": round(float(delta["ci_low"]), 6),
                        "ci_high": round(float(delta["ci_high"]), 6),
                        "significant": bool(delta["significant"]),
                    }
                )

    summary_with_ci_path = run_dir / "summary_with_ci.csv"
    write_summary_csv(
        summary_with_ci_path,
        summary_rows,
        fieldnames=[
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
        ],
    )

    delta_ss_path = run_dir / "delta_ss.csv"
    write_summary_csv(
        delta_ss_path,
        delta_rows,
        fieldnames=["subset", "domain_a", "domain_b", "delta_ss", "ci_low", "ci_high", "significant"],
    )

    plot_ss_bars(summary_rows, layout["plots"])
    plot_ss_heatmap(summary_rows, layout["plots"])

    metrics = json.loads(layout["metrics"].read_text(encoding="utf-8")) if layout["metrics"].exists() else {}
    metrics["analysis"] = {
        "bootstrap_samples": args.bootstrap,
        "summary_with_ci": str(summary_with_ci_path.name),
        "delta_ss": str(delta_ss_path.name),
    }
    write_json(layout["metrics"], metrics)

    print(f"[llm-ss] analyze bootstrap complete: {run_dir}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir)
    summary_ci_path = run_dir / "summary_with_ci.csv"
    delta_path = run_dir / "delta_ss.csv"

    if not summary_ci_path.exists():
        print(f"[llm-ss] missing summary_with_ci: {summary_ci_path}")
        return 1

    with summary_ci_path.open("r", encoding="utf-8") as f:
        summary_rows = list(csv.DictReader(f))

    if delta_path.exists():
        with delta_path.open("r", encoding="utf-8") as f:
            delta_rows = list(csv.DictReader(f))
    else:
        delta_rows = []

    print("[llm-ss] report")
    for subset in ["intersentence", "intrasentence"]:
        subset_rows = [r for r in summary_rows if r.get("subset") == subset]
        if not subset_rows:
            continue
        print(f"- {subset}")
        for row in sorted(subset_rows, key=lambda r: r["domain"]):
            print(
                f"  * {row['domain']}: SS={float(row['ss']):.2f} "
                f"(95% CI {float(row['ss_ci_low']):.2f}, {float(row['ss_ci_high']):.2f})"
            )

        most_biased = max(subset_rows, key=lambda r: abs(float(r["ss"]) - 50.0))
        print(
            f"  most biased domain: {most_biased['domain']} "
            f"(distance from 50 = {abs(float(most_biased['ss']) - 50.0):.2f})"
        )

    significant = [
        row
        for row in delta_rows
        if str(row.get("significant", "")).strip().lower() in {"true", "1", "yes"}
    ]
    significant.sort(key=lambda r: abs(float(r["delta_ss"])), reverse=True)
    if significant:
        print("- top significant delta_ss pairs")
        for row in significant[:3]:
            print(
                f"  * {row['subset']}: {row['domain_a']} - {row['domain_b']} = {float(row['delta_ss']):.2f} "
                f"(95% CI {float(row['ci_low']):.2f}, {float(row['ci_high']):.2f})"
            )
    else:
        print("- no significant delta_ss pairs")

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
    analyze_parser.add_argument("--seed", type=int, default=42)
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
