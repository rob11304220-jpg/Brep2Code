from tools import audit_runtime_guidance


def test_runtime_guidance_audit_passes() -> None:
    audit_runtime_guidance.main()
