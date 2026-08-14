#!/usr/bin/env python3
"""Check Git-tracked task-lifecycle invariants for this repository."""

from __future__ import annotations

import argparse
from datetime import date
import json
import re
from pathlib import Path


IGNORED_NAMES = {".gitkeep"}
WORKPACK_STATUS = re.compile(r"^- Status: (?P<status>[a-z]+)$", re.MULTILINE)
HANDOFF_STATUS = re.compile(r"^- \*\*Status\*\*: `(?P<status>[a-z]+)`", re.MULTILINE)
WORKPACK_FIELD = re.compile(r"^- (?P<name>Owner|Reviewer|Risk tier): (?P<value>.+)$", re.MULTILINE)
RELATED_WORKPACK = re.compile(r"^- \*\*Related workpack\*\*: `(?P<value>[^`]+)`", re.MULTILINE)
ACTIVE_WORKPACK = re.compile(r"\| active workpack \| (?P<value>.*?) \|", re.IGNORECASE)
ADR_NAME = re.compile(r"^(?P<number>\d{4})-[a-z0-9][a-z0-9-]*\.md$")
RISK_TIERS = {"G0", "G1", "G2", "G3"}
BACKLOG_STATES = {"backlog", "blocked"}
STATUS_UPDATED = re.compile(r"^- \*\*更新日期\*\*：(?P<date>\d{4}-\d{2}-\d{2})$", re.MULTILINE)


def tracked_markdown(directory: Path) -> list[Path]:
    return sorted(path for path in directory.glob("*.md") if path.name not in IGNORED_NAMES)


def status_of(path: Path, pattern: re.Pattern[str], kind: str, errors: list[str]) -> str | None:
    match = pattern.search(path.read_text(encoding="utf-8"))
    if match is None:
        errors.append(f"{kind} has no parseable status: {path}")
        return None
    return match.group("status")


def workpack_fields(path: Path) -> dict[str, str]:
    return {match.group("name"): match.group("value").strip() for match in WORKPACK_FIELD.finditer(path.read_text(encoding="utf-8"))}


def check_workpack_directory(
    directory: Path, expected_states: set[str], label: str, errors: list[str]
) -> None:
    """Require immutable workpack directories to agree with their headers."""
    for path in tracked_markdown(directory):
        status = status_of(path, WORKPACK_STATUS, label, errors)
        if status is not None and status not in expected_states:
            allowed = "/".join(sorted(expected_states))
            errors.append(
                f"{label} must have Status: {allowed}: {path.name} has {status}"
            )


def inventory(repo_root: Path) -> dict[str, object]:
    """Return a compact, machine-readable navigation summary without history reads."""
    status_text = (repo_root / "docs" / "workflow" / "status.md").read_text(encoding="utf-8")
    active_match = ACTIVE_WORKPACK.search(status_text)
    updated_match = STATUS_UPDATED.search(status_text)
    return {
        "schema_version": 1,
        "status_updated": updated_match.group("date") if updated_match else None,
        "active_workpack": active_match.group("value") if active_match else None,
        "counts": {
            "workpacks_active": len(tracked_markdown(repo_root / "docs" / "workpacks" / "active")),
            "workpacks_backlog": len(tracked_markdown(repo_root / "docs" / "workpacks" / "backlog")),
            "workpacks_done": len(tracked_markdown(repo_root / "docs" / "workpacks" / "done")),
            "handoffs_active": len(tracked_markdown(repo_root / "docs" / "handoff" / "active")),
            "handoffs_archive": len(tracked_markdown(repo_root / "docs" / "handoff" / "archive")),
        },
        "navigation": {
            "current_state": "docs/workflow/status.md",
            "current_task": "docs/workpacks/active/",
            "current_handoff": "docs/handoff/active/",
            "history": "docs/workflow/milestone-history.md",
            "archive_policy": "docs/workflow/navigation.md",
        },
    }


