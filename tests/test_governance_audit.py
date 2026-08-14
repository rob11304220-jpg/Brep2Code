from __future__ import annotations

import re
import shutil
from pathlib import Path

from tools.check_governance import audit
from tools.governance_health import collect, render_markdown


REPO_ROOT = Path(__file__).resolve().parents[1]


def copy_governance_tree(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    for relative in ("docs/workpacks/active", "docs/handoff/active", "docs/workflow", "docs/architecture/adr"):
        source = REPO_ROOT / relative
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target)
    return root


def test_current_repository_governance_passes() -> None:
    assert audit(REPO_ROOT) == []


def test_completed_handoff_cannot_remain_active(tmp_path: Path) -> None:
    root = copy_governance_tree(tmp_path)
    handoff = root / "docs/handoff/active/stale.md"
    handoff.write_text("- **Status**: `done`\n", encoding="utf-8")

    assert any("handoff in active/ must have Status: active" in error for error in audit(root))


def test_status_must_name_the_active_workpack(tmp_path: Path) -> None:
    root = copy_governance_tree(tmp_path)
    for existing in (root / "docs/workpacks/active").glob("*.md"):
        existing.unlink()
    workpack = root / "docs/workpacks/active/WP-M99-001-example.md"
    workpack.write_text(
        "# Example\n\n- Status: active\n- Owner: agent-a\n- Risk tier: G1\n",
        encoding="utf-8",
    )

    assert any("does not name the active workpack" in error for error in audit(root))


def test_active_workpack_requires_owner_risk_tier_and_handoff(tmp_path: Path) -> None:
    root = copy_governance_tree(tmp_path)
    for existing in (root / "docs/handoff/active").glob("*.md"):
        existing.unlink()
    workpack = root / "docs/workpacks/active/WP-M99-001-example.md"
    workpack.write_text("# Example\n\n- Status: active\n", encoding="utf-8")
    status = root / "docs/workflow/status.md"
    status.write_text(
        re.sub(
            r"(\| active workpack \| ).*?( \|)",
            r"\1`WP-M99-001-example`; fixture active workpack\2",
            status.read_text(encoding="utf-8"),
        ),
        encoding="utf-8",
    )

    errors = audit(root)

    assert any("must name an owner" in error for error in errors)
    assert any("must declare Risk tier" in error for error in errors)
    assert any("requires an active handoff" in error for error in errors)


def test_g2_workpack_requires_independent_reviewer(tmp_path: Path) -> None:
    root = copy_governance_tree(tmp_path)
    workpack = root / "docs/workpacks/active/WP-M99-001-example.md"
    workpack.write_text(
        "# Example\n\n- Status: active\n- Owner: agent-a\n- Reviewer: agent-a\n- Risk tier: G2\n",
        encoding="utf-8",
    )
    handoff = root / "docs/handoff/active/example.md"
    handoff.write_text(
        "- **Status**: `active`\n- **Related workpack**: `WP-M99-001-example`\n",
        encoding="utf-8",
    )
    status = root / "docs/workflow/status.md"
    status.write_text(status.read_text(encoding="utf-8").replace("无；M37", "WP-M99-001-example；M37"), encoding="utf-8")

    assert any("reviewer must differ" in error for error in audit(root))


def test_evidence_ledger_requires_existing_paths(tmp_path: Path) -> None:
    root = copy_governance_tree(tmp_path)
    ledger = root / "docs/workflow/evidence-ledger.json"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_text('{"records":[{"decision_id":"x","status":"deferred","reentry_condition":"x","evidence_paths":["missing.md"]}]}', encoding="utf-8")
    (root / "docs/workflow/milestone-history.md").write_text("# history\n", encoding="utf-8")
    status = root / "docs/workflow/status.md"
    status.write_text(status.read_text(encoding="utf-8") + "\n[milestone](milestone-history.md) [ledger](evidence-ledger.json)\n", encoding="utf-8")
    assert any("evidence ledger path is missing" in error for error in audit(root))


def test_governance_health_reports_current_offline_snapshot() -> None:
    snapshot = collect(REPO_ROOT)

    active_workpacks = list((REPO_ROOT / "docs/workpacks/active").glob("*.md"))
    assert snapshot["workpacks"]["active"] == len(active_workpacks)
    assert snapshot["governance_audit"]["passed"] is True
    assert "Governance Health Snapshot" in render_markdown(snapshot)
