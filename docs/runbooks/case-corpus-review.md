# Case Corpus Review

This runbook describes the local M4 workflow for manifest-driven case review.

## Purpose

Use a small deterministic corpus to inspect Harness behavior across cases before adding hosted LLM integration, larger datasets, or new modeling abstractions.

## Default Constraints

- Keep runs network-free.
- Use existing P0 fixtures first: `box`, `cylinder`, `block_with_hole`.
- Use self-authored P1 fixtures for local parametric coverage: `filleted_block`, `chamfered_block`, `three_hole_plate`, `box_cylinder_union`.
- Do not require hosted LLM credentials.
- Use fake-provider repair replay only when the case manifest provides a local `reference_script`.
- Treat corpus reports as engineering evidence, not benchmark claims.

## Command

Run the default P0 corpus:

```powershell
uv run python -m brep2code.cli corpus --manifest case-library\manifests\self-authored\p0.json --data-root data
```

Run the P1 parametric corpus:

```powershell
uv run python -m brep2code.cli corpus --manifest case-library\manifests\self-authored\p1.json --data-root data
```

The command writes per-case records under `data/records/` and a compact report under `data/corpus-runs/`.

To replay local fake-provider repairs for cases with `reference_script`:

```powershell
uv run python -m brep2code.cli corpus --manifest case-library\manifests\self-authored\p0.json --data-root data --repair
```

Use `case-library\manifests\self-authored\p1.json` with `--repair` to replay P1 reference scripts.

## Explicit external STEP baseline

External source data is never downloaded by this command or by tests. After the selected files have been placed under the ignored path recorded in a reviewed selection file, run its explicit manifest only:

```powershell
uv run python -m brep2code.cli corpus --manifest docs\corpus\external\abc-v00-m8-001-manifest.json --executor wsl-bwrap --data-root data --report data\corpus-runs\abc-v00-m8-001-baseline.json
```

Before treating the report as completed evidence, verify every selected file against the SHA-256 values in `docs/corpus/external/abc-v00-m8-001-selection.json`. A fixed default scaffold may fail geometry gates; that is control evidence, while hash, input-probe, manifest, or sandbox failures are admission failures.

### Local ABC archive cache

Under [ADR-0011](../architecture/adr/0011-local-external-archive-cache.md), the already acquired ABC archive may be completely extracted into ignored `data/datasets/abc/v00/step/` to avoid repeated archive decoding.  Run it as a durable local process, keep the archive unchanged, and create the ignored completion catalog only after its SHA-256, all 10,000 STEP members, and the archive-listed byte total match.  If that catalog is absent, treat the cache as incomplete and verify each selected file independently.

The cache is not an execution manifest: do not add all members to default tests, a tracked manifest, provider context, or a hosted batch.  Only a separately recorded deterministic selection and its explicit manifest may be probed, controlled, or evaluated.

## Explicit M9 split preflight and hosted evaluation

M9 keeps development and held-out samples in separate explicit manifests. First, verify each manifest's local STEP files against the M8 selection hashes, then run its fixed-scaffold control through the secure executor. These commands remain offline:

```powershell
uv run python -m brep2code.cli corpus --manifest docs\corpus\external\abc-v00-m9-001-development-manifest.json --executor wsl-bwrap --data-root data --report data\corpus-runs\abc-v00-m9-001-development-preflight.json
uv run python -m brep2code.cli corpus --manifest docs\corpus\external\abc-v00-m9-001-held-out-manifest.json --executor wsl-bwrap --data-root data --report data\corpus-runs\abc-v00-m9-001-held-out-preflight.json
```

Do not issue a hosted request after a hash, manifest, input-probe, or sandbox failure. Fixed-scaffold geometry-gate failures remain control evidence.

The input summary deadline is 45 seconds and the generated output artifact deadline remains 15 seconds. An unavailable input summary is a failing `input_model_step_readable` gate, not a passing control with skipped comparisons. In first-pass mode it prevents provider request issuance and preserves the request budget.

Only after a new explicit authorization may the development command use `deepseek-v4-pro`, `--first-pass`, `--max-cases 8`, `--max-rounds 1`, `--request-budget 16`, and `--provider-timeout 120`. The held-out command requires a separate authorization and the unchanged model/policy/executor/round/deadline settings with `--max-cases 4` and `--request-budget 8`. Use separate ignored report paths. A `running` or `interrupted` report is partial evidence; do not reuse the remaining budget.

## Validation

After implementing or changing corpus behavior:

```powershell
uv run python -m pytest
uv run python -m ruff check .
```

For a manual Harness spot check:

```powershell
uv run python -m brep2code.cli run --record box-smoke --input case-library\self-authored\box\input.step
```

## Review Checklist

- Every manifest case resolves repository-relative paths.
- Every case produces a record id, revision id, status, and gate summary.
- Probe failures are classified separately from script failures.
- Fake-provider replay is clearly marked and does not mutate earlier revisions.
- Report output is compact enough to paste into handoff or review notes.

## External attribution and repair-routing review

After a completed external development/held-out evaluation, review only completed reports, sanitized revisions, signal bundles, and traces.  Keep development and held-out funnels separate.  Update the cumulative attribution ledger before selecting the next action; do not write classifications into the corpus report unless a later dedicated schema decision authorizes it.

For each case, record the batch/split, first-pass outcome, repair outcome, primary attribution, evidence level, revision/trace reference, unresolved question, candidate repair hypothesis, and counterexample status.  Use these levels:

- `direct`: the generated revision and execution trace prove the asserted causal failure.
- `supported`: signals are consistent with a mechanism, but do not prove it caused execution failure.
- `unknown`: the existing evidence cannot decide.

Only `direct` cases count toward the three-case narrow-helper threshold.  Do not count provider lifecycle failures as script evidence, geometry gates skipped for absent output as geometry failures, or a static unexecuted symptom as a causal failure.

Select one route after the ledger update:

1. Report-only geometry diagnostics only for at least three executable/readable first-pass outputs with non-actionable geometry failures.
2. A narrow helper only for at least three external cases with one `direct`, reproducible root cause.
3. A minimal offline repair experiment for at least two external cases sharing one `direct` or `supported` locally reproducible mechanism.  Preregister fixed-script reproduction, a non-matching control, retained gate evidence, and the limited claim: deterministic compatibility or repair-signal usefulness only.
4. Otherwise, a deterministic external increment that records the attribution question, expected information gain, and stopping condition.

An offline experiment cannot establish model improvement or change production policy.  A prompt/context or other provider-policy comparison requires a separate preregistered development-only workpack, the hosted preflight in `llm-provider-config.md`, and explicit authorization.  Conduct held-out only after development review and a separate authorization.