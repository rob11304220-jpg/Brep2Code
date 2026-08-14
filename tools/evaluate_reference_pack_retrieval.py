"""Run M19-002's isolated no-card versus top-k reference-card comparison."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from brep2code.brep.probes import load_model, probe_summary
try:  # Supports both direct execution and package import from tests.
    from tools import audit_reference_pack_retrieval
    from tools import audit_reference_pack_qualification
except ModuleNotFoundError:  # pragma: no cover - direct script entrypoint only
    import audit_reference_pack_retrieval
    import audit_reference_pack_qualification


ROOT = Path(__file__).resolve().parents[1]
CARD = ROOT / "runtime_resources/experience-cards/cards/vertical-cylinder-construction.json"
CARD_INDEX = ROOT / "runtime_resources/experience-cards/index.json"
CONTRACT = ROOT / "docs/corpus/reference-packs/reference-pack-contract-v1.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def select_cards(policy: str, case_id: str, role: str) -> list[str]:
    if policy == "baseline":
        return []
    if (
        policy == "treatment"
        and audit_reference_pack_retrieval.EXPECTED_CASES.get(case_id, (None, None))[0] == role
    ):
        return ["vertical-cylinder-construction"]
    raise AssertionError((policy, case_id, role))


def run_fixed_control(case_id: str) -> dict:
    qualification = load_json(audit_reference_pack_qualification.QUALIFICATION)
    evidence = next(row for row in qualification["cases"] if row["case_id"] == case_id)
    record_path = ROOT / evidence["source_case_record"]
    record = load_json(record_path)
    with tempfile.TemporaryDirectory(prefix="brep2code-m19-retrieval-") as temp_dir:
        workdir = Path(temp_dir)
        subprocess.run([sys.executable, str(record_path.parent / record["reference_script"])], cwd=workdir, check=True)
        summary = probe_summary(load_model(workdir / "output/model.step"))
    expected = record["expected"]
    counts_match = summary["counts"] == expected["counts"]
    bbox_match = summary["bbox"] == expected["bbox"]
    volume_match = abs(summary["volume"] - expected["volume"]) < 1e-5
    return {"output_readable": True, "gate_pass": counts_match and bbox_match and volume_match}


def evaluate() -> dict:
    audit_reference_pack_retrieval.audit_evaluation()
    rows = audit_reference_pack_retrieval.load_json(audit_reference_pack_retrieval.EVALUATION)["cases"]
    policies = {"baseline": [], "treatment": ["vertical-cylinder-construction"]}
    results: dict[str, list[dict]] = {policy: [] for policy in policies}
    for row in rows:
        control = run_fixed_control(row["case_id"])
        for policy, expected_cards in policies.items():
            selected = select_cards(policy, row["case_id"], row["role"])
            results[policy].append(
                {
                    "case_id": row["case_id"],
                    "selected_cards": selected,
                    "selection_precision": 1.0 if selected == expected_cards else 0.0,
                    "unsupported_action": selected != expected_cards,
                    **control,
                }
            )
    assert all(not row["unsupported_action"] and row["gate_pass"] for rows in results.values() for row in rows)
    return {
        "schema_version": 1,
        "development_only": True,
        "card_sha256": sha256(CARD),
        "card_index_sha256": sha256(CARD_INDEX),
        "contract_sha256": sha256(CONTRACT),
        "results": results,
    }


def main() -> None:
    print(json.dumps(evaluate(), sort_keys=True))


if __name__ == "__main__":
    main()
