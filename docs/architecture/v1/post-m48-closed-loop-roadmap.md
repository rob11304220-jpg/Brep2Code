---
type: roadmap
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - M48
  - LLM
  - evaluation
---

# Post-M48 Closed-Loop Roadmap

## Purpose

This roadmap records the selected implementation order after M48. The primary
goal is to demonstrate that a real LLM can use only bounded Q01 observation
facts through the Harness, generate a Q02 CAD build sequence, and receive
structured execution and gate feedback. Broader corpus work follows that
closed-loop proof; it is not a substitute for it.

This document routes future work. It does not authorize a provider call,
external-data access, a prompt change, a manifest change, or a runtime change.
`docs/workflow/status.md` remains the current-work authority.

## Current baseline

M48 implements a path-free observation envelope, a bounded transcript context,
and an opt-in build mode with no original STEP mount. Provider, repair, corpus,
and sandbox components already exist, but the M48 observation transcript is
not yet an end-to-end provider context for a generated build script. Therefore
the next proof is integration, not a claim of general B-Rep reconstruction.

## Required progression

```text
M49 documentation alignment (G1)
  -> offline observation-to-provider integration and semantic fixes (G2)
  -> one existing self-authored case with a real LLM, secure execution (G3)
  -> fixed development split: generation and bounded repair evaluation (G3)
  -> controlled local variants derived from reference models (G2)
  -> offline external-data admission and frozen split (G2)
  -> separately authorized external-data LLM evaluation (G3)
```

Each arrow is a new bounded workpack. G2 and G3 workpacks require an
independent reviewer. Every G3 workpack requires its own hosted preflight and
explicit user authorization for destination, provider/model, egress content,
fixed cases/split, rounds, deadline, and request or cost budget.

## Work packages by stage

| Stage | Tier | Required outcome | Must remain out of scope |
|---|---:|---|---|
| Documentation alignment | G1 | Correct contract state, route, and terminology | Runtime behavior or hosted call |
| Offline closed-loop integration | G2 | A fake provider receives only a bounded M48 observation context; its script runs without original STEP and receives structured gates/feedback | Real provider, prompt policy expansion, manifest change |
| Semantic and quality fixes | G2 | Per-session call budgets; provenance eligibility distinct from geometry health; fast/standard/sandbox test selection | Weakening fail-closed provenance or test coverage |
| Real-LLM smoke | G3 | One fixed self-authored case completes a secure, observation-only provider call with auditable request/response, execution, and budget evidence | Generalization or model-quality claim |
| Development-split evaluation | G3 | Frozen policy and development split report first-pass and bounded repair funnels separately | Held-out run, mutable prompts/splits, aggregate success claim without denominators |
| Controlled reference variants | G2 | Local reference models/scripts generate preregistered variants with hashes, parameters, input identity, split, and local oracle evidence | Reference script/history exposure to the LLM |
| External admission | G2 | Offline source, license, SHA-256, probe, sandbox and split checks | LLM egress or automatic runtime inclusion |
| External evaluation | G3 | A newly authorized, fixed external split report under the unchanged secured policy | Reusing a prior request budget or changing inputs after results |

The semantic and quality fixes may be one G2 workpack or separately bounded
G2 workpacks, but the integration test must cover their final contracts.

## Reference-model variant rule

A reference model, native history, or reference `build_sequence.py` is a local
control only. It may generate deterministic parameter or geometry variants and
may supply local gate/oracle evidence. It must never be serialized into the
LLM's observation context, provider request, tool response, or runtime mount.
The LLM receives only the frozen Q01 tool schema, bounded observed facts, and
permitted Q03/Q04 feedback.

## Evaluation interpretation

Report at least these independent states:

1. Provider lifecycle: request issued, response received, timeout/error.
2. Build health: script exit, output readability, and existing geometry gates.
3. Provenance eligibility: `independent_reconstruction`, `round_trip`, or
   `provenance_unknown` based on the M46 control.
4. Repair outcome: first-pass and bounded repair results remain separate.

A geometry-healthy result with unknown provenance is not evidence of an
independent reconstruction. A successful local reference replay is Harness
compatibility evidence, not LLM-quality evidence.

## Re-entry and stopping rules

- If the offline closed loop cannot maintain the no-input capability and
  traceable provenance boundary, stop before any hosted call.
- If the real-LLM smoke does not produce a verifiable result, record the
  failure taxonomy before selecting a larger split.
