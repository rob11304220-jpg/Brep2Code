import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.replay_m23_additive_boss_dependent_cut import replay  # noqa: E402

replay("param_additive_boss_dependent_cut_offset_high", Path("output") / "model.step")
