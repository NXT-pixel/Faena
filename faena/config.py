"""
Configuration management for Faena.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


def load_env_file(filepath: Optional[Path] = None):
    """Simple .env file loader that sets os.environ if not already set."""
    env_path = filepath or Path.cwd() / ".env"
    if not env_path.exists() or not env_path.is_file():
        return

    try:
        with open(env_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("\"'")
                if k not in os.environ:
                    os.environ[k] = v
    except Exception:
        pass


def load_config_file(filepath: Optional[Path] = None) -> Dict[str, Any]:
    """Loads faena.config.json if it exists."""
    config_path = filepath or Path.cwd() / "faena.config.json"
    if not config_path.exists() or not config_path.is_file():
        return {}

    try:
        with open(config_path, "r", encoding="utf-8", errors="replace") as f:
            return json.load(f)
    except Exception:
        return {}
