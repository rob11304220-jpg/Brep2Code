import os
from pathlib import Path

import pytest

from brep2code.execution import secure_backend_status


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-secure",
        action="store_true",
        help="run tests that require the configured WSL2/bubblewrap backend",
    )


def pytest_configure(config: pytest.Config) -> None:
    if config.getoption("basetemp") is None:
        config.option.basetemp = str(Path.cwd() / f".pytest-tmp-{os.getpid()}")
    config.addinivalue_line(
        "markers",
        "secure: requires the configured Ubuntu-24.04 WSL2/bubblewrap backend",
    )


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if config.getoption("--run-secure"):
        return
    ready, reason = secure_backend_status()
    if ready:
        return
    skip = pytest.mark.skip(reason=f"{reason}; rerun with --run-secure after setup")
    for item in items:
        if "secure" in item.keywords:
            item.add_marker(skip)
