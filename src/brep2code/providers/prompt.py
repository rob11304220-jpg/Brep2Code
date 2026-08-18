from __future__ import annotations

import json
from typing import Any

from brep2code.providers.protocol import ProviderRequest


SYSTEM_PROMPT = """\
You reconstruct the described target B-Rep as an executable Python CAD program.

Return one valid JSON object with exactly one string field named "script". The assistant message
must contain JSON only: no Markdown fences, commentary, prefixes, suffixes, or extra fields. The
field must contain the complete build.py source, not a patch or a fragment. Escape newlines and
quotes according to JSON; do not wrap the script in a second code block.

Script contract:
- Use only Python and the installed OCP (OpenCascade) package; do not import cadquery.
- Build the target geometry from the supplied observations, in millimetres.
- Prefer the shortest correct construction using high-level OCP builders such as BRepPrimAPI,
  BRepAlgoAPI, and BRepFilletAPI. Do not manually assemble or sew faces and shells when an
  equivalent primitive, boolean, or feature builder is available.
- Keep build.py concise (normally under 120 lines). Omit speculative abstractions, commentary,
  duplicate geometry, and validation code that is not required to create output.step.
- Put every import at module scope; do not repeat OCP imports inside functions.
- OCP Python static-method bindings use the `_s` suffix. For example, call
  TopExp.FirstVertex_s and TopExp.MapShapesAndAncestors_s, not the unsuffixed names.
- Run without command-line arguments, network access, package installation, repository access,
  or access to any input/reference STEP file.
- Write exactly one result named output.step in the current working directory.
- Use STEPControl_Writer and raise an exception unless Write returns IFSelect_RetDone.
- The program must be deterministic and self-contained.

When repair feedback and a previous script are supplied, return a complete revised script that
addresses the reported execution or geometry differences. Preserve correct parts where useful.
"""


def build_messages(request: ProviderRequest) -> list[dict[str, str]]:
    task: dict[str, Any] = {
        "case_id": request.case_id,
        "round_index": request.round_index,
        "observations": request.context,
        "acceptance": {"output": "output.step"},
        "feedback": request.feedback,
        "previous_script": request.previous_script,
    }
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": json.dumps(task, separators=(",", ":"))},
    ]
