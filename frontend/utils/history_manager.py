import json
import os
from datetime import datetime

HISTORY_FILE = "data/history.json"


def _load_history() -> list:
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def _save_history(history: list):
    os.makedirs("data", exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def save_analysis(filename: str, analysis: str):
    history = _load_history()
    history.append({
        "id": len(history) + 1,
        "filename": filename,
        "analysis": analysis,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    _save_history(history)


def get_all_history() -> list:
    return _load_history()


def clear_history():
    _save_history([])
