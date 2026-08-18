from brep2code.execution.secure import _decode, _is_wsl_backend_failure


def test_wsl_utf16_diagnostic_output_is_decoded() -> None:
    assert _decode("Wsl/Service/E_ACCESSDENIED\r\n".encode("utf-16-le")) == (
        "Wsl/Service/E_ACCESSDENIED\r\n"
    )


def test_wsl_launcher_failures_are_not_script_errors() -> None:
    assert _is_wsl_backend_failure(0xFFFFFFFF, "", "")
    assert _is_wsl_backend_failure(1, "Wsl/Service/E_ACCESSDENIED", "")
    assert not _is_wsl_backend_failure(1, "Traceback: RuntimeError", "")
