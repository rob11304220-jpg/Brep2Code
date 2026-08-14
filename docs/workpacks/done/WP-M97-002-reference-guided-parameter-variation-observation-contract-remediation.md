# WP-M97-002: Reference-Guided Parameter-Variation Observation-Contract Remediation

- Status: done
- Milestone: M97-002
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Repair the offline development-only bridge so the actual provider-bound
observation context is exactly the M96 measured-fact contract, and make the
supported OCP construction surface explicit and fail closed before any future
hosted calibration is considered.

## Scope

- Route each M94 development row through the M96 measured-through-hole-facts
  adapter instead of generic `probe_summary` when constructing M97 context.
- Assert before every provider boundary that context contains only the frozen
  `base_bbox`, cylinder `radius`, `axis`, `center_xy`, and `extent` facts, and
  reject paths, STEP, scripts, hashes, provider payloads and held-out rows.
- Add a versioned, locally tested OCP recipe for the declared +Z through-cut:
  `gp_Dir(0, 0, 1)`, measured centre/radius, and cutter extents that cross the
  base. Add a pre-execution symbol/API check that classifies unsupported
  imports such as `gp_DZ` without relaxing existing gates.
- Add fixtures that inspect the actual outbound development context and verify
  low-row values (`radius=2`, `center_xy=[9,10]`, `extent=through`), no-input
  `wsl-bwrap`, source-leak rejection, and unchanged fake-provider accounting.

## Attribution question and sampling intent

M97-001 confounded card/no-card comparison with an implementation mismatch:
the actual transcript omitted the parameters required by the frozen policy.
This workpack distinguishes a contract-conformant context/API path from that
failure mode using only the three existing development rows. Stop after the
offline contract, negative controls and regressions pass or classify a local
failure; do not add cases or send a provider request.

## Inputs

- `docs/corpus/sequence-paired/reference-guided-through-hole-variation-v1-m96-policy.json`
- M96 measured-fact adapter and its development-only tests
- M97-001 terminal report and generated low-row script evidence
- Existing no-input Harness and build-script contract tests

## Code paths

- `brep2code/agent/observed_build.py` and the M97 CLI path
- M96 observation adapter and focused tests
- Build-script contract validation only if needed for import-symbol checking

## Docs to update

- `docs/architecture/v1/contracts/q01-observation-build-separation.md` if the
  outbound context contract changes
- module documentation for any changed CLI/observation contract
- `docs/architecture/v1/four-track-program-roadmap.md`, M97/M98 workpacks,
  `docs/workflow/status.md`, active handoff and this workpack

## Trace/schema changes

Additive only: retain a content-free, inspectable context-contract disposition
or trace summary if required. Do not persist raw STEP, paths, reference
scripts, hashes, provider payloads or provider responses in the new contract.
No manifest, provider, report-schema or runtime retrieval change is allowed.

## Decision-package impact

- `decision_id`: M93/M94 reference-guided through-hole parameter variation.
- Q01/Q02 effect: makes the M96 measured facts the actual Q01-to-Q02 input;
  it does not add a CAD IR or alter the declared four-operation hypothesis.
- Q03/Q04 effect: strengthens pre-issuance failure classification and keeps
  OCP API, provenance, output, bbox, volume and topology gates unchanged.
- Evidence role: regression and negative-control evidence for a failed hosted
  contract path; no capability or held-out evidence.
- Knowledge disposition: record the M97-001 counterexample; no card promotion
  or runtime retrieval authorization.

## Compatibility constraints

Default execution remains offline and credential-free. Preserve existing CLI
commands, fake-provider M97 accounting, no-input `wsl-bwrap`, zero repair and
zero retry boundaries. M97-001 report/monitor and its six unissued requests
are immutable evidence. No hosted request, held-out inspection, card mutation,
prompt tuning after hosted evidence, endpoint/model change or manifest change
is in scope.

## Acceptance

```powershell
uv --cache-dir .uv-cache run python -m pytest tests\test_m96_reference_guided_through_hole_observation.py tests\test_observed_build_loop.py -q
uv --cache-dir .uv-cache run python -m ruff check .
uv --cache-dir .uv-cache run python tools\check_governance.py
git diff --check
```

The independent reviewer must verify the actual outbound context fixture, the
low-row parameter values, held-out fail-closed behavior, preserved gates and
absence of hosted egress.

## Evidence reuse / guidance-card disposition

M97-001 is a counterexample to using generic `probe_summary` as the frozen
parameter-variation transcript. The existing card is not promoted or mutated;
any future recipe/card/prompt hash is a separately frozen experimental input.

## Status transition

On completion, update `status.md` first, then this workpack and the active
handoff. ADR-0058 records the route change. Completion permits only selection
of a new bounded G3 development calibration workpack; it does not authorize
provider use or M98.

## Closure rationale

Record terminal offline validation and independent G2 review. A passing local
repair establishes implementation readiness only; it cannot make a card,
model-quality or parameter-generalization claim.

## Owner validation (2026-08-10)

- `uv --cache-dir .uv-cache run python -m pytest tests\test_m96_reference_guided_through_hole_observation.py tests\test_observed_build_loop.py -q` — pass, 41 tests in 144.358 s (JUnit local evidence only).
- `uv --cache-dir .uv-cache run python -m pytest tests\test_harness_m2.py::test_harness_rejects_unavailable_ocp_symbol_before_executor_runs tests\test_harness_m2.py::test_harness_accepts_ocp_script_contract -q` — pass, 2 tests in 5.38 s.
- `uv --cache-dir .uv-cache run python -m ruff check .` — pass.
- `uv --cache-dir .uv-cache run python tools\check_governance.py` — pass.
- `git diff --check` — pass.

Liaol independently confirmed the G2 review on 2026-08-10, including the
actual outbound-context fixture, low-row values, held-out/source-leak
fail-closed boundary, OCP symbol classification, unchanged gates/accounting
and absence of hosted egress. No provider was constructed or called; the tests
use only fake providers and local OCP/WSL execution.

## Out of scope

Any provider request, reuse of M97-001 capacity, a retry, repair, held-out
evaluation, prompt/card change based on a held-out result, manifest promotion,
runtime retrieval, training input or generic OCP SDK/IR work.

## Repair hypothesis and evaluation boundary

The trace-supported hypothesis is that generic summary context caused the
provider to default the low-row centre to `x=15`, while an unsupported `gp_DZ`
import caused execution rejection. Fixed-script reproductions must demonstrate
the supported measured-parameter recipe; negative controls must reject missing
facts and unsupported imports. This package is offline and development-only;
any later hosted paired comparison requires its own preflight and explicit
authorization.
