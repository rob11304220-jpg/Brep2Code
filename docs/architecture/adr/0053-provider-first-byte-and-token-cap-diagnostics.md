# ADR-0053: Provider First-byte and Token-cap Diagnostics

- **Status**: Accepted
- **Date**: 2026-08-10

## Context

M89's second provider boundary reached its deadline after HTTP started, before
a script or Harness result existed. The existing non-streaming adapter could
record worker start, HTTP start, and complete response, but not whether any
response body arrived. It also had no semantically accurate remote output cap:
the local character cap was correctly rejected.

## Decision

Keep the request non-streaming and JSON-only. Read only the first response body
byte, discard it after reconstructing the ordinary response, and emit its
elapsed-millisecond lifecycle event. Permit only a positive
`max_output_tokens` field mapped directly to DeepSeek `max_tokens`. Do not
enable thinking mode or retain `reasoning_content`, raw bytes, headers,
request IDs, prompts, credentials, or full provider responses.

## Consequences

Timeout evidence can distinguish no observed response body from a response
that began before timing out, without changing case selection, CAD gates,
repair policy, or hosted authority. A later retry still needs its own bounded
G3 workpack, new report path, and explicit authorization.
