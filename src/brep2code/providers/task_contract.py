from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Any

from brep2code.backends import BackendProfileId, backend_profile


@dataclass(frozen=True)
class ProviderTaskContract:
    contract_version: int
    backend_profile: str
    backend_package: str
    backend_version_spec: str
    allowed_import_roots: tuple[str, ...]
    api_summary: str
    export_contract: str
    output_file: str
    retrieval_policy: str
    prompt_version: str
    actions: tuple[str, ...]
    available_tools: tuple[str, ...]
    restrictions: tuple[str, ...]

    def projection(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def identity(self) -> str:
        encoded = json.dumps(self.projection(), sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
        return sha256(encoded).hexdigest()


def build_provider_task_contract(
    backend: BackendProfileId | str,
    retrieval_policy: str,
    *,
    contract_version: int = 2,
) -> ProviderTaskContract:
    profile = backend_profile(backend)
    if retrieval_policy not in {"disabled", "bounded_seed"}:
        raise ValueError("provider task contract retrieval policy is invalid")
    retrieval_enabled = retrieval_policy == "bounded_seed"
    if contract_version not in {1, 2}:
        raise ValueError("provider task contract version is invalid")
    prompt_generation = "v3" if contract_version == 1 else "v4"
    return ProviderTaskContract(
        contract_version=contract_version,
        backend_profile=profile.profile_id,
        backend_package=profile.package,
        backend_version_spec=profile.version_spec,
        allowed_import_roots=profile.import_roots,
        api_summary=profile.api_summary,
        export_contract=profile.export_contract,
        output_file="output.step",
        retrieval_policy=retrieval_policy,
        prompt_version=(
            f"active-{prompt_generation}-retrieval"
            if retrieval_enabled
            else f"active-{prompt_generation}-no-retrieval"
        ),
        actions=(
            ("probe", "retrieve", "submit", "finish")
            if retrieval_enabled
            else ("probe", "submit", "finish")
        ),
        available_tools=(
            ("edge_candidates", "knowledge_search", "ocp_symbol")
            if retrieval_enabled
            else ("edge_candidates",)
        ),
        restrictions=(
            "no_network",
            "no_subprocess",
            "no_absolute_paths",
            "no_repository_files",
            "no_eval_references",
            "no_private_oracles",
            "no_secrets",
        ),
    )


def validate_task_contract_projection(
    value: Any,
    *,
    backend: BackendProfileId | str,
    retrieval_policy: str,
) -> ProviderTaskContract:
    expected = build_provider_task_contract(backend, retrieval_policy)
    if value != expected.projection():
        raise ValueError("provider task contract projection drift")
    return expected
