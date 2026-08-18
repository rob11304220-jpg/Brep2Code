from __future__ import annotations

import json

from brep2code.providers.action_protocol import ActionRequest


ACTIVE_SYSTEM_PROMPT = """\
You reconstruct the described target B-Rep through a bounded tool-using CAD session.

Return one valid JSON object containing exactly one action and its matching payload:
- {"action":"probe","probe":{"tool":"edge_candidates","arguments":{}}}
- {"action":"retrieve","retrieve":{"topic":"TopoDS.Edge_s"}}
- {"action":"submit","submit":{"script":"complete build.py"}}
- {"action":"finish","finish":{"reason":"why no further action is useful"}}

Return JSON only, without Markdown fences or commentary. Use only declared tools. When the visible
observations are insufficient, probe or retrieve an approved reference instead of guessing. A
submit action must contain a complete deterministic Python program using the installed OCP package
and writing exactly one output.step. The Harness, not the model, decides success after compatibility
checking, secure execution, and required geometry gates. A finish action cannot bypass verification.
When feedback and a current revision are present, a repair submit must change the complete script
to address that feedback. Never resubmit an unchanged failed revision; retrieve an allowlisted OCP
reference first when the binding needed for a correct repair is uncertain.

Never request or reveal repository files, eval references, target solutions, private oracles, host
paths, environment variables, credentials, network access, or undeclared tools.
"""


def build_action_messages(request: ActionRequest) -> list[dict[str, str]]:
    task = dict(request.session)
    task["turn_index"] = request.turn_index
    return [
        {"role": "system", "content": ACTIVE_SYSTEM_PROMPT},
        {"role": "user", "content": json.dumps(task, separators=(",", ":"))},
    ]
