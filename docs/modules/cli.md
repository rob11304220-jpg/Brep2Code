# CLI Module

## Responsibility

`brep2code/cli/` exposes manual development commands for the harness. It is a thin wrapper over module APIs and prints JSON for agent/tool consumption.

Manual harness run:

```powershell
uv run python -m brep2code.cli run --record demo
```

Optional external script:

```powershell
uv run python -m brep2code.cli run --record demo --script path\to\build_sequence.py
```

Run with a STEP input and M2 gates:

```powershell
uv run python -m brep2code.cli run --record box-smoke --input case-library\self-authored\box\input.step
```

Probe an explicit input:

```powershell
uv run python -m brep2code.cli probe --input case-library\self-authored\box\input.step
```

Run a local fake-provider repair replay:

```powershell
uv run python -m brep2code.cli repair --record box-repair --script broken_build.py --fake-replacement-script replacement_build.py --input case-library\self-authored\box\input.step
```

Run the M4 P0 case corpus:

```powershell
uv run python -m brep2code.cli corpus --manifest case-library\manifests\self-authored\p0.json --data-root data
```

## Boundary

The CLI is a thin entrypoint over harness behavior. It should not own storage layout, subprocess execution details, CAD backend logic, or LLM prompts.

## Output

The command prints a JSON summary with record paths, revision paths, status, execution details, artifacts, gates, and repair hints.

## Current Commands

| Command | Status | Owner |
|---------|--------|-------|
| `run` | implemented | `ManualHarness` |
| `probe` | implemented | `brep2code.brep` probe functions |
| `repair` | implemented for local fake-provider replay | `RepairLoopRunner` |
| `corpus` | implemented for local manifest-driven review | `brep2code/corpus/` |
| `observed-first-pass` | M52 single-case M48 observation-to-build path; fake by default, hosted only with explicit single-request authorization | `ObservedBuildLoopRunner` |
| `reference-assisted-smoke` | M85 fixed `cylinder` two-request path: one validated guidance-card request followed by one OCP script-generation request; fake by default | `ObservedBuildLoopRunner`, `GuidanceCardBridge` |
| `reference-assisted-block-with-hole-smoke` | M87 fixed `block_with_hole` two-request path: one validated `single boolean-cut tool` request followed by one OCP script-generation request; fake by default | `ObservedBuildLoopRunner`, `GuidanceCardBridge` |
| `reference-assisted-three-hole-plate-smoke` | M89 fixed P1 `three_hole_plate` two-request path: one validated `repeated boolean-cut tool` request followed by one OCP script-generation request; fake by default | `ObservedBuildLoopRunner`, `GuidanceCardBridge` |
| `reference-assisted-three-hole-plate-bounded-output-smoke` | M89-003 fixed P1 `three_hole_plate` two-request path: M89 role/card/gates plus a required 4096-token cap recorded in its fresh checkpoint; fake by default | `ObservedBuildLoopRunner`, `GuidanceCardBridge` |
| `reference-assisted-three-hole-plate-stability-smoke` | M118 fixed P1 `three_hole_plate` two-request stability-only path: same role/card boundary plus a required 4096-token cap under the M118 fresh policy namespace; fake by default | `ObservedBuildLoopRunner`, `GuidanceCardBridge` |
| `reference-assisted-three-hole-plate-stability-reentry-smoke` | M127 fixed P1 `three_hole_plate` two-request shared stability re-entry path: same role/card boundary plus a required 4096-token cap under a fresh M127 policy namespace; fake by default | `ObservedBuildLoopRunner`, `GuidanceCardBridge` |
| `observed-development` | M55 explicit multi-case M48 observation-only path; fake by default and hosted only under separate bounds/authorization; atomically checkpoints provider deadlines as `interrupted` without retry | `ObservedBuildLoopRunner` |
| `reference-guided-through-hole-development-calibration` | M97 development-only paired calibration adapter. It derives and validates the one M96 measured-fact transcript per development row before either fake or future authorized provider boundary; held-out rows and generic summaries fail closed. | `derive_m96_development_context`, `ObservedBuildLoopRunner` |
| `provider-control` | M64 fixed `Return exactly OK.` endpoint/model response control; hosted use requires an explicit one-request authorization and writes no prompt or response content to its report | provider worker boundary |
| `m176-asymmetric-campaign-preflight` | M178 fixed dual-product local preflight: validates the M175/M176 main cohort, annex roles/card hashes, executor, identities and 102 completion-slot / 69 provider-request ceilings, then creates only fresh local checkpoints and monitor state | `brep2code.asymmetric_campaign` |
| `m176-asymmetric-campaign-admission` | M178 local-only check that both M176 product checkpoints remain unissued and not authorized; it never constructs a provider | `brep2code.asymmetric_campaign` |
| `m179-asymmetric-campaign-preflight` | M179 local-only refreeze for four new identities, cryptographically bound to M176; it never constructs a provider | `brep2code.asymmetric_campaign` |
| `m179-asymmetric-campaign-admission` | M179 local-only check that both refrozen checkpoints remain unissued and unauthorized | `brep2code.asymmetric_campaign` |
| `m180-asymmetric-campaign-execute` | M180's sole fixed execute entrypoint.  It accepts only explicit authorization and an env-file location, revalidates M179 checkpoints before provider construction, and preserves serial no-retry 102-slot / 69-request accounting. | `brep2code.asymmetric_campaign`, `ObservedBuildLoopRunner` |
| `m182-asymmetric-campaign-preflight` | M182 local-only refreeze for four fresh identities, cryptographically bound to M179; it never constructs a provider. | `brep2code.asymmetric_campaign` |
| `m182-asymmetric-campaign-admission` | M182 local-only check that both continuation-contract checkpoints remain unissued and unauthorized. | `brep2code.asymmetric_campaign` |
| `m182-asymmetric-campaign-execute` | M182's sole continuation execute entrypoint. It requires a new itemized authorization, retains an eligible case-local provider failure as that case's terminal result, and continues serially without retry, resume, or budget reuse. | `brep2code.asymmetric_campaign`, `ObservedBuildLoopRunner` |

`observed-first-pass` and `observed-development` now project M65 telemetry:
content-free system/observation character and UTF-8-byte counts, null fields
for unavailable first-byte/token evidence, and local-phase elapsed milliseconds.
Character counts must not be interpreted as token counts.

`observed-development --case-id ID --max-cases 1` selects exactly one existing
manifest row without changing manifest membership; it supports independent
development-only checkpoints and does not relax hosted authorization bounds.

The M178 asymmetric commands do not confer hosted authority. The main product
is development-only; the three-case annex is bound by its exact frozen roles
and one hash-bound card. They expose 102 interaction-completion slots and a
tighter 69-request HTTP ceiling as distinct quantities; a future G3 execution
still requires a newly selected workpack, fresh preflight and itemized user
authorization.

M180 or M182 must not be invoked merely because the command exists.  Each remains
blocked on fresh preflight, independent G3 review, and user authorization for
the exact frozen campaign.  Its reports checkpoint every issued provider
request before provider work; an authorized run has no resume or policy
override surface.
| `compile` | not implemented; do not document as available | deferred |
| `eval` | not implemented as standalone command; current gates run through `run` | deferred |
