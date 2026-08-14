# ADR-0010: Govern External Evaluation by Cumulative Attribution and Minimal Repair Experiments

- **Status**: Accepted
- **Date**: 2026-08-03

## Context

ADR-0009 correctly prevented an early helper, IR, or SDK decision after M9.  Its fallback route, however, was another deterministic external increment whenever neither the geometry nor narrow-helper threshold qualified.  After M10-005 and M10-008, six completed external cases have useful but distributed evidence: provider lifecycle, unknown STEP-read, sandbox input-path, and unavailable-import outcomes.  Repeating increments without recording what each increment is meant to distinguish would make corpus growth the default rather than a means to improve attribution or validate a repair hypothesis.

## Decision

- M10-010 was originally limited to deterministic 2/1 external admission and offline controls.  ADR-0011 later permits only its complete ignored local-cache preparation; its selection, evaluation, and provider boundaries remain unchanged.
- After M10-010, maintain one reviewed, document-only cumulative attribution ledger.  Each completed external case records batch/split, first-pass and repair outcome, primary attribution, evidence level, revision/trace reference, unresolved question, candidate repair hypothesis, and counterexample status.
- Evidence levels are `direct` (an execution trace proves causation), `supported` (existing evidence is consistent but lacks direct execution causation), and `unknown` (the existing evidence cannot decide).  Only `direct` evidence counts toward the narrow-helper threshold; a static symptom never becomes direct evidence.
- A subsequent review first updates the ledger, then selects exactly one route: report-only geometry diagnostics for three executable/readable non-actionable geometry failures; a narrow helper for three cases sharing one `direct` root cause; a minimal offline repair experiment for two external cases sharing one `direct` or `supported` locally reproducible mechanism; or a deterministic increment with an explicit discrimination question, expected information gain, and stopping condition.
- A minimal offline repair experiment proves only deterministic execution compatibility, observability, or repair-signal behavior.  It neither makes a model-quality claim nor changes production behavior.  Prompt/context comparisons and hosted policy experiments require a separate preregistered development-only workpack, the normal preflight, and explicit authorization; held-out follows only after development review and separate authorization.

## Consequences

- The Harness, CLI, corpus-report schema, provider policy, probes, gates, manifests, and default offline boundary remain unchanged.
- The ledger is a Markdown governance artifact, not a machine-readable corpus-report field.
- Future external increments are still deterministic and split-preserving, but must state why the selected examples can resolve a recorded attribution question and when further sampling stops.
- ADR-0009 remains historical evidence-gating rationale; this ADR supersedes only its default fallback-routing rule.
