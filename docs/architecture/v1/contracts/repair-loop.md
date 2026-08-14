---
type: contract
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - contract
  - repair
---

# Contract: Repair Loop Runner

The M3 repair runner creates immutable Harness revisions while a provider proposes replacement scripts. Repair context includes the input B-Rep summary together with execution results, gates, hints, and output previews so a provider can target the required geometry. M3-003 supports deterministic local fake-provider loops only; hosted provider SDKs remain out of scope.

## Loop

1. Execute the current `build_sequence.py` through `ManualHarness`.
2. Stop if the revision passes.
3. Build compact repair context from the failed revision: script snapshot, execution summary, stdout/stderr previews, gates, and repair hints.
4. Append request messages to `traces/llm_messages.jsonl`.
5. Ask the provider for a `ScriptUpdate`.
6. Save `traces/provider_response.json` and `traces/script_update.json`.
7. Create a new revision with the replacement script.
8. Stop on pass, `max_rounds`, or structured provider error.

Prior revision workspaces are never mutated.

## CLI

Local fake-provider smoke:

```powershell
uv run python -m brep2code.cli repair --record box-smoke --script broken_build.py --fake-replacement-script replacement_build.py --input case-library\self-authored\box\input.step
```

The existing manual run path remains unchanged:

```powershell
uv run python -m brep2code.cli run --record box-smoke --input case-library\self-authored\box\input.step
```