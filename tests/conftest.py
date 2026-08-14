"""M53 test-feedback selection metadata.

The categories are assigned by test module so moving a test across the
execution boundary changes its selection deliberately in review.
"""

from __future__ import annotations

from pathlib import Path

import pytest


SANDBOX_MODULES = frozenset(
    {
        "test_agent_m3_repair_loop.py",
        "test_brep_m1.py",
        "test_corpus_m4.py",
        "test_harness_m0.py",
        "test_harness_m2.py",
        "test_observed_build_loop.py",
    }
)

FAST_MODULES = frozenset(
    {
        "test_agent_m3_provider_trace.py",
        "test_agent_m3_tool_bridge.py",
        "test_case_library_m12.py",
        "test_fusion360_m17_line3d_selector.py",
        "test_governance_audit.py",
        "test_m10_012_offline_repair_experiment.py",
        "test_m29_selector_ambiguity.py",
        "test_m30_blind_through_observability.py",
        "test_m31_sequence_rollback.py",
        "test_m32_nested_cylindrical_shoulder.py",
        "test_m33_axis_relative_nested_cylinder.py",
        "test_runtime_guidance.py",
        "test_sequence_paired_intake.py",
    }
)


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Apply the documented M53 selections to every collected test."""
    for item in items:
        module_name = Path(str(item.fspath)).name
        if module_name in SANDBOX_MODULES:
            item.add_marker(pytest.mark.sandbox)
            continue

        item.add_marker(pytest.mark.standard)
        if module_name in FAST_MODULES:
            item.add_marker(pytest.mark.fast)
