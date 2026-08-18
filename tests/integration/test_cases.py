from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil

import pytest

from brep2code.cases import (
    CaseValidationError,
    discover_cases,
    load_manifest,
    validate_case,
    validate_catalog,
)
from brep2code.mechanisms import load_mechanism_registry


EXPECTED_CASES = {
    ("eval", "cylinder"),
    ("eval", "box_held_out"),
    ("eval", "cylinder_held_out"),
    ("eval", "through_cut_held_out"),
    ("eval", "blind_cut_held_out"),
    ("eval", "filleted_box_held_out"),
    ("smoke", "box"),
    ("smoke", "block_with_hole"),
    ("train", "blind_hole_block"),
    ("train", "filleted_box"),
}


def test_catalog_and_manifests_validate() -> None:
    root = Path("cases")
    discovered = discover_cases(root)
    manifests = validate_catalog(root)

    assert {(path.parent.name, path.name) for path in discovered} == EXPECTED_CASES
    assert {
        (manifest.split, item.case.case_id)
        for manifest in manifests
        for item in manifest.cases
    } == EXPECTED_CASES


def test_catalog_binds_cases_to_mechanism_registry_and_dossiers() -> None:
    registry = load_mechanism_registry(Path("cases"))
    manifests = validate_catalog(Path("cases"))

    assert set(registry.definitions) == {"primitive", "analytic_surface", "boolean_cut", "fillet"}
    assert {
        item.metadata["mechanism"]
        for manifest in manifests
        for item in manifest.cases
    } <= set(registry.definitions)
    assert all(
        (item.case.root / "dossier.json").is_file()
        for manifest in manifests
        for item in manifest.cases
    )
    assert all(
        item.dossier["harness_assets"]["development_cohort"]
        == ["nominal", "parameter_variation", "failure_sensitive"]
        for manifest in manifests
        for item in manifest.cases
    )
    assert all(
        [control["variant"] for control in item.dossier["harness_assets"]["controls"]]
        == ["nominal", "parameter_variation", "failure_sensitive"]
        and all(
            (item.case.root / control["asset"]).is_file()
            for control in item.dossier["harness_assets"]["controls"]
        )
        for manifest in manifests
        for item in manifest.cases
    )


def test_catalog_rejects_control_asset_hash_drift(tmp_path: Path) -> None:
    copied_root = tmp_path / "cases"
    shutil.copytree(Path("cases"), copied_root)
    dossier = copied_root / "smoke" / "box" / "dossier.json"
    payload = json.loads(dossier.read_text(encoding="utf-8"))
    payload["harness_assets"]["controls"][0]["sha256"] = "0" * 64
    dossier.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(CaseValidationError, match="control asset sha256 mismatch"):
        validate_catalog(copied_root)


def test_catalog_rejects_held_out_fixture_hash_drift(tmp_path: Path) -> None:
    copied_root = tmp_path / "cases"
    shutil.copytree(Path("cases"), copied_root)
    dossier = copied_root / "eval" / "box_held_out" / "dossier.json"
    payload = json.loads(dossier.read_text(encoding="utf-8"))
    payload["harness_assets"]["held_out_fixture"]["sha256"] = "0" * 64
    dossier.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(CaseValidationError, match="held-out fixture asset sha256 mismatch"):
        validate_catalog(copied_root)


def test_case_rejects_hash_mismatch(tmp_path: Path) -> None:
    root = tmp_path / "cases"
    case_root = root / "smoke" / "box"
    case_root.mkdir(parents=True)
    (case_root / "input.step").write_bytes(b"step")
    (case_root / "case.json").write_text(
        json.dumps(_metadata(sha256="0" * 64)), encoding="utf-8"
    )

    with pytest.raises(CaseValidationError, match="sha256 mismatch"):
        validate_case(case_root, root)


def test_catalog_rejects_dossier_drift(tmp_path: Path) -> None:
    root = tmp_path / "cases"
    shutil.copytree("cases", root)
    dossier = root / "smoke" / "box" / "dossier.json"
    payload = json.loads(dossier.read_text(encoding="utf-8"))
    payload["mechanism_id"] = "boolean_cut"
    dossier.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(CaseValidationError, match="dossier mechanism_id"):
        validate_catalog(root)


