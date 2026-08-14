# WP-M31-002: Verified-Prefix Fixed-Script Rollback Experiment

- Status: done
- Milestone: M31
- Owner: Codex

## Goal

Execute the preregistered offline experiment: preserve a verified boss prefix,
inject a suffix-only defect, and regenerate only the suffix.

## Scope

- Use only the two preregistered nominal additive-boss oracle rows.
- Retain STEP artifacts after base, boss and cut; hash the boss prefix.
- Check the suffix defect, rollback and early-defect non-match control.

## Compatibility constraints

Experiment-only offline tool. Do not modify Harness, provider repair, public
probe, runtime, manifests, registries, parser, gates, helpers, IR or SDK.

## Acceptance

- Both fixed rows preserve byte-identical boss prefixes through suffix rollback.
- Existing final comparison gates pass after canonical suffix regeneration.
- The early defect returns `unsupported`.
- Focused tests, Ruff and `git diff --check` pass.

## Completion

- Added `tools/run_sequence_rollback_experiment.py`; it retains baseline STEP
  artifacts, injects the frozen suffix defect, reuses the boss-prefix file,
  and regenerates only the canonical final suffix.
- One development and one held-out nominal row both preserved a byte-identical
  boss prefix and passed existing final comparison gates after rollback.
- The early defect returned `unsupported`. Re-exporting the same boss shape is
  not hash-stable because STEP exporter header metadata can vary, so it is not
  accepted as prefix preservation.
- Three focused tests, Ruff and `git diff --check` passed. Default Harness and
  all runtime/provider paths remain unchanged.

## Out of scope

Automatic rollback, generated-script repair, history recovery, public artifact
schema or any runtime behavior change.
