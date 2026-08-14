# Handoff: M7-002 first-pass generation design

- **Date**: 2026-08-02
- **Subproject**: `brep2code`
- **Status**: `complete`

## Goal

Define and validate M7-002's first-pass generation mode, keeping the default CLI offline and credential-free. Do not make a hosted request during design or implementation without new explicit authorization.

## Done

- M7-001 is complete, its workpack is in `docs/workpacks/done/`, and its acceptance evidence was reviewed against the M7 roadmap.
- Added deterministic coverage for worker deadline termination/join, loopback provider errors, issued-request accounting, checkpoint status semantics, and default offline/fake-provider guards.
- Focused verification passed: `uv run python -m pytest tests/test_corpus_m4.py -q` (25 passed in 78.37s) and `uv run python -m ruff check tests/test_corpus_m4.py`.
- Final verification passed: `uv run python -m pytest` (54 passed in 105.26s) and `uv run python -m ruff check .`.
- The existing implementation met this coverage without a production-code or report-schema change.

## In progress

- M7-002 offline implementation is complete: `corpus --first-pass` uses `first_pass_script` with the local fake provider, writes schema-v3 reports, and keeps fake replay explicit through `--repair`.
- Contract, provider runbook, and corpus module documentation define the v3 policy, provenance, budget, and trace boundary.
- Final verification passed: `uv run python -m pytest` (58 passed in 122.99s) and `uv run python -m ruff check .`.
- A hosted P0 first-pass command completed on 2026-08-02 with schema-v3 status `completed`: 3 cases, 1 maximum repair round, a 6-request bound, 120-second provider timeout, 4 actual requests, and `wsl-bwrap`. `box` and `block_with_hole` passed at primary generation; `cylinder` had primary `script_failure` and passed one repair. The ignored report is `data/corpus-runs/deepseek-p0-first-pass-20260802.json`.
- Scope deviation: its report identifies `deepseek-v4-pro`, while the batch authorization identified Flash. Do not treat it as Flash evaluation evidence or use it to complete M7-002; do not issue follow-up requests without fresh, model-specific authorization.
- A separately authorized `deepseek-v4-pro` replacement P0 first-pass batch then completed with the same bounds and explicit permission to send the bounded probe summaries. Its schema-v3 report used 4/6 requests with `wsl-bwrap`: `box` and `cylinder` passed at primary generation, while `block_with_hole` had primary `script_failure` and passed one repair. This is accepted M7-002 engineering evidence, not a model-quality benchmark.

## Next

- Begin M7-003: layered, self-authored corpus expansion. Keep default execution offline; no further hosted request is authorized by this handoff.

## Decisions

- M7-002 uses schema v3 only for explicit first-pass reports; legacy local v1 and hosted-repair v2 reports remain compatible.
- A hosted first-pass maximum request budget is `max_cases × (1 + max_rounds)`.
- External force-stop preserves only the last `running` checkpoint, whereas handled failures write `interrupted`.
- No hosted request is authorized by this completed offline/loopback work.

## Blockers

- None for offline design. Any hosted generation evaluation requires fresh explicit authorization with provider/model, case/round bounds, timeout, and request or cost budget.

## Key paths

| Kind | Path |
|------|------|
| Branch | `main` |
| Completed workpack | `docs/workpacks/done/WP-M7-001-provider-reliability-and-recovery.md` |
| Active workpack | `docs/workpacks/active/WP-M7-002-first-pass-generation-evaluation.md` |
| Commands | `uv run python -m pytest`; `uv run python -m ruff check .` |

## Resume prompt

```
Continue Brep2Code M7-002 hosted first-pass evaluation only after explicit authorization.
Read AGENTS.md, docs/handoff/active/2026-08-02-m7-acceptance-review.md, docs/workflow/status.md, and the completed M7-001 workpack.
First action: verify the authorization scope, then run only the approved bounded command and review its completed schema-v3 report.
```
