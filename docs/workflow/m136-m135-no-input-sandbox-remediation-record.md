# M136 M135 No-Input Sandbox Remediation Record

- **Date**: 2026-08-12
- **Workpack**: `WP-M136-001-m135-no-input-sandbox-preflight-remediation`
- **Boundary**: offline-only; fake provider; no credentials, provider
  construction, egress, or hosted authorization

## Mechanism and control

The original M135 centered-low revolve control exited 1 because its frozen
reference script imported `tools.audit_sequence_paired_revolve` from the host
repository. The no-input `wsl-bwrap` workspace intentionally exposes neither
the repository root nor `tools/`; the structured terminal evidence was
`ModuleNotFoundError: No module named 'tools'`.

The repeated-feature centered-low no-card control passed under the same runner
with exit code 0. Completing the full frozen no-card control after the first
repair exposed the same forbidden import mechanism in the face-selected-cut
and multi-inner-loop-pocket development scripts. This is one local
reference-script portability defect, not a provider or epoch-policy result.

## Repair

The nine affected frozen development reference scripts now contain only their
case-specific deterministic OCP construction and STEP export. The no-input
sandbox itself was not relaxed, the frozen input STEP hashes are unchanged, and
the scripts do not import `tools.*`. A regression test asserts that all frozen
M135 no-card reference scripts have no repository-helper import; the existing
dynamic fixed-script no-input test is the non-matching execution control.

## Validation

| Command | Terminal result |
|---|---|
| `uv run python -m pytest tests\test_m135_epoch.py -q` | 5 passed in 93.43s |
| `uv run python -m pytest -m fast -q` | 66 passed, 177 deselected in 3.73s |
| `uv run python -m ruff check .` | All checks passed |
| `uv run python -m pytest -q` | 243 passed in 441.71s |
| `uv run python tools\check_governance.py` | Governance audit passed |
| `git diff --check` | passed (line-ending warnings only) |

## Interpretation and re-entry

This establishes local fixed-script no-input portability only. It makes no
provider-quality, epoch-result, or hosted-readiness claim. M136 must first
receive independent G2 review. Only then may M135 be reconsidered through an
entirely fresh G3 preflight with the unchanged frozen cohort and new report/
monitor identities, followed by separately itemized hosted authorization.

## Independent review

Liaol approved the independent G2 review on 2026-08-12. The review accepted
the bounded local mechanism, the retained no-input `wsl-bwrap` boundary, the
complete acceptance evidence, and the unchanged M135 re-entry constraints.
