# Handoff: M51 single-case secure real-LLM smoke

- **Date**: 2026-08-08
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M51-001-single-case-secure-llm-smoke`

## Goal

Complete the mandatory G3 preflight for one self-authored `box` real-LLM
smoke, then wait for explicit authorization before issuing any request.

## Done

- M50 is closed with Liaol approval.
- Liaol is M51's independent reviewer.
- One authorized DeepSeek `deepseek-v4-pro` request completed for `box`; its
  secure no-input output passed all existing geometry gates.

## In progress

- M51 is complete after Liaol's independent approval.

## Next

- Do not begin a new workpack until the user selects either fixed development
  evaluation (G3) or test-feedback segmentation (G2).

## Decisions

- Fixed case: self-authored `box`, chosen as the canonical single-case smoke.
- One first-pass generation only; no repair.

## Blockers

- None; M51 is closed.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M51-001-single-case-secure-llm-smoke.md` |
| Input | `case-library/self-authored/box/input.step` |
| Contract | `docs/architecture/v1/contracts/q01-observation-build-separation.md` |

## Resume prompt

```
Continue M51 preflight only. Read the active workpack and handoff. Verify the
fixed box input, secure executor, provider configuration, budget/report
boundary, and existing checkpoint state. Do not call any provider; present
the itemized authorization request after preflight.
```
