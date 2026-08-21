import pytest

from brep2code.execution.secure import (
    SecureBackendConfig,
    _decode,
    _is_wsl_backend_failure,
    secure_backend_config,
    secure_backend_profile_status,
)


def test_wsl_utf16_diagnostic_output_is_decoded() -> None:
    assert _decode("Wsl/Service/E_ACCESSDENIED\r\n".encode("utf-16-le")) == (
        "Wsl/Service/E_ACCESSDENIED\r\n"
    )


def test_wsl_launcher_failures_are_not_script_errors() -> None:
    assert _is_wsl_backend_failure(0xFFFFFFFF, "", "")
    assert _is_wsl_backend_failure(1, "Wsl/Service/E_ACCESSDENIED", "")
    assert not _is_wsl_backend_failure(1, "Traceback: RuntimeError", "")


def test_secure_backend_configuration_is_portable_and_explicit() -> None:
    assert secure_backend_config({}) == SecureBackendConfig()
    assert secure_backend_config(
        {
            "BREP2CODE_WSL_DISTRO": "Research-Ubuntu",
            "BREP2CODE_RUNTIME_ROOT": "/srv/brep2code/runtime",
        }
    ) == SecureBackendConfig("Research-Ubuntu", "/srv/brep2code/runtime")


@pytest.mark.parametrize(
    ("distro", "runtime_root"),
    [("", "/runtime"), ("Ubuntu;other", "/runtime"), ("Ubuntu", "relative/runtime")],
)
def test_secure_backend_configuration_rejects_unsafe_values(distro: str, runtime_root: str) -> None:
    with pytest.raises(ValueError):
        SecureBackendConfig(distro, runtime_root)


def test_secure_backend_profile_reports_installed_version(monkeypatch) -> None:
    class Completed:
        returncode = 0
        stdout = b"2.8.0\n"
        stderr = b""

    monkeypatch.setattr(
        "brep2code.execution.secure.secure_backend_status",
        lambda unused_config=None: (True, "ready"),
    )
    monkeypatch.setattr(
        "brep2code.execution.secure.subprocess.run", lambda *args, **kwargs: Completed()
    )

    assert secure_backend_profile_status("cadquery_v1") == (
        True,
        "secure backend profile cadquery_v1 ready",
        "2.8.0",
    )


def test_secure_backend_profile_fails_closed_when_package_is_missing(monkeypatch) -> None:
    class Completed:
        returncode = 1
        stdout = b""
        stderr = b"PackageNotFoundError"

    monkeypatch.setattr(
        "brep2code.execution.secure.secure_backend_status",
        lambda unused_config=None: (True, "ready"),
    )
    monkeypatch.setattr(
        "brep2code.execution.secure.subprocess.run", lambda *args, **kwargs: Completed()
    )

    assert secure_backend_profile_status("cadquery_v1") == (
        False,
        "secure backend profile cadquery_v1 package is unavailable",
        None,
    )
