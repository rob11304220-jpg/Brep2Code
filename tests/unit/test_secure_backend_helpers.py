import pytest

from brep2code.execution.secure import (
    SecureBackendConfig,
    _decode,
    _is_wsl_backend_failure,
    secure_backend_config,
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
def test_secure_backend_configuration_rejects_unsafe_values(
    distro: str, runtime_root: str
) -> None:
    with pytest.raises(ValueError):
        SecureBackendConfig(distro, runtime_root)
