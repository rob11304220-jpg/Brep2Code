import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from tools.audit_sequence_paired_oriented_rounded_slot import EXPANSION, build_shape  # noqa: E402
from tools.audit_sequence_paired_prismatic_hole import load_json, write_step  # noqa: E402
entry = next(x for x in load_json(EXPANSION)["cases"] if x["case_id"] == "param_oriented_rounded_slot_x_nominal")
Path("output").mkdir(exist_ok=True)
write_step(build_shape(entry), Path("output/model.step"))
