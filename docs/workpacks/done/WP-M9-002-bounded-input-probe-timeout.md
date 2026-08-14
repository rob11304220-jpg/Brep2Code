# WP-M9-002: Bounded Input Probe Timeout and Revalidation

- Status: done
- Milestone: M9
- Owner: unassigned

## Goal

Make complex external STEP input summaries bounded, fail closed, and usable by the existing first-pass path without relaxing output-artifact or provider safety limits.

## Scope

- Separate input summary timeout (45 seconds) from output summary timeout (15 seconds).
- Share isolated probe execution between Harness and first-pass corpus generation.
- Fail an input-bearing Harness revision when its input summary is unavailable; preserve skipped comparison gates and existing numerical tolerances.
- Revalidate the M8 8/4 ABC split locally through `wsl-bwrap`; do not run hosted evaluation.

## Trace/schema changes

No report schema version or CLI changes. Input-bearing `signal_bundle.json` files add `input_model_step_readable`; input-probe failures retain the structured `input_summary` error, and schema-v3 first-pass records `input_probe_failure` with `provider_requests: 0`.

## Compatibility constraints

- No-input M0 runs do not create an input gate and retain their passing behavior.
- Output artifact probe remains capped at 15 seconds; provider timeout and geometry thresholds are unchanged.
- Default commands remain offline and external assets stay ignored under `data/`.

## Acceptance and evidence

- Focused Harness/corpus tests: 40 passed; full pytest: 64 passed; Ruff passed.
- All 12 local ABC files matched their recorded M8 SHA-256 values.
- Both ignored split reports completed under `wsl-bwrap`; all 12 scripts exited 0 and all 12 input summaries succeeded. Development was 8 expected geometry-gate failures; held-out was 4 expected geometry-gate failures.
- No hosted request was made.

## Status transition

Updated M9-001 from input-probe blocked to authorization blocked, refreshed the M9 review and handoff, and recorded ADR-0008.

## Out of scope

Hosted authorization, prompt/policy changes, partial summaries, new gates beyond input-summary availability, IR, SDK, and CAD workplace.
