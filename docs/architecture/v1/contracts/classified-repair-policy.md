---
type: contract
related-project: Brep2Code
version: v1
status: active
---

# Contract: Classified Repair Policy

## Admission and vocabulary

M141 consumes one M140 terminal signal bundle. It maps that bundle to exactly
one of the following classifications:

| Classification | Route | Limit / terminal result |
| --- | --- | --- |
| `pass` | `stop` | `stop_pass`, zero requests |
| `static_api_contract` | `source_only` | one fake-provider request |
| `output_artifact` | `source_only` | one fake-provider request |
| `execution_local` | `source_only` | one fake-provider request |
| `selector_ambiguous` | `stop` | `stop_unsupported`, zero requests |
| `geometry_semantic` | `stop` | `stop_unsupported`, zero requests |
| `editability` | `stop` | `stop_unsupported`, zero requests |
| `sandbox_or_provenance` | `stop` | `stop_policy_rejected`, zero requests |
| `provider_or_protocol`, `unknown_or_mixed` | `stop` | `stop_ambiguous`, zero requests |
| `execution_timeout` | `stop` | `stop_unsupported`, zero requests |

`provenance_unknown` with `coverage=false` means that the local executor did
not provide a provenance trace; it is not evidence of a round trip and does
not by itself suppress an otherwise admitted source-only repair. A confirmed
`round_trip`, an actual sandboxed execution, or an abnormal sandbox termination
does suppress it.

## Route isolation

The sole admitted route is `source_only`. It accepts only an explicit
`ScriptUpdate(kind="edit", path="build_sequence.py", content=...)` from a
`FakeLLMProvider`; replacement-script responses, hosted providers, tools, input
B-Rep access, and sequence/IR editing are rejected. The route writes a new
immutable Harness revision and never mutates its failing predecessor.

Sequence/IR repair is deliberately not implemented here. Selector, geometry,
semantic and editability repair require an admitted stable locator and a
separate editor; absence of either is a terminal condition, never a fallback to
source replacement.

## Plateau and evidence

The source route consumes at most one request. If its successor has the same
normalized signature—classification, exit code, sandbox termination and failed
gate names—it stops with `stop_plateau`; a differing failed successor records
`source_patch_not_converged`. Each affected revision records
`traces/classified_repair.json` with schema version, decision, request count and
terminal reason.
