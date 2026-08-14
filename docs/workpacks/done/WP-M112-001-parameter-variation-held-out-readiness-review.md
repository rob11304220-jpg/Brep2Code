# WP-M112-001: Parameter-Variation Held-Out Readiness Review

- Status: done
- Milestone: M112
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Decide whether the unchanged M96/M97 paired held-out policy can still answer
its bounded card/no-card question after the nominal development baseline's
classified constructor-arity counterexample.

## Scope

- Read only the frozen M96/M97-003 policies and retained M97-003/004
  development evidence.
- State the policy's allowed terminal categories and decide `ready` or
  `inconclusive` without inspecting held-out inputs.
- Write one compact decision record and align only the parameter-variation
  route/status/handoff with its disposition.

## Compatibility constraints

Offline and credential-free. Do not inspect held-out cases or inputs; alter a
case, policy, card, prompt, model, endpoint, split, gate, request budget or
report path; construct a provider; run preflight; or issue a hosted request.
No result authorizes `TRG-009` unless it is independently reviewed as `ready`.

## Acceptance

```powershell
uv run python -m pytest -m fast -q
uv run python tools\check_governance.py
git diff --check
```

## Stopping rule

Stop after one `ready` or `inconclusive` disposition. A result cannot estimate
a card effect, parameter generalization or model reliability.

## Status transition

Record owner acceptance, then obtain Liaol's independent review before
closure. A reviewer cannot grant provider authority.

## Owner acceptance

- [`m112-parameter-variation-held-out-readiness-review.md`](../../workflow/m112-parameter-variation-held-out-readiness-review.md)
  records the policy-only decision: `inconclusive`.
- The frozen score has no category that separates the retained nominal baseline
  API-use failure from a favorable card/no-card asymmetry. The policy cannot be
  changed, and no permitted second sample can make that asymmetry discriminating.
- `TRG-009` is not selected or authorized; no held-out input was accessed.

## Independent review required

Liaol must verify the retained-source boundary, the allowed-interpretation
table, the `inconclusive` conclusion, and the route/status/handoff alignment.
Review cannot alter the policy or authorize provider use.

## Independent review and closure

- Reviewer: Liaol
- Outcome: approved on 2026-08-11.
- Review scope: confirmed the decision uses only the frozen M96/M97-003 policy
  and retained M97-003/004 development evidence; the category logic preserves
  the nominal baseline constructor-arity attribution; and neither the review
  nor its route updates access held-out inputs or grant hosted authority.
- Closure rationale: the unchanged comparison remains `inconclusive` for its
  bounded card/no-card question. `TRG-009` remains deferred and unselected;
  any future route needs a separately selected policy/design decision.

## Out of scope

`TRG-009` selection, held-out evaluation, retry, repair, capacity reuse,
runtime knowledge, provider configuration, preflight or authorization.
