from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


DATASET_NAME = "McGill-NLP/stereoset"
REQUIRED_LABELS = {"stereotype", "anti-stereotype", "unrelated"}


@dataclass
class StereoSetExample:
    example_id: str
    subset: str
    domain: str
    context: str
    candidates: dict[str, str]


@dataclass
class LoadResult:
    examples: list[StereoSetExample]
    skipped_invalid_labels: int
    split_name: str


def detect_split_name(split_names: Iterable[str]) -> str:
    names = list(split_names)
    for preferred in ("validation", "dev"):
        if preferred in names:
            return preferred
    if not names:
        raise ValueError("StereoSet dataset has no available splits.")
    return names[0]


def _normalize_label(label: str) -> str:
    return str(label).strip().lower()


def map_candidates_from_row(row: dict) -> dict[str, str] | None:
    sentences = row.get("sentences")
    if sentences is None:
        return None

    pairs: list[tuple[str, str]] = []
    if isinstance(sentences, dict):
        labels = sentences.get("gold_label", [])
        texts = sentences.get("sentence", [])
        pairs = [(_normalize_label(label), str(text)) for label, text in zip(labels, texts)]
    elif isinstance(sentences, list):
        for item in sentences:
            pairs.append((_normalize_label(item.get("gold_label", "")), str(item.get("sentence", ""))))

    label_to_text: dict[str, str] = {}
    for label, text in pairs:
        if label not in REQUIRED_LABELS:
            return None
        label_to_text[label] = text

    if set(label_to_text.keys()) != REQUIRED_LABELS:
        return None
    return label_to_text


def load_stereoset_subset(
    subset: str,
    domains: set[str] | None = None,
    max_examples: int | None = None,
    cache_dir: str | None = None,
) -> LoadResult:
    if subset not in {"intersentence", "intrasentence"}:
        raise ValueError(f"Unsupported subset: {subset}")

    from datasets import load_dataset

    ds_dict = load_dataset(DATASET_NAME, subset, cache_dir=cache_dir)
    split_name = detect_split_name(ds_dict.keys())
    split = ds_dict[split_name]

    examples: list[StereoSetExample] = []
    skipped_invalid_labels = 0

    for row in split:
        domain = str(row.get("bias_type", "unknown"))
        if domains is not None and domain not in domains:
            continue

        candidates = map_candidates_from_row(row)
        if candidates is None:
            skipped_invalid_labels += 1
            continue

        example_id = str(row.get("id") or row.get("target") or f"{subset}_{len(examples)}")
        context = str(row.get("context", ""))
        examples.append(
            StereoSetExample(
                example_id=example_id,
                subset=subset,
                domain=domain,
                context=context,
                candidates=candidates,
            )
        )

        if max_examples is not None and len(examples) >= max_examples:
            break

    return LoadResult(examples=examples, skipped_invalid_labels=skipped_invalid_labels, split_name=split_name)
