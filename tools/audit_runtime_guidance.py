"""Offline schema and evidence-boundary audit for experimental experience cards."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDANCE_ROOT = ROOT / "runtime_resources" / "experience-cards"
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
KINDS = {"operation", "diagnosis", "counterexample"}
STATUSES = {"experimental", "supported", "deprecated"}
EVIDENCE_LEVELS = {"direct", "supported", "unknown"}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def audit_card(card_path: Path, seen_ids: set[str]) -> None:
    card = load_json(card_path)
    required = {
        "schema_version", "id", "kind", "status", "scope", "claim", "evidence",
        "runtime_action", "validation", "sources",
    }
    assert required <= card.keys(), card_path
    assert card["schema_version"] == 1, card_path
    assert isinstance(card["id"], str) and ID_PATTERN.fullmatch(card["id"]), card_path
    assert card["id"] not in seen_ids, card["id"]
    seen_ids.add(card["id"])
    assert card["kind"] in KINDS, card_path
    assert card["status"] in STATUSES, card_path
    assert card["evidence"]["level"] in EVIDENCE_LEVELS, card_path
    assert isinstance(card["scope"]["applies_when"], list) and card["scope"]["applies_when"], card_path
    assert isinstance(card["claim"], str) and card["claim"], card_path
    assert isinstance(card["runtime_action"], str) and card["runtime_action"], card_path
    assert isinstance(card["validation"]["review_trigger"], str) and card["validation"]["review_trigger"], card_path
    assert isinstance(card["sources"], list) and card["sources"], card_path
    for source in card["sources"]:
        assert (ROOT / source).is_file(), source
    assert isinstance(card["evidence"]["supporting_cases"], list), card_path
    assert isinstance(card["evidence"]["counterexamples"], list), card_path
    if card["status"] == "supported":
        assert card["evidence"]["level"] != "unknown", card_path


def main() -> None:
    index = load_json(GUIDANCE_ROOT / "index.json")
    assert index == {"schema_version": 1, "status": "experimental", "cards": index["cards"]}
    assert index["cards"]
    seen_ids: set[str] = set()
    for relative_card in index["cards"]:
        assert isinstance(relative_card, str) and relative_card.startswith("cards/")
        card_path = GUIDANCE_ROOT / relative_card
        assert card_path.is_file(), card_path
        audit_card(card_path, seen_ids)
    print(f"runtime-guidance audit passed: {len(seen_ids)} cards")


if __name__ == "__main__":
    main()
