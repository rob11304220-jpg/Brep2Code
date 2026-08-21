from __future__ import annotations

import json

from brep2code.backends import BackendProfileId, backend_profile
from brep2code.providers.action_protocol import ActionRequest
from brep2code.providers.task_contract import (
    build_provider_task_contract,
    validate_task_contract_projection,
)


ACTIVE_RETRIEVAL_SYSTEM_PROMPT = """\
You reconstruct the described target B-Rep through a bounded tool-using CAD session.

Return one valid JSON object containing exactly one action and its matching payload:
- {"action":"probe","probe":{"tool":"edge_candidates","arguments":{}}}
- {"action":"retrieve","retrieve":{"query":"topology-aware edge selection","scope":["sdk","recipe"],"limit":2}}
- {"action":"retrieve","retrieve":{"topic":"TopoDS.Edge_s"}}
- {"action":"submit","submit":{"script":"complete build.py"}}
- {"action":"finish","finish":{"reason":"why no further action is useful"}}

Return JSON only, without Markdown fences or commentary. Use only declared tools. When the visible
observations are insufficient, probe or retrieve an approved SDK or recipe projection instead of guessing. A
submit action must contain a complete deterministic Python program. <<BACKEND_CONTRACT>>
The Harness, not the model, decides success after compatibility
checking, secure execution, and required geometry gates. A finish action cannot bypass verification.
When feedback and a current revision are present, a repair submit must change the complete script
to address that feedback. Never resubmit an unchanged failed revision; retrieve an approved SDK
or recipe projection first when the binding or modeling strategy needed for a correct repair is uncertain.

Never request or reveal repository files, eval references, target solutions, private oracles, host
paths, environment variables, credentials, network access, or undeclared tools.
"""

ACTIVE_NO_RETRIEVAL_SYSTEM_PROMPT = """\
You reconstruct the described target B-Rep through a bounded tool-using CAD session.

Return one valid JSON object containing exactly one action and its matching payload:
- {"action":"probe","probe":{"tool":"edge_candidates","arguments":{}}}
- {"action":"submit","submit":{"script":"complete build.py"}}
- {"action":"finish","finish":{"reason":"why no further action is useful"}}

Return JSON only, without Markdown fences or commentary. Use only declared tools. A submit action
must contain a complete deterministic Python program. <<BACKEND_CONTRACT>>
The Harness decides success after compatibility checking, secure execution,
and required geometry gates. A finish action cannot bypass verification. When feedback and a current
revision are present, a repair submit must change the complete script to address that feedback.

Never request or reveal repository files, eval references, target solutions, private oracles, host
paths, environment variables, credentials, network access, or undeclared tools.
"""


def build_action_messages(request: ActionRequest) -> list[dict[str, str]]:
    task = dict(request.session)
    task.pop("budgets", None)
    task.pop("task_contract", None)
    task.pop("task_contract_hash", None)
    task["turn_index"] = request.turn_index
    prompt = (
        ACTIVE_NO_RETRIEVAL_SYSTEM_PROMPT
        if request.session.get("retrieval_policy") == "disabled"
        else ACTIVE_RETRIEVAL_SYSTEM_PROMPT
    )
    allowed_actions = request.session.get("allowed_actions")
    if isinstance(allowed_actions, list):
        prompt = _project_allowed_action_examples(prompt, set(allowed_actions))
    profile = backend_profile(request.session.get("backend_profile", BackendProfileId.OCP_V1))
    retrieval_policy = request.session.get("retrieval_policy", "bounded_seed")
    projection = request.session.get("task_contract")
    contract = (
        build_provider_task_contract(profile.profile_id, retrieval_policy)
        if projection is None
        else validate_task_contract_projection(
            projection,
            backend=profile.profile_id,
            retrieval_policy=retrieval_policy,
        )
    )
    supplied_hash = request.session.get("task_contract_hash")
    if supplied_hash is not None and supplied_hash != contract.identity:
        raise ValueError("provider task contract hash drift")
    prompt = prompt.replace(
        "<<BACKEND_CONTRACT>>",
        f"Use backend profile {profile.profile_id}. {profile.api_summary} "
        f"{profile.export_contract}",
    )
    return [
        {"role": "system", "content": prompt},
        {"role": "user", "content": json.dumps(task, separators=(",", ":"))},
    ]


def _project_allowed_action_examples(prompt: str, allowed_actions: set[str]) -> str:
    prefixes = {
        "probe": '- {"action":"probe"',
        "retrieve": '- {"action":"retrieve"',
        "submit": '- {"action":"submit"',
        "finish": '- {"action":"finish"',
    }
    return "\n".join(
        line
        for line in prompt.splitlines()
        if not any(
            line.startswith(prefix) and action not in allowed_actions
            for action, prefix in prefixes.items()
        )
    )
