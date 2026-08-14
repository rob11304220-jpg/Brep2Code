---
type: contract
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - contract
  - llm
---

# Contract: LLM Provider + Trace

M3 provider boundary is intentionally small. The Harness asks one provider for one response; it does not execute tools, run scripts, or apply edits inside the provider layer.

## Provider Request

`ProviderRequest` contains:

| Field | Meaning |
|------|---------|
| `messages` | Ordered `system/user/assistant/tool` messages. |
| `model` | Provider model identifier, including fake local models. |
| `temperature` | Optional sampling setting. |
| `max_output_chars` | Optional local response-size intent. The current DeepSeek adapter rejects it fail-closed because it has no character-accurate provider mapping. |
| `max_output_tokens` | Optional positive provider-token cap. The DeepSeek adapter maps it exactly to `max_tokens`; it is not a character limit. |
| `metadata` | Non-secret routing/debug metadata. |

## Provider Response

`ProviderResponse` contains:

| Field | Meaning |
|------|---------|
| `provider` | Provider name, for example `fake`. |
| `model` | Actual model identifier used by the provider. |
| `output_text` | Natural-language response summary. |
| `finish_reason` | Provider stop reason summary. |
| `script_update` | Optional `replace` or `edit` instruction for `build_sequence.py`. |
| `usage` | Small token/char/count summary. |
| `raw_summary` | Small provider-specific summary, never the full raw response. |

`ScriptUpdate(kind="replace")` carries full replacement content for `build_sequence.py`. `ScriptUpdate(kind="edit")` carries instructions for a later edit/apply step.

## Trace Files

Each revision can write:

| Path | Format | Purpose |
|------|--------|---------|
| `traces/llm_messages.jsonl` | append-only JSONL | Sanitized request/response messages. |
| `traces/provider_response.json` | JSON | Sanitized provider response summary. |

Trace writers truncate oversized strings and redact secret-like metadata keys such as API keys, tokens, passwords, authorization headers, and env blobs. Hosted provider SDK integration must keep credentials in environment variables or external secret stores and must not write them into revision bundles.

## DeepSeek compatibility boundary (M71, amended by M89-002)

The adapter constructs exactly one non-streaming Chat Completions JSON request
with `response_format: {"type": "json_object"}`. It reads, but never retains,
the first response body byte and emits only its elapsed-millisecond lifecycle
event. It does not expose streaming tokens, response headers, or request IDs.
A complete response may retain only the sanitized status class,
request-id-presence flag, and first-response-byte elapsed milliseconds; header
values, request-id values, prompt content, reasoning content, raw bytes, and
raw response envelopes remain excluded.

The accepted executable envelope is a JSON object containing an
`output_text` string and `script_update.kind="replace"` with a string
`script_update.content`. A nonconforming response remains a provider response
but has no script update and is classified by the caller's existing missing-
update path. `max_output_chars` is not sent as a misleading remote cap; a
caller that supplies it receives a local compatibility error before HTTP. A
positive `max_output_tokens` maps to DeepSeek `max_tokens` and is the only
supported output-cap field. Thinking mode and `reasoning_content` are not part
of this adapter contract.
