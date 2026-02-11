from __future__ import annotations

import random
import subprocess
from datetime import datetime, timezone
from pathlib import Path



def set_seed(seed: int) -> None:
    random.seed(seed)
    try:
        import numpy as np

        np.random.seed(seed)
    except Exception:
        pass
    try:
        import torch

        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except Exception:
        # Torch is optional at runtime for bootstrap actions.
        pass


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def generate_run_id(prefix: str = "run") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{ts}"


def get_git_commit(cwd: Path | None = None) -> str:
    workdir = cwd or Path.cwd()
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=str(workdir), text=True
        ).strip()
        return commit
    except Exception:
        return "unknown"
