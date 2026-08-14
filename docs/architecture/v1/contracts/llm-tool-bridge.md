---
type: contract
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - contract
  - tool-calling
---

# Contract: LLM Tool Bridge

The M3 tool bridge exposes existing B-Rep probe functions as bounded internal tool calls. It does not call hosted LLMs, edit scripts, or execute CAD revisions.

## Tool Registry

Supported tools:

| Tool | Arguments | Purpose |
|------|-----------|---------|
| `probe_summary` | none | Return input file, bbox, topology counts, area, and volume summary. |
| `probe_topology` | `selector`, `max_entities` | Return bounded entity ids for `all/solid/shell/face/edge`. |
| `probe_entity` | `entity_id` | Return details for one stable entity id. |
| `sample_entity` | `entity_id`, `samples` | Return bounded samples for one face or edge. |

## Bounds

- Unknown tool names return structured `unknown_tool` errors.
- Unknown arguments and invalid argument types return structured validation errors.
- Selectors are limited to `all`, `solid`, `shell`, `face`, and `edge`.
- `max_entities`, `samples`, and result bytes are configured by `BRepToolBridge`.
- M48 observation calls have an independent total-call budget for each opaque
  `observation_session_id`; one session cannot consume another session's budget.
- Oversized full probe results are written to trace; compact tool results include `trace_path`.

## Trace

Each tool call can append to `traces/tool_calls.jsonl`:

```json
{
  "schema_version": 1,
  "created_at": "timestamp",
  "tool": "probe_summary",
  "arguments": {},
  "ok": true,
  "result": {},
  "error": null,
  "trace_path": null
}
```

The trace records the validated arguments, compact result or structured error, status, and full-result path when the probe result overflowed the configured size limit.

## Revision-scoped guidance selection

The opt-in `get_guidance_card` bridge is separate from the B-Rep tool registry.
A two-stage build may request exactly one predeclared `role`; the Harness
validates that role against the frozen revision bundle, resolves it to its
hash-bound card, and records only `selected_role`, index hash, returned card
ID, and structured result in `guidance_calls.jsonl` and the additive signal
bundle metadata.  Unknown roles, unavailable material, hash drift, or a card
not declared by the index fail closed.  The tool cannot accept a path, search
a directory, return a reference script, or alter any execution or geometry
gate.

## M48 observation envelope

`BRepToolBridge.observe()` is the Q01 runtime-facing variant. It wraps one
validated tool result in a versioned envelope with an opaque observation
session/call identifier and canonical-response SHA-256. Before it reaches the
runtime context, it removes `input`, `file_name`, and `trace_path`; the local
`observation_queries.jsonl` trace records only the call metadata, result hash,
and byte count. `build_observation_context()` rejects path-bearing fields and
enforces the 12 KB M47 context bound.
