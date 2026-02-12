from __future__ import annotations

from dataclasses import dataclass


def _torch_dtype(dtype: str):
    import torch

    mapping = {
        "bf16": torch.bfloat16,
        "fp16": torch.float16,
        "fp32": torch.float32,
    }
    if dtype not in mapping:
        raise ValueError(f"Unsupported dtype: {dtype}")
    return mapping[dtype]


def _ensure_boundary_space(prefix: str, continuation: str) -> tuple[str, str]:
    if not prefix or not continuation:
        return prefix, continuation
    if prefix[-1].isspace() or continuation[0].isspace():
        return prefix, continuation
    return prefix + " ", continuation


def build_prefix_and_continuation(subset: str, context: str, candidate_text: str) -> tuple[str, str]:
    if subset == "intersentence":
        prefix = context.rstrip() + " "
        return _ensure_boundary_space(prefix, candidate_text)

    if subset == "intrasentence":
        marker = "BLANK" if "BLANK" in context else "____" if "____" in context else None
        if marker is None:
            raise ValueError("Intrasentence context does not include BLANK or ____ marker.")
        left, right = context.split(marker, 1)
        prefix = left
        continuation = candidate_text + right
        return _ensure_boundary_space(prefix, continuation)

    raise ValueError(f"Unsupported subset: {subset}")


@dataclass
class CausalLMScorer:
    model_id: str
    dtype: str = "bf16"
    device_map: str = "auto"
    score_mode: str = "mean_logprob"
    cache_dir: str | None = None

    def __post_init__(self) -> None:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        if self.score_mode != "mean_logprob":
            raise ValueError("Only score_mode='mean_logprob' is supported in v0.1.")

        self._torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, cache_dir=self.cache_dir)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            torch_dtype=_torch_dtype(self.dtype),
            device_map=self.device_map,
            cache_dir=self.cache_dir,
        )
        self.model.eval()

    def score(self, prefix: str, continuation: str) -> float:
        torch = self._torch
        with torch.inference_mode():
            full_text = prefix + continuation
            encoded = self.tokenizer(
                full_text,
                return_tensors="pt",
                add_special_tokens=False,
                return_offsets_mapping=True,
            )

            offset_mapping = encoded.pop("offset_mapping")[0]
            input_ids = encoded["input_ids"]
            if input_ids.shape[1] < 2:
                return float("-inf")

            model_device = next(self.model.parameters()).device
            model_inputs = {k: v.to(model_device) for k, v in encoded.items()}

            logits = self.model(**model_inputs).logits
            logprobs = torch.log_softmax(logits[:, :-1, :], dim=-1)
            next_tokens = input_ids[:, 1:].to(model_device)
            token_logprobs = logprobs.gather(-1, next_tokens.unsqueeze(-1)).squeeze(-1)

            continuation_start_char = len(prefix)
            mask_vals = []
            for token_idx in range(1, len(offset_mapping)):
                start, end = offset_mapping[token_idx].tolist()
                mask_vals.append(start >= continuation_start_char and end > start)

            mask = torch.tensor(mask_vals, dtype=torch.bool, device=model_device)
            if mask.numel() == 0 or not bool(mask.any()):
                return float("-inf")

            continuation_logprobs = token_logprobs[0][mask]
            return float(continuation_logprobs.mean().item())
