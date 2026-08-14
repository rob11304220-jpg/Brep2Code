# M134 Frozen Hosted Batch Epoch Policy

- **Workpack**: `WP-M134-001-frozen-hosted-batch-epoch-policy`
- **Status**: frozen offline policy; no preflight, authorization, provider, or request
- **Epoch**: `existing-family-development-v1`

## Purpose

Collect comparable development-only hosted observations from existing frozen
cases without treating one condition's terminal result as a conclusion about
another family. The epoch is a fixed cohort, not a benchmark or project-level
capability score.

## Fixed cohort and denominator

| Family / condition | Development observations | Card boundary |
|---|---:|---|
| Repeated feature pattern | 3 | no card; M123 charter |
| Axisymmetric revolve | 3 | no card; M124 charter |
| Dependent face selection | 3 | no card; M125 charter |
| Multi-inner-loop pocket | 3 | no card; M126 charter |
| Prismatic cylindrical cut | 3 rows x card/no-card = 6 | exact M115 card hash for treatment; no card for paired control; M120 charter |
| **Total** | **18** | fixed, no substitutes |

The case IDs, row order, Q01 facts, constrained actions, semantic/editability
gates and family-local non-inferences remain authoritative in the linked
charters. No held-out row belongs to this epoch.

## Epoch freeze

M135 must freeze and validate, before any authorization, one exact value for
each of the following: provider/model; endpoint; provider-bound instruction
revision; bounded egress text and card hash; `wsl-bwrap` executor; static API
contract; gates; request order; deadline; output cap; fresh epoch policy,
report and monitor paths; and a maximum request count of 18. Retry and repair
are zero. No one may edit these values, add a case, replace a terminal
condition, or change code/prompt/policy while the epoch is running.

## Scheduling rule

At most one request may be in flight, so reporting, accounting and monitoring
remain attributable. This is serial **scheduling**, not serial **gating**:
after a terminal observation, issue the next frozen condition unchanged unless
an epoch-integrity stop rule applies.

## Terminal handling

| Class | Epoch action | Interpretation boundary |
|---|---|---|
| `pass`, script/API failure, geometry/semantic/editability failure, or one provider timeout/lifecycle failure | Record the condition result and continue remaining frozen conditions. | Applies only to that condition; never a family-wide or project-wide claim. |
| `interrupted` after a condition starts | Preserve partial evidence; do not reuse nominal remainder. Continue only if the frozen epoch runner can issue a fresh, not-yet-started condition without changing the boundary. | The interrupted condition is not pass/fail. |
| Policy/hash/split drift; unauthorized egress; invalid accounting/report identity; executor or provenance boundary failure; invalid provider configuration/authentication | Stop issuance immediately and mark remaining conditions `not_issued_epoch_integrity`. | The epoch is invalid or unavailable for comparison; do not repair in place. |
| Two consecutive provider lifecycle failures with no usable provider response | Pause issuance under the predeclared systemic-availability stop. Mark remaining conditions `not_issued_systemic_availability`. | Not a modeling or family conclusion; a later epoch requires fresh selection, preflight and authorization. |

## Follow-on workpacks

1. **M135 (G3, user-selected): Frozen batch epoch preflight and execution.**
   It validates every cohort hash/row, actual CLI accounting, no-input secure
   execution, provider/model configuration, fresh paths and the M134 handling
   table. It may request itemized authorization only after those checks pass;
   once authorized, it executes this unchanged 18-condition epoch.
2. **M136 (G2, user-selected after M135 terminal state): Batch terminal
   evidence review.** It independently checks accounting, condition states,
   integrity classification, no-mid-epoch-change evidence and allowed
   family-local conclusions. It may propose, but cannot start, a later epoch
   or remediation.

M134/M135/M136 do not authorize any held-out campaign, card promotion, runtime
change, generic capability claim, or reuse of old report/budget/authorization.
