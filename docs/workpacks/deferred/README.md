# Deferred Trigger Workpacks

This directory contains future work that cannot be selected until its stated
evidence, review, or authorization trigger is satisfied. `WP-TRG-*` is a
stable navigation identifier, not a milestone reservation. When a trigger is
met and the user selects work, create a new active `WP-M...` workpack with a
fresh bounded scope; do not reactivate or rename the deferred record.

Current routing priority is documented in `docs/workflow/status.md` and
`docs/architecture/v1/current-project-route.md`. Deferred records are
navigation, not a queue or provider authorization: only a user-selected
trigger becomes a fresh bounded `WP-M...` workpack. Their route disposition is
maintained separately in
[`workpack-route-disposition-index.md`](../../workflow/workpack-route-disposition-index.md);
`deferred` alone does not mean that a route remains a candidate. Historical
batch/family records remain background evidence unless a current workpack
explicitly cites them.

## Trigger index

| ID | Trigger | Intended follow-up |
|---|---|---|
| TRG-001 | Three non-actionable readable geometry failures | Report-only geometry diagnostics |
| TRG-002 | Three directly attributable, same-mechanism OCP failures | One narrow helper |
| TRG-003 | Two validated helpers reveal one shared dependency model | Parallel IR shadow experiment |
| TRG-004 | A documented Fusion representation/coverage blocker | DeepCAD admission audit |
| TRG-005 | A newly documented successful minimal hosted path | Output-contract and repair correctness |
| TRG-006 | Output-contract work is independently accepted | P0 observation-only rebaseline |
| TRG-007 | P0 rebaseline finishes without its stop rule | Frozen P0 formulation comparison |
| TRG-008 | One reviewed P0 formulation meets its disposition | P1 progressive evaluation |
| TRG-009 | A readiness review retains held-out interpretability | Held-out parameter-variation evaluation |
| TRG-010 | The frozen held-out evaluation reaches terminal state | Independent parameter-variation evidence review |
| TRG-016 | The user selects exactly one named portfolio family after its dossier and a fresh readiness review pass | One-family development hosted campaign |
| TRG-018 | The same named family has independently reviewed development terminal evidence under an unchanged frozen policy, and the user selects held-out scope | One-family held-out hosted campaign |
| TRG-039 | User selects offline G2 release freeze after M157; M139/M140/M141 and M19-003 contracts remain reviewable | Freeze three-case closed-loop Harness release and fake-provider dossier; no provider use |
| TRG-040 | TRG-039 independently completes; frozen hashes pass fresh preflight and user selects G3 scope | One finite three-case development hosted closed-loop evaluation with fresh itemized authorization |
| TRG-041 | TRG-040 terminal report is independently reviewed with complete repair/tool accounting and user selects offline G2 scope | Calibrate one repair-attempt or interaction-budget policy from evidence; no provider rerun |

Consumed deferred triggers are preserved under `../archive/` once a fresh
bounded `WP-M...` workpack is selected and completed. Historical completed M
workpacks stay in `../done/`; the obsolete development split rerun plan and
other non-runnable trigger records remain in `../archive/` as evidence only.