- If development evidence does not justify a held-out run, do not expand cases
  merely to seek a pass.
- External data remains downstream of offline admission; a hosted result never
  substitutes for source, license, hash, probe, or split review.

## Post-M69 stability lane (additive, 2026-08-09)

This lane is additive to the progression above; it does not replace M48--M69
history or authorize a retry. It delays prompt/output-quality changes until
provider-call stability has fresh evidence.

```text
M70 durable monitor (G2)
  -> M71 DeepSeek compatibility diagnostics (G2)
  -> M72 fresh bounded stability experiment (G3)
  -> M79 offline historical-contract drift diagnosis (G2)
  -> M80 paired minimal P0 end-to-end revalidation (G3)
  -> M73 output-contract and repair correctness (G2)
```

M70 makes report-driven heartbeat monitoring reusable: it may wake a task on a
terminal checkpoint but never retry, change a request, or spend budget. M71
adds offline-tested compatibility modes and safe control-report transport
metadata. M72 stopped at a bounded timeout, so it cannot unlock output work.
M79 compares only preserved historical contract fields and freezes a
reproduction profile. M80 then tests the narrow P0 control-plus-`box`
end-to-end path under a new authorization. M73 is deferred until that M80 gate
passes, so output correctness remains separate from provider lifecycle.

## P0 re-baseline and task-formulation lane (planned)

After M73's offline output-contract work is accepted, the project returns to
the original Harness-first question through the existing self-authored P0
cases. This lane uses the current observation-only boundary, fresh reports and
fresh G3 authorizations; it never reuses M7--M10 reports, budgets or prompt
policies.

```text
M73 output-contract / repair correctness
  -> M76 P0 observation-only hosted re-baseline
  -> M77 P0 preregistered task-formulation comparison
  -> M78 P1 progressive hosted evaluation
```

- **M76** establishes a fresh, sequential P0 baseline with the existing
  `box`, `cylinder` and `block_with_hole` fixtures. It separates provider
  lifecycle, script execution and geometry gates without comparing prompts.
- **M77** compares a small preregistered set of one-request task formulations
  using identical model, observation input, case, deadline and gate policy.
  It does not adapt a formulation after an earlier result.
- **M78** uses only the preregistered M77 disposition and proceeds through P1
  complexity one case at a time. A timeout or unclassified script failure
  stops the progression rather than expanding the sample.

These workpacks remain backlog planning only. M80 and every later hosted
workpack require their own fresh preflight and itemized user authorization.

## Reference-assisted build lane (completed baseline and next boundary)

M82 closes the immediate API mismatch by rejecting unsupported `cadquery` and
`OCC` imports before sandbox execution. It does not make reference scripts
available to a runtime LLM. M83/M84, M19-002/M19-003 and M85 subsequently
completed the initial bounded pack, offline retrieval evaluation, opt-in
revision-scoped bridge and first hosted smoke.

```text
M82 OCP API contract alignment (done)
  -> M83 reference-case taxonomy and candidate-pack contract (G2)
  -> M84 direct-evidence qualification for one pack mechanism (G2)
  -> M19-002 development-only retrieval evaluation (G2, evidence-gated)
  -> M19-003 opt-in revision-scoped retrieval integration (G2)
  -> M85 one P0 reference-assisted hosted smoke (G3, fresh authorization)
```

M83 froze the initial development selection: P0 `box`, `cylinder`, and
`block_with_hole`; P1 `filleted_block`, `chamfered_block`,
`three_hole_plate`, and `box_cylinder_union`. Each pack must state observed
applicability, allowed OCP modules, a short construction outline, output
contract, source links, and counterexamples. It must not contain raw STEP,
full reference source, a broad repository read, or held-out authoring evidence.

M84 established the three-independent-direct-case bound for the vertical
cylinder mechanism. M19-002 then completed the frozen offline no-card/top-k
comparison, and M19-003 completed the explicit opt-in, revision-scoped bridge.
M85 completed the first separately authorized hosted smoke. These completed
steps qualify only the fixed cylinder card/roles; they do not make other packs
runtime-visible or automatically authorize another hosted run. The next route
is a separately selected candidate-card qualification audit, followed only by
the corresponding card/hosted gates in the four-track roadmap.

The M69 evidence summary, priority rationale and M72 stability gate are
maintained in the [M69 project progress and improvement review](m69-project-progress-and-improvement-review.md).
