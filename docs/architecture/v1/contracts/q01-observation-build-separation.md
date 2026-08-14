---
type: contract
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - Q01
  - Q02
  - capability-separation
---

# Contract: Q01 Observation / Q02 Build Separation

M48 implements the bounded observation envelope, transcript context guard, and
opt-in no-original-STEP build capability defined here. It does not yet connect
that transcript to a real provider request or authorize any provider call; the
next integration remains a separately selected G2 workpack.

## Capability boundary

| Plane | May read | May write/call | Must not receive |
|---|---|---|---|
| Q01 observation | Selected record STEP through internal probe backend only | Bounded probe computation and local query trace | Raw STEP bytes, host paths, overflow payloads, reference scripts, history labels |
| Q02 build | Versioned observation transcript or bounded transcript summary | `build_sequence.py`, `output/`, `intermediates/` | Original STEP mount, selected record path, observation-tool endpoint, local trace paths |

An `observation_session_id` is opaque and binds the transcript to one selected
input revision. It is not a path, a capability token, or a tool endpoint.

## Frozen Q01 tools

All calls use request envelope
`{"schema_version":1,"observation_session_id":"opaque","call_id":"opaque","tool":"...","arguments":{...}}`.
The runtime LLM sees only response envelope
`{"schema_version":1,"observation_session_id":"opaque","call_id":"opaque","ok":bool,"data":object|null,"error":object|null,"truncated":bool,"response_sha256":"hex"}`.
`data` omits the current bridge's `input` and `trace_path` fields. A response
is at most 12,000 UTF-8 bytes after envelope serialization; over-limit data is
not exposed and returns `response_too_large`.

| Tool | Arguments | Bounded data | Deadline | Unsupported / invalid result |
|---|---|---|---|---|
| `probe_summary` | `{}` | format, unit, bbox, counts, area, volume | 10 s | `backend_unavailable`, `read_failed`, or `response_too_large` |
| `probe_topology` | `selector` in `all/solid/shell/face/edge`; `max_entities` 1–80 | counts, selected entity IDs/types, returned, total_selected, truncated | 10 s | `invalid_selector`, `invalid_max_entities`, `response_too_large` |
| `probe_entity` | nonempty stable `entity_id` | entity ID/type, bbox, face surface/area/ranges or edge curve/length/range | 10 s | `entity_not_found`, `invalid_entity_id`, `response_too_large` |
| `sample_entity` | nonempty face/edge `entity_id`; `samples` 1–32 | requested/returned/truncated and sampled point+normal or point+tangent arrays | 10 s | `unsupported_entity`, `invalid_sample_count`, `response_too_large` |

The session has a maximum of eight calls. Any request beyond the limit returns
`tool_call_limit_exceeded`; no hidden traversal or fallback computation is
permitted.

## Local trace and exchange

The observation service writes a local-only JSONL entry for every accepted or
rejected call: session ID, call ID, tool, validated arguments, outcome code,
canonical-response SHA-256, serialized byte count, truncation flag, deadline
outcome, and timestamp. The trace stores neither raw STEP bytes nor an LLM
visible trace path. The build transcript stores the ordered response envelopes
and a transcript SHA-256; it must declare uncertainty or unsupported outcomes
instead of inventing missing facts.

## Build and provenance

The future executor starts the build plane without `/input/model.step` and
without an observation service mount/socket. It records that absence in an
additive capability attestation. M46 remains authoritative: a fresh normal
trace, no executed original-input read, and same-script absent-input control
are required before `independent_reconstruction`; any missing attestation is
`provenance_unknown`. Geometry gates remain unchanged and are not a substitute
for capability evidence.

Before an executor starts, Harness validates `build_sequence.py` against the
runtime CAD API contract. Known unavailable `cadquery`, `OCC`, and `OCC.Core`
imports, and statically imported symbols absent from the installed `OCP`
module (for example `OCP.gp.gp_DZ`), are rejected locally with additive
`build_script_contract` evidence; the script is not sandboxed, and this
classification is distinct from a CAD script error, a sandbox failure, or a
geometry-gate result. The allowed backend surface remains the installed `OCP`
bindings.

## Fixed later G2 fixture matrix

| Fixture | Expected outcome |
|---|---|
| M44 OCP reader-to-writer | `round_trip`; never reconstruction |
| Bounded box observation + independent box construction | all health gates pass and `independent_reconstruction` |
| Invalid tool request | structured error plus query trace; no build execution |
| Call-budget or response-bound exceedance | structured unsupported; no hidden full trace supplied |
| Build attempts `/input/model.step` after Q01 | mount absent; no independent claim |
| Missing query, build-capability, or tracer attestation | `provenance_unknown` |

Reference scripts are fixture controls only and must never be LLM inputs.

## M19-003 bounded guidance tool

An explicit revision may opt in to one checked guidance bundle through
`get_guidance_card(role)`. The default revision exposes no such tool. The
bundle verifies frozen index/card SHA-256 values, returns at most one compact
card (3,000 UTF-8 bytes), and writes only the revision ID, index hash, result
status, and returned card IDs to `traces/guidance_calls.jsonl`. Invalid hashes,
undeclared cards, invalid roles, or unavailable bundles fail closed. It never
searches `docs/`, exposes raw STEP/reference scripts, or changes build gates.

## Single-case adapter

`observed-first-pass` is the M52 single-case adapter for this contract. Its
fake mode is offline. Its non-fake path requires an explicit authorization
flag, exactly one request budget, a positive provider deadline, and
`wsl-bwrap`; it must not use the older filename-bearing corpus first-pass
summary policy.

For an explicitly monitored single request, `observed-first-pass --phase
prepare` writes a producer-owned, content-free `running` checkpoint before any
provider request. M70 may only read that report. `--phase execute` accepts only
the prepared checkpoint, marks the request issued immediately before provider
work, and must write a parseable terminal `completed` or `interrupted` report.
This lifecycle does not add retry, prompt, provider, or budget authority.

## Multi-case adapter

`observed-development` is the explicit M55 multi-case path. It creates one
fresh observation session per manifest case and uses the same path-free M48
transcript for every first-pass request. It never changes the legacy
`corpus --first-pass` policy. If a first pass fails, its bounded repair request
contains the generated script plus path-filtered execution and gate feedback;
it excludes the input summary and all local path-bearing fields. Both first
pass and repair execute with no original STEP mount.

The report is atomically checkpointed as `running` before the first request and
after each completed case. A first-pass provider deadline writes an
`interrupted` report instead: it retains only earlier completed cases and adds
the current case ID plus the non-sensitive `ProviderRequestTimeoutError` class.
When the M58 lifecycle boundary supplies a valid diagnostic, the interruption
also records only its `last_phase`, ordered phase/monotonic-elapsed-millisecond
events, and sanitized `error_class`; malformed or extra fields are omitted.
Timeout and returned lifecycle-error requests count as issued; the runner makes
no retry and does not process later cases. An `interrupted` report is partial
evidence only, so any new hosted batch requires a new report path, preflight,
and authorization.
