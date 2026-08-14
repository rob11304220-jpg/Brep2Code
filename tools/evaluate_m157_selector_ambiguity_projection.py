"""Run M157's fixed local guidance-card ablation without case-asset access."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from brep2code.agent.guidance import GuidanceBundle, GuidanceCardBridge, TOOL_NAME


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "runtime_resources/experience-cards/index.json"
SELECTOR_CARD = ROOT / "runtime_resources/experience-cards/cards/selector-cardinality-stop.json"
WRONG_CARD = ROOT / "runtime_resources/experience-cards/cards/vertical-cylinder-construction.json"
SOURCE_RECORD = ROOT / "docs/corpus/knowledge/admissions/selector-ambiguity-v1.json"
ROLE = "selector cardinality stop"


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def evaluate() -> dict[str, Any]:
    """Compare no card, a wrong explicit card, and the selected explicit card."""

    no_reference = GuidanceCardBridge("m157-no-reference").call(TOOL_NAME, {"role": ROLE})
    wrong_reference = GuidanceCardBridge(
        "m157-wrong-reference",
        GuidanceBundle.from_paths(INDEX, WRONG_CARD, roles=("final primitive",)),
    ).call(TOOL_NAME, {"role": "final primitive"})
    explicit_reference = GuidanceCardBridge(
        "m157-explicit-reference",
        GuidanceBundle.from_paths(INDEX, SELECTOR_CARD, roles=(ROLE,)),
    ).call(TOOL_NAME, {"role": ROLE})

    if no_reference.error != {
        "code": "guidance_not_enabled",
        "message": "no guidance bundle selected for this revision",
    }:
        raise ValueError("no-reference arm drift")
    if not wrong_reference.ok or wrong_reference.result["id"] != "vertical-cylinder-construction":
        raise ValueError("wrong-reference arm drift")
    if not explicit_reference.ok or explicit_reference.result["id"] != "selector-cardinality-stop":
        raise ValueError("explicit-reference arm drift")

    return {
        "projection_id": "selector-cardinality-stop-v1",
        "case_scope": [
            "param_face_selected_cut_centered_nominal",
            "param_selector_ambiguity_twin_centered_nominal",
        ],
        "held_out_access": "not_performed",
        "provider_requests": 0,
        "ablation_budget": 3,
        "arms": {
            "no_reference": {"ok": no_reference.ok, "error_code": no_reference.error["code"]},
            "wrong_reference": {"ok": wrong_reference.ok, "returned_card_id": wrong_reference.result["id"]},
            "explicit_reference": {"ok": explicit_reference.ok, "returned_card_id": explicit_reference.result["id"]},
        },
        "source_record_sha256": _sha256(SOURCE_RECORD),
        "projection_card_sha256": _sha256(SELECTOR_CARD),
        "index_sha256": _sha256(INDEX),
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), sort_keys=True))
