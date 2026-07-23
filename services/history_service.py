import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional 
from core.folders_init import FOLDER_HISTORY

def _get_log_path() -> Path:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return FOLDER_HISTORY / f"graphmaker_{today}.jsonl"

def _write_entry(entry: dict) -> None:
    path = _get_log_path()
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def _base_entry(level: str, module: str, func: str, msg: str) -> dict:
    return {
        "ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "level": level,
        "module": module,
        "func": func,
        "msg": msg,
    }

def log_info(module: str, func: str, msg: str, **data: Any) -> None:
    entry = _base_entry("INFO", module, func, msg)
    if data:
        entry["data"] = data
    _write_entry(entry)

def log_warning(module: str, func: str, msg: str, **data: Any) -> None:
    entry = _base_entry("WARNING", module, func, msg)
    if data:
        entry["data"] = data
    _write_entry(entry)

def log_error(module: str, func: str, msg: str, error: Exception | None = None, **data: Any) -> None:
    entry = _base_entry("ERROR", module, func, msg)
    if data:
        entry["data"] = data
    entry["error"] = f"{type(error).__name__}: {error}" if error else None
    _write_entry(entry)

def log_debug(module: str, func: str, msg: str, **data: Any) -> None:
    entry = _base_entry("DEBUG", module, func, msg)
    if data:
        entry["data"] = data
    _write_entry(entry)

#def cleanup_old_logs(days: int = 90) -> None:
#    cutoff = datetime.now(timezone.utc).timestamp() - (days * 86400)
#    for f in HISTORY_DIR.glob("graphmaker_*.jsonl"):
#        if f.stat().st_mtime < cutoff:
#            f.unlink()