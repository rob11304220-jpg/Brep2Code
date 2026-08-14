"""Compact corpus report serialization."""

from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4


def write_corpus_report(path: Path | str, payload: dict) -> Path:
    report_path = Path(path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = report_path.with_name(f".{report_path.name}.{uuid4().hex}.tmp")
    try:
        temporary_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        temporary_path.replace(report_path)
    finally:
        temporary_path.unlink(missing_ok=True)
    return report_path