def test_catalog_rejects_failure_sensitive_cohort_without_negative_control(tmp_path: Path) -> None:
    root = tmp_path / "cases"
    shutil.copytree("cases", root)
    dossier = root / "smoke" / "box" / "dossier.json"
    payload = json.loads(dossier.read_text(encoding="utf-8"))
    payload["harness_assets"]["negative_control"] = False
    dossier.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(CaseValidationError, match="failure_sensitive development cohort"):
        validate_catalog(root)


def test_case_rejects_path_traversal(tmp_path: Path) -> None:
    root = tmp_path / "cases"
    case_root = root / "smoke" / "box"
    case_root.mkdir(parents=True)
    (case_root / "case.json").write_text(
        json.dumps(_metadata(input_step="../input.step")), encoding="utf-8"
    )

    with pytest.raises(CaseValidationError, match="must be a filename"):
        validate_case(case_root, root)


def test_manifest_rejects_duplicate_case_ids(tmp_path: Path) -> None:
    manifest = tmp_path / "smoke.json"
    manifest.write_text(
        json.dumps({"schema_version": 1, "split": "smoke", "cases": ["box", "box"]}),
        encoding="utf-8",
    )

    with pytest.raises(CaseValidationError, match="duplicate"):
        load_manifest(manifest, tmp_path)


def test_eval_manifest_is_not_runtime_visible(tmp_path: Path) -> None:
    manifest = tmp_path / "eval.json"
    manifest.write_text(
        json.dumps({"schema_version": 1, "split": "eval", "cases": ["held_out"]}),
        encoding="utf-8",
    )

    with pytest.raises(CaseValidationError, match="not visible to the runtime"):
        load_manifest(manifest, tmp_path, runtime=True)


@pytest.mark.parametrize(
    ("relative_path", "expected_hash"),
    [
        ("smoke/box/input.step", "c79a4f205ed7bf698a367832f855c716abfee1c9891848384d0e46ad026db927"),
        (
            "smoke/block_with_hole/input.step",
            "ad0557d72beec842cbe1a5cbb5aef9b7267ea4632bd058106f61a67f2e12624c",
        ),
        (
            "train/blind_hole_block/input.step",
            "aa0c9d023caef2cfb19f1c3f21f4fe130d5b19be7a1554fd82603399c091f656",
        ),
        ("eval/cylinder/input.step", "98f7bbdd9e3f24e3532f4adfe0837f5a0862e6f614bfb998f1520a297d607f4c"),
        ("eval/box_held_out/input.step", "d41f288a26a789eb4beb18094fdcae7282d20592e40d791c0fa62e86fa49195b"),
        ("eval/cylinder_held_out/input.step", "7855afb6e59f82460facff646da83122fc71122dc16cf8e7e0a2d861855a72e0"),
        ("eval/through_cut_held_out/input.step", "0abef779812f5f55b610bb4ad40766a43b671a3b86328dc079bdf55429a1f62f"),
        ("eval/blind_cut_held_out/input.step", "b30007ffc7d0f16fac496a4c5bc2e3ef02d90ada698cea1a8a8cc25c42146e3e"),
        ("train/filleted_box/input.step", "e6d8f0ffd097cd24010165a0bcd030d89e5dce9cc5b43a07cb2eb8401f48fd1e"),
        ("eval/filleted_box_held_out/input.step", "d3d2b9dcf1f9d1ff6aa688dd09a06c0a40df9bb5a5cac6176dab405fe4ee7bd9"),
    ],
)
def test_fixture_hashes(relative_path: str, expected_hash: str) -> None:
    assert hashlib.sha256((Path("cases") / relative_path).read_bytes()).hexdigest() == expected_hash


def _metadata(*, input_step: str = "input.step", sha256: str = "0" * 64) -> dict:
    return {
        "case_id": "box",
        "input_step": input_step,
        "sha256": sha256,
        "unit": "mm",
        "summary": "test case",
        "tags": ["test"],
        "mechanism": "primitive",
        "capability_level": "L0",
        "compatibility_tier": "T0",
        "kernel_properties": ["planar_faces"],
        "sequence": ["primitive"],
        "difficulty": 1,
        "expected": {
            "bbox": {"min": [0, 0, 0], "max": [1, 1, 1]},
            "volume": 1,
            "counts": {"solid": 1, "shell": 1, "face": 6, "edge": 24},
        },
    }
