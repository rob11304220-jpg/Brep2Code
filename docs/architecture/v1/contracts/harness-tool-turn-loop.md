---
type: contract
related-project: Brep2Code
version: v1
status: active
---

# Contract: Harness Tool-Turn Loop

## Admission

M140 is offline and accepts only a fake provider.  The caller extracts the
frozen `campaign_id` and `campaign_spec_sha256` from an M139 checkpoint only
when `request_state=prepared` and `requests_used=0`, plus a registered input
held only by the Harness.  It accepts no
provider configuration, workspace path, raw B-Rep, reference script, or
repair policy.

## State machine

```text
initial → provider turn → tool request → sanitized tool result → provider turn
                        └→ replacement script → restricted Harness execution
                                                   → structured gate feedback → terminal
```

A provider response contains exactly one tool request or one full replacement
script.  Tools are the declared Q01 probe schemas and, only when configured,
the single hash-pinned card role.  Unknown, malformed, unavailable, wrong-card
and over-budget requests become sanitized tool errors; they never gain access
to a path, a directory listing, shell, raw input, or a reference answer.

## Bounds and traces

The caller freezes positive limits for turns, total tool calls and each tool
result's encoded bytes.  Tool results are path-free envelopes.  The execution
terminal records only a structured status, selected execution fields, gates and
repair hints.  `tool_turn_trace.json` records the campaign identity, limits,
turn kinds and payload hashes, not raw provider secrets or unbounded data.

M140 ends after the first submitted script's execution feedback. M141 consumes
only that terminal feedback through `classified-repair-v1`: static API
contract, missing/unreadable output, and non-timeout local execution failures
may enter one fake-provider `source_only` edit with a cap of one request.
Selector ambiguity, geometry/semantic/editability feedback without an admitted
IR locator, sandbox/provenance, provider/protocol, mixed and unknown feedback
stop fail-closed. Source edits never fall back to a sequence/IR editor or a
replacement-script response. The classification and stop reason are retained in
`traces/classified_repair.json`; this contract still does not alter campaign
identity or construct a hosted provider.
