# Handoff: Generated-Script API Instruction / Feedback Alignment

- **Date**: 2026-08-11
- **Subproject**: `brep2code`
- **Status**: `active`
- **Related workpack**: `WP-M129-001-generated-script-api-instruction-feedback-alignment`

## Goal

Complete a narrow offline G2 alignment audit of fixed provider-bound
generated-script API instruction and sanitized static-contract feedback.

## Context

- M127 terminalized after two authorized requests with a generated script that
  imported unavailable `OCP.STEPControl.STEPControl_STEPModelType`.
- M128 confirmed the local contract already rejects that exact symbol before
  execution and added regression coverage. M129 checks whether the fixed
  generator instruction states the same installed-binding boundary clearly.
- M129 owner work is complete: the fixed system instruction and first
  sanitized contract-rejection hint now use the same installed-module/symbol
  boundary. Fake-provider and exact-symbol regression assertions passed; the
  focused suite passed 60 tests, and Ruff, governance audit and diff check
  passed.

## Next

- Obtain Liaol's independent G2 review of the exact fixed instruction,
  sanitized repair hint, M127-symbol regression, egress boundary and offline
  scope. If approved, close M129; otherwise record the exact blocker without
  widening into hosted work.

## Boundaries

No provider construction, hosted request, checkpoint, retry, M127 reuse,
card/manifest/split/reference-script change, or prompt-family expansion.

## Resume prompt

```
Continue M129 offline generated-script API instruction / feedback alignment.
Locate the provider-bound fixed instruction, compare it to build-script-api-v1
and M127's exact STEPControl symbol, then make only the smallest safe change.
```
