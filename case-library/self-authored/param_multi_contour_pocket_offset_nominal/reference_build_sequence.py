import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.audit_sequence_paired_multi_contour_pocket import EXPANSION, build_shape  # noqa: E402
from tools.audit_sequence_paired_prismatic_hole import load_json, write_step  # noqa: E402

entry = next(row for row in load_json(EXPANSION)["cases"] if row["case_id"] == "param_multi_contour_pocket_offset_nominal")
output = Path("output")
output.mkdir(exist_ok=True)
write_step(build_shape(entry), output / "model.step")
