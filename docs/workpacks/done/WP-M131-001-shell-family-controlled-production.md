# WP-M131-001: Shell Family Controlled Production

- Status: done
- Milestone: M131
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Produce and audit exactly the six frozen `shell-v1` candidates from M130.

## Scope

Implement a deterministic candidate producer and family-specific audit for the frozen preregistration only. Verify normalized STEP hash stability, geometry replay, exact sequence, declared editability mutations, top-opening uniform thickness, bottom wall, one-solid semantics and all negative controls.

## Compatibility constraints

No row substitution, preregistration change, executable manifest, runtime/card, provider, hosted request, external data or rib-family work. Rejected rows stay recorded with their stable reason class.

## Acceptance

Run the producer/audit twice in clean output roots, its focused tests, Ruff, governance audit and `git diff --check`. Record exact output paths and results before independent review.

## Owner evidence (2026-08-11)

- Added `tools/build_m131_shell_candidates.py` and `tools/audit_sequence_paired_shell.py`, then produced exactly the six M130-frozen experimental directories under `case-library/self-authored/param_shell_*`.
- Each row passed clean-directory normalized STEP hash stability, geometry replay, exact sequence, two declared editability mutations, single-solid volume semantics, and split isolation. The producer contains no manifest/provider/runtime path.
- Added `tests/test_sequence_paired_shell.py`. The focused test passed; Ruff, governance audit and `git diff --check` passed after formatting the new tools.
- No row was substituted and no hosted/provider action occurred. Liaol's independent G2 review is now required before closure.

## Independent G2 review and closure (2026-08-11)

Liaol independently approved closure. The review confirmed the six frozen rows,
hash stability, family audit, split and negative-control boundary, acceptance
evidence, and absence of promotion or hosted scope. M131 closes as an
experimental controlled release only; a separate package controls any evidence
review, disposition or promotion.