def audit(repo_root: Path) -> list[str]:
    errors: list[str] = []
    workpacks = tracked_markdown(repo_root / "docs" / "workpacks" / "active")
    handoffs = tracked_markdown(repo_root / "docs" / "handoff" / "active")
    status_path = repo_root / "docs" / "workflow" / "status.md"

    if len(workpacks) > 1:
        errors.append(f"expected at most one active workpack, found {len(workpacks)}")
    for path in workpacks:
        if status_of(path, WORKPACK_STATUS, "active workpack", errors) != "active":
            errors.append(f"workpack in active/ must have Status: active: {path.name}")
        fields = workpack_fields(path)
        owner = fields.get("Owner", "")
        tier = fields.get("Risk tier", "")
        if not owner or owner.lower() == "unassigned":
            errors.append(f"active workpack must name an owner: {path.name}")
        if tier not in RISK_TIERS:
            errors.append(f"active workpack must declare Risk tier G0-G3: {path.name}")
        if tier in {"G2", "G3"}:
            reviewer = fields.get("Reviewer", "")
            if not reviewer or reviewer.lower() == "unassigned":
                errors.append(f"{tier} workpack must name an independent reviewer: {path.name}")
            elif reviewer.lower() == owner.lower():
                errors.append(f"{tier} reviewer must differ from owner: {path.name}")

    if len(handoffs) > 3:
        errors.append(f"expected at most three active handoffs, found {len(handoffs)}")
    for path in handoffs:
        if status_of(path, HANDOFF_STATUS, "active handoff", errors) != "active":
            errors.append(f"handoff in active/ must have Status: active: {path.name}")
        related = RELATED_WORKPACK.search(path.read_text(encoding="utf-8"))
        if related is None:
            errors.append(f"active handoff must name its related workpack: {path.name}")
        elif not any(workpack.stem == related.group("value") for workpack in workpacks):
            errors.append(f"active handoff related workpack is not active: {path.name}")

    if workpacks and not handoffs:
        errors.append("an active workpack requires an active handoff")

    check_workpack_directory(
        repo_root / "docs" / "workpacks" / "done", {"done"}, "done workpack", errors
    )
    check_workpack_directory(
        repo_root / "docs" / "workpacks" / "backlog",
        BACKLOG_STATES,
        "backlog workpack",
        errors,
    )

    status_text = status_path.read_text(encoding="utf-8")
    updated = STATUS_UPDATED.search(status_text)
    if updated is None:
        errors.append("status.md has no parseable 更新日期 (YYYY-MM-DD)")
    else:
        try:
            date.fromisoformat(updated.group("date"))
        except ValueError:
            errors.append("status.md 更新日期 is not a valid calendar date")
    match = ACTIVE_WORKPACK.search(status_text)
    if match is None:
        errors.append("status.md has no parseable active workpack row")
    else:
        declared = match.group("value")
        declares_none = "无" in declared.lower() or "none" in declared.lower()
        if workpacks and (declares_none or workpacks[0].stem not in declared):
            errors.append("status.md active workpack row does not name the active workpack")
        if not workpacks and not declares_none:
            errors.append("status.md declares an active workpack but active/ is empty")

    adr_paths = tracked_markdown(repo_root / "docs" / "architecture" / "adr")
    numbers: list[int] = []
    for path in adr_paths:
        match = ADR_NAME.match(path.name)
        if match is None:
            errors.append(f"ADR filename is not numbered kebab-case: {path.name}")
        else:
            numbers.append(int(match.group("number")))
    if numbers and numbers != list(range(1, max(numbers) + 1)):
        errors.append("ADR numbers must be contiguous from 0001")

    history = repo_root / "docs" / "workflow" / "milestone-history.md"
    ledger = repo_root / "docs" / "workflow" / "evidence-ledger.json"
    if not history.is_file() or not ledger.is_file():
        errors.append("workflow history and evidence ledger must exist")
        return errors
    if "milestone-history.md" not in status_text or "evidence-ledger.json" not in status_text:
        errors.append("status.md must link milestone history and evidence ledger")
    try:
        records = json.loads(ledger.read_text(encoding="utf-8")).get("records", [])
    except json.JSONDecodeError as exc:
        errors.append(f"evidence ledger is not valid JSON: {exc.msg}")
        return errors
    ids: set[str] = set()
    for record in records:
        decision_id = record.get("decision_id")
        if not isinstance(decision_id, str) or decision_id in ids:
            errors.append("evidence ledger decision_id values must be unique strings")
            continue
        ids.add(decision_id)
        if record.get("status") not in {"deferred", "backlog"} or not record.get("reentry_condition"):
            errors.append(f"evidence ledger record is incomplete: {decision_id}")
        for relative_path in record.get("evidence_paths", []):
            if not isinstance(relative_path, str) or not (repo_root / relative_path).is_file():
                errors.append(f"evidence ledger path is missing: {relative_path}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--inventory",
        action="store_true",
        help="print compact current-state navigation metadata as JSON",
    )
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    errors = audit(repo_root)
    if errors:
        print("Governance audit failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    if args.inventory:
        print(json.dumps(inventory(repo_root), ensure_ascii=False, indent=2))
    else:
        print("Governance audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
