# Handoff: M54 development-split secure evaluation preflight

- **Date**: 2026-08-08
- **Subproject**: `brep2code`
- **Status**: `blocked`
- **Related workpack**: `WP-M54-001-fixed-development-split-secure-llm-evaluation`

## Goal

Determine whether a fixed 12-case self-authored development split can safely
enter a G3 observation-only LLM evaluation, then request itemized authorization
only if every hosted-preflight check passes.

## Done

- M53 is closed and independently reviewed.
- User selected the next route stage: fixed development-split secure LLM
  evaluation.
- The candidate split is the 12-row parametric-development manifest.
- Manifest SHA-256, all 12 input SHA-256 values, non-secret provider
  configuration entries, and WSL/bubblewrap availability were verified.
- Local reference replay through `wsl-bwrap` completed: 12/12 repair passes
  and 12/12 no-input provenance controls passed; report is
  `data/m54-preflight/reference-repair-wsl-bwrap.json`.
- No provider request was issued. The hosted report path is new.

## In progress

- M55 closed with independent review. Resume with a fresh read-only preflight
  through the explicit `observed-development` M48 path; no provider request is
  authorized or issued.

## Next

- Verify fresh input hashes, `wsl-bwrap` no-input execution, provider config,
  selected model, exact CLI budget rule, and a new report path through
  `observed-development`. Then present itemized authorization only if every
  check passes.

## Decisions

- Candidate provider/model: DeepSeek `deepseek-v4-pro` at
  `https://api.deepseek.com`, pending user authorization.
- Candidate bounds: 12 fixed development cases, one repair round, at most 24
  requests, 120-second provider deadline. These are not authorization.
- Existing `corpus --first-pass` has an older filename-bearing context, so it
  is unacceptable unless an M48 observation-only multi-case route exists.

## Blockers

- No provider request before fresh preflight and explicit itemized user
  authorization.

## Key paths

| Kind | Path |
|------|------|
| Workpack | `docs/workpacks/active/WP-M54-001-fixed-development-split-secure-llm-evaluation.md` |
| Manifest | `case-library/manifests/self-authored/parametric-development.json` |
| Secure adapter | `brep2code/agent/observed_build.py` |
| Hosted runbook | `docs/runbooks/llm-provider-config.md` |

## Resume prompt

```
Continue M54 read-only hosted preflight. Do not call a provider. Verify every
selected SHA-256, offline wsl-bwrap evidence, no-input M48 multi-case egress
route, non-secret configuration, new report path, budget and deadlines. M55
has supplied the route, but do not ask for authorization until each fresh
check passes.
```
