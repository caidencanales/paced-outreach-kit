"""Load config.json (falls back to config.example.json) and resolve paths on any OS."""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _merge(base, over):
    out = dict(base)
    for k, v in over.items():
        out[k] = _merge(base[k], v) if isinstance(v, dict) and isinstance(base.get(k), dict) else v
    return out


def load(root=None):
    root = Path(root or os.environ.get("OUTREACH_HOME") or ROOT)
    cfg = json.loads((ROOT / "config.example.json").read_text(encoding="utf-8"))
    user = root / "config.json"
    if user.exists():
        cfg = _merge(cfg, json.loads(user.read_text(encoding="utf-8")))
    data = Path(cfg["data_dir"])
    cfg["_root"] = root
    cfg["_data"] = data if data.is_absolute() else root / data
    cfg["_templates"] = root / "templates"
    return cfg
