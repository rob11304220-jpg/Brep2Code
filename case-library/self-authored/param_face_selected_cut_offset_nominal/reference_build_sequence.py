"""Replay the promoted M25 deterministic reference into a STEP file."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from tools.audit_sequence_paired_face_selected_dependent_cut import EXPANSION, build_shape
from tools.audit_sequence_paired_prismatic_hole import load_json, write_step


def replay():
    entry = next(
        x
        for x in load_json(EXPANSION)["cases"]
        if x["case_id"] == "param_face_selected_cut_offset_nominal"
    )
    output = Path("output/model.step")
    output.parent.mkdir(parents=True, exist_ok=True)
    write_step(build_shape(entry), output)


if __name__ == "__main__":
    replay()
