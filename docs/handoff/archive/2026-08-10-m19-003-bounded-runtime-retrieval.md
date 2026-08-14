# Handoff: M19-003 bounded runtime guidance retrieval

- **Date**: 2026-08-10
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M19-003-bounded-runtime-guidance-retrieval`

## Goal

Implement an opt-in, revision-scoped, read-only Harness interface that returns
at most the M19-002-qualified top-k=1 card and records its index hash/card ID.

## Done

- M19-002 passed independent review and the user separately selected M19-003.

## In progress

- Await Liaol's independent G2 review of the completed bounded runtime
  interface. M19-003 does not automatically select held-out validation or a
  hosted smoke workpack.
- Wired explicit bundle/call inputs into `ManualHarness.run`; the default
  `guidance` signal-bundle field remains `null`, while an opt-in revision
  records only its index hash, returned card IDs, and compact call status.

## Next

- Freeze request/response size and visibility contract, then implement tool and
  trace metadata with deterministic failure modes and no broad file reads.
- Repeat M19-002's development controls and request independent review.

## Decisions

- Only the compact experimental card may be returned. No raw STEP, reference
  script, governance document, ignored trace, secret, or arbitrary repository
  file may be visible.
- No hosted request, prompt change, or provider configuration is authorized.

## Blockers

- None for offline integration. Gate regression, invalid index, source-boundary
  failure, or non-determinism rejects integration rather than widening access.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M19-003-bounded-runtime-guidance-retrieval.md` |
| Card | `runtime_resources/experience-cards/cards/vertical-cylinder-construction.json` |
| Evaluation | `docs/corpus/reference-packs/m19-retrieval-evaluation-v1.json` |

## Resume prompt

```
Continue Brep2Code M19-003 bounded runtime guidance retrieval.
Read docs/handoff/active/2026-08-10-m19-003-bounded-runtime-retrieval.md.
First action: inspect existing Harness tool and trace contracts, then define
the smallest opt-in revision-scoped top-k=1 read-only card interface. Do not
expose raw case assets or broad files, alter gates/provider/prompt/manifest, or
make a hosted request.
```
