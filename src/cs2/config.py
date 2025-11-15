"""
User configuration loader for cs2 project.

Order of precedence for values:
 1. repo root file `user_config.json` (if present)
 2. user home file `~/.cs2_user_config.json` (if present)
 3. environment variables (CS2_USER_DATA_DIR, CS2_OUTPUT_FILE)
 4. built-in defaults

This module exposes three constants for use by the scraper:
 - USER_DATA_DIR
 - OUTPUT_FILE

Create `user_config.json` in the repo root or `~/.cs2_user_config.json` in your home
directory to customize these values. An example `user_config.json.example` has
been added to the repo root.
"""
from __future__ import annotations

from pathlib import Path
import json
import os
from typing import Dict

# sensible defaults (can be overridden by files or env vars)
DEFAULTS: Dict[str, str] = {
    "USER_DATA_DIR": str(Path.home() / "chrome"),
    "OUTPUT_FILE": "scraped_data.jsonl",
}


def _repo_root() -> Path:
    # src/cs2/config.py -> repo root is two parents up
    return Path(__file__).resolve().parents[2]


def load_user_config() -> Dict[str, str]:
    """Load configuration from file(s) and environment variables.

    Search order:
      - {repo_root}/user_config.json
      - ~/.cs2_user_config.json
      - environment variables
    """
    cfg = DEFAULTS.copy()

    candidates = [
        _repo_root() / "user_config.json",
        Path.home() / ".cs2_user_config.json",
    ]

    for candidate in candidates:
        if candidate.exists():
            try:
                raw = json.loads(candidate.read_text(encoding="utf-8"))
                for key in ("USER_DATA_DIR", "OUTPUT_FILE"):
                    if key in raw and raw[key]:
                        cfg[key] = raw[key]
                break
            except (json.JSONDecodeError, OSError, ValueError):
                # ignore parse / IO errors and continue to next candidate
                continue

    # environment variables take precedence over file values
    cfg["USER_DATA_DIR"] = os.getenv("CS2_USER_DATA_DIR", cfg["USER_DATA_DIR"]) or cfg["USER_DATA_DIR"]
    cfg["OUTPUT_FILE"] = os.getenv("CS2_OUTPUT_FILE", cfg["OUTPUT_FILE"]) or cfg["OUTPUT_FILE"]

    return cfg


_cfg = load_user_config()

USER_DATA_DIR: str = _cfg["USER_DATA_DIR"]
OUTPUT_FILE: str = _cfg["OUTPUT_FILE"]


__all__ = ["USER_DATA_DIR", "OUTPUT_FILE"]
