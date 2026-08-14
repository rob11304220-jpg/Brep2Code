# ADR-0009: Gate Post-M9 Architecture Evolution on Completed External Evidence

- **Status**: Accepted
- **Date**: 2026-08-02

## Context

M9-001 is the first split-preserving hosted first-pass evaluation on locally admitted external STEP inputs. Earlier self-authored and small hosted runs established Harness behavior, but they do not identify a repeated cross-case limitation that warrants a modeling helper, an intermediate representation (IR), or a project CAD SDK. A timeout, a single repair result, or the expected geometry failure of the fixed scaffold would be insufficient evidence for such an expansion.

## Decision

- M9 development and held-out reports must both reach `completed` under the unchanged M9 policy before any aggregate post-M9 engineering conclusion is made.
- A dedicated evidence review selects one next route: report-only geometry diagnostics, deterministic external corpus expansion, or one narrow OCP operation helper. The selection follows the trigger rules in [the post-M9 roadmap](../v1/post-m9-evidence-gated-roadmap.md).
- A helper requires the same attributable OCP/API, parameter, or dependency-sequencing failure in at least three completed external cases and must retain the underlying gate evidence.
- An IR is deferred to a shadow experiment until at least two validated helpers demonstrate shared operation-dependency or entity-reference needs that script-level repair cannot represent. A project CAD SDK requires a later ADR after that experiment shows explicit benefit.

## Consequences

- At the time of this decision, M9 remained the only current work; no route in this decision authorizes a hosted request, changes the default offline path, or changes M9's model, policy, executor, deadline, case order, or gates.  ADR-0010 later supersedes this ADR's default fallback-routing rule; see `docs/workflow/status.md` for current work.
- Geometry diagnostics begin as report-only evidence; they are not pass/fail gates until separately validated for deterministic behavior and repair usefulness.
- New external inputs remain local research-only assets with a reviewed selection record, hash, probe, split, and license boundary; they do not receive external reference scripts.
- FEA, VLM judging, multi-agent orchestration, a full IR, and a CAD SDK remain out of scope unless later evidence opens a separately approved workpack.
