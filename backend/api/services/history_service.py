import json
import os
from typing import Optional
from datetime import datetime
from config.settings import HISTORY_FILE, DATA_DIR


def _load() -> list:
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def _save(records: list):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)


def save_record(filename: str, analysis: dict) -> int:
    records = _load()
    record_id = len(records) + 1
    records.append({
        "id": record_id,
        "filename": filename,
        "analysis": analysis,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    _save(records)
    return record_id


def get_all() -> list:
    return _load()


def get_by_id(record_id: int) -> Optional[dict]:
    records = _load()
    for r in records:
        if r["id"] == record_id:
            return r
    return None


def delete_all():
    _save([])


def delete_by_id(record_id: int) -> bool:
    records = _load()
    new_records = [r for r in records if r["id"] != record_id]
    if len(new_records) == len(records):
        return False
    _save(new_records)
    return True
