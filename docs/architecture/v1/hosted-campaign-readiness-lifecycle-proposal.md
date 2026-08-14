---
type: route-proposal
related-project: Brep2Code
status: future-option
---

# Hosted Campaign Readiness Lifecycle Proposal

## Status and boundary

This is a post-campaign governance proposal, not a current work selection,
execution contract, provider authorization, or interpretation of any hosted
result.  The active M180 workpack and its later itemized authorization remain
the sole route for the frozen 33-case asymmetric campaign.

The proposal may be selected only after that campaign has an independently
reviewed terminal report.  It must not delay, alter, or evaluate the current
campaign while it is being prepared or executed.

## Short-term handling for the current campaign

Before requesting the one itemized authorization, complete the existing M180
owner-side scope as one executable offline product:

1. Implement and fake-test the fixed per-case state machine: Q01, the annex's
   one returned card, initial generation, Harness gates, classified terminal
   handling, and at most one eligible `source_only` repair.
2. Make the runner atomically checkpoint request issuance before every HTTP
   request and retain separate completion-slot and HTTP-request accounting.
   The fixed ceilings remain 102 completion slots and 69 HTTP requests.
3. Verify interruption, timeout, provider/protocol failure, gate failure, and
   normal completion all produce immutable terminal reports with no in-place
   resume or budget reuse.
4. Re-run the fresh local preflight, validate only boolean provider-config and
   executor availability without exposing credentials, and obtain the required
   independent G3 review.
5. Generate one hash-bound authorization packet containing destination,
   provider/model, outbound-content boundary, 33-case scope, repair/retry
   policy, token/deadline limits, both ceilings, executor, and fresh report
   identities.  Only then request the user's one itemized authorization.

After authorization, execute the fixed campaign without policy assembly or
parameter choice.  Preserve the terminal report and conduct the already
required independent terminal review before interpreting the result.

## Long-term decision

The uncertainty is operational rather than model-facing: can a selected,
frozen campaign become a reviewed, authorization-ready executable artifact
before the user is asked to approve egress?  The current sequence freezes
assets and policy first, but discovered orchestration gaps after preflight.

The smallest competing dispositions are:

| Disposition | Meaning |
|---|---|
| Retain staged packages | Continue discovering executable gaps in later G2/G3 packages. |
| Adopt a readiness lifecycle | Require a machine-checkable, fake-executable campaign artifact before preflight and authorization. |

The later selected workpack must discriminate these dispositions using the
current terminal campaign record plus an offline audit of the campaign
artifact.  A counterexample is a campaign whose frozen artifact still needs a
new CLI, provider boundary, state-machine, accounting rule, report schema, or
policy assembly after it has been declared `authorization_ready`.  Such a
counterexample rejects adoption or returns the artifact to `executable_offline`.

## Proposed lifecycle and adoption boundary

The proposed lifecycle is:

```text
draft -> frozen -> executable_offline -> reviewed_ready
      -> authorized -> running -> terminal_reviewed
```

- `frozen` binds cases, splits, cards, Q01 boundary, repair policy, model,
  request/completion budgets, executor, and report identities.
- `executable_offline` requires a complete fake-provider run, exact accounting,
  all terminal checkpoint paths, and a `campaign doctor` audit.
- `reviewed_ready` requires independent review and emits an immutable
  authorization packet; it may not contain user-selectable policy overrides.
- `authorized` records the user's exact itemized approval of that packet.
- `running` and `terminal_reviewed` retain the existing no-resume, fresh-budget
  and independent-result-review rules.

Adoption may change only campaign preparation, local readiness validation, and
authorization presentation.  It does not authorize any provider request,
relax fresh preflight or independent review, reuse a budget/report/approval,
expand repair, alter the current cohort, or interpret model quality.

## Required future deliverables

If selected, the long-term workpack must produce a concise ADR, a versioned
campaign-artifact schema, a `campaign doctor` runbook/CLI contract, fake-only
end-to-end tests, and migration guidance.  It must not evaluate the preceding
campaign's model result; that remains a later terminal-review decision.
