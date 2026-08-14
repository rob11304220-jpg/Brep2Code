"""Select the preregistered independent default-Line3D regression population."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path("data/datasets/fusion360_gallery/r1.0.1/extracted/r1.0.1")
ASSETS = ROOT / "reconstruction"
OUTPUT = Path("docs/corpus/external/fusion360-gallery-r1.0.1-m17-008-selection.json")
EXCLUDED_FAMILIES = {
    "100243_9fb796fe", "100877_ac1e5a17", "110043_b73b8beb", "145540_a4f54d5f",
    "21646_a2dd0d00", "41026_295d1dc8", "141323_f85efdd4", "136900_4fe212e6",
    "143017_21d96cc2",
}
WINDOWS = {"development": ("train", 401, 600, 2), "held_out": ("test", 201, 400, 1)}


def _family(case_id: str) -> str:
    return "_".join(case_id.split("_")[:2])


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _is_subset(payload: dict) -> bool:
    entities, timeline = payload.get("entities", {}), payload.get("timeline", [])
    ordered = [entities.get(item.get("entity")) for item in timeline]
    if len(ordered) != 2 or any(not entry for entry in ordered):
        return False
    sketch, extrude = ordered
    extent = extrude.get("extent_one", {})
    if sketch.get("type") != "Sketch" or extrude.get("type") != "ExtrudeFeature":
        return False
    if extrude.get("operation") != "NewBodyFeatureOperation" or extrude.get("extent_type") != "OneSideFeatureExtentType":
        return False
    if extrude.get("start_extent", {}).get("type") != "ProfilePlaneStartDefinition":
        return False
    if extent.get("type") != "DistanceExtentDefinition" or extent.get("taper_angle", {}).get("value") != 0.0:
        return False
    profiles = sketch.get("profiles", {})
    if not sketch.get("transform") or len(profiles) != 1:
        return False
    loops = next(iter(profiles.values())).get("loops", [])
    if len(loops) != 1 or not loops[0].get("is_outer", False):
        return False
    curves = loops[0].get("profile_curves", [])
    return bool(curves) and {curve.get("type") for curve in curves} == {"Line3D"}


def _select(index: dict, role: str, used: set[str]) -> list[dict]:
    split, start, end, count = WINDOWS[role]
    rows = []
    for position in range(start, end + 1):
        case_id = index[split][position - 1]
        family = _family(case_id)
        if family in EXCLUDED_FAMILIES or family in used:
            continue
        json_path, step_path = ASSETS / f"{case_id}.json", ASSETS / f"{case_id}.step"
        if not json_path.exists() or not step_path.exists():
            continue
        if not _is_subset(json.loads(json_path.read_text(encoding="utf-8"))):
            continue
        rows.append({"case_id": case_id, "split": role, "official_split": split, "source_order": position, "source_family": family, "json_path": json_path.as_posix(), "step_path": step_path.as_posix(), "input_step_sha256": _sha256(step_path)})
        used.add(family)
        if len(rows) == count:
            return rows
    raise RuntimeError(f"missing_required_{role}_slot_within_{split}_{start}_{end}")


def main() -> int:
    report = {"schema_version": 1, "selection_id": "fusion360-gallery-r1.0.1-m17-008", "workpack": "WP-M17-008", "selection_status": "completed", "policy": "Default M17-007 replay; train 401--600 selects two development Line3D cases and test 201--400 selects one held-out case, with family isolation and no selector prefilter.", "excluded_source_families": sorted(EXCLUDED_FAMILIES)}
    try:
        index = json.loads((ROOT / "train_test.json").read_text(encoding="utf-8"))
        used = set(EXCLUDED_FAMILIES)
        report["samples"] = _select(index, "development", used) + _select(index, "held_out", used)
    except Exception as error:
        report.update({"selection_status": "stopped", "error": str(error), "samples": []})
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT)
    return 0 if report["selection_status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
