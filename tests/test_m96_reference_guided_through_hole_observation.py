import json

import pytest

from brep2code.agent.observation import build_observation_context
from brep2code.agent.m97_observation import validate_m97_observation_context
from brep2code.agent.m97_recipe import M97_THROUGH_CUT_RECIPE_VERSION, build_m97_through_cut_recipe
from brep2code.agent import ManualHarness
from brep2code.agent.guidance import GuidanceBundle
from tools.audit_m96_reference_guided_through_hole_observation import EXPANSION, audit, derive_transcript
from tools.audit_sequence_paired_prismatic_hole import load_json
from brep2code.storage import RecordStore


M96_M97_GUIDANCE_INDEX = "docs/corpus/sequence-paired/fixtures/m96-m97-guidance-index-v1.json"

def test_m96_development_transcripts_contain_only_required_measured_facts() -> None:
    rows = audit()
    assert len(rows) == 3
    entry = next(item for item in load_json(EXPANSION)["cases"] if item["data_split"] == "development")
    facts = json.loads(derive_transcript(entry))["observation_transcript"][0]["data"]["cylindrical_cut"]
    assert facts["axis"] == "+Z"
    assert facts["extent"] == "through"
    assert facts["radius"] > 0
    assert facts["center_xy"][1] == 10.0


def test_m96_rejects_held_out_transcript_derivation() -> None:
    entry = next(item for item in load_json(EXPANSION)["cases"] if item["data_split"] == "held_out")
    with pytest.raises(ValueError, match="development rows only"):
        derive_transcript(entry)


def test_observation_context_rejects_reference_source_fields() -> None:
    with pytest.raises(ValueError, match="forbidden"):
        build_observation_context([{"data": {"reference_script": "forbidden"}}])


def test_m96_policy_is_frozen_before_held_out_execution() -> None:
    policy = load_json(EXPANSION.parent / "reference-guided-through-hole-variation-v1-m96-policy.json")
    bundle = GuidanceBundle.from_paths(
        EXPANSION.parents[3] / M96_M97_GUIDANCE_INDEX,
        EXPANSION.parents[3] / "runtime_resources/experience-cards/cards/vertical-cylinder-construction.json",
    )
    assert policy["status"] == "frozen_before_held_out_execution"
    assert policy["reference_condition"]["requests_per_case"] == 2
    assert policy["baseline_condition"]["requests_per_case"] == 1
    assert policy["development_budget"]["maximum_issued_requests"] == 9
    assert policy["held_out_budget"]["maximum_issued_requests"] == 9
    assert policy["reference_condition"]["index_sha256"] == bundle.index_sha256
    assert policy["reference_condition"]["card_sha256"] == bundle.card_sha256


def test_m96_historical_index_fixture_is_not_the_live_default() -> None:
    fixture = EXPANSION.parents[3] / M96_M97_GUIDANCE_INDEX
    live_index = EXPANSION.parents[3] / "runtime_resources/experience-cards/index.json"
    assert fixture.read_bytes() != live_index.read_bytes()
    assert "cards/selector-cardinality-stop.json" not in load_json(fixture)["cards"]
    assert "cards/selector-cardinality-stop.json" in load_json(live_index)["cards"]


def test_m97_003_policy_refreezes_development_only_execution() -> None:
    policy = load_json(EXPANSION.parent / "reference-guided-through-hole-variation-v1-m97-003-policy.json")
    assert policy["status"] == "frozen_before_authorization"
    assert policy["scope"]["data_split"] == "development"
    assert policy["execution"]["maximum_issued_requests"] == 9
    assert policy["execution"]["max_repair_rounds"] == 0
    assert policy["execution"]["retry"] == "forbidden"
    assert policy["observation_contract"]["id"] == "m97-measured-through-hole-facts-v1"


def test_m97_context_rejects_extra_or_missing_measured_facts() -> None:
    entry = next(item for item in load_json(EXPANSION)["cases"] if item["case_id"].endswith("development_low"))
    payload = json.loads(derive_transcript(entry))
    payload["observation_transcript"][0]["data"]["probe_summary"] = {"volume": 1}
    with pytest.raises(ValueError, match="unsupported facts"):
        validate_m97_observation_context(json.dumps(payload))
    payload = json.loads(derive_transcript(entry))
    del payload["observation_transcript"][0]["data"]["cylindrical_cut"]["radius"]
    with pytest.raises(ValueError, match="invalid cylindrical cut"):
        validate_m97_observation_context(json.dumps(payload))


def test_m97_versioned_recipe_uses_low_row_measurements_and_passes_harness(tmp_path) -> None:
    entry = next(item for item in load_json(EXPANSION)["cases"] if item["case_id"].endswith("development_low"))
    context = derive_transcript(entry)
    recipe = build_m97_through_cut_recipe(context)
    assert M97_THROUGH_CUT_RECIPE_VERSION in recipe
    assert "gp_Dir(0, 0, 1)" in recipe
    assert "gp_DZ" not in recipe
    assert "2.0" in recipe and "9.0" in recipe and "10.0" in recipe
    script = tmp_path / "build_sequence.py"
    script.write_text(recipe, encoding="utf-8")
    result = ManualHarness(store=RecordStore(tmp_path / "data")).run(
        "m97-low-recipe", script=script,
        input_path=EXPANSION.parents[3] / entry["candidate_directory"] / "input.step",
        build_without_input=True,
    )
    assert result.status == "pass"
