from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

DOMAIN_ORDER = ["gender", "race", "religion", "profession"]
SUBSET_ORDER = ["intersentence", "intrasentence"]


def _subset_domain_map(summary_rows: list[dict]) -> dict[tuple[str, str], dict]:
    return {(row["subset"], row["domain"]): row for row in summary_rows}


def plot_ss_bars(summary_rows: list[dict], plots_dir: str | Path) -> list[Path]:
    plots_path = Path(plots_dir)
    plots_path.mkdir(parents=True, exist_ok=True)
    by_key = _subset_domain_map(summary_rows)
    created: list[Path] = []

    for subset in SUBSET_ORDER:
        values: list[float] = []
        err_low: list[float] = []
        err_high: list[float] = []
        labels: list[str] = []

        for domain in DOMAIN_ORDER:
            row = by_key.get((subset, domain))
            if row is None:
                continue
            ss = float(row["ss"])
            ci_low = float(row["ss_ci_low"])
            ci_high = float(row["ss_ci_high"])
            values.append(ss)
            err_low.append(max(0.0, ss - ci_low))
            err_high.append(max(0.0, ci_high - ss))
            labels.append(domain)

        if not values:
            continue

        fig, ax = plt.subplots(figsize=(7, 4))
        x = np.arange(len(values))
        ax.bar(x, values, yerr=np.array([err_low, err_high]), capsize=4)
        ax.axhline(50.0, linestyle="--")
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_ylim(0, 100)
        ax.set_ylabel("SS")
        ax.set_title(f"SS by domain ({subset})")

        out = plots_path / f"ss_by_domain_{subset}.png"
        fig.tight_layout()
        fig.savefig(out)
        plt.close(fig)
        created.append(out)

    return created


def plot_ss_heatmap(summary_rows: list[dict], plots_dir: str | Path) -> Path:
    plots_path = Path(plots_dir)
    plots_path.mkdir(parents=True, exist_ok=True)

    by_key = _subset_domain_map(summary_rows)
    data = np.full((len(SUBSET_ORDER), len(DOMAIN_ORDER)), np.nan)

    for i, subset in enumerate(SUBSET_ORDER):
        for j, domain in enumerate(DOMAIN_ORDER):
            row = by_key.get((subset, domain))
            if row is not None:
                data[i, j] = float(row["ss"])

    masked = np.ma.masked_invalid(data)

    fig, ax = plt.subplots(figsize=(8, 3))
    im = ax.imshow(masked, aspect="auto", vmin=0, vmax=100)
    ax.set_xticks(np.arange(len(DOMAIN_ORDER)))
    ax.set_xticklabels(DOMAIN_ORDER)
    ax.set_yticks(np.arange(len(SUBSET_ORDER)))
    ax.set_yticklabels(SUBSET_ORDER)
    ax.set_title("SS heatmap")

    for i in range(len(SUBSET_ORDER)):
        for j in range(len(DOMAIN_ORDER)):
            if np.isnan(data[i, j]):
                text = "NA"
            else:
                text = f"{data[i, j]:.1f}"
            ax.text(j, i, text, ha="center", va="center")

    fig.colorbar(im, ax=ax, label="SS")
    fig.tight_layout()
    out = plots_path / "heatmap_ss.png"
    fig.savefig(out)
    plt.close(fig)
    return out
