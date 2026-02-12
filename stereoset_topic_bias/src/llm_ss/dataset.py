from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Any


DATASET_NAME = "McGill-NLP/stereoset"
REQUIRED_LABELS = {"stereotype", "anti-stereotype", "unrelated"}

# StereoSet HF dataset often uses numeric gold_label ids:
# 0=stereotype, 1=anti-stereotype, 2=unrelated
LABEL_ID_TO_NAME = {
    0: "stereotype",
    1: "anti-stereotype",
    2: "unrelated",
}


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


def _normalize_label(label: Any) -> str | None:
    """
    Normalize StereoSet gold_label to one of:
      - stereotype
      - anti-stereotype
      - unrelated
    StereoSet gold_label may be:
      - int (0/1/2)
      - numeric strings ("0"/"1"/"2")
      - already string labels
    """
    if label is None:
        return None

    # direct int mapping (including numpy ints which are int-like)
    try:
        if isinstance(label, int):
            return LABEL_ID_TO_NAME.get(label)
    except Exception:
        pass

    s = str(label).strip().lower()
    if not s:
        return None

    # numeric string mapping
    if s.isdigit():
        try:
            return LABEL_ID_TO_NAME.get(int(s))
        except Exception:
            return None

    # already a label string (or close variants)
    if s in REQUIRED_LABELS:
        return s
    if s in ("anti", "antistereotype", "anti_stereotype", "anti-stereotype"):
        return "anti-stereotype"
    if s in ("stereo", "stereotypical", "stereotype"):
        return "stereotype"
    if s in ("unrel", "unrelated"):
        return "unrelated"

    # unknown label
    return None


def map_candidates_from_row(row: dict) -> dict[str, str] | None:
    sentences = row.get("sentences")
    if sentences is None:
        return None

    pairs: list[tuple[str | None, str]] = []

    # Case 1) dict-of-lists (this is what HF StereoSet returns)
    if isinstance(sentences, dict):
        labels = sentences.get("gold_label", [])
        texts = sentences.get("sentence", [])
        for lbl, txt in zip(labels, texts):
            pairs.append((_normalize_label(lbl), str(txt)))

    # Case 2) list-of-dicts (keep support just in case)
    elif isinstance(sentences, list):
        for item in sentences:
            if not isinstance(item, dict):
                continue
            pairs.append((_normalize_label(item.get("gold_label")), str(item.get("sentence", ""))))

    else:
        return None

    label_to_text: dict[str, str] = {}
    for label, text in pairs:
        if label is None:
            # unknown label -> invalid example for v0.1
            return None
        if label not in REQUIRED_LABELS:
            return None
        label_to_text[label] = text

    # must contain all 3 exactly (one each)
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
