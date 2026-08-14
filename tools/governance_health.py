#!/usr/bin/env python3
"""Produce a read-only governance-health snapshot for Brep2Code."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from tools.check_governance import IGNORED_NAMES, audit
except ModuleNotFoundError:  # Direct execution puts tools/, not the repo root, on sys.path.
    from check_governance import IGNORED_NAMES, audit


def markdown_count(directory: Path) -> int:
    return sum(1 for path in directory.glob("*.md") if path.name not in IGNORED_NAMES)


def collect(repo_root: Path) -> dict[str, object]:
    ledger_path = repo_root / "docs" / "workflow" / "evidence-ledger.json"
    records = json.loads(ledger_path.read_text(encoding="utf-8")).get("records", [])
    dispositions: dict[str, int] = {}
    for record in records:
        status = record.get("status", "invalid")
        dispositions[status] = dispositions.get(status, 0) + 1
    errors = audit(repo_root)
    return {
        "schema_version": 1,
        "workpacks": {
            "active": markdown_count(repo_root / "docs" / "workpacks" / "active"),
            "backlog": markdown_count(repo_root / "docs" / "workpacks" / "backlog"),
            "done": markdown_count(repo_root / "docs" / "workpacks" / "done"),
        },
        "active_handoffs": markdown_count(repo_root / "docs" / "handoff" / "active"),
        "evidence_ledger": dispositions,
        "governance_audit": {"passed": not errors, "errors": errors},
    }


def render_markdown(snapshot: dict[str, object]) -> str:
    workpacks = snapshot["workpacks"]
    ledger = snapshot["evidence_ledger"]
    audit_result = snapshot["governance_audit"]
    assert isinstance(workpacks, dict)
    assert isinstance(ledger, dict)
    assert isinstance(audit_result, dict)
    result = "passed" if audit_result["passed"] else "failed"
    ledger_summary = ", ".join(f"{key}: {value}" for key, value in sorted(ledger.items())) or "none"
    return "\n".join(
        [
            "# Governance Health Snapshot",
            "",
            f"- Workpacks: active {workpacks['active']}, backlog {workpacks['backlog']}, done {workpacks['done']}",
            f"- Active handoffs: {snapshot['active_handoffs']}",
            f"- Evidence ledger: {ledger_summary}",
            f"- Governance audit: {result}",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args()
    snapshot = collect(args.repo_root.resolve())
    if args.format == "json":
        print(json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_markdown(snapshot))
    return 0 if snapshot["governance_audit"]["passed"] else 1  # type: ignore[index]


if __name__ == "__main__":
    raise SystemExit(main())
