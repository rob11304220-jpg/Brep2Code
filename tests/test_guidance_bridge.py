import json
from pathlib import Path

from brep2code.agent.guidance import GuidanceBundle, GuidanceCardBridge, TOOL_NAME
from brep2code.agent.harness import ManualHarness
from brep2code.storage import RecordStore


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "runtime_resources/experience-cards/index.json"
CARD = ROOT / "runtime_resources/experience-cards/cards/vertical-cylinder-construction.json"


def test_guidance_bridge_is_opt_in_and_traceable(tmp_path: Path) -> None:
    disabled = GuidanceCardBridge("rev-1")
    assert disabled.specs() == []
    assert disabled.call(TOOL_NAME, {"role": "final primitive"}).error["code"] == "guidance_not_enabled"
    bridge = GuidanceCardBridge("rev-1", GuidanceBundle.from_paths(INDEX, CARD))
    result = bridge.call(TOOL_NAME, {"role": "final primitive"}, trace_dir=tmp_path)
    assert result.ok and result.result["id"] == "vertical-cylinder-construction"
    trace = (tmp_path / "guidance_calls.jsonl").read_text(encoding="utf-8")
    assert "vertical-cylinder-construction" in trace and "revision_id" in trace
    assert '"selected_role": "final primitive"' in trace


def test_guidance_bridge_fails_closed_on_hash_drift(tmp_path: Path) -> None:
    index = tmp_path / "index.json"
    card = tmp_path / "card.json"
    index.write_bytes(INDEX.read_bytes())
    card.write_bytes(CARD.read_bytes())
    bundle = GuidanceBundle.from_paths(index, card)
    card.write_text("{}", encoding="utf-8")
    result = GuidanceCardBridge("rev-1", bundle).call(TOOL_NAME, {"role": "final primitive"})
    assert result.error["code"] == "guidance_index_invalid"


def test_guidance_bridge_rejects_unavailable_or_undeclared_card(tmp_path: Path) -> None:
    unavailable = GuidanceBundle(tmp_path / "missing-index.json", CARD, "x", "y")
    assert GuidanceCardBridge("rev-1", unavailable).call(TOOL_NAME, {"role": "final primitive"}).error["code"] == "guidance_unavailable"
    index = tmp_path / "index.json"
    card = tmp_path / "card.json"
    index.write_text('{"schema_version":1,"status":"experimental","cards":[]}', encoding="utf-8")
    card.write_bytes(CARD.read_bytes())
    result = GuidanceCardBridge("rev-1", GuidanceBundle.from_paths(index, card)).call(TOOL_NAME, {"role": "final primitive"})
    assert result.error["code"] == "guidance_index_invalid"


def test_guidance_bridge_uses_one_explicitly_selected_card_and_bundle_roles(tmp_path: Path) -> None:
    index = tmp_path / "index.json"
    card = tmp_path / "selector-cardinality-stop.json"
    payload = json.loads(CARD.read_text(encoding="utf-8"))
    payload["id"] = "selector-cardinality-stop"
    card.write_text(json.dumps(payload), encoding="utf-8")
    index.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "status": "experimental",
                "cards": ["cards/vertical-cylinder-construction.json", "cards/selector-cardinality-stop.json"],
            }
        ),
        encoding="utf-8",
    )

    bundle = GuidanceBundle.from_paths(index, card, roles=("selector cardinality stop",))
    bridge = GuidanceCardBridge("rev-1", bundle)

    assert bridge.specs()[0].schema["properties"]["role"]["enum"] == ["selector cardinality stop"]
    result = bridge.call(TOOL_NAME, {"role": "selector cardinality stop"})
    assert result.ok and result.result["id"] == "selector-cardinality-stop"
    assert bridge.call(TOOL_NAME, {"role": "final primitive"}).error["code"] == "invalid_arguments"


def test_guidance_bundle_rejects_empty_or_duplicate_roles() -> None:
    try:
        GuidanceBundle.from_paths(INDEX, CARD, roles=())
    except ValueError as error:
        assert "non-empty and unique" in str(error)
    else:  # pragma: no cover - keeps the failure message specific.
        raise AssertionError("empty roles must fail")

    try:
        GuidanceBundle.from_paths(INDEX, CARD, roles=("final primitive", "final primitive"))
    except ValueError as error:
        assert "non-empty and unique" in str(error)
    else:  # pragma: no cover - keeps the failure message specific.
        raise AssertionError("duplicate roles must fail")


def test_guidance_response_preserves_sources_and_top_k_one() -> None:
    result = GuidanceCardBridge("rev-1", GuidanceBundle.from_paths(INDEX, CARD)).call(
        TOOL_NAME, {"role": "repeated boolean-cut tool"}
    )
    assert result.ok
    assert result.result["sources"] == [
        "docs/corpus/reference-packs/m84-cylinder-construction-qualification-v1.json",
        "docs/corpus/reference-packs/reference-pack-contract-v1.json",
    ]
    assert set(result.result) == {"id", "scope", "claim", "runtime_action", "validation", "sources"}


def test_manual_harness_records_explicit_revision_guidance(tmp_path: Path) -> None:
    store = RecordStore(tmp_path / "records")
    result = ManualHarness(store=store).run(
        "guidance-revision",
        guidance_bundle=GuidanceBundle.from_paths(INDEX, CARD),
        guidance_calls=[{"tool": TOOL_NAME, "arguments": {"role": "final primitive"}}],
    )
    assert result.signal_bundle["guidance"]["returned_card_ids"] == ["vertical-cylinder-construction"]
    assert (result.revision.traces / "guidance_calls.jsonl").is_file()


def test_manual_harness_no_card_baseline_is_unchanged(tmp_path: Path) -> None:
    result = ManualHarness(store=RecordStore(tmp_path / "records")).run("no-guidance")
    assert result.signal_bundle["guidance"] is None
    assert not (result.revision.traces / "guidance_calls.jsonl").exists()
