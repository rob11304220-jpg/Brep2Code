# WP-M171-001: M96/M97 Guidance-Index Fixture Remediation

- Status: done
- Milestone: M171
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Entry condition

M170's independent review accepted its focused evidence but recorded five
scope-external M96/M97 failures.  The user explicitly selected this bounded
remediation on 2026-08-14 before the staged hosted-capability route resumes.

## Goal

Restore reproducible M96/M97 frozen-policy validation after the unrelated
`selector-cardinality-stop` index addition, without mutating the historical
policy/card identities or the live guidance index.

## Scope

- Add one immutable, versioned historical guidance-index fixture whose SHA-256
  equals the M96/M97 frozen index hash `dfa731d597581b3b4d306782c1078c7de5b79672462229baaf5d7248fa230517`.
- Bind the affected M96/M97 regression checks to that fixture and verify the
  selected `vertical-cylinder-construction` card retains its frozen hash
  `55341683e3e7df3e058a845193e34fba20b0650c0db28a31489ad5d343b60d30`.
- Add focused evidence that the current index, including the selector card,
  remains the live default and that no M170 behavior changes.
- Record the fixture decision in ADR-0083 and update only the historical
  validation documentation needed to make its purpose and boundary clear.

## Decision-package impact

- Hypothesis ID: not applicable; historical regression-fixture restoration.
- Q01--Q04 decision: no semantic, execution, repair, or provider change.
- Evidence role: regression reproducibility for frozen M96/M97 provenance.
- Counterexample: a changed historical fixture hash, changed selected-card
  hash, or a live-index behavior change rejects this remediation.
- Stop rule: any need to alter an M96/M97 frozen policy, current index,
  GuidanceBundle/Harness behavior, case/split/manifest, or provider boundary
  stops this package.
- Adoption boundary: fixture-only; it is not a default runtime index, retrieval
  source, card promotion, or hosted input.

## Compatibility constraints

Offline and credential-free.  Do not modify the M96/M97 policy hashes,
`vertical-cylinder-construction` card, current `runtime_resources` index,
cases, splits, manifests, Harness/tool schema, repair policy, provider
configuration, or hosted controls.  Do not issue a provider request or access
held-out assets.

## Acceptance

```powershell
uv run python -m pytest tests\test_m96_reference_guided_through_hole_observation.py tests\test_observed_build_loop.py -q
uv run python -m ruff check tests\test_m96_reference_guided_through_hole_observation.py tests\test_observed_build_loop.py
uv run python tools\audit_runtime_guidance.py
uv run python tools\check_governance.py
git diff --check
uv run python -m pytest tests -q
```

## Owner completion boundary

Publish the hash-bound fixture, focused regression evidence, and unchanged
live-index evidence; then obtain Liaol's independent G2 review.  Only after
that review may the route return to its next unmet named successor.

## Owner completion evidence

- Added `docs/corpus/sequence-paired/fixtures/m96-m97-guidance-index-v1.json`.
  Its SHA-256 is exactly the frozen M96/M97 value
  `dfa731d597581b3b4d306782c1078c7de5b79672462229baaf5d7248fa230517`.
- Bound the M96 regression assertion and M97 calibration CLI default to that
  fixture.  The selected vertical-cylinder card remains hash
  `55341683e3e7df3e058a845193e34fba20b0650c0db28a31489ad5d343b60d30`.
- Added a regression test proving the fixture differs from the live index and
  that the selector-cardinality card remains present only in the live default.
- Updated the historical M97 preflight to name the fixture and recorded the
  durable decision in ADR-0083.

## Validation evidence

| Command | Terminal result |
|---|---|
| `Get-FileHash docs\corpus\sequence-paired\fixtures\m96-m97-guidance-index-v1.json -Algorithm SHA256` | `DFA731D597581B3B4D306782C1078C7DE5B79672462229BAAF5D7248FA230517` |
| `uv run python -m pytest tests\test_m96_reference_guided_through_hole_observation.py -q` | 8 passed in 4.50s |
| `uv run python -m pytest tests\test_observed_build_loop.py -q` | 38 passed in 137.90s |
| `uv run python -m ruff check tests\test_m96_reference_guided_through_hole_observation.py tests\test_observed_build_loop.py brep2code\cli\__init__.py` | passed |
| `uv run python tools\audit_runtime_guidance.py` | passed: live index has 5 cards |
| `uv run python -m pytest tests -q` | 289 passed in 519.78s |
| `git diff --check` | passed; existing LF/CRLF warnings only |

## Review state

Owner-side scope and validation are complete.  Await Liaol's independent G2
review of the fixture-only boundary, recorded hashes, unchanged live index,
historical CLI binding, ADR-0083, and validation evidence.  Review must not
treat this fixture as a policy rewrite or hosted authorization.

Liaol approved the independent G2 review on 2026-08-14. The fixture-only
boundary, frozen hashes, unchanged live index, historical CLI binding,
ADR-0083, and recorded validation evidence were accepted. This approval does
not confer provider or hosted authority.

## Closure rationale

M171 closes because it restored the historical M96/M97 index identity through
an immutable fixture, preserved the live index and selected-card identity,
passed all focused and full regression gates, and received independent G2
approval. The route resumes at M172, its next unmet named successor.

## Status transition

Update `status.md` first, then move this workpack to `done/` and update the
active handoff. Activate only the next selected G1 charter; do not select
cases or initiate any provider/hosted activity.

## Permitted stop conditions

Independent review, a frozen source-hash mismatch, a required change beyond
the fixture/test/document boundary, or a reproducible validation blocker.

## Out of scope

M170 behavior, M96/M97 policy redesign, index/card content changes, runtime
selection changes, retrieval, provider or hosted execution, credentials,
cases, held-out use, manifests, Harness/tool schema, repair changes, model or
prompt changes, and the 30-case campaign.
