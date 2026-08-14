"""Filesystem layout management for records and revisions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import re


_RECORD_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")


@dataclass(frozen=True)
class RecordPaths:
    record_id: str
    root: Path
    input_dir: Path
    revisions_dir: Path
    manifest: Path


@dataclass(frozen=True)
class RevisionPaths:
    revision_id: str
    root: Path
    workspace: Path
    intermediates: Path
    output: Path
    traces: Path
    signal_bundle: Path
    execution_summary: Path


class RecordStore:
    """Creates and resolves the M0 record/revision directory structure."""

    def __init__(self, data_root: Path | str = "data") -> None:
        self.data_root = Path(data_root)
        self.records_root = self.data_root / "records"

    def ensure_record(self, record_id: str) -> RecordPaths:
        self._validate_record_id(record_id)
        root = self.records_root / record_id
        input_dir = root / "input"
        revisions_dir = root / "revisions"
        input_dir.mkdir(parents=True, exist_ok=True)
        revisions_dir.mkdir(parents=True, exist_ok=True)

        manifest = root / "record.json"
        now = _utc_now()
        if manifest.exists():
            record = json.loads(manifest.read_text(encoding="utf-8"))
            record["updated_at"] = now
        else:
            record = {
                "record_id": record_id,
                "created_at": now,
                "updated_at": now,
                "schema_version": 1,
            }
        _write_json(manifest, record)
        return RecordPaths(record_id, root, input_dir, revisions_dir, manifest)

    def create_revision(self, record: RecordPaths) -> RevisionPaths:
        revision_id = _revision_id()
        root = record.revisions_dir / revision_id
        counter = 1
        while root.exists():
            counter += 1
            revision_id = f"{_revision_id()}-{counter}"
            root = record.revisions_dir / revision_id

        workspace = root / "workspace"
        intermediates = workspace / "intermediates"
        output = workspace / "output"
        traces = root / "traces"
        for path in (intermediates, output, traces):
            path.mkdir(parents=True, exist_ok=True)

        return RevisionPaths(
            revision_id=revision_id,
            root=root,
            workspace=workspace,
            intermediates=intermediates,
            output=output,
            traces=traces,
            signal_bundle=root / "signal_bundle.json",
            execution_summary=root / "execution.json",
        )

    @staticmethod
    def _validate_record_id(record_id: str) -> None:
        if not _RECORD_ID_RE.match(record_id):
            raise ValueError(
                "record id must start with an ASCII letter or digit and contain only "
                "letters, digits, '.', '_' or '-'"
            )


def write_json(path: Path, payload: object) -> None:
    _write_json(path, payload)


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _revision_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
