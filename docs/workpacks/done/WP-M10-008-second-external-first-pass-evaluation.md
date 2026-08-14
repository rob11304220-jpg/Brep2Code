# WP-M10-008: Second External Frozen-Policy First-Pass Evaluation

- Status: done
- Milestone: M10
- Owner: unassigned

## Goal

Evaluate the M10-007 external development and held-out manifests with the unchanged first-pass policy, only after separate split-level authorization, without treating results as a benchmark.

## Scope

- Complete a fresh read-only preflight for each split: selected hashes, manifest membership, offline control, non-secret provider configuration, `wsl-bwrap`, request capacity, and a new unused report path.
- After separate explicit authorization, run development first with `deepseek-v4-pro`, bounded `first-pass-summary-v1` egress, one repair round, a 120-second provider deadline, and a 4-request maximum; review it before held-out.
- Under a separate authorization, run held-out unchanged except for its 1-case/2-request bound, then publish a sanitized split-preserving review.

## Compatibility constraints

- Default commands remain offline and credential-free; no request may be issued without the matching explicit authorization.
- Keep provider/model, bounded context, executor, case order, repair bound, deadline, existing probes, gates, and Harness implementation unchanged between splits.
- Do not retain raw assets, credentials, full provider responses, or benchmark claims.

## Acceptance

- Both authorized reports reach `completed`, or a preflight/authorization failure is recorded without an unapproved request.
- The review reports the evidence funnel, requests, duration, first-pass outcomes, and repair outcomes separately by split.
- No production behavior, schema, prompt, or fixture changes occur.

## Current evidence and authorization blocker

- M10-007's three selected files hash-match and its development/held-out `wsl-bwrap` controls completed with readable inputs/outputs and successful scripts; fixed-scaffold geometry failures are expected control evidence.
- Development preflight confirmed the `deepseek-v4-pro` configuration entry, secure executor, 2-case/one-round/120-second frozen policy, 4-request capacity, and unused report path. Under separate explicit authorization, `abc-v00-m10-008-development-pro-authorized-20260803.json` completed with 2/2 first-pass `script_failure` results, no readable first-pass output, one repair pass, and one `repair_exhausted` outcome; it used 4/4 requests. Held-out preflight also passed: the selected SHA-256 matched, the `wsl-bwrap` offline control `abc-v00-m10-008-held-out-preflight.json` completed with readable input/output and script exit, non-secret configuration is present, and the planned hosted report path was unused before its separate authorization. Review remains split-preserving.

## Completion evidence

- Under separate explicit authorization, held-out report `abc-v00-m10-008-held-out-pro-authorized-20260803.json` completed with one `script_failure` first pass, no readable first-pass output, and one repair pass; it used 2/2 requests.
- The split-preserving sanitized review is [`m10-008-second-external-first-pass-evaluation-review.md`](../../architecture/v1/m10-008-second-external-first-pass-evaluation-review.md). No Harness behavior changed.
